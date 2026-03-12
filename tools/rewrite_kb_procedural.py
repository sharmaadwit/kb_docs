#!/usr/bin/env python3
"""
Rewrite kb/**/*.md into a more procedural structure.

Goals:
- Preserve `source_url:` (and any similar top metadata lines).
- Preserve *all* original content (no data loss), but reorganize under a consistent template:
  Overview, When to use, Setup path, Step-by-step configuration,
  Business hours vs after-hours behavior, Save/publish behavior.
- Be idempotent (skip files already rewritten by this script).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "kb"

PROCEDURAL_MARKER = "<!-- procedural:v2 -->"


META_LINE_RE = re.compile(r"^[a-zA-Z0-9_]+:\s+\S+.*$")
H_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")


def _split_meta(lines: List[str]) -> Tuple[List[str], List[str]]:
    """
    Extract leading metadata lines like `source_url: ...` (no YAML fences in this repo).
    Stops at the first non-meta non-empty line.
    """
    meta: List[str] = []
    rest = lines[:]
    i = 0
    while i < len(rest):
        line = rest[i]
        if line.strip() == "":
            if meta:
                meta.append(line)
                i += 1
                continue
            break
        if META_LINE_RE.match(line) and not line.lstrip().startswith("#"):
            meta.append(line)
            i += 1
            continue
        break
    return meta, rest[i:]


def _extract_module_and_title(body_lines: List[str]) -> Tuple[str | None, str | None]:
    """
    Heuristics based on current repo style:
    - Many files begin with `# MODULE`
    - Then `## Page title`
    - Then `# Page title` (duplicate)
    """
    module = None
    title = None

    headings: List[Tuple[int, str]] = []
    for line in body_lines[:80]:
        m = H_RE.match(line)
        if not m:
            continue
        headings.append((len(m.group(1)), m.group(2).strip()))

    if headings:
        # First H1 is typically the module name (Agent Assist, Bot Studio, Integrations, etc.)
        for level, text in headings:
            if level == 1 and text:
                module = text
                break

        # Title is typically the first H2 after module; fallback to first non-module heading.
        for level, text in headings:
            if not text:
                continue
            if module and text.lower() == module.lower():
                continue
            if level == 2:
                title = text
                break
        if title is None:
            for level, text in headings:
                if not text:
                    continue
                if module and text.lower() == module.lower():
                    continue
                if level in (1, 2):
                    title = text
                    break

    if module:
        module = module.strip().title()
    return module, title


def _strip_leading_headings(lines: List[str], module: str | None, title: str | None) -> List[str]:
    """
    Remove the typical header block:
      # MODULE
      ## Title
      # Title
    plus surrounding blank lines.
    """
    out: List[str] = []
    i = 0
    # drop leading blanks
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    # drop module/title headings + surrounding blanks, but keep any other headings
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            i += 1
            continue
        m = H_RE.match(ln)
        if m:
            txt = m.group(2).strip()
            if (module and txt.lower() == module.lower()) or (title and txt.lower() == title.lower()):
                i += 1
                continue
        break
    out.extend(lines[i:])
    return out


def _first_paragraph(text: str) -> str:
    # Grab first "real" paragraph (skip headings / placeholder words).
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    if not chunks:
        return ""

    def is_low_signal(p: str) -> bool:
        s = p.strip()
        if not s:
            return True
        if s.lstrip().startswith("#"):
            return True
        if len(s) < 25 and s.lower() in {"introduction", "overview", "definition", "uses"}:
            return True
        return False

    for c in chunks:
        if not is_low_signal(c):
            return c
    return chunks[0]


def _collect_lines_matching(lines: List[str], pattern: re.Pattern[str]) -> List[str]:
    out: List[str] = []
    for ln in lines:
        if pattern.search(ln):
            out.append(ln.rstrip())
    return out


def _collect_setup_path(lines: List[str]) -> List[str]:
    """
    Pull common navigation steps.
    """
    nav: List[str] = []
    seen = set()
    for ln in lines:
        l = ln.strip().lower()
        if any(l.startswith(p) for p in ("- log into", "- login", "- navigate to", "- go to", "navigate to", "go to", "log into")):
            key = ln.strip()
            if key in seen:
                continue
            seen.add(key)
            nav.append(ln.rstrip())
    # keep short
    return nav[:10]


def _strip_updated_footer(lines: List[str]) -> Tuple[List[str], str | None]:
    """
    Many pages end with `Updated X months ago`.
    Remove it from the body and return it as last_updated.
    """
    if not lines:
        return lines, None
    # scan from end for first non-empty line
    i = len(lines) - 1
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    if i >= 0 and re.match(r"^Updated\s+.+$", lines[i].strip(), re.IGNORECASE):
        last = lines[i].strip()
        new_lines = lines[:i] + ["\n"]  # keep trailing newline spacer
        return new_lines, last
    return lines, None


def rewrite_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    # idempotency: allow upgrading v1 -> v2; skip only if already v2
    if PROCEDURAL_MARKER in raw:
        return False
    # If file was already rewritten as v1, allow rewriting to v2
    raw = raw.replace("<!-- procedural:v1 -->", "")

    lines = raw.splitlines(keepends=True)
    meta, body_lines = _split_meta(lines)
    module, title = _extract_module_and_title(body_lines)
    title = title or path.stem.replace("-", " ").strip()

    # Remove procedural v1 marker if present (we may be upgrading)
    body_text = "".join(body_lines).replace("<!-- procedural:v1 -->", "")
    body_lines2 = body_text.splitlines(keepends=True)
    body_lines2 = _strip_leading_headings(body_lines2, module, title)
    body_lines2, last_updated = _strip_updated_footer(body_lines2)

    body_text2 = "".join(body_lines2).strip()

    overview = _first_paragraph(body_text2)

    # When to use: capture explicit "Uses:" lines and "use cases" bullets if present
    uses_lines = _collect_lines_matching(body_lines2, re.compile(r"^\s*Uses:\s*", re.IGNORECASE))
    usecase_block = []
    m = re.search(r"(Here are the common use cases\s*-\s*.*)", body_text2, re.IGNORECASE | re.DOTALL)
    if m:
        # take until first double newline after the list starts
        block = m.group(1)
        block = re.split(r"\n\s*\n", block, maxsplit=1)[0]
        usecase_block = [ln.rstrip() for ln in block.splitlines() if ln.strip()]

    setup_path = _collect_setup_path(body_lines2)

    bh_lines = _collect_lines_matching(body_lines2, re.compile(r"\b(business hours|outside business hours|after[-\s]?hours)\b", re.IGNORECASE))
    # Keep this section tight: focus on lifecycle verbs and avoid grabbing JSON payload lines.
    save_lines = _collect_lines_matching(
        body_lines2,
        re.compile(r"\b(save|deploy|publish|submit|go live|launch)\b", re.IGNORECASE),
    )
    save_lines = [
        ln
        for ln in save_lines
        if not ln.lstrip().startswith(("{", "`{"))
        and "`{" not in ln
        and len(ln.strip()) <= 200
    ]

    out: List[str] = []
    if meta:
        out.extend(meta)
        if not meta[-1].endswith("\n"):
            out.append("\n")
        if meta[-1].strip() != "":
            out.append("\n")

    out.append(PROCEDURAL_MARKER + "\n")
    out.append(f"# {title}\n\n")
    if module:
        out.append(f"**Module**: {module}\n\n")

    out.append("## Overview\n")
    if overview:
        out.append(overview.strip() + "\n\n")
    else:
        out.append("_Not specified in source._\n\n")

    out.append("## When to use\n")
    if usecase_block:
        # convert into bullets if not already
        for ln in usecase_block:
            if ln.lower().startswith("here are"):
                continue
            if ln.strip().startswith("-"):
                out.append(ln.strip() + "\n")
            else:
                out.append(f"- {ln.strip()}\n")
        out.append("\n")
    elif uses_lines:
        for ln in uses_lines:
            cleaned = re.sub(r"^\s*Uses:\s*", "", ln.strip(), flags=re.IGNORECASE)
            out.append(f"- {cleaned}\n")
        out.append("\n")
    else:
        out.append("_Add the primary scenarios and personas._\n\n")

    out.append("## Setup path\n")
    if setup_path:
        for ln in setup_path:
            out.append(ln.strip() + "\n")
        out.append("\n")
    else:
        out.append("_In Console: add the navigation path (e.g., `Module → Settings → …`)._\n\n")

    out.append("## Step-by-step configuration\n")
    out.append(body_text2 + "\n\n" if body_text2 else "_Not specified in source._\n\n")

    out.append("## Business hours vs after-hours behavior\n")
    if bh_lines:
        out.append("Key notes found in source:\n\n")
        for ln in bh_lines[:25]:
            out.append(f"- {ln.strip()}\n")
        out.append("\n")
    else:
        out.append("_Not applicable / not specified._\n\n")

    out.append("## Save/publish behavior\n")
    if save_lines:
        out.append("Key notes found in source:\n\n")
        for ln in save_lines[:25]:
            out.append(f"- {ln.strip()}\n")
        out.append("\n")
    else:
        out.append("_Not specified._\n\n")

    if last_updated:
        out.append(f"**Last updated (from source)**: {last_updated}\n")

    new = "".join(out)
    path.write_text(new, encoding="utf-8")
    return True


def iter_md_files() -> Iterable[Path]:
    for p in KB_DIR.rglob("*.md"):
        # skip extremely large marketing decks if any creep in (still keep in repo, but avoid rewriting)
        if p.parts[-2:] and "Success Stories" in p.name:
            continue
        yield p


def main() -> None:
    changed = 0
    for p in iter_md_files():
        if rewrite_file(p):
            changed += 1
    print(f"rewritten_files={changed}")


if __name__ == "__main__":
    main()

