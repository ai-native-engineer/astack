import AppKit
import PDFKit

let folder = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let paragraphs = [
    ["도서관에서 책을 읽습니다.", "Deep learning helps us study.", "01 first line", "02 second line"],
    ["문장 사이 공백을 유지합니다.", "A local reader keeps the original PDF."]
]
func draw(_ lines: [String]) {
    NSColor.white.setFill()
    NSRect(x: 0, y: 0, width: 620, height: 800).fill()
    for (index, line) in lines.enumerated() {
        (line as NSString).draw(at: NSPoint(x: 40, y: 700 - index * 65), withAttributes: [
            .font: NSFont.systemFont(ofSize: 24), .foregroundColor: NSColor.black
        ])
    }
}
for variant in ["reference", "spaced", "reordered", "resized"] {
    let url = folder.appendingPathComponent(variant + ".pdf")
    var box = CGRect(x: 0, y: 0, width: variant == "resized" ? 620 : 600, height: 800)
    let context = CGContext(url as CFURL, mediaBox: &box, nil)!
    for original in paragraphs {
        let lines = variant == "spaced" ? original.map { $0.map(String.init).joined(separator: " ") }
            : variant == "reordered" ? Array(original.reversed()) : original
        context.beginPDFPage(nil)
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(cgContext: context, flipped: false)
        draw(lines)
        NSGraphicsContext.restoreGraphicsState()
        context.endPDFPage()
    }
    context.closePDF()
}
let raster = PDFDocument()
for lines in paragraphs {
    let image = NSImage(size: NSSize(width: 600, height: 800))
    image.lockFocus(); draw(lines); image.unlockFocus()
    raster.insert(PDFPage(image: image)!, at: raster.pageCount)
}
guard raster.write(to: folder.appendingPathComponent("scan.pdf")) else { fatalError("Fixture write failed") }
