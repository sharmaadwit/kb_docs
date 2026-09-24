#!/usr/bin/env python3
"""
Probe SuperAgent with the non-English failing queries from the supervisor report.
Hypothesis: SuperAgent normalises / translates before hitting kb_answer, so
adding foreign-language keywords to CONCEPT_REGISTRY is unnecessary.

Queries sampled from Fix Now gaps #1, #3, #4 in supervisor_20260924_100200.md
"""
import os, json, ssl, uuid, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_env():
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

QUERIES = [
    # Gap #1 — Channels/setup__2 — Portuguese 24h window queries
    ("PT 24h-window",
     "Qual é a regra de janela de 24 horas para mensagens WhatsApp Business API? "
     "Quando posso enviar sem template e quando preciso usar um?"),
    ("PT payment-reminder",
     "O que a documentação diz sobre o uso de templates 'utility' para lembrete "
     "de pagamento/cobrança no WhatsApp Business API?"),
    ("PT debt-collection",
     "É permitido enviar mensagens de cobrança de dívidas a clientes finais pelo "
     "WhatsApp Business?"),
    # Gap #3 — Bot Studio/setup__2 — Hindi/multilingual
    ("HI main-menu",
     "Journey Builder ke andar main menu par wapas jane ke liye kaun sa action "
     "ya node use karte hain? 'Main Menu' navigation kaise karte hain?"),
    # Gap #4 — Agent Assist — Portuguese/Spanish analytics
    ("PT agent-assignment",
     "No Agent Assist ou Analytics existe um relatório nativo de produtividade "
     "ou desempenho dos agentes?"),
    ("ES agent-metrics",
     "Necesito conocer todas las métricas disponibles para monitorear chats, "
     "productividad y desempeño de agentes en Gupshup Console."),
    # Gap #5 — Integrations — Spanish webhooks
    ("ES webhooks",
     "Cómo integrar WhatsApp Cloud con Gupshup para un CRM: flujo general de "
     "configuración del canal y recepción de eventos (webhooks) en Gupshup Console?"),
]

def send_query(query: str, session_id: str) -> dict:
    api_url = os.environ.get("SUPERAGENT_API_URL", "")
    api_key = os.environ.get("SUPERAGENT_API_KEY", "")
    org_id  = os.environ.get("SUPERAGENT_ORG_ID", "")
    project_id = os.environ.get("SUPERAGENT_PROJECT_ID", "")
    user_email = os.environ.get("USER_EMAIL", "test@example.com")

    payload = {
        "message": query,
        "session_id": session_id,
        "user_email_id": user_email,
    }
    if org_id or project_id:
        payload["tenant_context"] = {}
        if org_id:   payload["tenant_context"]["org_id"] = org_id
        if project_id: payload["tenant_context"]["project_id"] = project_id

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(api_url, data=json.dumps(payload).encode(),
                                 headers=headers, method="POST")

    sse_events, answer_text, answered = [], "", False
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            for raw in resp:
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                if not line.startswith("data:"):
                    continue
                data_str = line[5:].strip()
                if data_str in ("[DONE]", ""):
                    continue
                try:
                    evt = json.loads(data_str)
                except json.JSONDecodeError:
                    sse_events.append({"raw": data_str})
                    continue

                sse_events.append(evt)
                # accumulate answer chunks
                chunk = evt.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if chunk:
                    answer_text += chunk
    except Exception as e:
        return {"error": str(e), "answered": False, "answer": "", "sse_events": []}

    answered = bool(answer_text.strip()) and "don't know" not in answer_text.lower() \
               and "i don't" not in answer_text.lower() \
               and "idk" not in answer_text.lower()

    # look for translated_query signal in SSE metadata events
    translated = None
    for evt in sse_events:
        if isinstance(evt, dict):
            tq = evt.get("translated_query") or evt.get("normalized_query") \
                 or (evt.get("metadata") or {}).get("translated_query")
            if tq:
                translated = tq
                break

    return {
        "answered": answered,
        "answer_preview": answer_text[:300].strip(),
        "translated_query": translated,
        "sse_event_types": list({list(e.keys())[0] if isinstance(e, dict) and e else "raw"
                                 for e in sse_events[:20]}),
        "total_sse_events": len(sse_events),
    }


def main():
    load_env()
    api_url = os.environ.get("SUPERAGENT_API_URL", "")
    if not api_url:
        print("❌ SUPERAGENT_API_URL not set in .env")
        return

    print(f"Probing {len(QUERIES)} non-English queries via {api_url}\n")
    print(f"{'Label':<22} {'Answered':<10} {'Translated?':<12} {'Answer preview'}")
    print("-" * 100)

    results = []
    for label, query in QUERIES:
        session_id = str(uuid.uuid4())
        r = send_query(query, session_id)
        answered = "✅ ANS" if r.get("answered") else "❌ IDK"
        translated = r.get("translated_query") or "—"
        preview = (r.get("answer_preview") or r.get("error") or "")[:80].replace("\n", " ")
        print(f"{label:<22} {answered:<10} {translated[:12]:<12} {preview}")
        results.append({"label": label, "query": query[:80], **r})

    # dump full SSE event-type breakdown
    print("\n--- SSE event-type breakdown ---")
    for r in results:
        print(f"  {r['label']}: {r.get('sse_event_types')} ({r.get('total_sse_events')} events)")

    out = ROOT / "local" / "reports" / "probe_non_english.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nFull results → {out}")


if __name__ == "__main__":
    main()
