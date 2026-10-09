#!/usr/bin/env python3
"""Fire several queries to each of two SuperAgent microagents (SUPERAGENT_API_KEY_guide_test_smsgupshup
and SUPERAGENT_API_KEY_test_smsgupshup), sequentially, then match each kb_answer Langfuse trace to the
call that produced it (by timestamp window) and report the observed source_agent.

Expected: agent1 -> test-agent-a, agent2 -> test-agent-b.

Usage: python3 local/scripts/probe_two_agents_identity.py [--n 3] [--wait 240]
"""
import argparse, datetime, json, os, time, uuid
import requests

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "local", "reports", "two_agent_probe.json")


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
QUESTIONS = [
    "What modules does Gupshup Console have? List the main modules.",
    "How do I configure a condition node in Journey Builder?",
    "What is the JSON handler node used for in Bot Studio?",
    "How does agent transfer work in Agent Assist?",
    "What can I do in Campaign Manager?",
    "How do I set up a trigger event node in a journey?",
    "What channels does Gupshup Console support?",
    "How do I manage variables in Bot Studio?",
    "What is AI Admin and what does it do?",
    "How do goals work in Journey Builder?",
    "Can I call an external API from a bot flow?",
    "How do I create a template in Gupshup Console?",
]


def fire(label, key, question):
    sid = f"AGENTPROBE-{label}-{uuid.uuid4().hex[:6]}"
    payload = {"message": question, "session_id": sid, "user_email_id": "agent-probe@gupshup.io"}
    start, calls, status = time.time(), 0, None
    with requests.post(URL, headers={"Content-Type": "application/json", "X-API-Key": key},
                       json=payload, stream=True, timeout=180) as r:
        status = r.status_code
        for raw in r.iter_lines():
            line = raw.decode("utf-8", "replace") if raw else ""
            if line.startswith("data:"):
                d = line[5:].strip()
                if d == "[DONE]":
                    break
                try:
                    ev = json.loads(d)
                except Exception:
                    continue
                if ev.get("type") == "tool_call" and ev.get("tool") == "execute_action":
                    calls += 1
    end = time.time()
    print(f"{label}: HTTP {status}, skill calls={calls}, {end - start:.0f}s | {question[:50]}")
    return {"label": label, "expect": AGENTS[label]["expect"], "start": start, "end": end,
            "http": status, "skill_calls": calls, "question": question}


def fetch_traces(since):
    frm = datetime.datetime.fromtimestamp(since - 10, datetime.timezone.utc).isoformat()
    r = requests.get(f"{LF_HOST}/api/public/traces",
                     params={"limit": 100, "name": "kb_answer", "fromTimestamp": frm},
                     auth=LF_AUTH, timeout=30)
    return r.json().get("data", [])


def ts(t):
    return datetime.datetime.fromisoformat(t["timestamp"].replace("Z", "+00:00")).timestamp()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--wait", type=int, default=240)
    a = ap.parse_args()

    calls = []
    for i in range(a.n):
        for label, cfg in AGENTS.items():
            calls.append(fire(label, cfg["key"], QUESTIONS[i % len(QUESTIONS)]))

    expected = sum(c["skill_calls"] for c in calls)
    since = min(c["start"] for c in calls)
    print(f"\nExpecting ~{expected} traces. Polling Langfuse up to {a.wait}s ...")
    deadline, traces = time.time() + a.wait, {}
    while time.time() < deadline:
        try:
            for t in fetch_traces(since):
                traces[t["id"]] = t
        except Exception as e:
            print("poll error:", e)
        if len(traces) >= expected:
            break
        time.sleep(10)

    rows = []
    for t in sorted(traces.values(), key=ts):
        meta = (t.get("metadata") or {})
        inp = t.get("input") if isinstance(t.get("input"), dict) else {}
        sa = meta.get("source_agent") or (inp.get("_meta") or {}).get("source_agent")
        owner = next((c for c in calls if c["start"] <= ts(t) <= c["end"]), None)
        rows.append({"trace": t["id"][:12], "ts": t["timestamp"], "observed": sa,
                     "expected": owner["expect"] if owner else None,
                     "agent": owner["label"] if owner else None})

    print(f"\n{'agent':7} {'expected':14} {'observed':14} trace")
    ok = 0
    for r in rows:
        match = r["observed"] == r["expected"]
        ok += match
        print(f"{str(r['agent']):7} {str(r['expected']):14} {str(r['observed']):14} {r['trace']} {'OK' if match else 'MISMATCH'}")
    print(f"\n{ok}/{len(rows)} traces matched; skill calls fired: {expected}; traces found: {len(rows)}")

    json.dump({"calls": calls, "rows": rows, "traces": list(traces.values())},
              open(OUT, "w"), indent=2, default=str)
    print("Saved:", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
