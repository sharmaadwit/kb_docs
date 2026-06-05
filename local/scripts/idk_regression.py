#!/usr/bin/env python3
"""IDK regression harness (analytics-only; never edits skill code).

Runs the curated set of production IDK questions through the *current* kb_answer
pipeline using local chunks + manifest, classifies each outcome, and compares to
the expected post-fix target. Run before and after code changes to measure delta.

Usage:
  python3 local/scripts/idk_regression.py
  python3 local/scripts/idk_regression.py --label after   # tag the snapshot

Outputs:
  local/reports/idk_regression_<label>.json
  prints a table + pass-rate summary
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

DECLINE_MARKERS = (
    "don't have documentation",
    "do not have documentation",
    "isn't covered in the documentation",
    "not covered in the documentation",
    "i can help only with documented",
    "ask me about a documented",
    "i can't help with secrets",
)
IDK_MARKERS = ("i don't know", "i don t know", "i don’t know")

# Curated production IDK questions (from dashboard D8 + analysis).
# expected: "answer" (should produce a substantive answer post-fix)
#           "decline" (no docs exist -> must decline gracefully, NOT wrong-page guess)
QUESTIONS = [
    {"id": "ccx_roles", "expected": "decline", "topic": "CC Express",
     "q": "In CC Express, what roles are there?"},
    {"id": "ccx_arabic", "expected": "decline", "topic": "CC Express",
     "q": "\u0645\u0627 \u0647\u064a \u0645\u0646\u0635\u0629 CC Express \u0645\u0646 Gupshup\u061f"},
    {"id": "console_roles", "expected": "answer", "topic": "Console roles",
     "q": "What are the console roles in Gupshup Console?"},
    {"id": "retail_demo", "expected": "answer", "topic": "Pitch/demo",
     "q": "Show me a demo of Gupshup Console features for a retail client, including relevant modules, retail examples, and videos."},
    {"id": "meta_bm_postdeploy", "expected": "defer", "topic": "Post-deploy Meta BM",
     "q": "For a WhatsApp chatbot journey, once I have saved and deployed the new journey and the agents are created, do I need to do anything with the Meta Business Manager ID, or is everything already good?"},
    {"id": "template_then_ai", "expected": "defer", "topic": "Template->AI journey",
     "q": "In Gupshup Console, what is the documented end-to-end process to create a WhatsApp bot journey such that an approved outbound WhatsApp template message is sent first, and when the customer replies with anything, the WhatsApp AI bot/agent that is already created gets triggered?"},
    {"id": "catalog_api", "expected": "defer", "topic": "Catalog message API",
     "q": "Catalog message API"},
    {"id": "flow_id", "expected": "answer", "topic": "Flow ID",
     "q": "In Gupshup Console / Journey Builder / Bot Studio, what is a Flow ID in the console? Explain in simple terms using only documented product guidance if available."},
    {"id": "journey_complete_email", "expected": "defer", "topic": "Journey complete event",
     "q": "In Gupshup Journey Builder / WhatsApp journeys, can a custom event be triggered when a journey is completed, and can that be used to send an email notification to the journey owner?"},
    {"id": "gupshup_sla", "expected": "defer", "topic": "SLA",
     "q": "Gupshup SLA"},
    {"id": "import_contacts", "expected": "defer", "topic": "Import contacts",
     "q": "How can I import contacts in Gupshup?"},
    {"id": "customer_360", "expected": "answer", "topic": "Customer 360",
     "q": "What is Customer 360 as a Gupshup product? Explain what it does, its purpose, main capabilities, and who uses it."},
    {"id": "inapp_support_nodes", "expected": "answer", "topic": "API/JSON/Agent nodes",
     "q": "For an in-app customer support experience using Gupshup, what does the documentation say about API Node, backend API calls, JSON Handler, Trigger Event Node, and Agent Transfer Node? Summarize the documented capabilities only."},
    {"id": "webhooks_fields", "expected": "answer", "topic": "Webhooks fields",
     "q": "What does the documentation say about Webhooks, webhook fields to store, delivery/read events, and retained customer chat history? Summarize the documented behavior only."},
    {"id": "webhook_server_setup", "expected": "answer", "topic": "Webhook server setup",
     "q": "How can we connect the server and what are the required setup steps/configuration for Gupshup Console integration? Include server/webhook setup, endpoint requirements, authentication, and any module-specific notes if documented."},
    {"id": "webhook_v3_modes", "expected": "defer", "topic": "Webhook V3 modes",
     "q": "For Gupshup WhatsApp V3 inbound webhooks, how are webhook modes TEMPLATE, ACCOUNT, BILLING, and PAYMENTS mapped to Meta webhook event references?"},
    {"id": "retained_history", "expected": "answer", "topic": "Retained chat history",
     "q": "What does the documentation say about retained customer chat history for returning web widget users?"},
    {"id": "wa_delivery_logs", "expected": "answer", "topic": "Delivery status/logs",
     "q": "How can users verify WhatsApp message sent/delivered status, view user replies, and track message history or conversation logs in Gupshup WhatsApp Business API / Console?"},
    {"id": "ctx_error_4006", "expected": "defer", "topic": "CTX error 4006",
     "q": "UserNotFoundException errorCode 4006 \"User Not Found By UserId\" while connecting conversation cloud account onboarding. What causes this and how to fix it?"},
    {"id": "mo_callback_gg", "expected": "answer", "topic": "MO callback",
     "q": "How to set a call back for MO for GG accounts"},
    {"id": "external_event_pt", "expected": "answer", "topic": "External event (PT)",
     "q": "Explique o passo a passo documentado para receber evento externo no Console via Integrations Custom Integrations e depois usar esse evento em Journey Builder."},
    {"id": "webhook_sla_latency", "expected": "defer", "topic": "Webhook SLA/latency",
     "q": "What is the SLA/latency for delivering inbound WhatsApp webhooks to a client's endpoint?"},
    {"id": "leadsquared", "expected": "decline", "topic": "LeadSquared",
     "q": "What are the details required for Gupshup WhatsApp integration with LeadSquared?"},
    {"id": "ai_admin_tools", "expected": "answer", "topic": "AI Admin tools",
     "q": "Explain AI Admin tool functionality"},
    {"id": "template_ops_guidelines", "expected": "answer", "topic": "Template guidelines",
     "q": "What are the operational guidelines for sending WhatsApp templates?"},
    {"id": "analytics_overview", "expected": "answer", "topic": "Analytics overview",
     "q": "Give me a concise overview of Analytics in Gupshup with its main capabilities and what teams use it for. Keep it practical."},
]


def _setup_local_kb():
    import kb_storage
    import kb_answer

    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"
    chunks = [json.loads(l) for l in chunks_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def _read_json_local(path, context=None):
        p = ROOT / path if not str(path).startswith("/") else Path(path)
        return json.loads(p.read_text(encoding="utf-8"))

    captured = {}

    def _cap_lf(trace_name, query, answer, results, explicit_module, intents,
                selected_answer_mode, clarification_asked, latency_ms, context,
                params=None, video_meta=None):
        captured["last"] = {
            "top_source": results[0].get("source") if results else None,
            "top_score": results[0].get("score") if results else None,
            "source_count": len(results),
            "mode": selected_answer_mode,
            "intents": intents,
            "module": explicit_module,
            "video_attached": (video_meta or {}).get("video_attached"),
        }
        return {}

    kb_answer._load_chunks = lambda ctx=None: chunks
    kb_answer._send_langfuse = _cap_lf
    kb_storage.read_json = _read_json_local
    try:
        import kb_video
        kb_video.record_video_delivery = lambda *a, **k: None
    except Exception:
        pass

    class Ctx:
        def get_secret(self, name):
            return None

    return kb_answer, Ctx(), captured


def classify(answer: str) -> str:
    low = (answer or "").lower()
    if any(m in low for m in DECLINE_MARKERS):
        return "declined"
    if any(m in low for m in IDK_MARKERS):
        return "idk"
    if low.strip():
        return "answered"
    return "empty"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="baseline")
    args = ap.parse_args()

    kb_answer, ctx, captured = _setup_local_kb()
    rows = []
    outcomes = Counter()
    passes = 0
    video_on_answered = 0

    for item in QUESTIONS:
        try:
            res = kb_answer.kb_answer(parameters={"query": item["q"]}, context=ctx)
            ans = str(res.get("answer") or "")
            video = bool(res.get("video") or res.get("videos"))
        except Exception as exc:
            ans = ""
            video = False
            captured["last"] = {"error": str(exc)}
        outcome = classify(ans)
        meta = captured.get("last", {})
        # pass logic
        if item["expected"] == "decline":
            ok = outcome == "declined"
        elif item["expected"] == "defer":
            # no doc yet: acceptable to decline or IDK, but NOT to answer from a wrong page
            ok = outcome in ("idk", "declined")
        else:
            ok = outcome == "answered"
        if ok:
            passes += 1
        if outcome == "answered" and video:
            video_on_answered += 1
        outcomes[outcome] += 1
        rows.append({
            "id": item["id"],
            "topic": item["topic"],
            "expected": item["expected"],
            "outcome": outcome,
            "pass": ok,
            "video": video,
            "top_score": meta.get("top_score"),
            "top_source": meta.get("top_source"),
            "mode": meta.get("mode"),
            "answer_preview": ans[:140],
        })

    total = len(QUESTIONS)
    summary = {
        "label": args.label,
        "total": total,
        "passes": passes,
        "pass_rate_pct": round(100 * passes / total, 1),
        "outcomes": dict(outcomes),
        "video_on_answered": video_on_answered,
        "expected_answer": sum(1 for q in QUESTIONS if q["expected"] == "answer"),
        "expected_decline": sum(1 for q in QUESTIONS if q["expected"] == "decline"),
        "expected_defer": sum(1 for q in QUESTIONS if q["expected"] == "defer"),
    }

    out = ROOT / "local" / "reports" / f"idk_regression_{args.label}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, default=str), encoding="utf-8")

    print(f"=== IDK regression [{args.label}] ===")
    print(f"pass {passes}/{total} ({summary['pass_rate_pct']}%)  outcomes={summary['outcomes']}  video_on_answered={video_on_answered}")
    print(f"{'id':<22}{'expected':<9}{'outcome':<10}{'pass':<6}{'score':<7}topic")
    for r in rows:
        sc = r["top_score"]
        sc = f"{sc:.2f}" if isinstance(sc, (int, float)) else "-"
        print(f"{r['id']:<22}{r['expected']:<9}{r['outcome']:<10}{str(r['pass']):<6}{sc:<7}{r['topic']}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
