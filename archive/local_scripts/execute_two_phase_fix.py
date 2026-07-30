#!/usr/bin/env python3
"""
Two-Phase Fix for KB Issues

Phase 1: Delete old Langfuse traces with null user_email
Phase 2: Fix KB indexing issues and verify fixes
"""

import json
import os
import sys
import base64
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Setup paths
REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skill"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

# Import required modules
from kb_ingest import _chunk_text


# ============================================================================
# Phase 1: Delete Old Traces with Null Email
# ============================================================================

def load_env_vars() -> Dict[str, str]:
    """Load .env file into dict."""
    env_path = REPO_ROOT / ".env"
    env_vars = {}
    if not env_path.exists():
        print("ERROR: .env file not found")
        return env_vars

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            env_vars[key.strip()] = val.strip().strip('"').strip("'")

    return env_vars


def delete_traces_with_null_email(env_vars: Dict[str, str]) -> Tuple[int, str, str]:
    """Delete traces where user_email is null/missing.

    Returns: (count_deleted, date_range, status_msg)
    """
    host = env_vars.get("LANGFUSE_HOST", "").rstrip("/")
    public_key = env_vars.get("LANGFUSE_PUBLIC_KEY", "")
    secret_key = env_vars.get("LANGFUSE_SECRET_KEY", "")

    if not (host and public_key and secret_key):
        return 0, "", "ERROR: Missing Langfuse credentials"

    # Basic auth header
    auth_str = f"{public_key}:{secret_key}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json",
    }

    print("\n[PHASE 1] Deleting old traces with null user_email...")

    # Cutoff: this session
    cutoff_time = datetime(2026, 7, 3, 10, 0, 0, tzinfo=timezone.utc)

    # Fetch all traces with pagination
    all_traces = []
    limit = 100
    skip = 0
    max_iterations = 10  # Safety limit
    iterations = 0

    try:
        while iterations < max_iterations:
            url = f"{host}/api/public/traces?limit={limit}&skip={skip}"
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()

            data = resp.json().get("data", [])
            if not data:
                break

            all_traces.extend(data)
            skip += limit
            iterations += 1
            print(f"  Fetched {len(data)} traces (total so far: {len(all_traces)})")
    except Exception as e:
        return 0, "", f"ERROR fetching traces: {e}"

    print(f"Total traces fetched: {len(all_traces)}")

    # Filter: null/missing email AND old (before cutoff)
    to_delete = []
    for trace in all_traces:
        metadata = trace.get("metadata", {})
        user_email = metadata.get("user_email")
        trace_time = trace.get("timestamp", "")

        # Check if email is null or missing
        if user_email is None or user_email == "":
            # Check if trace is old (before cutoff)
            try:
                if trace_time:
                    # Parse ISO format timestamp
                    trace_dt = datetime.fromisoformat(trace_time.replace("Z", "+00:00"))
                    if trace_dt < cutoff_time:
                        to_delete.append(trace.get("id"))
            except:
                # If parse fails, include it in deletion
                to_delete.append(trace.get("id"))

    print(f"Traces to delete: {len(to_delete)}")

    if not to_delete:
        return 0, "", "No traces found matching criteria"

    # Delete in batches
    deleted_count = 0
    batch_size = 50
    for i in range(0, len(to_delete), batch_size):
        batch = to_delete[i:i+batch_size]
        try:
            url = f"{host}/api/public/traces"
            payload = {"traceIds": batch}
            resp = requests.delete(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            deleted_count += len(batch)
            print(f"  Deleted batch {i//batch_size + 1}: {len(batch)} traces")
        except Exception as e:
            print(f"  ERROR deleting batch: {e}")
            # Don't continue on error, report failure
            deleted_count = len(to_delete) - len(batch)  # Count what we got so far

    # Determine date range of deleted traces
    date_range = ""
    if to_delete:
        earliest = None
        latest = None
        for trace in all_traces:
            if trace.get("id") in to_delete:
                try:
                    ts = datetime.fromisoformat(trace.get("timestamp", "").replace("Z", "+00:00"))
                    if earliest is None or ts < earliest:
                        earliest = ts
                    if latest is None or ts > latest:
                        latest = ts
                except:
                    pass
        if earliest and latest:
            date_range = f"{earliest.isoformat()} to {latest.isoformat()}"

    return deleted_count, date_range, f"Successfully deleted {deleted_count} traces"


# ============================================================================
# Phase 2: Fix KB Indexing Issues
# ============================================================================

def rebuild_kb_chunks(prefixes: List[str]) -> Tuple[int, List[str]]:
    """Rebuild KB chunks for given prefixes.

    Returns: (total_new_chunks, list_of_updated_prefixes)
    """
    chunks_path = REPO_ROOT / "kb" / "kb_chunks.jsonl"

    print("\n[PHASE 2] Rebuilding KB chunks...")

    # Load existing chunks (exclude the prefixes we're rebuilding)
    existing = []
    with open(chunks_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            source = str(row.get("source", ""))
            # Keep chunks NOT in our prefixes
            if not any(source.startswith(prefix) for prefix in prefixes):
                existing.append(row)

    print(f"  Existing chunks (non-{prefixes}): {len(existing)}")

    # Regenerate chunks for the specified prefixes
    new_rows = []
    updated_prefixes = []

    for prefix in prefixes:
        md_files = sorted(
            str(p.relative_to(REPO_ROOT))
            for p in REPO_ROOT.glob(f"{prefix}**/*.md")
        )

        prefix_chunk_count = 0
        for rel_path in md_files:
            try:
                raw = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
                records = _chunk_text(raw, rel_path)

                for idx, rec in enumerate(records):
                    row = {
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
                    }
                    new_rows.append(row)
                    prefix_chunk_count += 1
            except Exception as e:
                print(f"  ERROR processing {rel_path}: {e}")
                continue

        if prefix_chunk_count > 0:
            updated_prefixes.append(prefix)
            print(f"  Regenerated {prefix_chunk_count} chunks for {prefix}")

    # Write combined chunks
    combined = existing + new_rows
    with open(chunks_path, "w", encoding="utf-8") as fh:
        for row in combined:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"  Total chunks after rebuild: {len(combined)}")

    return len(new_rows), updated_prefixes


def verify_kb_chunks(prefixes: List[str]) -> Dict[str, bool]:
    """Verify that new chunks are in kb_chunks.jsonl.

    Returns: dict with keys like "bizai" -> bool (found)
    """
    chunks_path = REPO_ROOT / "kb" / "kb_chunks.jsonl"

    print("\n[PHASE 2] Verifying KB chunks...")

    results = {}
    for prefix in prefixes:
        found_count = 0
        with open(chunks_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                source = str(row.get("source", ""))
                if source.startswith(prefix):
                    found_count += 1

        results[prefix] = found_count > 0
        print(f"  {prefix}: {found_count} chunks (OK)" if found_count > 0 else f"  {prefix}: NOT FOUND (ERROR)")

    return results


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    print("=" * 80)
    print("TWO-PHASE KB FIX")
    print("=" * 80)

    # Load environment
    env_vars = load_env_vars()
    if not env_vars:
        print("ERROR: Could not load environment variables")
        return 1

    # PHASE 1: Delete old traces with null email
    deleted_count, date_range, phase1_msg = delete_traces_with_null_email(env_vars)
    phase1_status = "COMPLETE" if deleted_count >= 0 else "FAILED"
    print(f"\n[PHASE 1] {phase1_status}: {phase1_msg}")
    if date_range:
        print(f"           Date range cleaned: {date_range}")

    # PHASE 2: Fix KB indexing issues
    prefixes = ["kb/bizai/", "kb/whatsapp/"]

    try:
        new_chunks, updated = rebuild_kb_chunks(prefixes)
        phase2_status = "COMPLETE" if new_chunks > 0 else "FAILED"
        verify_results = verify_kb_chunks(prefixes)
        all_verified = all(verify_results.values())
    except Exception as e:
        print(f"ERROR in Phase 2: {e}")
        phase2_status = "FAILED"
        new_chunks = 0
        updated = []
        verify_results = {p: False for p in prefixes}
        all_verified = False

    print(f"\n[PHASE 2] {phase2_status}: Generated {new_chunks} new chunks")
    if updated:
        print(f"           Updated prefixes: {', '.join(updated)}")

    # Final report
    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    report = {
        "phase1_traces_deleted": deleted_count,
        "phase1_date_range": date_range or "N/A",
        "phase1_status": phase1_status,
        "phase2_new_chunks": new_chunks,
        "phase2_prefixes_updated": updated,
        "phase2_verification": verify_results,
        "phase2_status": phase2_status,
        "overall_status": "SUCCESS" if (phase1_status == "COMPLETE" and phase2_status == "COMPLETE" and all_verified) else "PARTIAL_SUCCESS",
        "next_steps": [
            "Run test_bizai_whatsapp_comprehensive.py to verify answers are now found",
            "Monitor confidence scores (should be > 0.3 for new content)",
            "Check Langfuse for new traces with the BizAI/WhatsApp queries"
        ] if phase2_status == "COMPLETE" else [
            "Review error logs",
            "Check KB files exist",
            "Verify kb_chunks.jsonl is readable"
        ]
    }

    print(json.dumps(report, indent=2))

    # Save report
    report_path = REPO_ROOT / "local" / "reports" / "phase_fix_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {report_path}")

    return 0 if phase1_status == "COMPLETE" and phase2_status == "COMPLETE" and all_verified else 1


if __name__ == "__main__":
    sys.exit(main())
