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
  "i am a retail/FMCG company, what can superagent do and what are gupshup features that have helped other clients, show me a demo with videos",
  "what can superagent do for retail and show me a demo with videos",
]
for q in qs:
    explicit_module = kb_answer._detect_module(q)
    entities = kb_answer._extract_entities(q)
    intent = kb_answer._classify_intent(q, entities)
    res = kb_answer.kb_answer({"query": q}, context=ctx)
    v = res.get("video")
    ans = res.get("answer","")
    idk = "i don't know" in ans.lower()
    vid = f'{v["video_id"]} "{v["title"]}" src={v.get("source")}' if v else "(none)"
    print("="*90)
    print(f"Q: {q}")
    print(f"  module={explicit_module} intent={intent} idk={idk}")
    print(f"  video={vid}")
    print(f"  answer[:200]: {ans[:200]!r}")
