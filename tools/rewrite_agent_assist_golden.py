#!/usr/bin/env python3
"""
Agent Assist docs rewrite: Golden Rule format.

Golden rule
- A. Definition block: good for understanding
- B. Procedure block: required for answer quality

This script rewrites `kb/agent-assist/*.md` (except the Auto Replies page which is
hand-authored) into a predictable, operator-first template while preserving
source content in a trailing "Reference" section.

Idempotency
- Rewritten files include `<!-- agent-assist-golden:v8 -->`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
AA_DIR = ROOT / "kb" / "agent-assist"

OLD_MARKERS = {
    "<!-- agent-assist-golden:v1 -->",
    "<!-- agent-assist-golden:v2 -->",
    "<!-- agent-assist-golden:v3 -->",
    "<!-- agent-assist-golden:v4 -->",
    "<!-- agent-assist-golden:v5 -->",
    "<!-- agent-assist-golden:v6 -->",
    "<!-- agent-assist-golden:v7 -->",
}
MARKER = "<!-- agent-assist-golden:v8 -->"

def extract_action_bullets(text: str) -> List[str]:
    actions: List[str] = []
    seen = set()
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("- "):
            b = s[2:].strip()
        else:
            b = s
        if b.startswith("_"):
            continue
        if re.match(r"^(select|click|enable|disable|enter|provide|choose|configure|add|go|navigate|open|set|toggle|connect|save|test|verify|confirm|ensure)\b", b, re.IGNORECASE):
            k = b.lower()
            if k in seen:
                continue
            seen.add(k)
            actions.append(b.rstrip(".") + ".")
    return actions[:12]

META_LINE_RE = re.compile(r"^[a-zA-Z0-9_]+:\s+\S+.*$")
H_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")
UPDATED_RE = re.compile(r"^\*\*Last updated .*?\*\*:\s*(Updated.+)$", re.IGNORECASE)


def split_meta(lines: List[str]) -> Tuple[List[str], List[str]]:
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
    return meta, lines[i:]


def get_first_h1(text: str) -> str | None:
    for ln in text.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", ln)
        if m:
            return m.group(1).strip()
    return None


def get_module(text: str) -> str | None:
    m = re.search(r"^\*\*Module\*\*:\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def section(text: str, heading: str) -> str | None:
    """
    Extract a procedural:v2 section body by heading name (e.g., 'Overview').
    Returns text up to the next H2.
    """
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    # find next H2
    m2 = re.search(r"^##\s+\S.*$", text[start:], flags=re.MULTILINE)
    end = start + (m2.start() if m2 else len(text) - start)
    body = text[start:end].strip("\n")
    return body.strip() if body.strip() else None


def guess_where_to_configure(filename: str) -> str:
    if filename.startswith("response-management-"):
        return "Agent Assist → Settings → Response Management"
    if filename.startswith("chat-management-"):
        return "Agent Assist → Settings → Chat Management"
    if filename.startswith("user-management-"):
        return "Agent Assist → Settings → User Management"
    if filename.startswith("insights-") or "insights" in filename:
        return "Agent Assist → Insights"
    if filename.startswith("others-"):
        return "Agent Assist → Settings → Others"
    if filename == "settings.md":
        return "Agent Assist → Settings"
    if filename == "chats.md":
        return "Agent Assist → Chats"
    if "downloading-chat-transcripts" in filename:
        return "Agent Assist → Chats"
    if "global-search" in filename:
        return "Agent Assist → Chats → Search"
    return "Agent Assist"


def extract_setup_path(setup_path_section: str | None) -> List[str]:
    if not setup_path_section:
        return []
    lines = []
    seen = set()
    for ln in setup_path_section.splitlines():
        s = ln.strip()
        if not s:
            continue
        # ignore placeholder guidance from the earlier procedural template
        if s.startswith("_") and "navigation path" in s.lower():
            continue
        if "add the navigation path" in s.lower():
            continue
        if s.startswith("- "):
            step = s[2:].strip()
        else:
            # allow raw lines like "Go to X"
            step = s
        if step.lower() in seen:
            continue
        seen.add(step.lower())
        lines.append(step)
    return lines[:12]


def synthesize_steps(where: str, setup_path: List[str], *, needs_save: bool) -> List[str]:
    if setup_path:
        # Convert bullets into numbered steps, with a consistent opener/closer.
        steps = ["Open Agent Assist."]
        steps.extend(setup_path)
        if needs_save and not any(re.search(r"\bsave\b|\bdeploy\b|\bpublish\b", s, re.IGNORECASE) for s in steps):
            steps.append("Click **Save** to apply changes.")
        return steps[:14]

    parts = [p.strip() for p in where.split("→")]
    parts = [p for p in parts if p and p.lower() != "agent assist"]
    steps = ["Open Agent Assist."]
    if parts:
        steps.append(f"Go to **{parts[0]}**.")
        for p in parts[1:]:
            steps.append(f"Click **{p}**.")
    steps.append("Configure the required fields.")
    if needs_save:
        steps.append("Click **Save** to apply changes.")
    return steps


def extract_definition(overview: str | None, when_to_use: str | None) -> str:
    """
    Build a short, non-prosy definition from Overview + (optional) When to use.
    """
    parts: List[str] = []
    def is_low_signal(p: str) -> bool:
        s = p.strip()
        if not s:
            return True
        if re.match(r"^(section\s+\d+[:.)-]|introduction)$", s, flags=re.IGNORECASE):
            return True
        if len(s) < 30 and s.lower() in {"overview", "definition", "uses"}:
            return True
        return False

    if overview:
        # take first 1–2 useful paragraphs max
        paras = [p.strip() for p in re.split(r"\n\s*\n", overview) if p.strip()]
        useful = [p for p in paras if not is_low_signal(p)]
        if useful:
            parts.append(useful[0])
            if len(useful) > 1 and len(useful[0]) < 240:
                parts.append(useful[1])
        else:
            parts.append(paras[0])
    if when_to_use:
        # keep only first few bullets if present
        bullets = []
        for ln in when_to_use.splitlines():
            s = ln.strip()
            if s.startswith("- "):
                bullets.append(s[2:].strip())
        if bullets:
            parts.append("Common uses:")
            parts.extend([f"- {b}" for b in bullets[:3]])
    out = "\n\n".join(parts).strip()
    return out if out else "Short description in 2–3 lines."

def extract_reference_body(raw_body: str) -> str:
    """
    If the file already contains a "Reference (from source)" block, use it as the
    source of truth for extraction so we don't lose original content.
    """
    m = re.search(r"^##\s+Reference\s+\(from source\)\s*$", raw_body, flags=re.MULTILINE)
    if not m:
        return raw_body
    return raw_body[m.end() :].strip()

def first_useful_paragraph(text: str) -> str | None:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paras:
        if p.startswith("#"):
            continue
        if p.startswith("_"):
            continue
        if re.match(r"^(section\s+\d+[:.)-]|introduction)$", p, flags=re.IGNORECASE):
            continue
        if len(p) < 30 and p.lower() in {"overview", "definition", "uses"}:
            continue
        return p
    return paras[0] if paras else None

def best_operational_summary(*candidates: str | None) -> str | None:
    """
    Prefer a paragraph that is not a section label and has enough substance.
    """
    for c in candidates:
        if not c:
            continue
        p = first_useful_paragraph(c) or ""
        if re.match(r"^section\s+\d+\s*[:.)-]", p.strip(), flags=re.IGNORECASE):
            continue
        if len(p.strip()) < 40:
            continue
        return p.strip()
    # fallback: any first useful paragraph
    for c in candidates:
        if not c:
            continue
        p = first_useful_paragraph(c)
        if p:
            return p.strip()
    return None

def first_long_paragraph(text: str) -> str | None:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paras:
        if re.match(r"^section\s+\d+\s*[:.)-]", p, flags=re.IGNORECASE):
            continue
        if p.startswith("#") or p.startswith("_"):
            continue
        if len(p) >= 60:
            return p
    return None

def extract_from_reference(ref: str) -> tuple[str | None, str | None, str | None]:
    """
    Pull overview/details/setup-path from the reference block.
    Supports both:
    - older procedural sections (## Overview / ## Setup path / ## Step-by-step configuration)
    - our v2 reference sections (### Overview / ### Details / ### Setup path (as described))
    """
    # Prefer v2-style ### Details
    m_details = re.search(r"^###\s+Details\s*$", ref, flags=re.MULTILINE)
    if m_details:
        tail = ref[m_details.end() :].strip()
        # stop at next ### if present
        m_next = re.search(r"^###\s+\S.*$", tail, flags=re.MULTILINE)
        details = tail[: m_next.start()].strip() if m_next else tail.strip()
    else:
        details = None

    # Overview
    m_ov = re.search(r"^###\s+Overview\s*$", ref, flags=re.MULTILINE)
    if m_ov:
        tail = ref[m_ov.end() :].strip()
        m_next = re.search(r"^###\s+\S.*$", tail, flags=re.MULTILINE)
        overview = tail[: m_next.start()].strip() if m_next else tail.strip()
    else:
        overview = None

    # Setup path
    m_sp = re.search(r"^###\s+Setup path(?:\s+\\(as described\\))?\s*$", ref, flags=re.MULTILINE)
    if m_sp:
        tail = ref[m_sp.end() :].strip()
        m_next = re.search(r"^###\s+\S.*$", tail, flags=re.MULTILINE)
        setup = tail[: m_next.start()].strip() if m_next else tail.strip()
    else:
        # fallback to procedural "## Setup path"
        m_sp2 = re.search(r"^##\s+Setup path\s*$", ref, flags=re.MULTILINE)
        if m_sp2:
            tail = ref[m_sp2.end() :].strip()
            m_next = re.search(r"^##\s+\S.*$", tail, flags=re.MULTILINE)
            setup = tail[: m_next.start()].strip() if m_next else tail.strip()
        else:
            setup = None

    return overview, details, setup


def extract_options(step_by_step: str | None) -> List[str]:
    """
    Pull option-like tokens from headings / enumerations.
    """
    if not step_by_step:
        return []
    opts: List[str] = []
    for ln in step_by_step.splitlines():
        m = re.match(r"^(?:###|####)\s+(.+?)\s*$", ln.strip())
        if m:
            t = m.group(1).strip()
            if t and len(t) <= 80:
                opts.append(t)
    # also capture numbered feature variants like "1.1: X"
    for ln in step_by_step.splitlines():
        m = re.match(r"^\s*\d+(?:\.\d+)*\s*[:.)-]\s*(.+?)\s*$", ln.strip())
        if m:
            t = m.group(1).strip()
            if t and len(t) <= 80:
                opts.append(t)
    # de-dup
    seen = set()
    out = []
    for o in opts:
        k = o.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(o)
    return out[:10]


def extract_notes(text: str) -> List[str]:
    notes: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if re.search(r"\b(important note|important|note:|only\s+\d+|cannot|warning)\b", s, re.IGNORECASE):
            # avoid huge json-ish lines
            if len(s) > 220:
                continue
            notes.append(s.lstrip("- ").strip())
    # de-dup
    seen = set()
    out = []
    for n in notes:
        k = n.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(n)
    return out[:8]


def rewrite_one(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in raw:
        return False
    for om in OLD_MARKERS:
        raw = raw.replace(om, "")

    if path.name == "response-management-auto-replies-and-customer-satisfaction.md":
        # gold standard is hand-authored
        return False

    lines = raw.splitlines(keepends=True)
    meta, body_lines = split_meta(lines)
    body = "".join(body_lines)
    ref_body = extract_reference_body(body)
    ref_overview, ref_details, ref_setup = extract_from_reference(ref_body)

    # Expect procedural:v2 format from earlier rewrite
    title = get_first_h1(body) or path.stem.replace("-", " ").title()
    module = get_module(body) or "Agent Assist"
    # Prefer procedural sections if present; otherwise fall back to reference-derived parts
    overview = section(body, "Overview") or ref_overview
    when_to_use = section(body, "When to use")
    setup_path_section = section(body, "Setup path") or ref_setup
    step_by_step = section(body, "Step-by-step configuration") or ref_details or ref_overview
    last_updated = None
    m = UPDATED_RE.search(body)
    if m:
        last_updated = m.group(1).strip()

    where = guess_where_to_configure(path.name)
    setup_path = extract_setup_path(setup_path_section)
    needs_save = "→ Settings" in where or "Settings →" in where
    # If the underlying page itself mentions save/deploy, keep save semantics.
    if step_by_step and re.search(r"\b(save|deploy|publish)\b", step_by_step, flags=re.IGNORECASE):
        needs_save = True
    steps = synthesize_steps(where, setup_path, needs_save=needs_save)
    # Enrich steps with any actionable bullets in the reference details
    extra = extract_action_bullets(ref_body)
    if extra:
        # Insert after navigation steps (keep small)
        steps = steps[:3] + extra[:6] + steps[3:]
        steps = steps[:14]
    definition = extract_definition(overview, when_to_use)
    # If definition is still low-signal, try the first useful paragraph from details
    low_signal = definition.strip().lower() in {"short description in 2–3 lines.", "short description in 2-3 lines."}
    low_signal = low_signal or bool(re.match(r"^section\s+\d+\s*[:.)-]", definition.strip(), flags=re.IGNORECASE))
    low_signal = low_signal or definition.strip().lower() in {"introduction", "overview"}
    if low_signal:
        alt = best_operational_summary(step_by_step, ref_details, ref_overview)
        if alt:
            definition = alt
    # Hard fallback: never keep a "Section X:" label as the summary
    if re.match(r"^section\s+\d+\s*[:.)-]", definition.strip(), flags=re.IGNORECASE):
        alt2 = first_long_paragraph(step_by_step or "") or first_long_paragraph(ref_details or "")
        if alt2:
            definition = alt2.strip()
    options = extract_options(step_by_step)
    notes = extract_notes(body)

    out: List[str] = []
    if meta:
        out.extend(meta)
        if not meta[-1].endswith("\n"):
            out.append("\n")
        if meta[-1].strip() != "":
            out.append("\n")

    out.append(MARKER + "\n")
    out.append(f"# {title}\n\n")
    out.append(f"**Module**: {module}\n\n")

    # Recommended operator template headings
    out.append("## What this feature does\n")
    out.append(definition.strip() + "\n\n")

    out.append("## Where to configure it\n")
    out.append(where + "\n\n")

    out.append("## Exact path\n")
    out.append(where + "\n\n")

    out.append("## Prerequisites\n")
    out.append("- _List required roles/access, teams, and any upstream configuration._\n\n")

    out.append("## Setup path\n")
    if setup_path:
        for s in setup_path:
            out.append(f"- {s}\n")
        out.append("\n")
    else:
        # fallback: derive from where string
        out.append(f"- {where}\n\n")

    out.append("## Steps\n")
    for i, s in enumerate(steps, start=1):
        out.append(f"{i}. {s}\n")
    out.append("\n")

    out.append("## Save/publish behavior\n")
    if needs_save:
        out.append("- Click **Save** (or **Save & Deploy** if available) to apply changes.\n\n")
    else:
        out.append("- _No save/publish step is required for this page unless explicitly stated in the UI._\n\n")

    out.append("## Validation\n")
    out.append("- _Run a quick test (new chat / assignment / workflow) and confirm expected behavior._\n\n")

    out.append("## Available options\n")
    if options:
        for o in options:
            out.append(f"- {o}\n")
        out.append("\n")
    else:
        out.append("- _List the key variants/toggles visible in the UI._\n\n")

    out.append("## Notes\n")
    if notes:
        for n in notes:
            out.append(f"- {n}\n")
    else:
        out.append("- _Add prerequisites, constraints, and rollout behavior._\n")
    if last_updated:
        out.append(f"- **Last updated (from source)**: {last_updated}\n")
    out.append("\n")

    out.append("## Troubleshooting\n")
    if notes:
        out.append("- If something doesn’t work as expected, re-check the **Exact path** and confirm you saved changes.\n")
    out.append("- _Add common failure modes and how to fix them._\n\n")

    out.append("## Field mapping / schemas\n")
    out.append("- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._\n\n")

    out.append("## Cross-module workflows\n")
    out.append("- _Link this feature to adjacent modules (e.g., Business Hours ↔ Auto Replies; Assignment Rules ↔ Teams ↔ Views)._\n\n")

    out.append("## Module disambiguation\n")
    out.append("- _Add 1–2 bullets distinguishing this feature from adjacent settings to reduce retrieval drift._\n\n")

    out.append("## Reference (from source)\n")
    # Preserve reference body rather than re-deriving partial blocks
    out.append(ref_body.strip() + "\n")

    path.write_text("".join(out), encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for p in sorted(AA_DIR.glob("*.md")):
        if rewrite_one(p):
            changed += 1
    print(f"rewritten_files={changed}")


if __name__ == "__main__":
    main()

