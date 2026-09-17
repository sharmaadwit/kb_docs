#!/usr/bin/env python3
"""
KB Metadata Addition Script
Adds missing metadata fields to all KB chunks.

Phase: Metadata Enrichment
Input: kb/kb_chunks.jsonl (cleaned chunks from Phase A)
Output: kb/kb_chunks.jsonl (with metadata), local/reports/chunks_metadata_added_20260813.json
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re
import os

# Configuration
KB_CHUNKS_PATH = Path("/Users/adwit.sharma/kb_docs/kb/kb_chunks.jsonl")
OUTPUT_PATH = Path("/Users/adwit.sharma/kb_docs/kb/kb_chunks.jsonl")
REPORT_PATH = Path("/Users/adwit.sharma/kb_docs/local/reports/chunks_metadata_added_20260813.json")

# Metadata constants
VERSION = "1.0"
UPDATE_DATE = "2026-08-13"
DEFAULT_AUDIENCE_LEVEL = "beginner"

# Intent classification keywords
INTENT_KEYWORDS = {
    "procedural": [
        "how to", "setup", "install", "configure", "create", "set up", "step",
        "guide", "process", "procedure", "implement", "deploy", "initialize",
        "start", "launch", "build", "enable", "activate", "run", "execute",
        "start with", "getting started", "quick start"
    ],
    "reference": [
        "api", "endpoint", "parameter", "field", "attribute", "schema",
        "definition", "reference", "specification", "format", "type",
        "request", "response", "payload", "data structure", "class",
        "method", "function", "property", "constant", "enum"
    ],
    "conceptual": [
        "concept", "principle", "pattern", "architecture", "design",
        "theory", "explain", "understand", "overview", "introduction",
        "why", "when to use", "best practice", "approach", "strategy",
        "model", "framework", "paradigm"
    ],
    "troubleshooting": [
        "error", "problem", "issue", "troubleshoot", "debug", "fix",
        "solution", "resolve", "faq", "frequently asked", "common issue",
        "known", "limitation", "workaround", "failed", "failure",
        "crash", "break", "doesn't work", "not working"
    ]
}


def classify_intent(chunk: Dict[str, Any]) -> str:
    """
    Classify chunk intent based on content analysis.

    Returns one of: "procedural", "reference", "conceptual", "troubleshooting"
    """
    text = (chunk.get("text", "") + " " +
            chunk.get("heading", "") + " " +
            chunk.get("section_type", "")).lower()

    # Normalize text
    text = re.sub(r'[^\w\s]', ' ', text)

    # Count keyword matches per category
    scores = {}
    for intent_type, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[intent_type] = score

    # Determine primary intent by section_type first (override if high confidence)
    section_type = chunk.get("section_type", "").lower()

    # Override logic: if section_type gives us a strong signal
    if section_type == "how-to" or section_type == "procedural":
        if scores.get("procedural", 0) > 0:
            return "procedural"
    elif section_type == "reference" or section_type == "api":
        if scores.get("reference", 0) > 0:
            return "reference"
    elif section_type == "faq" or section_type == "troubleshooting":
        if scores.get("troubleshooting", 0) > 0:
            return "troubleshooting"

    # Return highest scoring intent, default to "conceptual"
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    return "conceptual"


def add_metadata_to_chunk(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add missing metadata fields to a chunk.
    Preserves all existing fields.
    """
    # Preserve existing metadata if present
    if "version" not in chunk:
        chunk["version"] = VERSION

    if "update_date" not in chunk:
        chunk["update_date"] = UPDATE_DATE

    # Handle intent: overwrite if it's not in the standard 4 categories
    # (some chunks have comma-separated intent fields that need fixing)
    existing_intent = chunk.get("intent", "")
    valid_intents = {"procedural", "reference", "conceptual", "troubleshooting"}

    if existing_intent not in valid_intents:
        # Classify based on content
        chunk["intent"] = classify_intent(chunk)

    if "audience_level" not in chunk:
        chunk["audience_level"] = DEFAULT_AUDIENCE_LEVEL

    return chunk


def validate_chunk(chunk: Dict[str, Any]) -> bool:
    """Validate that chunk has all required metadata fields."""
    required_fields = ["version", "update_date", "intent", "audience_level"]
    for field in required_fields:
        if field not in chunk:
            return False
        if field == "intent" and chunk[field] not in ["procedural", "reference", "conceptual", "troubleshooting"]:
            return False
        if field == "audience_level" and chunk[field] not in ["beginner", "intermediate", "advanced"]:
            return False
    return True


def process_chunks() -> Dict[str, Any]:
    """
    Main processing function.
    Reads chunks, adds metadata, writes output, generates report.
    """
    print(f"[INFO] Reading chunks from {KB_CHUNKS_PATH}")

    if not KB_CHUNKS_PATH.exists():
        raise FileNotFoundError(f"KB chunks file not found: {KB_CHUNKS_PATH}")

    chunks_processed = 0
    chunks_metadata_added = 0
    intent_distribution = {
        "procedural": 0,
        "reference": 0,
        "conceptual": 0,
        "troubleshooting": 0
    }
    validation_failures = []

    # Use temporary file to avoid overwriting input while reading
    temp_fd, temp_path = tempfile.mkstemp(suffix='.jsonl', text=True)
    os.close(temp_fd)  # Close the file descriptor, we'll open it properly

    try:
        # Read, enrich, and write chunks
        with open(KB_CHUNKS_PATH, 'r') as infile, open(temp_path, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                try:
                    chunk = json.loads(line.strip())
                    original_chunk = chunk.copy()

                    # Add metadata
                    chunk = add_metadata_to_chunk(chunk)
                    chunks_processed += 1

                    # Track what was added
                    if chunk != original_chunk:
                        chunks_metadata_added += 1

                    # Track intent distribution
                    intent_distribution[chunk["intent"]] += 1

                    # Validate
                    if not validate_chunk(chunk):
                        validation_failures.append(line_num)

                    # Write enriched chunk
                    outfile.write(json.dumps(chunk) + '\n')

                    # Progress indicator
                    if chunks_processed % 1000 == 0:
                        print(f"[PROGRESS] Processed {chunks_processed} chunks...")

                except json.JSONDecodeError as e:
                    print(f"[ERROR] Failed to parse JSON on line {line_num}: {e}", file=sys.stderr)
                    raise
                except Exception as e:
                    print(f"[ERROR] Error processing line {line_num}: {e}", file=sys.stderr)
                    raise

        # Move temp file to output
        shutil.move(temp_path, str(OUTPUT_PATH))
        print(f"[INFO] Output written to {OUTPUT_PATH}")

    except Exception as e:
        # Clean up temp file on error
        if Path(temp_path).exists():
            Path(temp_path).unlink()
        raise

    print(f"[INFO] Processed {chunks_processed} chunks")
    print(f"[INFO] Metadata added to {chunks_metadata_added} chunks")

    # Generate report
    if chunks_processed == 0:
        raise ValueError("No chunks were processed. The input file may be empty.")

    report = {
        "timestamp": datetime.now().isoformat(),
        "chunks_processed": chunks_processed,
        "chunks_metadata_added": chunks_metadata_added,
        "metadata_fields_added": 4,  # version, update_date, intent, audience_level
        "intent_distribution": {
            intent: {
                "count": count,
                "percentage": round((count / chunks_processed) * 100, 2)
            }
            for intent, count in intent_distribution.items()
        },
        "validation_failures": len(validation_failures),
        "validation_failure_line_numbers": validation_failures[:100],  # First 100 for debugging
        "version": VERSION,
        "update_date": UPDATE_DATE
    }

    # Write report
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"[SUCCESS] Report written to {REPORT_PATH}")

    # Print summary
    print("\n" + "="*60)
    print("METADATA ENRICHMENT SUMMARY")
    print("="*60)
    print(f"Total chunks processed: {chunks_processed}")
    print(f"Chunks modified: {chunks_metadata_added}")
    print(f"Metadata fields added: 4")
    print("\nIntent Distribution:")
    for intent, data in report["intent_distribution"].items():
        print(f"  {intent}: {data['count']} ({data['percentage']}%)")
    print(f"\nValidation failures: {len(validation_failures)}")
    if validation_failures:
        print(f"  Lines: {validation_failures[:10]}")
    print("="*60)

    return report


if __name__ == "__main__":
    try:
        report = process_chunks()
        print(f"\n[SUCCESS] Metadata addition complete!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL] {e}", file=sys.stderr)
        sys.exit(1)
