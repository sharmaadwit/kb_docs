#!/usr/bin/env python3
"""
KB docs rewrite: Golden Rule for non-Agent Assist pages.

Golden rule
- A. Definition block (good for understanding)
- B. Procedure block (required for answer quality)

Scope
- Rewrites kb/**/*.md excluding kb/agent-assist/*
- Keeps `source_url:` style metadata lines at the top.
- Preserves original content under "Reference (from source)".

Idempotency
- Rewritten files include `<!-- kb-golden:v1 -->`
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "kb"

MARKER = "<!-- kb-golden:v1 -->"

META_LINE_RE = re.compile(r"^[a-zA-Z0-9_]+:\s+\S+.*$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")


def split_meta(text: str) -> Tuple[str, str]:
    lines = text.splitlines(keepends=True)
    meta: List[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            if meta:
                meta.append(ln)
                i += 1
                continue
            break
        if META_LINE_RE.match(ln) and not ln.lstrip().startswith("#"):
            meta.append(ln)
            i += 1
            continue
        break
    return "".join(meta).rstrip() + ("\n\n" if meta else ""), "".join(lines[i:]).lstrip()


def extract_title(body: str, fallback: str) -> str:
    for ln in body.splitlines():
        m = H1_RE.match(ln)
        if m:
            return m.group(1).strip()
    return fallback


def extract_module(body: str, rel_path: Path) -> str | None:
    m = re.search(r"^\*\*Module\*\*:\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # fallback to top-level folder as module
    parts = rel_path.parts
    if parts:
        return parts[0].replace("-", " ").title()
    return None


def section(body: str, name: str) -> str | None:
    # Works for prior procedural:v2 sections
    pat = re.compile(rf"^##\s+{re.escape(name)}\s*$", re.MULTILINE)
    m = pat.search(body)
    if not m:
        return None
    start = m.end()
    m2 = re.search(r"^##\s+\S.*$", body[start:], flags=re.MULTILINE)
    end = start + (m2.start() if m2 else len(body) - start)
    txt = body[start:end].strip()
    return txt if txt else None


def first_useful_paragraph(text: str) -> str | None:
    # prefer non-heading, non-placeholder paragraph
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paras:
        if p.startswith("#"):
            continue
        if p.startswith("_") and "add" in p.lower():
            continue
        if re.match(r"^Updated\s+.+$", p, flags=re.IGNORECASE):
            continue
        if len(p) < 25 and p.lower() in {"introduction", "overview", "definition", "uses"}:
            continue
        return p
    return paras[0] if paras else None


def guess_where_to_configure(rel_path: Path, title: str, module: str | None) -> str:
    """
    Best-effort UI location. We only know the KB folder structure, not exact console IA.
    """
    top = rel_path.parts[0] if rel_path.parts else ""
    top_norm = top.lower()
    if top_norm == "bot-studio":
        return f"Gupshup Console → Bot Studio → {title}"
    if top_norm == "campaign-manager":
        return f"Gupshup Console → Campaign Manager → {title}"
    if top_norm == "integrations":
        return f"Gupshup Console → Integrations → {title}"
    if top_norm == "channels":
        return f"Gupshup Console → Channels → {title}"
    if top_norm == "ctx":
        return f"Gupshup Console → CTX → {title}"
    if top_norm == "overview":
        return f"Gupshup Console → Overview → {title}"
    if top_norm == "goals":
        return f"Gupshup Console → Goals → {title}"
    if top_norm == "personalize":
        return f"Gupshup Console → Personalize → {title}"
    if top_norm == "wallet":
        return f"Gupshup Console → Wallet → {title}"
    if top_norm == "extension":
        return f"Gupshup Console → Extensions → {title}"
    if module:
        return f"Gupshup Console → {module} → {title}"
    return f"Gupshup Console → {title}"


def extract_setup_path(body: str) -> List[str]:
    setup = section(body, "Setup path")
    if not setup:
        return []
    steps: List[str] = []
    seen = set()
    for ln in setup.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("_") and "navigation path" in s.lower():
            continue
        if "add the navigation path" in s.lower():
            continue
        if s.startswith("- "):
            s = s[2:].strip()
        k = s.lower()
        if k in seen:
            continue
        seen.add(k)
        steps.append(s)
    return steps[:12]


def synthesize_steps(where: str, setup_path: List[str], body: str) -> List[str]:
    # If we have explicit bullet steps, reuse them
    if setup_path:
        out = ["Open Gupshup Console."]
        out.extend(setup_path)
        if not any(re.search(r"\bsave\b|\bdeploy\b|\bpublish\b", s, re.IGNORECASE) for s in out):
            # add save step only if doc mentions it
            if re.search(r"\b(save|deploy|publish)\b", body, flags=re.IGNORECASE):
                out.append("Click **Save** (or **Save & Deploy**) to apply changes.")
        return out[:14]

    # Otherwise synthesize generic
    out = [
        "Open Gupshup Console.",
        f"Navigate to **{where}**.",
        "Configure the required fields.",
    ]
    if re.search(r"\b(save|deploy|publish)\b", body, flags=re.IGNORECASE):
        out.append("Click **Save** (or **Save & Deploy**) to apply changes.")
    return out


def rewrite_one(path: Path) -> bool:
    rel = path.relative_to(KB_DIR)
    if rel.parts and rel.parts[0] == "agent-assist":
        return False

    raw = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in raw:
        return False

    meta, body = split_meta(raw)
    # If previously rewritten by procedural script, keep it as reference; we’ll build golden blocks on top
    title = extract_title(body, fallback=path.stem.replace("-", " ").title())
    module = extract_module(body, rel)

    overview = section(body, "Overview") or section(body, "Step-by-step configuration") or body
    definition = first_useful_paragraph(overview or "") or "Short description in 2–3 lines."

    where = guess_where_to_configure(rel, title, module)
    setup_path = extract_setup_path(body)
    steps = synthesize_steps(where, setup_path, body)

    # Options: reuse any "Business hours vs after-hours" section or pull obvious headings
    opts: List[str] = []
    bha = section(body, "Business hours vs after-hours behavior")
    if bha and "_Not applicable" not in bha:
        opts.append("Business hours vs after-hours behavior")
    for ln in body.splitlines():
        m = re.match(r"^(?:###|####)\s+(.+?)\s*$", ln.strip())
        if m:
            t = m.group(1).strip()
            if t and len(t) <= 80:
                opts.append(t)
    # de-dup
    seen = set()
    options = []
    for o in opts:
        k = o.lower()
        if k in seen:
            continue
        seen.add(k)
        options.append(o)
    options = options[:10]

    out: List[str] = []
    out.append(meta)
    out.append(MARKER + "\n")
    out.append(f"# {title}\n\n")
    if module:
        out.append(f"**Module**: {module}\n\n")

    out.append("## Definition\n")
    out.append(definition.strip() + "\n\n")

    out.append("## Procedure\n")
    out.append("### Where to configure it\n")
    out.append(where + "\n\n")

    out.append("### Setup path\n")
    if setup_path:
        for s in setup_path:
            out.append(f"- {s}\n")
        out.append("\n")
    else:
        out.append("- _Add the click-by-click navigation path for this page._\n\n")

    out.append("### Steps\n")
    for i, s in enumerate(steps, start=1):
        out.append(f"{i}. {s}\n")
    out.append("\n")

    out.append("### Save/publish behavior\n")
    if re.search(r"\b(save|deploy|publish)\b", body, flags=re.IGNORECASE):
        out.append("- Click **Save** (or **Save & Deploy**) to apply changes.\n\n")
    else:
        out.append("- _If this page has a Save/Publish action, document it here._\n\n")

    out.append("## Available options\n")
    if options:
        for o in options:
            out.append(f"- {o}\n")
        out.append("\n")
    else:
        out.append("- _List the key variants/toggles visible in the UI._\n\n")

    out.append("## Notes\n")
    out.append("- _Add prerequisites, constraints, and rollout behavior._\n\n")

    out.append("## Reference (from source)\n")
    out.append(body.strip() + "\n")

    path.write_text("".join(out).rstrip() + "\n", encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for p in sorted(KB_DIR.rglob("*.md")):
        if rewrite_one(p):
            changed += 1
    print(f"rewritten_files={changed}")


if __name__ == "__main__":
    main()

