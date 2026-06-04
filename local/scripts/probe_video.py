import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "skill"))
import kb_storage, kb_answer
CHUNKS_PATH = os.path.join(ROOT, "kb", "kb_chunks.jsonl")

def load(context=None):
    items=[]
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line: items.append(json.loads(line))
    return items

def rj(path, context=None):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)

class C:
    def get_secret(self, n): return None

kb_answer._load_chunks = load
kb_answer._send_langfuse = lambda *a, **k: {}
kb_storage.read_json = rj
import kb_video
kb_video.record_video_delivery = lambda *a, **k: None
ctx=C()

qs = [
  "give me more details about gupshup features",
  "give me more details about gupshup features in full detail",
  "tell me about gupshup",
  "what are gupshup's features",
  "what can the gupshup platform do",
  "what can gupshup do",
  "gupshup features overview",
  "overview of projects",                      # console-specific, NOT a platform pitch
  "how do i create an agent in superagent",    # specific -> single
  "how do agent assist reports work",          # specific -> single
  "what can superagent do",                    # module overview -> superagent only
]
for q in qs:
    res = kb_answer.kb_answer({"query": q}, context=ctx)
    intent = kb_answer._classify_intent(q, kb_answer._extract_entities(q))
    vids = res.get("videos") or []
    idk = "i don't know" in res.get("answer","").lower()
    ids = ", ".join(f'{v["title"]}' for v in vids)
    print(f"intent={intent:9} idk={str(idk):5} n_videos={len(vids)}  [{ids}]")
    print(f"   Q: {q[:80]}")
