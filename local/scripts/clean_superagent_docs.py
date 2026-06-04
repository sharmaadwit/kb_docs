#!/usr/bin/env python3
"""One-off cleanup of extracted SuperAgent docs.

Strips extraction artifacts so the pages chunk cleanly:
  - `*Interactive preview: ...*` caption lines
  - the "Interactive preview (Skills Guide pattern): ..." helper sentence
  - fenced ```mermaid ... ``` diagram blocks (kept only the box labels as noise otherwise)

Run from repo root:  python3 local/scripts/clean_superagent_docs.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SA_DIR = ROOT / "kb" / "superagent"

PREVIEW_CAPTION = re.compile(r"^\s*\*Interactive preview:.*\*\s*$")
PREVIEW_SENTENCE = re.compile(r"^\s*Interactive preview \(Skills Guide pattern\):")


def clean_text(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_mermaid = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            continue
        if in_mermaid:
            if stripped.startswith("```"):
                in_mermaid = False
            continue
        if PREVIEW_CAPTION.match(line):
            continue
        if PREVIEW_SENTENCE.match(line):
            continue
        out.append(line)
    cleaned = "\n".join(out)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def main() -> int:
    if not SA_DIR.exists():
        print(f"missing {SA_DIR}", file=sys.stderr)
        return 1
    changed = 0
    for md in sorted(SA_DIR.rglob("*.md")):
        original = md.read_text(encoding="utf-8")
        cleaned = clean_text(original)
        if cleaned != original:
            md.write_text(cleaned, encoding="utf-8")
            changed += 1
            print(f"cleaned {md.relative_to(ROOT)}")
    print(f"done: {changed} file(s) cleaned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
