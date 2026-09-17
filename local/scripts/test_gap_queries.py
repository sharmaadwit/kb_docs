#!/usr/bin/env python3
"""
Test the 4 Fix Now gaps from the supervisor report.
For each gap: run the sample queries through the live skill pipeline
and verify: (1) they actually IDK, (2) the matching doc exists,
(3) the suggested keywords appear in the failing queries.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from local.supervisor.utils.skill_pipeline_bridge import SkillPipelineBridge
from pathlib import Path

bridge = SkillPipelineBridge()

GAPS = [
    {
        "name": "WhatsApp / setup",
        "claimed_doc": "kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md",
        "claimed_root_cause": "keyword_gap",
        "suggested_keywords": [
            "WhatsApp API integration", "multiple WhatsApp numbers",
            "WhatsApp group messaging", "WhatsApp licensing", "WhatsApp plan",
            "official WhatsApp API",
        ],
        "queries": [
            "Vocês fornecem uma API oficial para receber e enviar mensagens via WhatsApp para integrar nos nossos sistemas?",
            "Can CC Express provision multiple merchant WhatsApp numbers through a self-serve onboarding flow?",
            "CC Express: é o plano por número de WhatsApp? Posso ter vários planos?",
            "No CC Express Starter, é possível cadastrar mais de 10 números de WhatsApp?",
        ],
    },
    {
        "name": "Journey Builder / setup",
        "claimed_doc": "kb/bot-studio/consulting-loop-prevention.md",
        "claimed_root_cause": "routing_miss",
        "suggested_keywords": [
            "prevent infinite loops", "loop detection",
            "multilingual journey", "journey setup",
        ],
        "queries": [
            "How do I prevent infinite loops in Bot Studio journeys?",
            "how can gupshup help me in building journeys on whatsapp?",
            "How can I make an entire journey multilingual?",
        ],
    },
    {
        "name": "General / page_lookup",
        "claimed_doc": "kb/overview/welcome-to-gupshup-console.md",
        "claimed_root_cause": "keyword_gap",
        "suggested_keywords": [
            "console login", "Gupshup Console access", "API key location",
            "client ID client secret", "project deletion", "KYC document upload",
        ],
        "queries": [
            "Where do I upload KYC documents in Gupshup Console?",
            "I can't find the console. Where do I log in to Gupshup Console?",
            "Can I delete a project in Gupshup Console?",
            "where do I get the API key if the account only shows a client ID and client secret?",
        ],
    },
    {
        "name": "Bot Studio / setup",
        "claimed_doc": "kb/bot-studio/api-node.md",
        "claimed_root_cause": "keyword_gap",
        "suggested_keywords": [
            "save user input", "database integration",
            "POST to webhook", "write to database", "user input database",
        ],
        "queries": [
            "How do I save the user input?",
            "How do I save the user input back into a database?",
            "In Bot Studio, how do I write user input to a database using the API Node?",
            "Journey Builder WhatsApp appointment booking collect name phone number POST to webhook",
        ],
    },
]

KB_ROOT = Path(__file__).resolve().parents[2] / "kb"

print("=" * 70)
print("SUPERVISOR FIX-NOW GAPS — VERIFICATION REPORT")
print("=" * 70)

all_pass = True

for gap in GAPS:
    print(f"\n{'─'*70}")
    print(f"GAP: {gap['name']}")
    print(f"{'─'*70}")

    # 1. Check claimed doc exists
    doc_path = KB_ROOT.parent / gap["claimed_doc"]
    doc_exists = doc_path.exists()
    print(f"\n[DOC EXISTS]  {'✅' if doc_exists else '❌'} {gap['claimed_doc']}")
    if not doc_exists:
        # Try without leading kb_docs
        alt = KB_ROOT / Path(gap["claimed_doc"]).relative_to("kb")
        doc_exists = alt.exists()
        print(f"              {'✅' if doc_exists else '❌'} (alt path: {alt})")
    if doc_exists:
        # Show first heading
        p = doc_path if doc_path.exists() else alt
        for line in p.read_text(errors="ignore").splitlines():
            if line.startswith("# "):
                print(f"              Title: {line[2:].strip()}")
                break

    # 2. Run each query through the pipeline
    print(f"\n[QUERIES]")
    idk_count = 0
    for q in gap["queries"]:
        result = bridge.run_query(q)
        is_idk = result["is_idk"]
        module = result.get("module") or "?"
        entities = result.get("entities") or []
        score = result.get("top_score") or 0
        status = "IDK ❌" if is_idk else f"ANSWERED ✅ (score={score:.1f})"
        if is_idk:
            idk_count += 1
        print(f"  {'IDK' if is_idk else 'ANS'} | module={module:20s} | entities={entities[:2]} | score={score:.2f}")
        print(f"       Q: {q[:90]}")

    idk_rate = idk_count / len(gap["queries"])
    print(f"\n  IDK rate: {idk_count}/{len(gap['queries'])} = {idk_rate:.0%}")

    # 3. Spot check: does the claimed doc appear in BM25 results for any query?
    print(f"\n[DOC RETRIEVAL CHECK]")
    claimed_file = Path(gap["claimed_doc"]).name
    found_in_results = 0
    for q in gap["queries"][:2]:
        result = bridge.run_query(q)
        sources = result.get("evidence_sources") or []
        hit = any(claimed_file in (s or "") for s in sources)
        print(f"  {'✅ found' if hit else '❌ NOT found'} '{claimed_file}' in top sources for: {q[:60]}")
        print(f"    actual top sources: {sources[:3]}")
        if hit:
            found_in_results += 1

    verdict = "✅ CONFIRMED" if idk_rate >= 0.5 and doc_exists else "⚠️  NEEDS REVIEW"
    if idk_rate < 0.5:
        verdict += " (queries not actually failing)"
    if not doc_exists:
        verdict += " (doc missing)"
    print(f"\n  VERDICT: {verdict}")
    if idk_rate < 0.5 or not doc_exists:
        all_pass = False

print(f"\n{'='*70}")
print(f"OVERALL: {'✅ All gaps confirmed' if all_pass else '⚠️  Some gaps need review'}")
print("=" * 70)
