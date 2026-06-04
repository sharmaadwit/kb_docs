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

industries = [
  "retail/FMCG", "healthcare", "banking and finance", "edtech", "logistics",
  "ecommerce", "insurance", "real estate", "travel and hospitality",
  "automotive", "telecom", "manufacturing", "D2C",
]
tmpl = "i am a {ind} company, what can superagent do and what are gupshup features that have helped other clients, show me a demo with videos"
fails = 0
for ind in industries:
    q = tmpl.format(ind=ind)
    res = kb_answer.kb_answer({"query": q}, context=ctx)
    v = res.get("video")
    idk = "i don't know" in res.get("answer","").lower()
    ok = (not idk) and v and v.get("video_id") == "bGCS4rp84EM"
    if not ok: fails += 1
    print(f"[{'OK ' if ok else 'BAD'}] {ind:24} idk={idk} video={v['video_id'] if v else None}")
print(f"\n{len(industries)-fails}/{len(industries)} industries OK")
