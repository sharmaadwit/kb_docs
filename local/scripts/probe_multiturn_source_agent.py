#!/usr/bin/env python3
"""Multi-turn check of the source_agent instruction on two SuperAgent test agents.

Each conversation reuses one session_id for 4 turns (follow-ups, topic drift, a
non-KB turn). Every kb_answer trace is matched to its turn by timestamp window and
checked for the expected source_agent. Turns that never call the skill are reported
separately (no skill call = no tag possible, not an instruction failure).

Expected: agent1 -> test-agent-a, agent2 -> test-agent-b.
Usage: python3 local/scripts/probe_multiturn_source_agent.py [--convs 3] [--wait 240]
"""
import argparse, datetime, json, os, time, uuid
import requests

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "local", "reports", "multiturn_probe.json")


def _load_env():
    for line in open(os.path.join(ROOT, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()
URL = os.environ["SUPERAGENT_API_URL"]
LF_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
LF_AUTH = (os.environ["LANGFUSE_PUBLIC_KEY"], os.environ["LANGFUSE_SECRET_KEY"])
AGENTS = {
    "agent1": {"key": os.environ["SUPERAGENT_API_KEY_guide_test_smsgupshup"], "expect": "test-agent-a"},
    "agent2": {"key": os.environ["SUPERAGENT_API_KEY_test_smsgupshup"], "expect": "test-agent-b"},
}
CONVERSATIONS = [
    ["What modules does Gupshup Console have?", "Tell me more about Journey Builder.",
     "How do I add a condition node?", "Thanks. And what about the API node?"],
    ["How do I create a template in Gupshup Console?", "Can I A/B test it?",
     "Hello, who are you?", "What channels does Console support?"],
    ["What is Agent Assist?", "How does agent transfer work?",
     "Give me the steps in detail.", "How do goals work in Journey Builder?"],
]


def fire(label, key, session_id, turn, message):
    payload = {"message": message, "session_id": session_id, "user_email_id": "agent-probe@gupshup.io"}
    start, calls, conv_id = time.time(), 0, None
    with requests.post(URL, headers={"Content-Type": "application/json", "X-API-Key": key},
                       json=payload, stream=True, timeout=180) as r:
        status = r.status_code
        for raw in r.iter_lines():
            line = raw.decode("utf-8", "replace") if raw else ""
            if not line.startswith("data:"):
                continue
            d = line[5:].strip()
            if d == "[DONE]":
                break
            try:
                ev = json.loads(d)
            except Exception:
                continue
            if ev.get("type") == "tool_call" and ev.get("tool") == "execute_action":
                calls += 1
            if ev.get("type") == "done":
                conv_id = ev.get("conversation_id")
    end = time.time()
    print(f"{label} {session_id[-6:]} t{turn}: HTTP {status}, skill calls={calls}, conv={conv_id} | {message[:40]}")
    return {"label": label, "expect": AGENTS[label]["expect"], "session": session_id, "turn": turn,
            "start": start, "end": end, "http": status, "skill_calls": calls,
            "conversation_id": conv_id, "message": message}


def ts(t):
    return datetime.datetime.fromisoformat(t["timestamp"].replace("Z", "+00:00")).timestamp()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--convs", type=int, default=3)
    ap.add_argument("--wait", type=int, default=240)
    a = ap.parse_args()

    turns = []
    for ci in range(min(a.convs, len(CONVERSATIONS))):
        for label, cfg in AGENTS.items():
            sid = f"MTPROBE-{label}-{uuid.uuid4().hex[:8]}"
            for ti, msg in enumerate(CONVERSATIONS[ci], 1):
                turns.append(fire(label, cfg["key"], sid, ti, msg))

    expected = sum(t["skill_calls"] for t in turns)
    since = min(t["start"] for t in turns)
    print(f"\nTurns: {len(turns)}; skill calls: {expected}. Polling Langfuse up to {a.wait}s ...")
    frm = datetime.datetime.fromtimestamp(since - 10, datetime.timezone.utc).isoformat()
    deadline, traces = time.time() + a.wait, {}
    while time.time() < deadline:
        try:
            r = requests.get(f"{LF_HOST}/api/public/traces",
                             params={"limit": 100, "name": "kb_answer", "fromTimestamp": frm},
                             auth=LF_AUTH, timeout=30)
            for t in r.json().get("data", []):
                traces[t["id"]] = t
        except Exception as e:
            print("poll error:", e)
        if len(traces) >= expected:
            break
        time.sleep(10)

    for t in turns:
        t["observed"] = []
    for tr in traces.values():
        meta = tr.get("metadata") or {}
        inp = tr.get("input") if isinstance(tr.get("input"), dict) else {}
        sa = meta.get("source_agent") or (inp.get("_meta") or {}).get("source_agent")
        owner = next((t for t in turns if t["start"] <= ts(tr) <= t["end"]), None)
        if owner:
            owner["observed"].append(sa)

    print(f"\n{'agent':7} {'sess':7} turn calls observed")
    hit = miss = no_call = 0
    for t in turns:
        if t["skill_calls"] == 0:
            no_call += 1
            tag = "NO SKILL CALL"
        else:
            ok = len(t["observed"]) > 0 and all(o == t["expect"] for o in t["observed"])
            hit += ok
            miss += (not ok)
            tag = "OK" if ok else "MISS"
        print(f"{t['label']:7} {t['session'][-6:]:7} {t['turn']:4} {t['skill_calls']:5} {str(t['observed']):40} {tag}")

    by_turn = {}
    for t in turns:
        if t["skill_calls"]:
            b = by_turn.setdefault(t["turn"], [0, 0])
            b[1] += 1
            b[0] += len(t["observed"]) > 0 and all(o == t["expect"] for o in t["observed"])
    print(f"\nTurns with skill call: {hit + miss} | tagged correctly: {hit} | missed/wrong: {miss} | no skill call: {no_call}")
    print("Hit rate by turn number:", {k: f"{v[0]}/{v[1]}" for k, v in sorted(by_turn.items())})
    conv_ids = {}
    for t in turns:
        conv_ids.setdefault(t["session"], set()).add(t["conversation_id"])
    print("conversation_id stable across turns:", {k[-6:]: len(v) == 1 for k, v in conv_ids.items()})

    json.dump({"turns": turns, "traces": list(traces.values())}, open(OUT, "w"), indent=2, default=str)
    print("Saved:", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
