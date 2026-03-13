#!/usr/bin/env python3
"""
KB docs rewrite: task-oriented operating guides for non-Agent Assist pages.

Golden rule (task-oriented)
- Definition: good for understanding
- Procedure: required for answer quality (explicit path, steps, fields, validation, troubleshooting)

Scope
- Rewrites kb/**/*.md excluding kb/agent-assist/*
- Keeps `source_url:` style metadata lines at the top.
- Preserves original content under "Reference (from source)".

Idempotency
- Rewritten files include `<!-- kb-golden:v9 -->`
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "kb"

OLD_MARKERS = {
    "<!-- kb-golden:v1 -->",
    "<!-- kb-golden:v2 -->",
    "<!-- kb-golden:v3 -->",
    "<!-- kb-golden:v4 -->",
    "<!-- kb-golden:v5 -->",
    "<!-- kb-golden:v6 -->",
    "<!-- kb-golden:v7 -->",
    "<!-- kb-golden:v8 -->",
}
MARKER = "<!-- kb-golden:v9 -->"

META_LINE_RE = re.compile(r"^[a-zA-Z0-9_]+:\s+\S+.*$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")

SECTION_SPLIT_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


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

def extract_reference_from_golden(body: str) -> str:
    """
    If the file was already golden-wrapped, extract only the original source portion
    to prevent recursive nesting.
    """
    m = re.search(r"^##\s+Reference\s+\(from source\)\s*$", body, flags=re.MULTILINE)
    if not m:
        return body.strip()
    return body[m.end() :].strip()


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
        t = title.lower()
        if "prompt" in t and "timeout" in t:
            return "Gupshup Console → Bot Studio → Journey Builder → Prompt Node → Timeout"
        if "manage variables" in t or "variables" == t.strip():
            return "Gupshup Console → Bot Studio → Manage Variables"
        if "journey" in t and "builder" in t:
            return "Gupshup Console → Bot Studio → Journey Builder"
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

def synthesize_setup_path_from_exact_path(exact_path: str) -> List[str]:
    # Convert "A → B → C" into click-by-click bullets.
    parts = [p.strip() for p in exact_path.split("→") if p.strip()]
    if not parts:
        return []
    out: List[str] = []
    # Drop the root "Gupshup Console" since Steps already includes opening it.
    parts2 = parts[1:] if parts and parts[0].lower() == "gupshup console" else parts
    for p in parts2:
        out.append(f"Go to **{p}**.")
    return out[:10]

def extract_action_bullets(text: str) -> List[str]:
    """
    Pull operator actions from the source (usually under how-to sections).
    """
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
        if re.match(r"^(select|click|enable|disable|enter|provide|choose|configure|add|go|navigate|open|set|toggle|connect|deploy|save|test|verify|confirm|ensure|note that)\b", b, re.IGNORECASE):
            k = b.lower()
            if k in seen:
                continue
            seen.add(k)
            actions.append(b.rstrip(".") + ".")
    return actions[:18]

def extract_fields_to_configure(text: str) -> List[str]:
    """
    Heuristic: derive "fields to configure" from action bullets.
    Examples:
    - "Add your Callback URL and save." -> "Callback URL"
    - "Provide the desired timeout duration..." -> "Timeout duration"
    """
    fields: List[str] = []
    seen = set()
    actions = extract_action_bullets(text)

    def add_field(name: str) -> None:
        k = name.lower().strip()
        if not k or k in seen:
            return
        seen.add(k)
        fields.append(name.strip())

    for a in actions:
        s = a.strip().rstrip(".")
        # Add your X
        m = re.search(r"\badd\s+(?:your\s+)?(.+?)(?:\s+and\s+save|\s+and\s+click|\s+then|\s*$)", s, flags=re.IGNORECASE)
        if m:
            cand = m.group(1).strip(" :")
            if 2 <= len(cand) <= 60:
                if cand.lower().startswith("desired "):
                    cand = cand[8:].strip()
                if "as needed" in cand.lower() or "located at" in cand.lower():
                    continue
                add_field(cand)

        # Provide/Enter/Set the X
        m = re.search(r"\b(?:provide|enter|set)\s+(?:the\s+)?(.+?)(?:\s+in|\s+on|\s+to|\s*$)", s, flags=re.IGNORECASE)
        if m:
            cand = m.group(1).strip(" :")
            if 2 <= len(cand) <= 60:
                if cand.lower().startswith("desired "):
                    cand = cand[8:].strip()
                if "as needed" in cand.lower() or "located at" in cand.lower():
                    continue
                add_field(cand)

        # Common fields
        if re.search(r"\bcallback url\b", s, re.IGNORECASE):
            add_field("Callback URL")
        if re.search(r"\btimeout\b", s, re.IGNORECASE):
            add_field("Timeout duration")
        if re.search(r"\btime zone\b|\btimezone\b", s, re.IGNORECASE):
            add_field("Time zone")
        if re.search(r"\bholiday\b", s, re.IGNORECASE):
            add_field("Holidays")
        if re.search(r"\bmessage\b", s, re.IGNORECASE):
            add_field("Message content")
        if re.search(r"\bvalidation\b", s, re.IGNORECASE):
            add_field("Validation rules")
        if re.search(r"\bfallback\b", s, re.IGNORECASE):
            add_field("Fallback connector path")

    # Normalize + de-dup with a canonical vocabulary
    canon: List[str] = []
    canon_seen = set()
    for f in fields:
        s = f.strip().rstrip(".")
        sl = s.lower()
        if "callback" in sl and "url" in sl:
            s = "Callback URL"
        elif "timeout" in sl or "duration" in sl:
            s = "Timeout duration"
        elif "validation" in sl:
            s = "Validation rules"
        elif "message" in sl:
            s = "Message content"
        elif "fallback" in sl or "connector" in sl:
            s = "Fallback connector path"
        k = s.lower()
        if k in canon_seen:
            continue
        canon_seen.add(k)
        canon.append(s)
        if len(canon) >= 10:
            break
    return canon

def extract_payload_examples(text: str) -> List[str]:
    """
    Extract a few compact payload examples (inline/backticked JSON).
    """
    examples: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("`{") and s.endswith("}`") and len(s) <= 450:
            examples.append(s.strip("`"))
        elif s.startswith("{") and s.endswith("}") and len(s) <= 450:
            examples.append(s)
        if len(examples) >= 3:
            break
    return examples

def extract_markdown_tables(text: str) -> List[str]:
    """
    Extract up to 2 markdown tables (pipe tables) as raw blocks.
    """
    lines = text.splitlines()
    tables: List[str] = []
    i = 0
    while i < len(lines) - 1:
        if "|" in lines[i] and "|" in lines[i + 1] and re.search(r"\|\s*---", lines[i + 1]):
            start = i
            j = i + 2
            while j < len(lines) and "|" in lines[j]:
                j += 1
            block = "\n".join(lines[start:j]).strip()
            if block:
                tables.append(block)
                if len(tables) >= 2:
                    break
            i = j
            continue
        i += 1
    return tables

def extract_prerequisites(text: str) -> List[str]:
    prereq: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if re.search(r"\b(before you begin|prerequisite|requirements?)\b", s, re.IGNORECASE):
            if len(s) <= 200:
                prereq.append(s.lstrip("- ").strip())
    # de-dup
    seen = set()
    out = []
    for p in prereq:
        k = p.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return out[:8]

def extract_validation(text: str) -> List[str]:
    items: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if re.search(r"\b(test|validate|verification|verify|confirm)\b", s, re.IGNORECASE):
            if len(s) <= 200:
                items.append(s.lstrip("- ").strip())
    # de-dup
    seen = set()
    out = []
    for it in items:
        k = it.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out[:8]

def extract_troubleshooting(text: str) -> List[str]:
    items: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if re.search(r"\b(error|failed|fails|not working|cannot|only\s+\d+|important note|warning)\b", s, re.IGNORECASE):
            if len(s) <= 220 and not s.startswith("{"):
                cleaned = s.lstrip("- ").strip()
                if len(cleaned.split()) <= 1:
                    continue
                items.append(cleaned)
    # de-dup
    seen = set()
    out = []
    for it in items:
        k = it.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out[:10]

def extract_field_mapping(text: str) -> List[str]:
    """
    Pull key: description style lines, and flag sample payload areas.
    """
    items: List[str] = []
    state = "scan"
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue

        if state == "scan":
            if re.search(r"\b(key\s*:?\s*description)\b", s, re.IGNORECASE) or s.lower().startswith("## key"):
                state = "keys"
                continue
            if re.search(r"\bsample payload\b", s, re.IGNORECASE):
                # keep scanning; many docs place keys after payloads
                continue

        if state == "keys":
            # stop at next H2 that isn't "Key"
            if s.startswith("## ") and "key" not in s.lower():
                break
            m = re.match(r"^([a-zA-Z0-9_\\-]+)\s*:\s+(.+)$", s)
            if m and len(s) <= 220:
                items.append(s)
    # de-dup
    seen = set()
    out = []
    for it in items:
        k = it.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out[:12]

def extract_options(text: str) -> List[str]:
    """
    Heuristic: capture UI-like options/toggles rather than section headings.
    """
    items: List[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        # Prefer action-like bullets
        if s.startswith("- "):
            b = s[2:].strip()
            if re.match(r"^(toggle|enable|disable|select|choose|set|add|enter)\b", b, re.IGNORECASE):
                if len(b) <= 120:
                    items.append(b)
        if re.search(r"\b(toggle|switch)\b", s, re.IGNORECASE) and len(s) <= 120:
            items.append(s.lstrip("- ").strip())
    # de-dup
    seen = set()
    out = []
    for it in items:
        k = it.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out[:10]

def disambiguation_for_module(rel_path: Path) -> List[str]:
    top = rel_path.parts[0].lower() if rel_path.parts else ""
    if top == "bot-studio":
        return [
            "**Save** stores changes; **Save & Deploy** publishes to live channels.",
            "Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.",
        ]
    if top == "campaign-manager":
        return [
            "Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).",
        ]
    if top == "integrations":
        return [
            "Integrations configure connectivity/events; they don’t change bot conversation logic (Bot Studio) by themselves.",
        ]
    if top == "channels":
        return [
            "Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.",
        ]
    if top == "ctx":
        return [
            "CTX covers ad-to-WhatsApp campaign flows; bot conversation logic still lives in **Bot Studio**.",
        ]
    return []

def related_workflows(rel_path: Path) -> List[str]:
    top = rel_path.parts[0].lower() if rel_path.parts else ""
    if top == "integrations" and "webhooks" in rel_path.name.lower():
        return [
            "Delivery Webhooks → Campaign Manager analytics",
            "Webhook events → downstream CRM/warehouse ingestion",
        ]
    if top == "bot-studio":
        return [
            "Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)",
            "Bot Studio journey → Observability via Webhooks",
        ]
    if top == "ctx":
        return [
            "CTX campaign → Bot Studio journey → Goal measurement",
        ]
    return []


def synthesize_steps(where: str, setup_path: List[str], body: str) -> List[str]:
    # If we have explicit bullet steps, reuse them
    if setup_path:
        out = ["Open Gupshup Console."]
        # Avoid repeating "Open ..." if it's already in setup path
        for s in setup_path:
            if re.match(r"^open\b", s.strip(), flags=re.IGNORECASE):
                continue
            out.append(s)
        # Add extracted action bullets from the source (how-to lists)
        actions = extract_action_bullets(body)
        if actions:
            # avoid duplicating navigation-like actions
            nav_prefixes = ("go to ", "navigate to ", "open ")
            for a in actions:
                if a.lower().startswith(nav_prefixes):
                    continue
                out.append(a)
                if len(out) >= 12:
                    break
        if not any(re.search(r"\bsave\b|\bdeploy\b|\bpublish\b", s, re.IGNORECASE) for s in out):
            # add save step only if doc mentions it
            if re.search(r"\b(save|deploy|publish|go live)\b", body, flags=re.IGNORECASE):
                out.append("Click **Save** (or **Save & Deploy**) to apply changes.")
        return out[:14]

    # Otherwise synthesize generic but include any extracted action bullets from the source
    out = [
        "Open Gupshup Console.",
        f"Navigate to **{where}**.",
    ]
    actions = extract_action_bullets(body)
    if actions:
        out.extend(actions[:10])
    else:
        out.append("Configure the required fields.")
    if re.search(r"\b(save|deploy|publish|go live)\b", body, flags=re.IGNORECASE):
        out.append("Click **Save** (or **Save & Deploy**) to apply changes.")
    return out[:14]


def rewrite_one(path: Path) -> bool:
    rel = path.relative_to(KB_DIR)
    if rel.parts and rel.parts[0] in {"agent-assist", "workflows"}:
        return False

    raw = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in raw:
        return False
    for om in OLD_MARKERS:
        raw = raw.replace(om, "")

    meta, body = split_meta(raw)
    body = extract_reference_from_golden(body)
    # If previously rewritten by procedural script, keep it as reference; we’ll build golden blocks on top
    title = extract_title(body, fallback=path.stem.replace("-", " ").title())
    module = extract_module(body, rel)

    overview = section(body, "Overview") or section(body, "Step-by-step configuration") or body
    definition = first_useful_paragraph(overview or "") or "Short description in 2–3 lines."

    where = guess_where_to_configure(rel, title, module)
    exact_path = where  # single canonical breadcrumb used by the KB
    setup_path = extract_setup_path(body)
    if not setup_path:
        setup_path = synthesize_setup_path_from_exact_path(exact_path)
    steps = synthesize_steps(where, setup_path, body)
    prereq = extract_prerequisites(body)
    validation = extract_validation(body)
    troubleshooting = extract_troubleshooting(body)
    field_map = extract_field_mapping(body)
    tables = extract_markdown_tables(body)
    fields = extract_fields_to_configure(body)
    payload_examples = extract_payload_examples(body)
    opt2 = extract_options(body)

    # Options: prefer explicit UI option bullets; keep BH/after-hours disambiguation cue if present
    options: List[str] = []
    bha = section(body, "Business hours vs after-hours behavior")
    if bha and "_Not applicable" not in bha:
        options.append("Business hours vs after-hours behavior")

    out: List[str] = []
    out.append(meta)
    out.append(MARKER + "\n")
    out.append(f"# {title}\n\n")
    if module:
        out.append(f"**Module**: {module}\n\n")

    out.append("## Definition\n")
    out.append(definition.strip() + "\n\n")

    out.append("## Procedure\n")
    out.append("### Exact UI path\n")
    out.append(exact_path + "\n\n")

    out.append("### Steps\n")
    for i, s in enumerate(steps, start=1):
        out.append(f"{i}. {s}\n")
    out.append("\n")

    out.append("### Validation / where to check\n")
    if validation:
        for v in validation:
            out.append(f"- {v}\n")
        out.append("\n")
    else:
        out.append("- _Run a quick smoke test and confirm expected behavior._\n\n")

    out.append("### Fields to configure\n")
    if fields:
        for f in fields:
            out.append(f"- {f}\n")
        out.append("\n")
    else:
        out.append("- _List the fields/inputs you must set in the UI (and expected format)._\n\n")

    out.append("### Save / publish / deploy behavior\n")
    if re.search(r"\b(save|deploy|publish)\b", body, flags=re.IGNORECASE):
        out.append("- Click **Save** (or **Save & Deploy**) to apply changes.\n\n")
    else:
        out.append("- _If this page has a Save/Publish action, document it here._\n\n")

    out.append("### Troubleshooting\n")
    if troubleshooting:
        for t in troubleshooting:
            out.append(f"- {t}\n")
        out.append("\n")
    else:
        out.append("- _Add common failure modes and how to fix them._\n\n")

    out.append("### Prerequisites\n")
    if prereq:
        for p in prereq:
            out.append(f"- {p}\n")
        out.append("\n")
    else:
        out.append("- _List required access, assets, and upstream setup needed before configuration._\n\n")

    out.append("### Setup path\n")
    for s in setup_path[:10]:
        out.append(f"- {s}\n")
    out.append("\n")

    out.append("## Options / variants\n")
    combined_options = options or []
    for o in opt2:
        combined_options.append(o)
    # de-dup combined
    seen_opt = set()
    deduped = []
    for o in combined_options:
        k = o.lower().strip()
        if k in seen_opt:
            continue
        seen_opt.add(k)
        deduped.append(o)
    # filter generic headings that aren't UI options
    GENERIC = {
        "when to use",
        "limitations",
        "overview",
        "introduction",
        "use cases",
        "summary",
        "notes",
        "steps",
        "step-by-step configuration",
        "setup path",
    }
    filtered = []
    for o in deduped:
        k2 = re.sub(r"[^a-z0-9]+", " ", o.lower()).strip()
        if k2 in GENERIC or k2.startswith("step "):
            continue
        filtered.append(o)
    filtered = filtered[:12]

    if filtered:
        for o in filtered:
            out.append(f"- {o}\n")
        out.append("\n")
    else:
        out.append("- _List the key variants/toggles visible in the UI._\n\n")

    out.append("## Notes\n")
    out.append("- _Add prerequisites, constraints, and rollout behavior._\n\n")

    out.append("## Field mapping / schemas\n")
    if tables:
        out.append("Tables from the source:\n\n")
        for t in tables:
            out.append(t.strip() + "\n\n")
    if field_map:
        out.append("Keys/fields called out in the source:\n\n")
        for fm in field_map:
            out.append(f"- {fm}\n")
        out.append("\n")
    elif not tables:
        out.append("- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._\n\n")

    out.append("## Field/payload examples\n")
    if payload_examples:
        for ex in payload_examples:
            out.append(f"- `{ex}`\n")
        out.append("\n")
    else:
        out.append("- _Add a minimal example payload or field/value example._\n\n")

    out.append("## Cross-module workflow docs\n")
    flows = related_workflows(rel)
    if flows:
        for f in flows:
            out.append(f"- {f}\n")
        out.append("\n")
    else:
        out.append("- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._\n\n")

    out.append("## Module disambiguation docs\n")
    dis = disambiguation_for_module(rel)
    if dis:
        for d in dis:
            out.append(f"- {d}\n")
        out.append("\n")
    else:
        out.append("- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._\n\n")

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

