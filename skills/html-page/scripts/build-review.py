#!/usr/bin/env python3
"""Build a frozen, offline review sheet from one UTF-8 Markdown source."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import mimetypes
import os
from pathlib import Path
import re
import tempfile

TEMPLATE = Path(__file__).resolve().parents[1] / "assets/review-template.html"
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
H2 = re.compile(r" {0,3}##(?:[ \t]+(.*))?$")
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})(.*)$")


@dataclass
class Section:
    label: str
    kind: str
    heading: str
    start_line: int
    body_start_line: int
    end_line: int
    text: str
    item_id: str = ""


def split_sections(text: str, source_uri: str) -> list[Section]:
    if not text.lstrip("\ufeff").strip():
        raise ValueError("source is empty or whitespace-only; no review was written")
    if "\x00" in text:
        raise ValueError("source contains NUL, which HTML cannot preserve as text")
    # Only CR/LF delimit Markdown lines; other Unicode separators stay in the text.
    lines = re.findall(r"[^\r\n]*(?:\r\n|\r|\n|$)", text)
    if lines and not lines[-1]:
        lines.pop()
    headings = []
    fence = None
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        if index == 0:
            content = content.removeprefix("\ufeff")
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}[ \t]*", content):
                fence = None
            continue
        opening = FENCE.fullmatch(content)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            continue
        heading = H2.fullmatch(content)
        if heading:
            headings.append((index, heading[1] or ""))

    sections = []
    if not headings:
        sections.append(Section("전체 원문 (레벨 2 제목 없음)", "document", "", 1, 1, len(lines), text))
    else:
        first = headings[0][0]
        if first:
            sections.append(Section("머리말", "preamble", "", 1, 1, first, "".join(lines[:first])))
        for position, (index, label) in enumerate(headings):
            end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
            sections.append(Section(label, "section", lines[index], index + 1, index + 2, end, "".join(lines[index + 1:end])))

    occurrences = {}
    for section in sections:
        key = (section.kind, section.label)
        occurrences[key] = occurrences.get(key, 0) + 1
        identity = json.dumps([source_uri, *key, occurrences[key]], ensure_ascii=False)
        section.item_id = "R-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    if len({section.item_id for section in sections}) != len(sections):
        raise ValueError("section ID collision; no review was written")
    return sections


@dataclass
class Element:
    tag: str
    attrs: dict
    start: int
    open_end: int
    parent: Element | None
    end_start: int = 0
    end: int = 0


class TemplateIndex(HTMLParser):
    """Locate structural replacement spans without reserializing scripts or HTML."""

    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.offsets = [0] + [match.end() for match in re.finditer("\n", source)]
        self.elements = []
        self.stack = []
        self.feed(source)
        self.close()
        if self.stack:
            raise ValueError("review template has unclosed elements")

    def source_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_offset()
        node = Element(tag, dict(attrs), start, start + len(self.get_starttag_text()), self.stack[-1] if self.stack else None)
        self.elements.append(node)
        if tag in VOID_TAGS:
            node.end_start = node.end = node.open_end
        else:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            node = self.stack.pop()
            node.end_start = node.end = node.open_end

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1].tag != tag:
            raise ValueError(f"review template has an unmatched closing tag: {tag}")
        node = self.stack.pop()
        node.end_start = self.source_offset()
        node.end = self.source.index(">", node.end_start) + 1

    def one(self, predicate, name):
        matches = [node for node in self.elements if predicate(node)]
        if len(matches) != 1:
            raise ValueError(f"review template must contain exactly one {name}")
        return matches[0]

    def by_id(self, name):
        return self.one(lambda node: node.attrs.get("id") == name, f"#{name}")


def html_text(value: str) -> str:
    # Literal CR is normalized by HTML parsers; a character reference preserves it.
    return escape(value, quote=True).replace("\r", "&#13;")


def html_attr(value: str) -> str:
    return html_text(value).replace("\n", "&#10;").replace("\t", "&#9;")


def render_section(section: Section, source_uri: str, revision: str) -> str:
    item = section.item_id
    label = section.label or "(빈 제목)"
    location = f"{source_uri} · 원문 {section.start_line}–{section.end_line}행 · SHA-256 {revision}"
    body_location = f"본문 {section.body_start_line}–{section.end_line}행" if section.text else "본문 없음"
    answer = f"{label} 원문을 확인했습니다 (승인·게시 아님)"
    empty_notice = '<p class="hint">이 제목 아래 본문은 비어 있습니다.</p>' if not section.text else ""
    return f'''<section class="section" id="item-{item}" data-item="{item}"
  data-source-kind="{section.kind}" data-source-label="{html_attr(section.label)}"
  data-source-heading="{html_attr(section.heading)}" data-source-uri="{html_attr(source_uri)}"
  data-source-start-line="{section.start_line}" data-source-end-line="{section.end_line}"
  data-source-body-start-line="{section.body_start_line}" aria-labelledby="title-{item}">
  <h2 id="title-{item}"><span class="section-no">{item}</span><span class="source-label">{html_text(label)}</span></h2>
  <fieldset class="review-row" data-review-state="unanswered" aria-describedby="checklist-hint">
    <legend>{item} 검토</legend>
    <div class="review-line">
      <label class="review-check" for="check-{item}"><input type="checkbox" id="check-{item}" name="{item}"
        value="{html_attr(answer)}" aria-describedby="review-state-{item}"><span>{html_text(answer)}</span></label>
      <span class="review-state" id="review-state-{item}" data-reply-state="unanswered" aria-live="polite">미확인</span>
    </div>
  </fieldset>
  <p class="hint">원문 {section.start_line}–{section.end_line}행 · {body_location}</p>
  {empty_notice}
  <pre class="example-card source-text" id="source-{item}" data-source-text tabindex="0"
    aria-label="{html_attr(label)} 원문" data-comment-anchor="source-{item}"
    data-comment-title="{html_attr(label)}" data-comment-context="{html_attr(location)}"><code>{html_text(section.text)}</code></pre>
  <button type="button" class="source-copy" data-source-copy="source-{item}"
    aria-describedby="copy-status-{item}">{html_text(label)} 본문 복사</button>
  <p class="hint" id="copy-status-{item}" data-source-copy-status role="status">위 원문 본문만 복사합니다. 복사는 확인·승인·게시·회신 전송이 아닙니다.</p>
  <details class="section-notes" id="notes-{item}" hidden>
    <summary id="notes-count-{item}">주석 0</summary><div class="notes-list" id="notes-list-{item}"></div>
  </details>
  <div class="annotation-wire" inert><textarea id="memo-{item}" data-reply-notes tabindex="-1"
    aria-label="{item}에 연결된 주석"></textarea></div>
</section>'''


def local_file(path: Path, role: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_file():
        raise ValueError(f"{role} must be an existing regular file: {path}")
    return resolved


def media_files(paths: list[Path]) -> list[tuple[Path, str]]:
    result = []
    for path in paths:
        resolved = local_file(path, "media")
        mime, _ = mimetypes.guess_type(resolved.name)
        kind = (mime or "").split("/")[0]
        if kind not in {"audio", "video", "image"}:
            raise ValueError(f"unsupported media type (use an audio, video or image file): {path}")
        result.append((resolved, kind))
    return result


def render_media(media: list[tuple[Path, str]]) -> str:
    figures = []
    for index, (path, kind) in enumerate(media, 1):
        uri = html_attr(path.as_uri())
        label = html_attr(path.name)
        if kind == "image":
            element = f'<img class="source-media" src="{uri}" alt="{label}" loading="lazy">'
        else:
            element = f'<{kind} class="source-media" src="{uri}" controls preload="metadata" aria-label="{label}"></{kind}>'
        figures.append(f'<figure class="section" id="source-media-{index}">{element}<figcaption class="hint">{html_text(str(path))}</figcaption></figure>')
    if not figures:
        return ""
    return '<section class="section" aria-labelledby="source-media-title"><h2 id="source-media-title">명시적으로 연결한 로컬 미디어</h2><p class="hint">파일 존재만 확인했습니다. 이 브라우저에서 재생·표시되는지 직접 확인하세요.</p>' + "\n".join(figures) + "</section>"


def render(template: str, source: Path, revision: str, sections: list[Section], title: str, media: list[tuple[Path, str]]) -> str:
    index = TemplateIndex(template)
    root = index.by_id("review-document")
    shared_start = index.by_id("review-orphans")
    title_node = index.one(lambda node: node.tag == "title", "title")
    context_node = index.one(lambda node: node.tag == "meta" and node.attrs.get("name") == "html-reply-context", "reply context meta")
    if root.tag != "main" or shared_start.parent is not root:
        raise ValueError("review template sample/shared-control boundary is invalid")
    # These existing shared elements must remain outside the replaced sample region.
    for name in ("standalone-review", "selection-action", "selection-editor", "selection-storage", "selection-state"):
        if not shared_start.start < index.by_id(name).start < root.end_start:
            raise ValueError(f"review template shared control is outside its preserved region: {name}")
    uri = source.as_uri()
    identity = hashlib.sha256(uri.encode("utf-8")).hexdigest()
    context = f"{title} · 원문 {uri} · SHA-256 {revision} · 생성 시점의 고정 사본이며 원문 변경은 자동 반영되지 않습니다. 복사·체크는 승인이나 게시가 아닙니다."
    header = f'''<header>
  <p class="preview-label">원문 연결 검토 / 드래그 주석</p>
  <h1>{html_text(title)}</h1>
  <p class="reading-guide">원문을 읽고 확인한 항목만 체크하세요. 본문을 선택하면 주석 아이콘이 나타납니다. 선택 후 <kbd>Alt</kbd>+<kbd>Enter</kbd>로도 열 수 있습니다.</p>
  <p class="hint" id="source-summary" data-source-summary>원문: <a href="{html_attr(uri)}">{html_text(str(source))}</a><br>
SHA-256: <code>{revision}</code><br>
생성 시점의 고정 사본입니다. 원문 변경은 자동 반영되지 않으며 다시 생성해야 합니다.</p>
  <p class="hint" id="checklist-hint">체크하면 초록, 미확인은 빨강입니다. 복사와 주석 입력은 체크·승인·게시·전송이 아닙니다. 본문 복사는 제목 줄을 제외하고 원래 공백·줄바꿈·출처 링크를 보존합니다.</p>
  <p class="hint" id="review-storage-status" role="status"></p>
  <p class="notice" id="review-validation" role="status"></p>
  <p class="notice" id="review-selection-status" role="status"></p>
</header>
<noscript><p class="notice">원문을 읽고 직접 선택해 복사할 수 있습니다. 체크 상태 표시, 주석, 초안 보관과 복사 버튼에는 자바스크립트가 필요합니다.</p></noscript>'''
    content = "\n" + header + "\n" + render_media(media) + "\n" + "\n\n".join(render_section(section, uri, revision) for section in sections) + "\n\n"
    opening = template[root.start:root.open_end - 1] + f' data-source-id="{identity}" data-source-revision="{revision}">'
    meta = f'<meta name="html-reply-context" content="{html_attr(context)}">\n<meta name="html-review-source" content="{html_attr(uri)}">\n<meta name="html-review-source-sha256" content="{revision}">'
    replacements = [
        (title_node.start, title_node.end, f"<title>{html_text(title)}</title>"),
        (context_node.start, context_node.end, meta),
        (root.start, root.open_end, opening),
        (root.open_end, shared_start.start, content),
    ]
    for start, end, replacement in sorted(replacements, reverse=True):
        template = template[:start] + replacement + template[end:]
    return template


def validate_output(output: Path, protected: list[Path], force: bool) -> None:
    if output.is_symlink():
        raise ValueError(f"output must not be a symlink: {output}")
    if any(output == path or (output.exists() and output.samefile(path)) for path in protected):
        raise ValueError("output must not replace the source, template or linked media")
    if output.exists():
        if not output.is_file():
            raise ValueError(f"output must be a regular file: {output}")
        if not force:
            raise ValueError(f"output already exists; choose another path or explicitly pass --force: {output}")


def write_output(output: Path, content: bytes, protected: list[Path], force: bool) -> None:
    validate_output(output, protected, force)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=f".{output.name}.", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        validate_output(output, protected, force)
        if force:
            os.replace(temporary, output)
        else:
            # Atomic publication without clobbering a file created after validation.
            os.link(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="one existing UTF-8 Markdown file; never modified")
    parser.add_argument("--output", required=True, type=Path, help="HTML file in an existing directory")
    parser.add_argument("--title", help="document title (defaults to the source filename)")
    parser.add_argument("--media", action="append", nargs="+", type=Path, default=[], help="explicit existing local image/audio/video files; repeatable; linked, not copied")
    parser.add_argument("--force", action="store_true", help="atomically replace an existing regular output file after validation")
    args = parser.parse_args(argv)
    try:
        source = local_file(args.source, "source")
        template_path = local_file(TEMPLATE, "template")
        raw = source.read_bytes()
        sections = split_sections(raw.decode("utf-8"), source.as_uri())
        revision = hashlib.sha256(raw).hexdigest()
        title = args.title if args.title is not None else f"원문 검토 · {source.name}"
        if not title.strip() or "\x00" in title:
            raise ValueError("title must be nonempty text without NUL")
        media = media_files([path for group in args.media for path in group])
        requested_output = args.output.expanduser()
        parent = requested_output.parent.resolve(strict=True)
        if not parent.is_dir():
            raise ValueError(f"output parent must be an existing directory: {parent}")
        output = parent / requested_output.name
        protected = [source, template_path, *(path for path, _ in media)]
        validate_output(output, protected, args.force)
        page = render(template_path.read_text(encoding="utf-8"), source, revision, sections, title, media)
        write_output(output, page.encode("utf-8"), protected, args.force)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"output": str(output), "source": str(source), "source_sha256": revision, "items": len(sections), "media": len(media)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
