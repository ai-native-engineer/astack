import Foundation
import PDFKit

func stop(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(2)
}

let usage = """
Usage: swift inspect-pdf-text.swift OUTPUT.pdf [--source INPUT.pdf]
       [--pages 1,3,10|all] [--expect "exact phrase"]... [--preserve-text]

Reads PDFs only; emits UTF-8 JSON. Defaults to first/middle/last text samples.
Checks all page geometry with --source and counts empty text pages in the output.
--expect requires literal, whitespace-sensitive text within the inspected pages.
--preserve-text requires --source and compares non-whitespace text/order on those pages.
Exit 2 means a requested check failed or an input was invalid.
Passing checks do not guarantee OCR accuracy, reading order, or image/pixel preservation.
"""

var arguments = Array(CommandLine.arguments.dropFirst())
if arguments.isEmpty || arguments == ["--help"] { print(usage); exit(0) }
let outputURL = URL(fileURLWithPath: arguments.removeFirst())
var sourceURL: URL?
var pageSpec: String?
var phrases: [String] = []
var preserveText = false
while !arguments.isEmpty {
    let option = arguments.removeFirst()
    if option == "--preserve-text" { preserveText = true; continue }
    guard ["--source", "--pages", "--expect"].contains(option), !arguments.isEmpty else {
        stop("Unknown option or missing value: \(option)\n\(usage)")
    }
    let value = arguments.removeFirst()
    switch option {
    case "--source": sourceURL = URL(fileURLWithPath: value)
    case "--pages": pageSpec = value
    default:
        guard !value.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { stop("--expect needs a nonempty phrase") }
        phrases.append(value)
    }
}
guard !preserveText || sourceURL != nil else { stop("--preserve-text requires --source") }

func openPDF(_ url: URL) -> PDFDocument {
    guard let pdf = PDFDocument(url: url), !pdf.isLocked, pdf.pageCount > 0 else {
        stop("Cannot read PDF (missing, locked, or empty): \(url.path)")
    }
    return pdf
}
let output = openPDF(outputURL)
let source = sourceURL.map(openPDF)
let selected: [Int]
if pageSpec == "all" {
    selected = Array(1...output.pageCount)
} else if let pageSpec {
    let tokens = pageSpec.split(separator: ",", omittingEmptySubsequences: false)
    let numbers = tokens.compactMap { Int($0) }
    guard !numbers.isEmpty, numbers.count == tokens.count,
          numbers.allSatisfy({ $0 >= 1 && $0 <= output.pageCount }) else {
        stop("--pages must contain valid 1-based page numbers or all")
    }
    selected = Set(numbers).sorted()
} else {
    selected = Set([1, (output.pageCount + 1) / 2, output.pageCount]).sorted()
}

var failures: [String] = []
var geometryChanged: [Int] = []
if let source {
    if source.pageCount != output.pageCount { failures.append("page_count_changed") }
    for index in 0..<min(source.pageCount, output.pageCount) {
        guard let a = source.page(at: index), let b = output.page(at: index) else { stop("Unreadable page") }
        let x = a.bounds(for: .mediaBox), y = b.bounds(for: .mediaBox)
        // Ignore sub-hundredth-point serialization differences, not visible page resizing.
        if abs(x.minX-y.minX) > 0.01 || abs(x.minY-y.minY) > 0.01 || abs(x.width-y.width) > 0.01 || abs(x.height-y.height) > 0.01 || a.rotation != b.rotation {
            geometryChanged.append(index + 1)
        }
    }
    if !geometryChanged.isEmpty { failures.append("page_geometry_changed") }
}

var emptyPages: [Int] = []
var pages: [[String: Any]] = []
var texts: [String] = []
var textChanged: [Int] = []
for index in 0..<output.pageCount {
    let text = output.page(at: index)?.string ?? ""
    if text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { emptyPages.append(index + 1) }
    if selected.contains(index + 1) {
        texts.append(text)
        pages.append(["page": index + 1, "text": text])
        if preserveText, let source {
            let before = source.page(at: index)?.string ?? ""
            if before.filter({ !$0.isWhitespace }) != text.filter({ !$0.isWhitespace }) { textChanged.append(index + 1) }
        }
    }
}
if emptyPages.count == output.pageCount { failures.append("no_extractable_text") }
let missing = phrases.filter { phrase in !texts.contains(where: { $0.contains(phrase) }) }
if !missing.isEmpty { failures.append("expected_phrase_missing") }
if !textChanged.isEmpty { failures.append("non_whitespace_text_or_order_changed") }
let result: [String: Any] = [
    "path": outputURL.path, "page_count": output.pageCount, "inspected_pages": selected,
    "empty_text_pages": emptyPages, "geometry_mismatch_pages": geometryChanged,
    "expected_phrases_missing": missing, "nonspace_text_changed_pages": textChanged,
    "preserve_text_requested": preserveText, "failures": failures, "pages": pages,
    "scope": "All output pages checked for text presence; all shared source pages for geometry; only inspected_pages for phrase/text comparison. No pixel or full OCR accuracy check."
]
do {
    let data = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write(Data("\n".utf8))
} catch { stop(error.localizedDescription) }
exit(failures.isEmpty ? 0 : 2)
