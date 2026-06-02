# kb_docs

Dev/working repo for the Gupshup KB skill. Files are organized into three zones by where they run.

## Zones

### `skill/` — deployable Gupshup skill functions (source of truth for deploy)
These are the editable functions in the Gupshup skill. Each is a standalone tool with a
`def <name>(parameters, context)` entrypoint; secrets are read via `context.get_secret(...)`.

| File | Skill function |
|------|----------------|
| `skill/kb_answer.py` | `kb_answer` — grounded answer + citations (the answer the user sees) |
| `skill/kb_search.py` | `kb_search` — ranked KB search results |
| `skill/kb_ingest.py` | `kb_ingest` — chunk markdown docs into the content repo |
| `skill/kb_analytics.py` | `kb_analytics` — append usage analytics |

`SKILL.md` and `docs/` live only in the deployed skill (gitignored here).

Note: the deployed skill keeps these files at its root. When syncing, upload the contents
of `skill/` to the skill root.

### `kb/` — content mirror
Reference mirror of the separate prod content repo (`GITHUB_REPO=product-introduction-kb`):
markdown docs, `kb_chunks.jsonl`, `kb_index.json`, manifests. At request time the skill
fetches content from the content repo over the network, not from this folder.

### `local/` — never deployed (Cursor/dev only)
| Path | Purpose |
|------|---------|
| `local/runtime_mirror/kb_answer_runtime.py` | Read-only local mirror of the non-editable Gupshup system runtime (gitignored) |
| `local/tests/` | Regression and smoke tests; repointed to import from `skill/` |
| `local/patches/` | Patch notes / instructions history |
| `local/scripts/` | One-off dev scripts |
| `local/raw/` | Source PDFs and event exports (gitignored) |

## Running tests
Run from the repo root (tests read `kb/...` relative paths and import from `skill/`):

```bash
python local/tests/test_regression.py
```
