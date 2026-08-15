#!/usr/bin/env python3
"""Test kb_ingest with increased timeout to verify the fix.

This script validates that kb_ingest can process all chunks without timing out,
by calling the fixed version and checking the results.
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

from kb_ingest import kb_ingest  # noqa: E402


class MockContext:
    """Mock context for testing kb_ingest locally."""

    def __init__(self):
        self.secrets = {
            "KB_GIT_PROVIDER": "github",
            "KB_REPO": "sharmaadwit/kb_docs",
            "KB_BRANCH": "main",
            "GITHUB_TOKEN": "",  # Will use unauthenticated access
            "GITHUB_DOCS_PATH": "kb",
            "GITHUB_KB_CHUNKS_PATH": "kb/kb_chunks.jsonl",
            "GITHUB_KB_INDEX_PATH": "kb/kb_index.json",
        }

    def get_secret(self, name):
        return self.secrets.get(name)


def main():
    print("Testing kb_ingest with increased timeout fix...")
    print("-" * 60)

    context = MockContext()
    start = time.time()

    try:
        result = kb_ingest(context=context)
        elapsed = time.time() - start

        # Print results
        print(f"\nIngestion completed in {elapsed:.1f} seconds")
        print(f"Status: {'✓ SUCCESS' if result.get('ok') else '✗ FAILED'}")

        if result.get('ok'):
            print(f"\nMetrics:")
            print(f"  - Files scanned: {result.get('files_scanned', 0)}")
            print(f"  - Total chunks generated: {result.get('chunks_generated', 0)}")
            print(f"  - Chunks written locally: {result.get('chunks_written', False)}")
            print(f"  - Excluded paths: {result.get('excluded', [])}")

            # Check if chunks were written
            if result.get('chunks_written'):
                written_paths = result.get('written_paths', {})
                print(f"\nWritten files:")
                for key, path in written_paths.items():
                    if path:
                        print(f"  - {key}: {path}")
            else:
                if result.get('write_error'):
                    print(f"\nWrite error: {result.get('write_error')}")

            # Print note
            if result.get('note'):
                print(f"\nNote: {result.get('note')}")

            return 0
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 1

    except Exception as e:
        elapsed = time.time() - start
        print(f"\n✗ FAILED after {elapsed:.1f} seconds")
        print(f"Exception: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
