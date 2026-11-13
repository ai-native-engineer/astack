"""패널 초기화를 깨뜨리는 DOM ID 누락과 기본 화면 계약을 검사한다."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ASSETS = Path(__file__).resolve().parents[1] / "assets"


class PanelIndex(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.duplicates = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identity = attrs.get("id")
        if identity:
            if identity in self.nodes:
                self.duplicates.add(identity)
            self.nodes[identity] = (tag, attrs)


class ReplyPanelContract(unittest.TestCase):
    def setUp(self):
        self.html = (ASSETS / "reply-panel.html").read_text()
        self.js = (ASSETS / "reply-panel.js").read_text()
        self.panel = PanelIndex()
        self.panel.feed(self.html)

    def test_all_literal_javascript_ids_exist_once(self):
        referenced = set(re.findall(r'(?:el|document\.getElementById)\("([^"\n]+)"\)', self.js))
        self.assertFalse(self.panel.duplicates)
        self.assertEqual(referenced - self.panel.nodes.keys(), set())

    def test_details_live_in_information_not_composer(self):
        dialog = self.html[self.html.index('<dialog id="context-view"'):self.html.index('</dialog>')]
        for identity in ("selection-summary", "payload-preview", "connection", "status", "actions", "copy"):
            self.assertIn(f'id="{identity}"', dialog)
        self.assertNotIn("toggle", self.panel.nodes)
        self.assertNotIn("recipient", self.panel.nodes)
        self.assertNotIn("dockHidden", self.js)
        self.assertIn("session-jump", self.panel.nodes)
        self.assertIn("annotation-trigger", self.panel.nodes)
        self.assertIn("annotationDraft", self.js)

    def test_source_remains_sandboxed_and_loading_is_explicit(self):
        sandbox = self.panel.nodes["document"][1]["sandbox"].split()
        self.assertNotIn("allow-same-origin", sandbox)
        self.assertIn("allow-scripts", sandbox)
        self.assertNotIn("hidden", self.panel.nodes["loading"][1])
        self.assertIn('event.source !== el("document").contentWindow', self.js)


if __name__ == "__main__":
    unittest.main()
