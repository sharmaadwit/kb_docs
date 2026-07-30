#!/usr/bin/env python3
"""
Test _translate_key_terms() against the 19 non-English queries from the
30-day Langfuse trace report, then run the full kb_answer pipeline to check
whether each query now returns an answer vs IDK.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

# ── Translation-only pass ────────────────────────────────────────────────────

def show_translations():
    from kb_answer import _translate_key_terms
    queries = [
        'Vou me reunir com uma marca automotiva. Que tipo de demonstração posso apresentar a eles?',
        'Sou uma loja de varejo; o que a Gupshup pode fazer por mim? Me dê a URL do vídeo.',
        'Muéstrame las áreas documentadas de Gupshup Console más relevantes para una demo de contact center de WhatsApp con agentes, colas, reglas de asignación, business hours, respuestas automáticas, analytics, IA para clasificación y resumen, plantillas, campañas e integraciones.',
        'No Gupshup Console, como consultar ou exportar analytics de WhatsApp por projeto com métricas de requested, sent, delivered, read, failed, clicks, templates, campanhas, origin type e principais erros?',
        'Qual a diferença entre WhatsApp username e display name no perfil da marca?',
        'No WhatsApp, qual é a diferença entre o Username e o Display Name das marcas?',
        'Quais são os principais clientes do segmento CPG da Gupshup e quais regiões de atuação? Sei que em Latam temos Diageo',
        'Por qué los templates se archivan en Gupshup Console y cómo ocurre esto? (WhatsApp templates: estado archived)',
        'No Agent Assist, onde verifico se os agentes da fila default vão receber assignment mesmo se estiverem offline ou busy? Existe algum registro na UI para confirmar isso?',
        'Como acessar no Gupshup Console os analytics de WhatsApp e campanhas para ver métricas como sent, delivered, read, failed, clicks, breakdown por origem, top templates e campanhas?',
        'Dá pra responder pelo Instagram?',
        'ما هي منصة CC Express من Gupshup؟',
        'No Bot Studio, quando um evento externo chega via Custom Integration para retomar uma jornada assíncrona, qual campo é usado para fazer o match com o usuário/sessão? É o número de telefone, o user_channel_id, ou outro identificador? E esse campo muda se o usuário não tiver telefone (BSUID-only)?',
        "No Agent Assist, por que o status de um agente fica 'away' e não consigo mudar para 'available'/'disponível'? Quais são as causas mais comuns e o que verificar?",
        'No Console, como habilitar a aba de configurações/canal Proxy para um projeto específico no menu Canais > Proxy? Existe um passo documentado para ativar a aba ou isso depende de habilitação interna/suporte?',
        'Explique o passo a passo documentado para receber evento externo no Console via Integrations Custom Integrations e depois usar esse evento em Journey Builder. Quero um fluxo prático: criar evento, configurar identificador único do evento, callback URL/token, e consumir esse evento na jornada.',
        'Como integrar Agent Assist com Journey Builder após encerramento de atendimento? Quero saber a abordagem documentada com webhook, API, eventos e quais campos carregar no payload.',
        'No Agent Assist da Gupshup, existe forma documentada de emitir evento ou webhook quando um chat é resolvido ou encerrado? O que a documentação indica sobre isso?',
        'No Journey Builder / Console, como configurar um teste A/B no menu principal da jornada para que 50% dos usuários vejam uma opção adicional no menu e os outros 50% não vejam essa opção? Quero os passos práticos de configuração e quais nós usar.',
    ]

    print("=" * 80)
    print("TRANSLATION LAYER — INPUT vs OUTPUT")
    print("=" * 80)
    changed = 0
    for i, q in enumerate(queries, 1):
        translated = _translate_key_terms(q)
        was_changed = translated.lower() != q.lower()
        marker = "✓" if was_changed else "·"
        print(f"\n[{i:02d}] {marker}")
        print(f"  IN : {q[:120]}")
        if was_changed:
            print(f"  OUT: {translated[:120]}")
            changed += 1
    print(f"\n{'=' * 80}")
    print(f"Translation changed {changed}/{len(queries)} queries")
    return queries


# ── Full kb_answer pipeline ──────────────────────────────────────────────────

def setup_local_kb():
    """Wire local file readers so kb_storage/kb_answer work offline."""
    import kb_storage
    import kb_answer as kba
    import kb_search as kbs

    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"

    def _load_chunks_local(context=None):
        items = []
        with chunks_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items

    def _read_json_local(path, context=None):
        p = ROOT / path if not str(path).startswith("/") else Path(path)
        return json.loads(p.read_text(encoding="utf-8"))

    class FakeCtx:
        def get_secret(self, name):
            return None

    ctx = FakeCtx()
    kb_storage._load_chunks = _load_chunks_local
    kb_storage._read_json   = _read_json_local
    kba._load_chunks = _load_chunks_local
    kba._read_json   = _read_json_local
    try:
        kbs._load_chunks = _load_chunks_local
        kbs._read_json   = _read_json_local
    except AttributeError:
        pass
    return ctx


def run_kb_answer(query: str, ctx) -> dict:
    import kb_answer as kba
    try:
        return kba.kb_answer({"query": query}, context=ctx)
    except Exception as e:
        return {"error": str(e)}


def is_idk(result: dict) -> bool:
    answer = result.get("answer") or result.get("response") or ""
    if not answer:
        return True
    idk_phrases = [
        "i don't have", "i do not have", "don't have information",
        "not covered", "no information", "cannot find", "can't find",
        "outside the scope", "not available", "not documented",
        "no documentation", "unable to find", "beyond the scope",
    ]
    lower = answer.lower()
    return any(p in lower for p in idk_phrases)


def main():
    queries = show_translations()

    print("\n\nRunning full kb_answer pipeline...")
    print("(This requires local KB chunks — may take ~30-60s)\n")

    try:
        ctx = setup_local_kb()
    except Exception as e:
        print(f"Could not set up local KB: {e}")
        print("Skipping full pipeline test — translation layer verified above.")
        return

    print("=" * 80)
    print("FULL PIPELINE RESULTS")
    print("=" * 80)

    answered = 0
    idk_count = 0
    errors = 0
    rows = []

    for i, q in enumerate(queries, 1):
        result = run_kb_answer(q, ctx)
        if "error" in result:
            status = "ERROR"
            errors += 1
            detail = result["error"][:80]
        elif is_idk(result):
            status = "IDK"
            idk_count += 1
            detail = (result.get("answer") or "")[:80]
        else:
            status = "ANSWERED"
            answered += 1
            detail = (result.get("answer") or "")[:80]

        rows.append((i, status, q[:70], detail))
        icon = "✓" if status == "ANSWERED" else ("✗" if status == "IDK" else "!")
        print(f"[{i:02d}] {icon} {status:8s}  {q[:65]!r}")
        if status != "ANSWERED":
            print(f"           → {detail}")

    print(f"\n{'=' * 80}")
    print(f"ANSWERED: {answered}/{len(queries)}   IDK: {idk_count}   ERRORS: {errors}")

    # Save report
    out = ROOT / "local" / "reports" / "multilingual_test_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump([{"id": r[0], "status": r[1], "query": r[2], "detail": r[3]} for r in rows],
                  f, ensure_ascii=False, indent=2)
    print(f"Results saved to {out}")


if __name__ == "__main__":
    main()
