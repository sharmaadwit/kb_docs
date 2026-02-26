import os, json
from typing import Dict, Any, List

# Import optimized search
from kb_search import kb_search, _searcher

def _format_sources(hits: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    sources = []
    for h in hits:
        sources.append({
            "file": h["file"],
            "heading_path": h.get("heading_path",""),
            "chunk_id": h.get("chunk_id",""),
            "score": str(h.get("score",""))
        })
    return sources

def kb_answer(query: str, top_k: int=5, style: str="customer", max_context_chars: int=12000) -> Dict[str, Any]:
    sr = kb_search(query=query, top_k=top_k)
    if not sr.get("ok"):
        return {"ok": False, "error": sr.get("error", "Search failed")}

    hits = sr["results"]
    if not hits:
        return {
            "ok": True,
            "answer": "I couldn’t find this in the provided documentation yet. If you share the relevant module name (e.g., Journey Builder, AI Admin, WA Campaign Manager) or paste a snippet, I can answer based on that.",
            "sources": []
        }

    # Optimization: Use the cached chunks from the singleton _searcher
    # instead of loading them from disk again.
    if _searcher._chunks is None:
        _searcher._initialize()
    
    chunks = _searcher._chunks

    context_parts = []
    used = 0
    
    # In my optimized search, hits are already sorted but only contain metadata.
    # We use the doc_id implicitly stored in the search result (if we added it)
    # or we can look it up by chunk_id.
    chunk_by_id = {c.get("chunk_id"): c for c in chunks}
    
    for h in hits:
        c = chunk_by_id.get(h.get("chunk_id"))
        if not c:
            continue
        
        block = f"[{c['file']} | {c.get('heading_path','')} | {c.get('chunk_id','')}]\n{c['text']}\n"
        if used + len(block) > max_context_chars:
            break
        context_parts.append(block)
        used += len(block)

    context = "\n---\n".join(context_parts).strip()

    tone_prefix = ""
    if style == "customer":
        tone_prefix = "Here’s what the Gupshup Console docs say:\n\n"
    else:
        tone_prefix = "KB-grounded notes:\n\n"

    answer = tone_prefix + context

    # Add human-friendly citations list
    sources_md = ["\n### Sources"]
    for i, h in enumerate(hits, 1):
        hp = h.get("heading_path","").strip()
        hp_fmt = f" → *{hp}*" if hp else ""
        sources_md.append(f"{i}. `{h['file']}`{hp_fmt} ({h.get('chunk_id','')})")
    answer += "\n" + "\n".join(sources_md)

    return {
        "ok": True,
        "answer": answer,
        "sources": _format_sources(hits),
        "note": "This implementation returns grounded excerpts. If you want fully synthesized natural-language answers, we can add an LLM step while keeping the same citations."
    }

if __name__ == "__main__":
    # Example usage
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "AI Admin"
    print(json.dumps(kb_answer(q), indent=2))
