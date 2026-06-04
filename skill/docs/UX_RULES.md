# UX Response Rule (KB)

## Rule
When generating end-user responses, **never mention internal tooling or infrastructure**.

### Do not mention (non-exhaustive)
- github, git
- repo, repository
- branch, main
- api.github.com
- token, authentication headers
- file paths like `kb/kb_index.json` or `kb/analytics/kb_usage.ndjson`
- action names like `github_kb_answer`, `github_kb_search`
- trace IDs, observation IDs, span IDs
- tool-call narration such as "Read skill documentation" or "Ran github kb answer"

## Allowed
- "Knowledge Base"
- "Docs" / "documentation"
- "Sources" / "citations"
- "I found this in the product docs"
- Product walkthrough video links (public YouTube watch URLs) returned by the KB
  tools — these are user-facing content, not internal URLs, and must be shown.

## Rendering policy
- End users should only see the final answer.
- Tool execution details belong in logs/debug panels only.
- Debug metadata must never be appended to the visible answer body.
- If traceability is needed, expose it only in a separate developer/debug UI, not in the chat transcript.

## Rationale
Keeps user experience product-first while allowing engineering to keep implementation details in logs.

## Video links

KB tools (`kb_answer` / `kb_search`) may return one or more videos. The answer
text already ends with correctly formatted, clickable links:

  - One video → **Watch:** [<Video Title>](<https://www.youtube.com/watch?v=...>)
  - Several videos (broad / overview / "what can Gupshup do" pitch) → a
    **Videos:** list with one `- [<Title>](<URL>)` bullet per video.

plus a structured `videos` list (and a `video` field for the primary one):
`{ url, title, video_id, start, end, source }`.

### Rules
- Always show EVERY video the KB tools return on the current turn. Never hide,
  suppress, or keep only the first when several are returned.
- Surface them proactively — do not wait for the user to ask "show me videos."
  If a product/demo/capability answer came from a KB tool that attached videos,
  include them in that first answer.
- Render each video as a clickable markdown link: [Title](URL). Never show the
  raw URL as visible text, and never output `Title — https://...`.
- If you synthesize one answer from several tool calls this turn, include the
  relevant video link(s) those calls returned (deduplicated), placed at the end.
- Do not reuse videos from earlier turns, and do not pad with unrelated videos.
- If no tool returned a video this turn, simply omit any video section. Do NOT
  say "I don't have videos" or narrate the absence — just give the answer.
- Do not alter the URL. Keep all query params exactly as returned
  (`t=`, `cc_load_policy`, `cc_lang_pref`, `hl`).

### Note
On WhatsApp, anchor-text links are not supported — the raw URL always shows and
is tappable. Apply the markdown-link form only on surfaces that support it.

## Product naming: SuperAgent vs Gupshup Console

These are two different products. Never merge them into one item (e.g.
"SuperAgent / Console") or swap their videos.

- **SuperAgent** — the AI agent builder (create agents, skills, recipes,
  integrations, scheduled tasks, browser control). Overview video: `bGCS4rp84EM`.
- **Gupshup Console** — the platform shell: projects, modules, org/members,
  the base operating layer. Overview video: `qV43fub35f8`.

When the question is about SuperAgent, use SuperAgent docs and the SuperAgent
video. When it's about Console/projects/modules, use Console docs and the
Console video.
