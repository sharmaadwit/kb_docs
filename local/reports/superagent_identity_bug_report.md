# Investigation Log: Missing/placeholder user identity on SuperAgent-routed `kb_answer` traces

## ROOT CAUSE CONFIRMED (2026-07-29)
**This was never a code bug.** Confirmed directly by the VAPT (security) team: SuperAgent's PII handling rules were tightened, and the placeholder-substitution behavior documented below (real identity present at every calling frontend, replaced with generic strings like `"anon"`/`"anonymous"` before reaching the skill) is that policy working as intended — a shared PII-scrubbing layer stripping real user identity before it reaches downstream skills, consistent across every independent frontend surface tested.

The investigation below (kept for reference) independently and correctly localized the behavior to a shared backend layer rather than any individual frontend or `kb_answer.py` itself — that conclusion holds, it's just policy, not a defect.

## Practical impact
Until an approved, PII-policy-compliant way to carry a distinct-but-non-PII user identifier through this pipeline is found, per-user attribution (real emails) is not recoverable from `kb_answer` traces for traffic going through the affected paths — the sales-facing external-user/leads table in the analytics dashboard is not usable for these segments until that's resolved.

## Original summary (superseded by the confirmed root cause above)
For SuperAgent chat sessions authenticated via a `localStorage`-stored JWT (`auth_token`) — the path used by non-`@gupshup.io` / external logins (e.g. Gmail sign-in) — the frontend never attaches that identity to the `POST /api/chat/stream` request. No `Authorization` header, no cookie, no `user_email_id` field in the body. As a result, every downstream skill invocation (including `gupshup_guide` / `kb_answer`) receives no real identity for these users and falls back to a shared placeholder account.

## Evidence

### 1. Working case — `@gupshup.io` login (cookie-based session)
Captured via browser HAR from `superagent.gupshup.ai/chat/162463`, logged in with an `@gupshup.io` account.

- `sa_session` cookie is present and automatically attached to `/api/chat/stream` by the browser.
- Decoded JWT payload: `{"user_id": 43, "email": "adwit.sharma@gupshup.io", "purpose": "access", ...}`
- Request body: `{"message": ..., "session_id": ..., "stream_id": ..., "conversation_id": 162463, ...}` — no explicit `user_email_id`, but identity is available server-side via the cookie.
- Result: traces downstream carry the correct real email.

### 2. Broken case — external Gmail login (JWT-in-localStorage session)
Captured via browser HAR from `superagent.gupshup.ai/chat/162475`, logged in with a personal Gmail account.

- `localStorage` for `https://superagent.gupshup.ai` contains a key `auth_token` holding a JWT, plus other keys clearly scoped to this specific user (e.g. `ai_studio_tour_seen_148`, `ai_studio_feature_launch_web_search_v1_148`) — confirming the frontend has resolved a real, specific user id (**148**) for this session.
- **No cookie is ever sent or set** for `superagent.gupshup.ai` anywhere in this session's HAR (checked across all requests — `cookies` array is empty everywhere, and no `Set-Cookie` response headers appear).
- **`POST /api/chat/stream` full header list** (verified, no `Authorization` header present):
  ```
  :authority, :method, :path, :scheme, accept, accept-encoding,
  accept-language, content-length, content-type, dnt, origin, priority,
  referer, sec-ch-ua, sec-ch-ua-mobile, sec-ch-ua-platform, sec-fetch-dest,
  sec-fetch-mode, sec-fetch-site, user-agent
  ```
- **Request body:**
  ```json
  {
    "message": "how to add templates on console",
    "session_id": "afc5c3e8-c453-4cca-a4c7-5dc38be804ac",
    "stream_id": "aaf5d7e6-09b3-471b-8df0-fadeb7f0811f",
    "browser_mode": "off",
    "enable_skill_creator_tools": false,
    "enable_dashboard_tools": false,
    "enable_web_search": false
  }
  ```
  No `user_email_id`, no `user_id`, no reference to `148` anywhere.
- A separate request, `GET /api/conversations/user/148?conversation_type=chat&limit=50&exclude_agent_chats=true`, proves the frontend *does* know the user's real id (148) elsewhere in the app — it's simply never carried into the chat-send call.

### 3. Downstream confirmation (Langfuse / `kb_answer` telemetry)
Traces on `trace_env=PROD_EXT` (Standalone-only environment, per product definition — no CC Express traffic) show a recurring pattern: callers with no real email, only a shared/generic `user_id=30` and (once instrumented) `executing_user_id=30` in the raw params delivered to the skill. This is consistent with many distinct external users (like the Gmail-login case above, id 148) all collapsing into one shared fallback identity once their real identity is dropped before it ever reaches the skill layer.

`kb_answer.py`'s identity-extraction logic was independently audited and confirmed to check every plausible parameter name (`user_email`, `userEmail`, `user_email_id`, `userEmailId`, `email`, `email_id`, `session_id`, `sessionId`, `user_id`, `userId`, `executing_user_id`, nested `params["parameters"]`, and relevant `context` attributes) — the skill has nothing left to extract because nothing is being sent.

## Root cause
Frontend bug in SuperAgent's own chat web app (branded internally as "ai_studio", per `localStorage` key prefixes). The chat-send code path only forwards identity for cookie-based (`sa_session`) sessions. For JWT-in-localStorage sessions (external/Gmail logins), the `auth_token` is read and used elsewhere in the app (e.g. building user-scoped URLs) but is never attached to `/api/chat/stream` — neither as an `Authorization: Bearer <auth_token>` header nor as a `user_email_id`/`user_id` body field.

## Suggested fix
On the SuperAgent frontend, attach `Authorization: Bearer {auth_token}` (or extract and pass the resolved user id/email explicitly in the request body) to `/api/chat/stream` whenever a JWT-based session is active — mirroring what already happens automatically for cookie-based (`sa_session`) sessions.

## Scope / impact
Affects all external (non-cookie-session) SuperAgent users across every skill invocation from this chat surface, not just `gupshup_guide`/`kb_answer` — any skill relying on caller identity for personalization, attribution, or analytics is equally affected.

## Addendum: a related, separate bug on the CC Express (Concierge) widget path

CC Express is anonymous by design (no login) — this is expected and correct. The relevant identity signal for this surface is `session_id`, not email.

### Evidence
Browser HAR from `concierge.gupshup.io`, using the public (no-login) CC Express widget:

- `POST https://concierge.gupshup.io/api/chat` body:
  ```json
  {
    "session_id": "9fdd6339-f218-40a3-ae86-367223c0a6fc",
    "message": "how to add templates for whatsapp"
  }
  ```
  The widget correctly generates and sends a real, distinct per-visitor `session_id` (a genuine UUID). No cookies/auth headers — expected, since there's no login.

### Downstream confirmation (Langfuse / `kb_answer` telemetry, `trace_env=PROD`, 1-day window)
- 36 of 40 CC Express traces carry **no identity at all** — `session_id` never reaches the skill.
- The remaining 3 do get a `session_id`-derived identity, but the value used is the **literal placeholder string `"anonymous"`** (e.g. `sess:anonymous@ccexpress.gupshup.io`), not the real per-visitor UUID the widget actually sent. Every visitor on this path collapses into one shared identity either way.

### Root cause
A **separate** bug from the SuperAgent-frontend one above — this is a backend/bridging issue on the `concierge.gupshup.io` → SuperAgent → skill path. The widget does its job correctly (sends a real UUID); something in Concierge's backend either drops it or substitutes a hardcoded `"anonymous"` placeholder before the request reaches SuperAgent's `execute_action` call for `kb_answer`. This matches (and sharpens) an existing code comment in `kb_answer.py` dating to a prior investigation: *"Concierge... doesn't forward session_id."*

### Suggested fix
On Concierge's backend, forward the real `session_id` value from the widget's `/api/chat` request through to the SuperAgent skill invocation unchanged, instead of dropping it or substituting a placeholder.

## Strongest evidence: real identity sent correctly, still overwritten with a hardcoded placeholder in-flight

This is the most conclusive finding across the whole investigation — it proves data loss/substitution happens in a shared backend pipeline, not at the source, and not in `kb_answer.py`.

### Setup
A third, distinct integration surface: `console.gupshup.io` (CC Express, logged in) → `POST https://plgapi.gupshup.io/api/gupshup-ai-chat` (a "PLG" API gateway, separate from both `superagent.gupshup.ai` and `concierge.gupshup.io`).

### Request (browser HAR, `ccx2_console.gupshup.io.har`)
```json
{
  "message": "@gupshup_guide show me how to add templates",
  "session_id": "1785343745647-29cenju2za3",
  "email_id": "plg@mailinator.com",
  "tenant_context": {"org_id": "31257006", "project_id": "31583675"},
  "apiKey": "..."
}
```
Both a real, correct `email_id` and a real, correct `session_id` are present — `email_id` is exactly one of the key names `kb_answer.py` already checks.

### What the skill actually received (Langfuse trace `kb-kb_answer-dbeebd92f3c046af`, 2026-07-29T16:52:23Z — timestamp matches the request 36s prior)
```
trace_env: PROD_EXT
user_email: sess:anon@ccexpress.gupshup.io
identity_source: session_id
```
Neither the real email nor the real session_id reached the skill. Instead, a third variant of the same hardcoded placeholder pattern (`"anon"`, alongside `"anonymous"` / `"anonymous-session"` seen on the Concierge path) was substituted in transit.

### Conclusion
This closes the investigation definitively:
- `kb_answer.py`'s extraction logic is proven correct — it looks for exactly the fields that were sent (`email_id`, `session_id`) and would have used them if they'd arrived.
- Real identity data provably existed in the request and was provably replaced with a generic placeholder before the skill ever saw it.
- The same placeholder-substitution signature appears across at least two independent integration surfaces (Concierge and this PLG/Console-embedded one), strongly suggesting a **shared piece of SuperAgent backend/bridging logic** — likely wherever `execute_action` assembles the skill call for any non-cookie-authenticated session — that substitutes a generic anonymous identity regardless of what the calling application actually sent.

### Suggested fix
Locate the shared backend code path in SuperAgent that constructs the `execute_action` call to skills for non-`sa_session`-cookie traffic, and stop it from discarding/overwriting `email_id`/`session_id`/equivalent fields that were present in the original request. Given the identical placeholder-substitution symptom across independent surfaces, this is very likely a single shared bug, not several unrelated ones — fixing it in one place should resolve identity attribution for CC Express, Concierge, and PLG/Console-embedded traffic simultaneously.
