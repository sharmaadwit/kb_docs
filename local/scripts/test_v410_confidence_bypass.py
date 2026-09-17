"""Replay harness for kb-answer-v4.10 confidence + bypass fix.

Usage:
  python3 local/scripts/test_v410_confidence_bypass.py <mode>
    mode = "current" (working tree)  or  "baseline" (git HEAD copy in /tmp)

Run both, diff the results. This avoids git-stash juggling.
"""
import sys, json, importlib

MODE = sys.argv[1] if len(sys.argv) > 1 else "current"

if MODE == "baseline":
    # load HEAD copy dumped to /tmp/head.py as module
    import types
    sys.path.insert(0, '/tmp')
    sys.path.insert(0, 'skill')
    import kb_search
    spec = importlib.util.spec_from_file_location("kb_answer_head", "/tmp/head.py")
    kb_answer = importlib.util.module_from_spec(spec)
    sys.modules["kb_answer_head"] = kb_answer
    spec.loader.exec_module(kb_answer)
else:
    sys.path.insert(0, 'skill')
    import kb_answer, kb_search

def fake_load_chunks(*a, **k):
    return [json.loads(l) for l in open('kb/kb_chunks.jsonl')]
kb_answer._load_chunks = fake_load_chunks
kb_search._load_chunks = fake_load_chunks
kb_answer.requests.post = lambda *a, **k: type('R', (), {'status_code': 200})()

class FakeContext:
    def get_secret(self, name): return None

def conf_of(r):
    lf = r.get('langfuse') or {}
    return (lf.get('metadata') or {}).get('confidence') if isinstance(lf, dict) else None

def run(q):
    r = kb_answer.kb_answer(parameters={'query': q}, context=FakeContext())
    ans = (r.get('answer') or '')
    idk = "i don't know" in ans.lower()
    return {'q': q, 'idk': idk, 'conf': conf_of(r), 'ans': ans[:60]}

REGRESSION = [
    "How do I set up WhatsApp?", "How do I use the WhatsApp API?",
    "What is WhatsApp API pricing?", "How do I build a bot in Bot Studio?",
    "What is Bot Studio?", "How do I create a campaign?",
    "How do I set up my first campaign in Gupshup?", "How do I set up webhooks?",
    "What is BizAI and what does it do?", "Explain BizAI architecture and components",
    "How do I onboard to BizAI?", "How does BizAI integrate with WhatsApp?",
    "What are the BizAI API endpoints?", "How do I set up SSO for Console?",
    "Does Gupshup Console support Single Sign-On via SAML 2.0?",
    "How do I integrate Azure AD with Console?",
    "What is Meta Business Agent for WhatsApp?", "rcs message template variables",
    "checkInBusinessHour API documentation",
]
IDK_EXPECTED = [
    "what is the refund policy", "asdkfj qweqwe zxcvzxcv nonsense",
    "how do I file my taxes in Germany",
]

out = {'regression': [run(q) for q in REGRESSION],
       'idk': [run(q) for q in IDK_EXPECTED]}
print(json.dumps(out))
