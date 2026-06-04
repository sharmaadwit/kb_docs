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
  "i am a retail/FMCG company, what can superagent do and what are gupshup features that have helped other clients, if you have videos, would love to see",
  "what can superagent do for retail",
  "what can superagent do",
  "superagent features",
  "show me videos for superagent",
]
for q in qs:
    res = kb_answer.kb_answer({"query": q}, context=ctx)
    v = res.get("video")
    idk = "i don't know" in (res.get("answer","" ).lower())
    vid = f'{v["video_id"]} "{v["title"]}" fallback={v.get("fallback")} src={v.get("source")}' if v else "(none)"
    print(f"idk={idk}  video={vid}\n  Q: {q[:90]}")
