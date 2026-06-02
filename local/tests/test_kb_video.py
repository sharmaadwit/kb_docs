import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))
import kb_video


class FakeContext:
    def __init__(self, secrets=None):
        self._secrets = dict(secrets or {})

    def get_secret(self, name):
        return self._secrets.get(name)


class TestKbVideo(unittest.TestCase):
    def test_build_video_url_without_end_or_lang(self):
        got = kb_video.build_video_url("abc123", 42.9)
        self.assertEqual(got, "https://www.youtube.com/watch?v=abc123&t=42")

    def test_build_video_url_ignores_end_for_clickable_link(self):
        # Watch URLs have no stop param; end is accepted but not placed in the URL.
        got = kb_video.build_video_url("abc123", 7.8, 19.2)
        self.assertEqual(got, "https://www.youtube.com/watch?v=abc123&t=7")

    def test_build_video_url_with_lang(self):
        got = kb_video.build_video_url("abc123", 42, 120, "hi")
        self.assertEqual(
            got,
            "https://www.youtube.com/watch?v=abc123&t=42"
            "&cc_load_policy=1&cc_lang_pref=hi&hl=hi",
        )

    def test_derive_window_finds_middle_cluster(self):
        cues = [
            {"start": 0.0, "dur": 15.0, "text": "welcome introduction", "lang": "en"},
            {"start": 15.0, "dur": 15.0, "text": "overview basics", "lang": "en"},
            {"start": 30.0, "dur": 15.0, "text": "agent transfer mapping", "lang": "en"},
            {"start": 45.0, "dur": 15.0, "text": "queue intent labels setup", "lang": "en"},
            {"start": 60.0, "dur": 15.0, "text": "final wrap up", "lang": "en"},
        ]
        start, end = kb_video.derive_window(cues, "map transfer queue intents", max_seconds=40)
        self.assertEqual((start, end), (30, 60))

    def test_derive_window_respects_max_seconds_cap(self):
        cues = [
            {"start": 0.0, "dur": 200.0, "text": "queue mapping transfer setup", "lang": "en"},
        ]
        start, end = kb_video.derive_window(cues, "queue mapping", max_seconds=90)
        self.assertEqual((start, end), (0, 90))

    def test_derive_window_zero_overlap_fallback(self):
        cues = [
            {"start": 0.0, "dur": 45.0, "text": "alpha beta", "lang": "en"},
            {"start": 45.0, "dur": 75.0, "text": "gamma delta", "lang": "en"},
        ]
        start, end = kb_video.derive_window(cues, "transfer queue intent", max_seconds=90)
        self.assertEqual((start, end), (0, 90))

    def test_pick_language_requested_supported(self):
        entry = {"caption_langs": ["en", "hi"], "default_lang": "en"}
        self.assertEqual(kb_video.pick_language("hi", "query", entry), ("hi", True))

    def test_pick_language_requested_unsupported_uses_default(self):
        entry = {"caption_langs": ["en", "hi"], "default_lang": "en"}
        self.assertEqual(kb_video.pick_language("ta", "query", entry), ("en", True))

    def test_pick_language_none_available(self):
        entry = {"caption_langs": ["en"], "default_lang": "ta"}
        self.assertEqual(kb_video.pick_language("hi", "query", entry), (None, False))

    def test_select_video_returns_none_when_manifest_read_fails(self):
        original = kb_video.kb_storage.read_json
        try:
            def failing_read_json(path, context=None):
                raise RuntimeError("missing manifest")

            kb_video.kb_storage.read_json = failing_read_json
            row = {"source": "kb/a.md", "heading": "H1", "text": "some text", "score": 1.0}
            with self.assertLogs("kb_video", level="ERROR"):
                got = kb_video.select_video(
                    query="how to setup queue mapping",
                    intent="setup",
                    module="bot-studio",
                    ranked_rows=[row],
                    language="en",
                    context=FakeContext(),
                )
            self.assertIsNone(got)
        finally:
            kb_video.kb_storage.read_json = original

    def test_select_video_returns_expected_payload_with_custom_paths(self):
        manifest_path = "custom/manifest.json"
        transcript_dir = "custom/transcripts"
        transcript_path = "custom/transcripts/vid123.json"
        calls = []

        manifest = [
            {
                "source": "kb/a.md",
                "video_id": "vid123",
                "title": "A walkthrough",
                "default_lang": "en",
                "caption_langs": ["en", "hi"],
                "embeddable": True,
                "intents": ["setup"],
            }
        ]
        transcript = [
            {"start": 0.0, "dur": 20.0, "text": "intro", "lang": "en"},
            {"start": 20.0, "dur": 20.0, "text": "agent transfer queue mapping", "lang": "en"},
            {"start": 40.0, "dur": 20.0, "text": "intent setup details", "lang": "en"},
        ]

        original = kb_video.kb_storage.read_json
        try:
            def fake_read_json(path, context=None):
                calls.append(path)
                if path == manifest_path:
                    return manifest
                if path == transcript_path:
                    return transcript
                raise RuntimeError("unexpected path")

            kb_video.kb_storage.read_json = fake_read_json

            ctx = FakeContext(
                {
                    "KB_VIDEO_MANIFEST_PATH": manifest_path,
                    "KB_VIDEO_TRANSCRIPT_DIR": transcript_dir,
                }
            )
            row = {
                "source": "kb/a.md",
                "heading": "Transfer mapping setup",
                "text": "need queue transfer mapping help",
                "score": 0.88,
            }
            got = kb_video.select_video(
                query="how to setup transfer mapping",
                intent="setup",
                module="bot-studio",
                ranked_rows=[row],
                language="hi",
                context=ctx,
            )
            self.assertIsNotNone(got)
            self.assertEqual(got["video_id"], "vid123")
            self.assertEqual(got["title"], "A walkthrough")
            self.assertEqual(got["source"], "kb/a.md")
            self.assertEqual(got["lang"], "hi")
            self.assertTrue(got["captions_on"])
            self.assertIn("https://www.youtube.com/watch?v=vid123", got["url"])
            self.assertIn("t=", got["url"])
            self.assertNotIn("end=", got["url"])
            self.assertIn("cc_load_policy=1", got["url"])
            self.assertEqual(calls, [manifest_path, transcript_path])
        finally:
            kb_video.kb_storage.read_json = original

    def test_select_video_matches_neighbor_via_also_sources(self):
        # A video mapped to a primary page must also surface when the retriever's
        # top row is a declared neighbor page (also_sources), not the primary.
        manifest = [
            {
                "source": "kb/primary.md",
                "also_sources": ["kb/neighbor.md"],
                "video_id": "vidN",
                "title": "Neighbor walkthrough",
                "default_lang": "en",
                "caption_langs": ["en"],
                "embeddable": True,
            }
        ]
        original = kb_video.kb_storage.read_json
        try:
            def fake_read_json(path, context=None):
                if path == "kb/video_manifest.json":
                    return manifest
                return []  # no transcript -> window falls back

            kb_video.kb_storage.read_json = fake_read_json
            got = kb_video.select_video(
                query="some neighbor topic",
                intent="setup",
                module="x",
                ranked_rows=[{"source": "kb/neighbor.md", "score": 0.9}],
                context=FakeContext({}),
            )
            self.assertIsNotNone(got)
            self.assertEqual(got["video_id"], "vidN")
            # The selected entry keeps its canonical (primary) source for display.
            self.assertEqual(got["source"], "kb/primary.md")
        finally:
            kb_video.kb_storage.read_json = original

    def test_select_video_skips_irrelevant_top_row(self):
        # kb_search has no "I don't know" gate; an off-topic query whose nearest
        # result merely maps to a video must NOT attach that video.
        manifest = [
            {
                "source": "kb/agent-assist/settings.md",
                "video_id": "vidS",
                "title": "Agent Assist Settings",
                "default_lang": "en",
                "caption_langs": ["en"],
                "embeddable": True,
            }
        ]
        original = kb_video.kb_storage.read_json
        try:
            kb_video.kb_storage.read_json = lambda path, context=None: (
                manifest if path == "kb/video_manifest.json" else []
            )
            got = kb_video.select_video(
                query="what is the refund policy",
                intent="definition",
                module="x",
                ranked_rows=[
                    {
                        "source": "kb/agent-assist/settings.md",
                        "heading": "Settings",
                        "text": "configure teams business hours and policy",
                        "score": 0.6,
                    }
                ],
                context=FakeContext({}),
            )
            self.assertIsNone(got)
        finally:
            kb_video.kb_storage.read_json = original


if __name__ == "__main__":
    unittest.main()
