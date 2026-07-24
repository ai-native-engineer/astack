// apple-stt - macOS 26 SpeechAnalyzer based local STT CLI.
// Build: swiftc -O -parse-as-library -target arm64-apple-macos26.0 apple-stt.swift -o apple-stt

import AVFoundation
import CoreMedia
import CryptoKit
import Foundation
import Speech

enum STTError: Error, CustomStringConvertible {
    case invalidArguments(String)
    case localeUnsupported(String, [String])
    case vocabReadFailed(String)

    var description: String {
        switch self {
        case .invalidArguments(let message):
            return message
        case .localeUnsupported(let locale, let available):
            return "지원하지 않는 로케일: \(locale)\n지원 로케일(일부): \(available.prefix(40).joined(separator: ", "))\n전체 목록: apple-stt --list-locales"
        case .vocabReadFailed(let path):
            return "vocab 파일 읽기 실패: \(path)"
        }
    }
}

struct Options {
    var localeID = "ko-KR"
    var files: [String] = []
    var timestamps = false
    var srt = false
    var json = false
    var analysisJSON = false
    var listLocales = false
    var output: String?
    var save = false
    var quiet = false
    var vocabFile: String?
    var oneOffVocab: [String] = []
}

struct ContextTerms {
    let selected: [String]
    let dropped: [String]
}

func eprint(_ message: String) {
    FileHandle.standardError.write((message + "\n").data(using: .utf8)!)
}

func printUsage() {
    print("""
    apple-stt - macOS 26 SpeechAnalyzer 기반 로컬 STT (음성 메모와 동일 엔진)

    사용법:
      apple-stt [옵션] <오디오파일> [<오디오파일> ...]

    옵션:
      -l, --locale <id>        로케일 (기본 ko-KR). 예: en-US, ja-JP
      -t, --timestamps         [mm:ss] 구간 타임스탬프 포함
          --srt                SRT 자막 형식 출력
          --json               기존 JSON 배열 출력 (start/end/text)
          --analysis-json      Apple evidence schema v1 JSON 출력 (단일 입력)
      -o, --output <파일>      결과를 지정 파일로 저장 (단일 입력)
          --save               각 입력 파일 옆에 <이름>.txt/.srt/.json 저장
          --list-locales       지원/설치된 로케일 목록
      -q, --quiet              진행 메시지 숨김
          --vocab <단어,...>   선택된 context에 일회성 용어 추가
          --vocab-file <파일>  기본 ~/.config/stt/vocab.txt를 대체
      -h, --help               이 도움말

    context는 입력 순서를 유지해 중복을 제거하고 최대 100개만 Apple에 전달합니다.
    """)
}

func parseArgs() throws -> Options {
    var options = Options()
    let args = Array(CommandLine.arguments.dropFirst())
    var index = 0

    func value(after flag: String) throws -> String {
        guard index + 1 < args.count else {
            throw STTError.invalidArguments("\(flag)에 값이 필요합니다")
        }
        index += 1
        return args[index]
    }

    while index < args.count {
        switch args[index] {
        case "-l", "--locale":
            options.localeID = try value(after: args[index])
        case "-t", "--timestamps":
            options.timestamps = true
        case "--srt":
            options.srt = true
        case "--json":
            options.json = true
        case "--analysis-json":
            options.analysisJSON = true
        case "--list-locales":
            options.listLocales = true
        case "--save":
            options.save = true
        case "-q", "--quiet":
            options.quiet = true
        case "-o", "--output":
            options.output = try value(after: args[index])
        case "--vocab":
            options.oneOffVocab += try value(after: args[index])
                .split(separator: ",", omittingEmptySubsequences: false)
                .map(String.init)
        case "--vocab-file":
            options.vocabFile = try value(after: args[index])
        case "-h", "--help":
            printUsage()
            exit(0)
        default:
            options.files.append(args[index])
        }
        index += 1
    }

    if options.analysisJSON && (options.timestamps || options.srt || options.json) {
        throw STTError.invalidArguments("--analysis-json은 --timestamps, --srt, --json과 함께 쓸 수 없습니다")
    }
    if options.analysisJSON && options.files.count != 1 {
        throw STTError.invalidArguments("--analysis-json은 오디오 파일 한 개만 받습니다")
    }
    return options
}

func readTerms(at path: String) throws -> [String] {
    let expanded = (path as NSString).expandingTildeInPath
    guard let raw = try? String(contentsOfFile: expanded, encoding: .utf8) else {
        throw STTError.vocabReadFailed(path)
    }
    return raw.components(separatedBy: .newlines)
}

func contextTerms(for options: Options) throws -> ContextTerms {
    let basePath = options.vocabFile ?? "~/.config/stt/vocab.txt"
    let expanded = (basePath as NSString).expandingTildeInPath
    let base: [String]
    if options.vocabFile != nil {
        base = try readTerms(at: basePath)
    } else if FileManager.default.fileExists(atPath: expanded) {
        base = try readTerms(at: basePath)
    } else {
        base = []
    }

    var selected: [String] = []
    var dropped: [String] = []
    var seen = Set<String>()
    let controls = CharacterSet.controlCharacters

    for raw in base + options.oneOffVocab {
        let term = raw.trimmingCharacters(in: .whitespacesAndNewlines)
        if term.isEmpty || term.hasPrefix("#") || !seen.insert(term).inserted { continue }
        let wordCount = term.split(whereSeparator: { $0.isWhitespace }).count
        let invalid = term.unicodeScalars.contains(where: controls.contains)
            || term.utf8.count > 128 || wordCount > 2
        if invalid || selected.count == 100 {
            dropped.append(term)
        } else {
            selected.append(term)
        }
    }
    return ContextTerms(selected: selected, dropped: dropped)
}

func bcp47(_ locale: Locale) -> String { locale.identifier(.bcp47) }

func resolveLocale(_ identifier: String) async throws -> Locale {
    let requested = Locale(identifier: identifier)
    let wanted = bcp47(requested).lowercased()
    let supported = await SpeechTranscriber.supportedLocales
    if let match = supported.first(where: { bcp47($0).lowercased() == wanted }) { return match }

    let language = requested.language.languageCode?.identifier.lowercased()
    if let language, let match = supported.first(where: {
        $0.language.languageCode?.identifier.lowercased() == language
    }) { return match }

    throw STTError.localeUnsupported(identifier, supported.map(bcp47).sorted())
}

func ensureModel(for transcriber: SpeechTranscriber, locale: Locale, quiet: Bool) async throws {
    let installed = await SpeechTranscriber.installedLocales
    if installed.contains(where: { bcp47($0).lowercased() == bcp47(locale).lowercased() }) { return }
    if !quiet { eprint("언어 모델 다운로드 중 (\(bcp47(locale)))") }
    if let request = try await AssetInventory.assetInstallationRequest(supporting: [transcriber]) {
        try await request.downloadAndInstall()
    }
}

struct ConfidenceSpan: Encodable {
    let startByte: Int
    let endByte: Int
    let confidence: Double

    enum CodingKeys: String, CodingKey {
        case startByte = "start_byte"
        case endByte = "end_byte"
        case confidence
    }
}

enum NullableDouble: Encodable {
    case value(Double)
    case null

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .value(let value): try container.encode(value)
        case .null: try container.encodeNil()
        }
    }
}

struct Alternative: Encodable {
    let text: String
    let start: Double
    let end: Double
    let confidence: NullableDouble
}

struct Segment {
    let start: Double
    let end: Double
    let text: String
    let confidenceSpans: [ConfidenceSpan]
    let reviewConfidence: Double?
    let alternatives: [Alternative]
}

struct LegacySegment: Encodable {
    let start: Double
    let end: Double
    let text: String
}

struct EvidenceSegment: Encodable {
    let id: String
    let start: Double
    let end: Double
    let text: String
    let confidenceSpans: [ConfidenceSpan]
    let reviewConfidence: NullableDouble
    let alternatives: [Alternative]

    enum CodingKeys: String, CodingKey {
        case id, start, end, text, alternatives
        case confidenceSpans = "confidence_spans"
        case reviewConfidence = "review_confidence"
    }
}

func lowerQuantile(_ values: [Double]) -> Double? {
    guard !values.isEmpty else { return nil }
    let sorted = values.sorted()
    return sorted[Int((Double(sorted.count - 1) * 0.1).rounded(.down))]
}

func attributedEvidence(_ attributed: AttributedString) -> ([ConfidenceSpan], Double?) {
    var spans: [ConfidenceSpan] = []
    for run in attributed.runs {
        guard let confidence = run.transcriptionConfidence, confidence.isFinite else { continue }
        let start = String(attributed.characters[..<run.range.lowerBound]).utf8.count
        let end = String(attributed.characters[..<run.range.upperBound]).utf8.count
        guard start < end else { continue }
        spans.append(ConfidenceSpan(startByte: start, endByte: end, confidence: confidence))
    }
    return (spans, lowerQuantile(spans.map(\.confidence)))
}

func attributedTimeBounds(_ attributed: AttributedString, fallback: (Double, Double)) -> (Double, Double) {
    let ranges = attributed.runs.compactMap { $0.audioTimeRange }
    let starts = ranges.map { $0.start.seconds }.filter { $0.isFinite }
    let ends = ranges.map { $0.end.seconds }.filter { $0.isFinite }
    return (starts.min() ?? fallback.0, ends.max() ?? fallback.1)
}

func transcribe(url: URL, locale: Locale, context: [String], quiet: Bool) async throws -> ([Segment], Int) {
    var preset = SpeechTranscriber.Preset.timeIndexedTranscriptionWithAlternatives
    preset.attributeOptions.insert(.audioTimeRange)
    preset.attributeOptions.insert(.transcriptionConfidence)
    preset.reportingOptions.insert(.alternativeTranscriptions)
    preset.reportingOptions.remove(.fastResults)
    let transcriber = SpeechTranscriber(locale: locale, preset: preset)
    try await ensureModel(for: transcriber, locale: locale, quiet: quiet)

    let analyzer = SpeechAnalyzer(modules: [transcriber])
    if !context.isEmpty {
        let analysisContext = AnalysisContext()
        analysisContext.contextualStrings[.general] = context
        try await analyzer.setContext(analysisContext)
        if !quiet { eprint("어휘 힌트 \(context.count)개 적용") }
    }

    let collector = Task { () throws -> [Segment] in
        var segments: [Segment] = []
        for try await result in transcriber.results {
            let text = String(result.text.characters)
            if text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { continue }
            let start = result.range.start.seconds.isFinite ? result.range.start.seconds : 0
            let rawEnd = result.range.end.seconds
            let end = rawEnd.isFinite ? rawEnd : start
            let (confidenceSpans, reviewConfidence) = attributedEvidence(result.text)
            let alternatives = result.alternatives.compactMap { alternative -> Alternative? in
                let alternativeText = String(alternative.characters)
                guard !alternativeText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                      alternativeText != text else { return nil }
                let (_, confidence) = attributedEvidence(alternative)
                let bounds = attributedTimeBounds(alternative, fallback: (start, end))
                return Alternative(
                    text: alternativeText,
                    start: bounds.0,
                    end: bounds.1,
                    confidence: confidence.map(NullableDouble.value) ?? .null
                )
            }
            segments.append(Segment(
                start: start,
                end: end,
                text: text,
                confidenceSpans: confidenceSpans,
                reviewConfidence: reviewConfidence,
                alternatives: alternatives
            ))
        }
        return segments
    }

    let audioFile = try AVAudioFile(forReading: url)
    let duration = audioFile.fileFormat.sampleRate > 0
        ? Int((Double(audioFile.length) / audioFile.fileFormat.sampleRate * 1000).rounded()) : 0
    if let last = try await analyzer.analyzeSequence(from: audioFile) {
        try await analyzer.finalizeAndFinish(through: last)
    } else {
        await analyzer.cancelAndFinishNow()
    }
    return (try await collector.value, duration)
}

func sha256(url: URL) throws -> String {
    let handle = try FileHandle(forReadingFrom: url)
    defer { try? handle.close() }
    var hasher = SHA256()
    while let chunk = try handle.read(upToCount: 1_048_576), !chunk.isEmpty {
        hasher.update(data: chunk)
    }
    return hasher.finalize().map { String(format: "%02x", $0) }.joined()
}

func sha256(text: String) -> String {
    SHA256.hash(data: Data(text.utf8)).map { String(format: "%02x", $0) }.joined()
}

struct AnalysisDocument: Encodable {
    struct Source: Encodable {
        let audioSha256: String
        let durationMs: Int
        enum CodingKeys: String, CodingKey {
            case audioSha256 = "audio_sha256"
            case durationMs = "duration_ms"
        }
    }
    struct Capabilities: Encodable {
        let alternatives: Bool
        let confidence: Bool
        let audioTimeRange: Bool
        enum CodingKeys: String, CodingKey {
            case alternatives, confidence
            case audioTimeRange = "audio_time_range"
        }
    }
    struct Context: Encodable {
        let fingerprint: String
        let selected: [String]
        let dropped: [String]
    }
    struct ReviewMethod: Encodable {
        let name = "lower_quantile"
        let version = 1
        let quantile = 0.1
    }

    let schemaVersion = 1
    let engine = "apple-speech-transcriber"
    let engineVersion: String
    let locale: String
    let offsetUnit = "utf8_bytes"
    let source: Source
    let capabilities: Capabilities
    let context: Context
    let reviewConfidenceMethod = ReviewMethod()
    let segments: [EvidenceSegment]

    enum CodingKeys: String, CodingKey {
        case engine, locale, source, capabilities, context, segments
        case schemaVersion = "schema_version"
        case engineVersion = "engine_version"
        case offsetUnit = "offset_unit"
        case reviewConfidenceMethod = "review_confidence_method"
    }
}

func analysisDocument(segments: [Segment], durationMs: Int, audioURL: URL,
                      locale: Locale, context: ContextTerms) throws -> AnalysisDocument {
    let evidence = segments.enumerated().map { index, segment in
        EvidenceSegment(
            id: String(format: "s%04d", index + 1),
            start: segment.start,
            end: segment.end,
            text: segment.text,
            confidenceSpans: segment.confidenceSpans,
            reviewConfidence: segment.reviewConfidence.map(NullableDouble.value) ?? .null,
            alternatives: segment.alternatives
        )
    }
    let executable = Bundle.main.executableURL
    let engineVersion = executable.flatMap { try? sha256(url: $0) } ?? "unavailable"
    return AnalysisDocument(
        engineVersion: engineVersion,
        locale: bcp47(locale),
        source: .init(audioSha256: try sha256(url: audioURL), durationMs: durationMs),
        capabilities: .init(
            alternatives: segments.contains { !$0.alternatives.isEmpty },
            confidence: segments.contains { !$0.confidenceSpans.isEmpty },
            audioTimeRange: segments.contains { $0.end > $0.start }
        ),
        context: .init(
            fingerprint: sha256(text: context.selected.joined(separator: "\u{0}")),
            selected: context.selected,
            dropped: context.dropped
        ),
        segments: evidence
    )
}

func fmtClock(_ seconds: Double) -> String {
    let total = Int(seconds.rounded())
    let (hours, minutes, secs) = (total / 3600, (total % 3600) / 60, total % 60)
    return hours > 0 ? String(format: "%d:%02d:%02d", hours, minutes, secs)
        : String(format: "%02d:%02d", minutes, secs)
}

func fmtSRT(_ seconds: Double) -> String {
    let milliseconds = max(0, Int((seconds * 1000).rounded()))
    return String(format: "%02d:%02d:%02d,%03d", milliseconds / 3_600_000,
                  (milliseconds % 3_600_000) / 60_000,
                  (milliseconds % 60_000) / 1000, milliseconds % 1000)
}

func encodeJSON<T: Encodable>(_ value: T) throws -> String {
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.prettyPrinted, .withoutEscapingSlashes, .sortedKeys]
    return String(decoding: try encoder.encode(value), as: UTF8.self)
}

func render(_ segments: [Segment], options: Options, analysis: AnalysisDocument?) throws -> String {
    if let analysis { return try encodeJSON(analysis) }
    if options.srt {
        return segments.enumerated().map { index, segment in
            "\(index + 1)\n\(fmtSRT(segment.start)) --> \(fmtSRT(segment.end))\n\(segment.text.trimmingCharacters(in: .whitespacesAndNewlines))\n"
        }.joined(separator: "\n")
    }
    if options.json {
        return try encodeJSON(segments.map {
            LegacySegment(start: $0.start, end: $0.end,
                          text: $0.text.trimmingCharacters(in: .whitespacesAndNewlines))
        })
    }
    if options.timestamps {
        return segments.map {
            "[\(fmtClock($0.start))] \($0.text.trimmingCharacters(in: .whitespacesAndNewlines))"
        }.joined(separator: "\n")
    }
    return segments.map { $0.text.trimmingCharacters(in: .whitespacesAndNewlines) }
        .joined(separator: " ")
}

func outputExtension(_ options: Options) -> String {
    if options.srt { return "srt" }
    if options.json || options.analysisJSON { return "json" }
    return "txt"
}

#if !APPLE_STT_TESTING
@main
struct AppleSTT {
    static func main() async {
        let options: Options
        do { options = try parseArgs() }
        catch { eprint("\(error)"); exit(2) }

        if options.listLocales {
            let supported = await SpeechTranscriber.supportedLocales
            let installed = Set((await SpeechTranscriber.installedLocales).map { bcp47($0).lowercased() })
            print("지원 로케일 (설치됨 표시):")
            for locale in supported.map(bcp47).sorted() {
                print("  \(installed.contains(locale.lowercased()) ? "*" : "-") \(locale)")
            }
            return
        }
        guard !options.files.isEmpty else { printUsage(); exit(1) }

        let locale: Locale
        let context: ContextTerms
        do {
            locale = try await resolveLocale(options.localeID)
            context = try contextTerms(for: options)
        } catch {
            eprint("\(error)")
            exit(1)
        }
        if !options.quiet, !context.dropped.isEmpty {
            eprint("context \(context.dropped.count)개 제외, \(context.selected.count)개 적용")
        }

        var failures = 0
        for (index, path) in options.files.enumerated() {
            let url = URL(fileURLWithPath: (path as NSString).expandingTildeInPath)
            guard FileManager.default.fileExists(atPath: url.path) else {
                eprint("파일 없음: \(path)")
                failures += 1
                continue
            }
            if !options.quiet { eprint("전사 중: \(url.lastPathComponent) [\(bcp47(locale))]") }
            do {
                let (segments, durationMs) = try await transcribe(
                    url: url, locale: locale, context: context.selected, quiet: options.quiet
                )
                guard !segments.isEmpty else {
                    eprint("결과 없음(무음/인식 실패): \(url.lastPathComponent)")
                    failures += 1
                    continue
                }
                let document = options.analysisJSON
                    ? try analysisDocument(segments: segments, durationMs: durationMs,
                                           audioURL: url, locale: locale, context: context)
                    : nil
                let text = try render(segments, options: options, analysis: document)

                if options.save {
                    let destination = url.deletingPathExtension().appendingPathExtension(outputExtension(options))
                    try (text + "\n").write(to: destination, atomically: true, encoding: .utf8)
                } else if let output = options.output, options.files.count == 1 {
                    try (text + "\n").write(toFile: (output as NSString).expandingTildeInPath,
                                              atomically: true, encoding: .utf8)
                } else {
                    if options.files.count > 1 {
                        if index > 0 { print("") }
                        print("===== \(url.lastPathComponent) =====")
                    }
                    print(text)
                }
            } catch {
                eprint("실패 (\(url.lastPathComponent)): \(error)")
                failures += 1
            }
        }
        exit(failures == 0 ? 0 : 1)
    }
}
#endif
