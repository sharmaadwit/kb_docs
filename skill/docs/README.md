# product_introduction_kb

## Quickstart

1. Put your Markdown files in `kb/`.
2. Run `kb_ingest(force_rebuild=true)`.
3. Test retrieval with `kb_search(query=..., top_k=5)`.
4. Use `kb_answer(query=..., top_k=5)`.

## Tips for best results

- Ensure each file has an H1 title (`# ...`).
- Ensure headings are on their own line (the ingester also auto-fixes inline headings like `... ## Heading`).
- Prefer meaningful H2/H3 headings; retrieval is boosted by heading path + filename.
