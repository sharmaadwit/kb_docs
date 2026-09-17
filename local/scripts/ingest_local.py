#!/usr/bin/env python3
"""Locally regenerate kb_chunks.jsonl rows for a subset of KB pages.

Reuses the exact chunker from skill/kb_ingest.py so locally-produced chunks
match what the production GitHub-based ingest would write. Used to make newly
added pages searchable for local testing before the real ingest runs.

Usage:
  python3 local/scripts/ingest_local.py --prefix kb/superagent/

Replaces all existing chunk rows whose `source` starts with the given prefix,
regenerating them from the on-disk markdown, and leaves every other row intact.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

from kb_ingest import _chunk_text  # noqa: E402

CHUNKS_PATH = ROOT / "kb" / "kb_chunks.jsonl"


def build_rows_for_file(rel_path: str) -> list:
    raw = (ROOT / rel_path).read_text(encoding="utf-8")
    records = _chunk_text(raw, rel_path)
    rows = []
    for idx, rec in enumerate(records):
        rows.append({
            "id": f"{rel_path}::chunk_{idx}",
            "source": rel_path,
            "chunk": idx,
            "section": rec.get("section"),
            "heading": rec.get("heading") or "",
            "heading_path": rec.get("heading_path") or [],
            "section_type": rec.get("section_type") or "general",
            "is_reference": rec.get("section_type") == "reference",
            "local_chunk": rec.get("local_chunk"),
            "text": rec.get("text") or "",
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True, help="source path prefix to (re)ingest, e.g. kb/superagent/")
    args = ap.parse_args()
    prefix = args.prefix

    existing = []
    with CHUNKS_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not str(row.get("source", "")).startswith(prefix):
                existing.append(row)

    md_files = sorted(
        str(p.relative_to(ROOT)) for p in (ROOT).glob(f"{prefix}**/*.md")
    )
    new_rows = []
    for rel in md_files:
        rows = build_rows_for_file(rel)
        new_rows.extend(rows)
        print(f"{rel}: {len(rows)} chunk(s)")

    out = existing + new_rows
    with CHUNKS_PATH.open("w", encoding="utf-8") as fh:
        for row in out:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\ntotal rows: {len(out)} (kept {len(existing)}, regenerated {len(new_rows)} under {prefix})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
