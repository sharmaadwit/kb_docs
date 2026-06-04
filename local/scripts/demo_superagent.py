#!/usr/bin/env python3
"""Demo: run a few SuperAgent questions through kb_answer/kb_search locally.

Stubs only the network boundary (chunk load, manifest/transcript reads, langfuse)
so we exercise the real scoring + video selection path.
"""
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "skill"))

import kb_storage  # noqa: E402
import kb_answer  # noqa: E402
import kb_search  # noqa: E402

CHUNKS_PATH = os.path.join(ROOT, "kb", "kb_chunks.jsonl")


def _load_chunks_local(context=None):
    items = []
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def _read_json_local(path, context=None):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


class FakeContext:
    def get_secret(self, name):
        return None


kb_answer._load_chunks = _load_chunks_local
kb_search._load_chunks = _load_chunks_local
kb_answer._send_langfuse = lambda *a, **k: {}
kb_search._compact_langfuse = lambda *a, **k: {}
kb_storage.read_json = _read_json_local
kb_answer.record_video_delivery = lambda *a, **k: None
try:
    import kb_video
    kb_video.record_video_delivery = lambda *a, **k: None
except Exception:
    pass

ctx = FakeContext()

QUESTIONS = [
    "what is superagent",
    "how do i create an agent in superagent",
    "how do i connect gmail to my superagent agent",
    "can i embed a superagent agent on my website",
    "how do i schedule a task in superagent",
    "what skills can superagent use",
    "how do i use superagent on whatsapp",
    "let an agent browse the web",
]


def short(s, n=160):
    s = (s or "").replace("\n", " ")
    return s[:n] + ("..." if len(s) > n else "")


print("=" * 90)
print("kb_answer")
print("=" * 90)
for q in QUESTIONS:
    res = kb_answer.kb_answer({"query": q}, context=ctx)
    v = res.get("video")
    idk = "i don't know" in (res.get("answer", "").lower())
    vid = f'{v["video_id"]} @ {v["start"]}s -> {v.get("source","?")}' if v else "(none)"
    print(f"\nQ: {q}")
    print(f"  idk={idk}  video={vid}")
    print(f"  ans: {short(res.get('answer'))}")

print("\n" + "=" * 90)
print("kb_search")
print("=" * 90)
for q in QUESTIONS:
    res = kb_search.kb_search({"query": q}, context=ctx)
    v = res.get("video")
    top = (res.get("results") or [{}])[0].get("source") if res.get("results") else "?"
    vid = f'{v["video_id"]} -> {v.get("source","?")}' if v else "(none)"
    print(f"\nQ: {q}")
    print(f"  top={top}")
    print(f"  video={vid}")
