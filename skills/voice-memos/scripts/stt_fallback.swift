#!/usr/bin/env swift
/// Apple SFSpeechRecognizer를 사용한 오프라인 음성 전사.
/// tsrp atom이 없는 Voice Memos 파일의 fallback 전사용.
///
/// Usage:
///   swift stt_fallback.swift <audio_file> [--language ko-KR]
///   swift stt_fallback.swift --list-no-tsrp
///   swift stt_fallback.swift --batch [--language ko-KR]

import Foundation
import Speech
import AVFoundation

let defaultDataDir = FileManager.default.homeDirectoryForCurrentUser
    .appendingPathComponent("Library/Mobile Documents/com~apple~CloudDocs/voice-memos")
let dataDir = ProcessInfo.processInfo.environment["VOICE_MEMOS_DATA_DIR"]
    .flatMap { $0.isEmpty ? nil : URL(fileURLWithPath: NSString(string: $0).expandingTildeInPath) }
    ?? defaultDataDir
let transcriptsDir = dataDir.appendingPathComponent("transcripts")

// MARK: - tsrp 체크

func hasTsrp(_ path: String) -> Bool {
    guard let data = try? Data(contentsOf: URL(fileURLWithPath: path)) else { return false }
    return data.range(of: "tsrp".data(using: .utf8)!) != nil
}

// MARK: - 파일명 파싱

func parseDateFromFilename(_ filename: String) -> (datePart: String, timePart: String, dateStr: String) {
    let base = filename
        .replacingOccurrences(of: ".m4a", with: "")
        .replacingOccurrences(of: ".qta", with: "")
        .components(separatedBy: "-")[0]
        .trimmingCharacters(in: .whitespaces)

    let formatter = DateFormatter()
    formatter.dateFormat = "yyyyMMdd HHmmss"
    if let date = formatter.date(from: base) {
        let df = DateFormatter()
        df.dateFormat = "yyyyMMdd"
        let datePart = df.string(from: date)
        df.dateFormat = "HHmmss"
        let timePart = df.string(from: date)
        df.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let dateStr = df.string(from: date)
        return (datePart, timePart, dateStr)
    }
    let d = String(base.prefix(8))
    let t = base.count > 8 ? String(base.dropFirst(9).prefix(6)) : "000000"
    return (d, t, base)
}

// MARK: - 전사

func transcribe(audioPath: String, language: String, completion: @escaping (String?) -> Void) {
    let locale = Locale(identifier: language)
    guard let recognizer = SFSpeechRecognizer(locale: locale) else {
        fputs("Error: SFSpeechRecognizer not available for locale \(language)\n", stderr)
        completion(nil)
        return
    }

    guard recognizer.isAvailable else {
        fputs("Error: Speech recognizer not available. Check System Settings > Privacy > Speech Recognition.\n", stderr)
        completion(nil)
        return
    }

    // 온디바이스 전사 요청
    if recognizer.supportsOnDeviceRecognition {
        fputs("  Using on-device recognition\n", stderr)
    }

    let url = URL(fileURLWithPath: audioPath)
    let request = SFSpeechURLRecognitionRequest(url: url)
    request.requiresOnDeviceRecognition = recognizer.supportsOnDeviceRecognition
    request.shouldReportPartialResults = false

    recognizer.recognitionTask(with: request) { result, error in
        if let error = error {
            fputs("Error: \(error.localizedDescription)\n", stderr)
            completion(nil)
            return
        }
        if let result = result, result.isFinal {
            completion(result.bestTranscription.formattedString)
        }
    }
}

// MARK: - 마크다운 생성

func generateMarkdown(filename: String, text: String, language: String) -> String {
    let (_, _, dateStr) = parseDateFromFilename(filename)
    return """
    # \(dateStr)

    - **녹음일시**: \(dateStr)
    - **언어**: \(language)
    - **원본파일**: `\(filename)`
    - **전사방식**: SFSpeechRecognizer (fallback)

    ## 전사 내용

    \(text)

    """
}

// MARK: - 저장

func saveTranscript(filename: String, text: String, language: String) -> String? {
    let (datePart, timePart, _) = parseDateFromFilename(filename)

    let outDir = transcriptsDir.appendingPathComponent(datePart).appendingPathComponent(timePart)
    let outPath = outDir.appendingPathComponent("transcript.md")

    // 이미 존재하면 스킵
    if FileManager.default.fileExists(atPath: outPath.path) {
        fputs("  Already exists: \(datePart)/\(timePart)/transcript.md\n", stderr)
        return nil
    }

    let md = generateMarkdown(filename: filename, text: text, language: language)

    do {
        try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
        try md.write(to: outPath, atomically: true, encoding: .utf8)
        return "\(datePart)/\(timePart)/transcript.md"
    } catch {
        fputs("Error writing: \(error.localizedDescription)\n", stderr)
        return nil
    }
}

// MARK: - Main

let args = CommandLine.arguments
let homeDir = FileManager.default.homeDirectoryForCurrentUser
let recordingsDir = homeDir
    .appendingPathComponent("Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings")

// 언어 파싱
var language = "ko-KR"
if let langIdx = args.firstIndex(of: "--language"), langIdx + 1 < args.count {
    language = args[langIdx + 1]
}

// --list-no-tsrp: tsrp 없는 파일 목록 출력
if args.contains("--list-no-tsrp") {
    let enumerator = FileManager.default.enumerator(at: recordingsDir, includingPropertiesForKeys: nil)
    var noTsrp: [String] = []
    while let url = enumerator?.nextObject() as? URL {
        if url.pathExtension == "m4a" && !hasTsrp(url.path) {
            noTsrp.append(url.lastPathComponent)
        }
    }
    noTsrp.sort()
    print("\(noTsrp.count)개 파일에 tsrp 없음:")
    for name in noTsrp {
        print("  \(name)")
    }
    exit(0)
}

// --batch: tsrp 없는 모든 파일 일괄 전사
if args.contains("--batch") {
    let enumerator = FileManager.default.enumerator(at: recordingsDir, includingPropertiesForKeys: nil)
    var targets: [URL] = []
    while let url = enumerator?.nextObject() as? URL {
        if url.pathExtension == "m4a" && !hasTsrp(url.path) {
            // 이미 전사된 것 스킵
            let (dp, tp, _) = parseDateFromFilename(url.lastPathComponent)
            let existing = transcriptsDir
                .appendingPathComponent("\(dp)/\(tp)/transcript.md")
            if !FileManager.default.fileExists(atPath: existing.path) {
                targets.append(url)
            }
        }
    }
    targets.sort { $0.lastPathComponent < $1.lastPathComponent }

    if targets.isEmpty {
        print("전사할 파일 없음 (모두 처리됨)")
        exit(0)
    }

    print("\(targets.count)개 파일 전사 시작...")
    let semaphore = DispatchSemaphore(value: 0)
    var processed = 0
    var currentIndex = 0

    func processNext() {
        guard currentIndex < targets.count else {
            semaphore.signal()
            return
        }
        let url = targets[currentIndex]
        currentIndex += 1
        let filename = url.lastPathComponent
        fputs("[\(currentIndex)/\(targets.count)] \(filename)\n", stderr)

        transcribe(audioPath: url.path, language: language) { text in
            if let text = text, !text.isEmpty {
                if let saved = saveTranscript(filename: filename, text: text, language: language) {
                    print("  \(filename) → \(saved)")
                    processed += 1
                }
            } else {
                fputs("  \(filename) → 전사 실패 또는 빈 결과\n", stderr)
            }
            processNext()
        }
    }

    processNext()
    semaphore.wait()
    print("\n\(processed)/\(targets.count) 처리됨")
    exit(0)
}

// 단일 파일 전사
guard args.count >= 2, !args[1].hasPrefix("--") else {
    fputs("""
    Usage:
      swift stt_fallback.swift <audio_file> [--language ko-KR]
      swift stt_fallback.swift --list-no-tsrp
      swift stt_fallback.swift --batch [--language ko-KR]

    Options:
      --language    BCP-47 locale (default: ko-KR)
      --list-no-tsrp  tsrp atom이 없는 파일 목록
      --batch       tsrp 없는 모든 파일 일괄 전사

    """, stderr)
    exit(1)
}

let audioPath = args[1]
guard FileManager.default.fileExists(atPath: audioPath) else {
    fputs("File not found: \(audioPath)\n", stderr)
    exit(1)
}

let semaphore = DispatchSemaphore(value: 0)
let filename = URL(fileURLWithPath: audioPath).lastPathComponent
fputs("Transcribing: \(filename)\n", stderr)

transcribe(audioPath: audioPath, language: language) { text in
    if let text = text, !text.isEmpty {
        if let saved = saveTranscript(filename: filename, text: text, language: language) {
            print("\(filename) → \(saved)")
        } else {
            // 이미 존재할 때는 stdout으로 전사 결과만 출력
            print(text)
        }
    } else {
        fputs("전사 실패 또는 빈 결과\n", stderr)
    }
    semaphore.signal()
}

semaphore.wait()
