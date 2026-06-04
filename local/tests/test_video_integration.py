"""
End-to-end integration tests for the YouTube video wiring in kb_answer/kb_search.

These exercise the REAL kb_answer()/kb_search() code paths (scoring, evidence,
selection, append) and stub ONLY the network boundary:
  - chunk loading  -> local kb/kb_chunks.jsonl
  - kb_storage.read_json (manifest + transcripts) -> local files
  - langfuse senders -> no-op

They lock in the behavior that:
  1. A substantive answer that maps to a video appends a clickable **Watch:** link
     and returns a structured `video` field.
  2. An "I don't know" answer never attaches a video (the gate).
  3. kb_search attaches a video to a mapped top result.
  4. An unmapped page yields no video (graceful skip, no broken link).

Run:  python3 local/tests/test_video_integration.py
"""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "skill"))

import kb_storage
import kb_answer
import kb_search

CHUNKS_PATH = os.path.join(ROOT, "kb", "kb_chunks.jsonl")
MANIFEST_PATH = os.path.join(ROOT, "kb", "video_manifest.json")


def _load_chunks_local(context=None):
    items = []
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
    return items


def _read_json_local(path, context=None):
    # path is repo-relative (e.g. "kb/video_manifest.json"); resolve against ROOT.
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


class FakeContext:
    def get_secret(self, name):
        return None


@unittest.skipUnless(
    os.path.exists(CHUNKS_PATH) and os.path.exists(MANIFEST_PATH),
    "requires local kb/kb_chunks.jsonl and kb/video_manifest.json",
)
class TestVideoIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig = {
            "ans_chunks": kb_answer._load_chunks,
            "srch_chunks": kb_search._load_chunks,
            "ans_lf": kb_answer._send_langfuse,
            "srch_lf": kb_search._compact_langfuse,
            "read_json": kb_storage.read_json,
        }
        kb_answer._load_chunks = _load_chunks_local
        kb_search._load_chunks = _load_chunks_local
        kb_answer._send_langfuse = lambda *a, **k: {}
        kb_search._compact_langfuse = lambda *a, **k: {}
        kb_storage.read_json = _read_json_local
        cls.ctx = FakeContext()

    @classmethod
    def tearDownClass(cls):
        kb_answer._load_chunks = cls._orig["ans_chunks"]
        kb_search._load_chunks = cls._orig["srch_chunks"]
        kb_answer._send_langfuse = cls._orig["ans_lf"]
        kb_search._compact_langfuse = cls._orig["srch_lf"]
        kb_storage.read_json = cls._orig["read_json"]

    def test_substantive_answer_appends_video_link(self):
        res = kb_answer.kb_answer({"query": "how do agent assist reports work"}, context=self.ctx)
        self.assertTrue(res.get("ok"))
        video = res.get("video")
        self.assertIsNotNone(video, "expected a video for a mapped, substantive answer")
        self.assertTrue(video["url"].startswith("https://www.youtube.com/watch?v="))
        # The clickable link must be appended to the answer text.
        self.assertIn("**Watch:**", res["answer"])
        self.assertIn(video["url"], res["answer"])
        # Timestamps must be sane integers with end after start when present.
        self.assertIsInstance(video["start"], int)
        if video["end"] is not None:
            self.assertGreaterEqual(video["end"], video["start"])

    def test_idk_answer_never_attaches_video(self):
        res = kb_answer.kb_answer(
            {"query": "what is the refund policy for enterprise customers"},
            context=self.ctx,
        )
        self.assertTrue(res.get("ok"))
        if "i don't know" in res["answer"].lower():
            self.assertIsNone(res.get("video"), "no video should attach to an 'I don't know' answer")
            self.assertNotIn("**Watch:**", res["answer"])

    def test_search_attaches_video_for_mapped_result(self):
        res = kb_search.kb_search({"query": "how to build whatsapp flows"}, context=self.ctx)
        self.assertTrue(res.get("ok"))
        video = res.get("video")
        self.assertIsNotNone(video, "expected a video on the mapped search result")
        self.assertIn("/watch?v=", video["url"])

    def test_unmapped_page_yields_no_broken_link(self):
        res = kb_answer.kb_answer(
            {"query": "zzqq nonexistent gibberish topic xyzzy"},
            context=self.ctx,
        )
        self.assertTrue(res.get("ok"))
        # Either no video, or if one is somehow chosen it must carry a valid embed url.
        video = res.get("video")
        if video is not None:
            self.assertIn("/watch?v=", video["url"])
        else:
            self.assertNotIn("**Watch:**", res["answer"])

    def test_platform_pitch_appends_all_module_videos(self):
        # A whole-platform pitch should surface the full catalog of module
        # walkthroughs (not just one) under a **Videos:** list.
        res = kb_answer.kb_answer({"query": "what can gupshup do"}, context=self.ctx)
        self.assertTrue(res.get("ok"))
        videos = res.get("videos") or []
        self.assertGreater(len(videos), 1, "platform pitch should return multiple videos")
        self.assertIn("**Videos:**", res["answer"])
        # Every returned video must be a valid, distinct watch link present in the text.
        ids = [v["video_id"] for v in videos]
        self.assertEqual(len(ids), len(set(ids)), "videos must be de-duplicated")
        for v in videos:
            self.assertIn("/watch?v=", v["url"])
            self.assertIn(v["url"], res["answer"])

    def test_specific_question_returns_single_video(self):
        # A specific, single-module question must NOT fan out to the full catalog.
        res = kb_answer.kb_answer({"query": "how do agent assist reports work"}, context=self.ctx)
        self.assertTrue(res.get("ok"))
        videos = res.get("videos") or []
        self.assertEqual(len(videos), 1, "specific question should return exactly one video")
        self.assertIn("**Watch:**", res["answer"])
        self.assertNotIn("**Videos:**", res["answer"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
