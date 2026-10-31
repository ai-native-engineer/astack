from contextlib import redirect_stderr
import hashlib
from html.parser import HTMLParser
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts/build-review.py"
TEMPLATE = SKILL / "assets/review-template.html"
SPEC = importlib.util.spec_from_file_location("build_review", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


class Page(HTMLParser):
    """Collect DOM text/attributes independently of the generator's span index."""

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "text": ""}
        self.nodes.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1]["tag"] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]["tag"] != tag:
            raise AssertionError(f"unmatched closing tag: {tag}")
        self.stack.pop()

    def handle_data(self, value):
        for node in self.stack:
            node["text"] += value

    def by_id(self, value):
        return next(node for node in self.nodes if node["attrs"].get("id") == value)

    @property
    def items(self):
        return [node for node in self.nodes if "data-source-kind" in node["attrs"]]

    @property
    def bodies(self):
        return [self.by_id("source-" + node["attrs"]["data-item"])["text"] for node in self.items]

    def meta(self, name):
        return next(node["attrs"]["content"] for node in self.nodes if node["tag"] == "meta" and node["attrs"].get("name") == name)


class BuildReviewTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.folder = Path(self.directory.name).resolve()
        self.source = self.folder / "업로드 #원문?.md"
        self.output = self.folder / "review.html"
        self.template_bytes = TEMPLATE.read_bytes()

    def write_source(self, text):
        self.source.write_bytes(text.encode("utf-8"))

    def run_cli(self, *args, source=None, output=None):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--source", str(source or self.source), "--output", str(output or self.output), *map(str, args)],
            capture_output=True, text=True, check=False,
        )

    def build(self, text, *args):
        self.write_source(text)
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.source.read_bytes(), text.encode("utf-8"))
        self.assertEqual(TEMPLATE.read_bytes(), self.template_bytes)
        page = Page(self.output.read_text(encoding="utf-8"))
        self.assertFalse(page.stack)
        return page, json.loads(result.stdout)

    def test_korean_upload_keeps_three_bodies_and_source_links(self):
        bodies = ["제목 한 줄\n\n", "설명 첫째 줄\n둘째 줄\n\n출처: [기사](https://example.invalid/a?q=1&v=2)\nhttps://example.invalid/b#anchor\n\n", "고정 댓글\n출처: https://example.invalid/final\n"]
        source = "".join(f"## {label}\n{body}" for label, body in zip(["제목", "설명", "고정 댓글"], bodies))
        page, report = self.build(source)
        self.assertEqual(report["items"], 3)
        self.assertEqual(page.bodies, bodies)
        self.assertEqual([node["attrs"]["data-source-label"] for node in page.items], ["제목", "설명", "고정 댓글"])
        self.assertEqual(page.meta("html-review-source"), self.source.as_uri())
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        self.assertEqual(page.meta("html-review-source-sha256"), digest)
        self.assertEqual(report["source_sha256"], digest)
        self.assertIn(digest, page.meta("html-reply-context"))
        self.assertIn("자동 반영되지", page.by_id("source-summary")["text"])
        for node in page.items:
            item = node["attrs"]["data-item"]
            check = page.by_id("check-" + item)["attrs"]
            self.assertEqual(check["type"], "checkbox")
            self.assertNotIn("checked", check)
            self.assertEqual(page.by_id("source-" + item)["attrs"]["data-comment-anchor"], "source-" + item)
            self.assertIn(digest, page.by_id("source-" + item)["attrs"]["data-comment-context"])
            copy = next(node for node in page.nodes if node["attrs"].get("data-source-copy") == "source-" + item)
            self.assertEqual(copy["tag"], "button")
            self.assertEqual(copy["attrs"]["type"], "button")
            self.assertIn("승인", page.by_id("copy-status-" + item)["text"])
            self.assertIn("data-reply-notes", page.by_id("memo-" + item)["attrs"])
            self.assertIn("hidden", page.by_id("notes-" + item)["attrs"])
        self.assertEqual(page.by_id("selection-state")["text"], '{"version":1,"notes":[],"activeId":null,"recovery":[]}')

    def test_unknown_sections_preamble_and_final_text_reconstruct_original(self):
        source = "# 문서 제목\n머리말\n\n## 낯선 섹션 'A'\n첫째\n## Another heading\n둘째\n\n마지막 출처: https://example.invalid/end"
        page, _ = self.build(source)
        self.assertEqual([node["attrs"]["data-source-kind"] for node in page.items], ["preamble", "section", "section"])
        self.assertEqual([node["attrs"]["data-source-label"] for node in page.items], ["머리말", "낯선 섹션 'A'", "Another heading"])
        rebuilt = "".join(node["attrs"]["data-source-heading"] + body for node, body in zip(page.items, page.bodies))
        self.assertEqual(rebuilt, source)
        self.assertEqual([(node["attrs"]["data-source-start-line"], node["attrs"]["data-source-end-line"]) for node in page.items], [("1", "3"), ("4", "5"), ("6", "9")])

    def test_no_h2_is_explicit_whole_document(self):
        source = "# 제목만\n본문\n### 작은 제목\n출처: https://example.invalid/no-h2"
        page, report = self.build(source)
        self.assertEqual(report["items"], 1)
        self.assertEqual(page.bodies, [source])
        self.assertEqual(page.items[0]["attrs"]["data-source-kind"], "document")
        self.assertIn("레벨 2 제목 없음", page.items[0]["attrs"]["data-source-label"])

    def test_local_file_links_remain_canonical_plain_text(self):
        media = self.folder / "evidence.png"
        media.write_bytes(b"existence only")
        body = f"출처: {media.as_uri()}\n![자료]({media.as_uri()})\n"
        page, _ = self.build("## 설명\n" + body)
        self.assertEqual(page.bodies, [body])
        self.assertFalse(any(node["tag"] in {"img", "audio", "video"} for node in page.nodes))

    def test_fenced_headings_do_not_split_and_unclosed_fence_keeps_rest(self):
        preamble = "```markdown\n## 코드 속 제목\n```\n"
        first = "````python\n## 코드 2\n```\n## 아직 코드\n````\n   ~~~ text\n## 틸드 속\n   ~~~~\n    ## 들여쓴 코드\n"
        last = "```\n## 닫히지 않은 코드\n마지막"
        page, _ = self.build(preamble + "## 실제 첫 제목\n" + first + "## 실제 둘째\n" + last)
        self.assertEqual(page.bodies, [preamble, first, last])
        self.assertEqual([node["attrs"]["data-source-label"] for node in page.items], ["머리말", "실제 첫 제목", "실제 둘째"])

    def test_hostile_html_quotes_newlines_remain_data(self):
        label = '<img src=x onerror="alert(1)"> & "제목"'
        title = '</title><script>alert("title")</script>\n두 번째 줄'
        body = '\n</code></pre><script>alert("source")</script>\n<!-- note --> &amp; & <textarea>"\'\\\n출처: [링크](javascript:alert(1))\n'
        page, _ = self.build(f"## {label}\n{body}", "--title", title)
        self.assertEqual(page.bodies, [body])
        self.assertEqual(page.items[0]["attrs"]["data-source-label"], label)
        self.assertEqual(next(node["text"] for node in page.nodes if node["tag"] == "title"), title)
        self.assertEqual(page.by_id("review-document")["attrs"]["data-source-revision"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertFalse(any(node["tag"] == "img" or any(key.startswith("on") for key in node["attrs"]) for node in page.nodes))
        template_scripts = [node["text"] for node in Page(TEMPLATE.read_text(encoding="utf-8")).nodes if node["tag"] == "script"]
        self.assertEqual([node["text"] for node in page.nodes if node["tag"] == "script"], template_scripts)
        self.assertFalse(any(node["attrs"].get("href", "").startswith("javascript:") for node in page.nodes))

    def test_crlf_leading_blank_lines_and_unicode_separators_are_preserved(self):
        source = "## 제목\r\n\r\n첫 줄\r\n둘째\r셋째\u2028## 제목 아님\r\n"
        page, _ = self.build(source)
        self.assertEqual(page.bodies, [source.split("\r\n", 1)[1]])
        self.assertEqual(page.items[0]["attrs"]["data-source-heading"], "## 제목\r\n")

    def test_utf8_bom_does_not_hide_first_heading(self):
        source = "\ufeff## 제목\n본문\n## 설명\n다음\n"
        page, _ = self.build(source)
        self.assertEqual([node["attrs"]["data-source-label"] for node in page.items], ["제목", "설명"])
        self.assertEqual("".join(node["attrs"]["data-source-heading"] + body for node, body in zip(page.items, page.bodies)), source)

    def test_duplicate_labels_get_stable_unique_ids_and_changed_revision(self):
        source = "## 동일\n첫 본문\n## 동일\n둘째\n"
        first, _ = self.build(source)
        original = self.output.read_bytes()
        result = self.run_cli("--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), original)
        ids = [node["attrs"]["data-item"] for node in first.items]
        all_ids = [node["attrs"]["id"] for node in first.nodes if "id" in node["attrs"]]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(len(ids), len(set(ids)))
        self.write_source(source.replace("첫 본문", "바뀐 본문"))
        result = self.run_cli("--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        changed = Page(self.output.read_text(encoding="utf-8"))
        self.assertEqual([node["attrs"]["data-item"] for node in changed.items], ids)
        self.assertNotEqual(first.meta("html-review-source-sha256"), changed.meta("html-review-source-sha256"))
        self.assertEqual(first.by_id("review-document")["attrs"]["data-source-id"], changed.by_id("review-document")["attrs"]["data-source-id"])
        other = self.folder / "different.md"
        other.write_bytes(self.source.read_bytes())
        result = self.run_cli("--force", source=other)
        self.assertEqual(result.returncode, 0, result.stderr)
        separate = Page(self.output.read_text(encoding="utf-8"))
        self.assertNotEqual(separate.by_id("review-document")["attrs"]["data-source-id"], changed.by_id("review-document")["attrs"]["data-source-id"])
        self.assertNotEqual([node["attrs"]["data-item"] for node in separate.items], ids)

    def test_whitespace_preamble_empty_sections_and_heading_line_are_not_lost(self):
        source = "\n\n## 제목\n## \n## 마지막"
        page, _ = self.build(source)
        self.assertEqual(page.bodies, ["\n\n", "", "", ""])
        self.assertEqual([node["attrs"]["data-source-label"] for node in page.items], ["머리말", "제목", "", "마지막"])
        self.assertEqual("".join(node["attrs"]["data-source-heading"] + body for node, body in zip(page.items, page.bodies)), source)
        self.assertIn("본문은 비어", page.items[1]["text"])
        self.assertIn("빈 제목", page.items[2]["text"])

    def test_missing_source_media_empty_invalid_utf8_fail_before_output(self):
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        result = self.run_cli(source=self.folder)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        self.write_source("## 제목\n본문\n")
        result = self.run_cli("--media", self.folder / "missing.mp4")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        result = self.run_cli("--media", self.folder)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        result = self.run_cli("--title", " ")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        for content in (b"", b" \r\n\t", b"\xff", b"a\x00b"):
            with self.subTest(content=content):
                self.source.write_bytes(content)
                result = self.run_cli()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.output.exists())
                self.assertEqual(self.source.read_bytes(), content)

    def test_explicit_local_media_uses_file_uris_without_reading_markdown_links(self):
        image = self.folder / '이미지 #?.png'
        audio = self.folder / '음성 "인용".wav'
        video = self.folder / "영상.mp4"
        for path in (image, audio, video):
            path.write_bytes(b"test media existence only")
        page, report = self.build("## 원문\n![없는 이미지](missing.png)\n출처: https://example.invalid\n", "--media", image, audio, "--media", video)
        resources = {node["tag"]: node["attrs"] for node in page.nodes if node["tag"] in {"img", "audio", "video"}}
        self.assertEqual(report["media"], 3)
        self.assertEqual(resources["img"]["src"], image.as_uri())
        self.assertEqual(resources["audio"]["src"], audio.as_uri())
        self.assertEqual(resources["video"]["src"], video.as_uri())
        self.assertIn("controls", resources["video"])
        self.assertNotIn("autoplay", resources["audio"])
        self.assertEqual(resources["video"]["preload"], "metadata")
        self.assertIn("missing.png", page.bodies[0])
        self.assertIn("재생·표시", page.by_id("review-document")["text"])
        for path in (image, audio, video):
            self.assertEqual(path.read_bytes(), b"test media existence only")
        unsupported = self.folder / "script.html"
        unsupported.write_text("<script>bad()</script>", encoding="utf-8")
        previous = self.output.read_bytes()
        result = self.run_cli("--force", "--media", unsupported)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), previous)

    def test_overwrite_refusal_force_and_validation_preserve_inputs(self):
        source = "## 제목\n원본\n"
        self.write_source(source)
        self.output.write_text("previous review", encoding="utf-8")
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--force", result.stderr)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "previous review")
        result = self.run_cli("--force", "--media", self.folder / "missing.mp4")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "previous review")
        result = self.run_cli("--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.output.read_text(encoding="utf-8").startswith("<!doctype html>"))
        self.assertEqual(self.source.read_text(encoding="utf-8"), source)
        self.assertEqual(TEMPLATE.read_bytes(), self.template_bytes)
        self.assertFalse(list(self.folder.glob(".*.tmp")))

    def test_source_template_media_and_aliases_cannot_be_output_even_with_force(self):
        self.write_source("## 제목\n원본\n")
        hardlink = self.folder / "hardlink.html"
        os.link(self.source, hardlink)
        symlink = self.folder / "symlink.html"
        symlink.symlink_to(self.source)
        dangling = self.folder / "dangling.html"
        dangling.symlink_to(self.folder / "absent")
        media = self.folder / "image.png"
        media.write_bytes(b"original media")
        for output in (self.source, hardlink, symlink, dangling, self.folder):
            with self.subTest(output=output):
                result = self.run_cli("--force", output=output)
                self.assertNotEqual(result.returncode, 0)
        private_template = self.folder / "template.html"
        private_template.write_bytes(self.template_bytes)
        with patch.object(builder, "TEMPLATE", private_template), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                builder.main(["--source", str(self.source), "--output", str(private_template), "--force"])
        self.assertEqual(caught.exception.code, 2)
        self.assertEqual(private_template.read_bytes(), self.template_bytes)
        result = self.run_cli("--force", "--media", media, output=media)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(media.read_bytes(), b"original media")
        self.assertEqual(self.source.read_text(encoding="utf-8"), "## 제목\n원본\n")
        self.assertEqual(TEMPLATE.read_bytes(), self.template_bytes)
        self.assertTrue(symlink.is_symlink())
        self.assertTrue(dangling.is_symlink())
        result = self.run_cli(output=self.folder / "missing-directory" / "review.html")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.folder / "missing-directory").exists())

    def test_atomic_no_clobber_on_race_and_replace_failure(self):
        original_link = os.link

        def racing_link(temporary, output):
            output.write_bytes(b"concurrent writer")
            return original_link(temporary, output)

        with patch.object(builder.os, "link", side_effect=racing_link):
            with self.assertRaises(FileExistsError):
                builder.write_output(self.output, b"generated", [], False)
        self.assertEqual(self.output.read_bytes(), b"concurrent writer")
        with patch.object(builder.os, "replace", side_effect=OSError("replace failed")):
            with self.assertRaises(OSError):
                builder.write_output(self.output, b"generated", [], True)
        self.assertEqual(self.output.read_bytes(), b"concurrent writer")
        self.assertFalse(list(self.folder.glob(".*.tmp")))

    def test_template_shared_region_and_script_preserved_verbatim(self):
        page, _ = self.build("## 제목\n본문\n")
        original = TEMPLATE.read_text(encoding="utf-8")
        generated = self.output.read_text(encoding="utf-8")
        original_index = builder.TemplateIndex(original)
        generated_index = builder.TemplateIndex(generated)
        self.assertEqual(original[original_index.by_id("review-orphans").start:], generated[generated_index.by_id("review-orphans").start:])
        for name in ("standalone-review", "selection-action", "selection-editor", "selection-storage", "selection-state"):
            page.by_id(name)
        self.assertFalse(any(node["attrs"].get("data-item") in {"C1", "C2", "C3"} for node in page.nodes))
        broken = original.replace('id="review-orphans"', 'id="wrong-boundary"')
        with self.assertRaisesRegex(ValueError, "review-orphans"):
            builder.render(broken, self.source, "revision", builder.split_sections("## 제목\n본문", self.source.as_uri()), "제목", [])

    def test_template_index_maps_multiline_html_positions_to_exact_spans(self):
        opening = '<pre\n id="source" data-label="가 > 나">'
        content = '원문 &lt;tag&gt;\r\n둘째 줄'
        script = '<script>const marker = "<main>";\n</script>'
        fragment = '<main>\r\n' + opening + content + '</pre>\n' + script + '</main>'
        index = builder.TemplateIndex(fragment)
        node = index.by_id("source")
        self.assertEqual(fragment[node.start:node.open_end], opening)
        self.assertEqual(fragment[node.open_end:node.end_start], content)
        self.assertEqual(fragment[node.end_start:node.end], '</pre>')
        script_node = index.one(lambda element: element.tag == "script", "script")
        self.assertEqual(fragment[script_node.start:script_node.end], script)
        self.assertEqual(index.source_offset(), len(fragment))


if __name__ == "__main__":
    unittest.main()
