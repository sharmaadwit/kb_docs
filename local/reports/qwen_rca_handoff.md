# Investigation Handoff: Missing User Identity in `kb_answer` Skill Traces

## Purpose of this document
This is a raw-evidence handoff for an independent root-cause analysis. Please do your own reasoning from the evidence below — do not assume any conclusion has already been reached. State your own hypothesis, what evidence supports/contradicts it, and what you'd want to test next if anything is still ambiguous.

## System overview
- `gupshup_guide` is a "skill" (a KB-answering action, `kb_answer`) registered with an orchestration platform called SuperAgent.
- SuperAgent exposes multiple chat-style frontends/integrations that all eventually route a user's message to `kb_answer` via an internal `execute_action` tool call, when the query looks like a documentation question.
- `kb_answer(parameters, context)` receives a `parameters` dict (called `params` below) and an opaque `context` object from the runtime. It must resolve a caller identity (ideally a real email) from whatever is in `params`/`context`, for telemetry/analytics attribution.
- The known, distinct front-end surfaces that call into this skill (via SuperAgent) are:
  1. `superagent.gupshup.ai` — SuperAgent's own hosted chat UI. Internal `@gupshup.io` staff log in here via a cookie (`sa_session`, a JWT). External/Gmail users log in here via a JWT stored in browser `localStorage` (key `auth_token`) instead of a cookie.
  2. `concierge.gupshup.io` — a separate, anonymous (no-login) chat widget product ("CC Express").
  3. `plgapi.gupshup.io` (called from `console.gupshup.io`) — a third integration, "CC Express" embedded inside the Console product, which does have a login.

## The code under investigation
This is the full identity-resolution function in the skill (`skill/kb_answer.py`), unmodified reasoning-relevant excerpt:

```python
def _langfuse_user_context(
    context, params: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[str], Dict[str, Any]]:
    params = params or {}
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    user_id_val: Any = None

    # SuperAgent sometimes nests the original skill-call args under a
    # "parameters" key instead of flattening them into the top-level params
    # dict. Resolve it once (coercing a JSON string if needed).
    _nested_parameters = params.get("parameters") if isinstance(params, dict) else None
    if isinstance(_nested_parameters, str):
        try:
            _nested_parameters = json.loads(_nested_parameters)
        except Exception:
            _nested_parameters = None
    if not isinstance(_nested_parameters, dict):
        _nested_parameters = None

    def _pick(keys):
        for key in keys:
            v = params.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        if _nested_parameters:
            for key in keys:
                v = _nested_parameters.get(key)
                if isinstance(v, str) and v.strip():
                    return v.strip()
        return None

    # Extract email: check all variants SuperAgent might send
    user_email = _pick(("user_email", "userEmail", "user_email_id", "userEmailId", "email", "email_id"))
    user_name = _pick(("user_name", "userName"))
    for key in ("user_id", "userId"):
        if key in params and params.get(key) is not None:
            user_id_val = params.get(key)
            break
    if user_id_val is None and _nested_parameters:
        for key in ("user_id", "userId"):
            if key in _nested_parameters and _nested_parameters.get(key) is not None:
                user_id_val = _nested_parameters.get(key)
                break

    if context is not None:
        if not user_email:
            for attr in ("user_email", "userEmail", "user_email_id", "userEmailId", "email"):
                em = getattr(context, attr, None)
                if isinstance(em, str) and em.strip():
                    user_email = em.strip()
                    break
        if not user_name:
            nm = getattr(context, "user_name", None)
            if isinstance(nm, str) and nm.strip():
                user_name = nm.strip()
        if user_id_val is None:
            user_id_val = getattr(context, "user_id", None)

    # Fallback: synthesize identity from session_id if no email resolved
    synthesized_session_identity = False
    if not user_email:
        session_id = params.get("session_id") or params.get("sessionId")
        if not session_id and _nested_parameters:
            session_id = _nested_parameters.get("session_id") or _nested_parameters.get("sessionId")
        if not session_id and isinstance(params, dict):
            for container_key in ("metadata", "context", "tenant_context", "user"):
                container = params.get(container_key)
                if isinstance(container, dict):
                    session_id = container.get("session_id") or container.get("sessionId")
                    if session_id:
                        break
        if not session_id and context is not None:
            session_id = getattr(context, "session_id", None) or getattr(context, "sessionId", None)
        if isinstance(session_id, str) and session_id.strip():
            user_email = f"sess:{session_id.strip()}@ccexpress.gupshup.io"
            synthesized_session_identity = True

    # Fallback: synthesize identity from executing_user_id if still nothing
    synthesized_executing_user_identity = False
    if not user_email:
        executing_user_id = params.get("executing_user_id") or params.get("executingUserId")
        if not executing_user_id and _nested_parameters:
            executing_user_id = _nested_parameters.get("executing_user_id") or _nested_parameters.get("executingUserId")
        if not executing_user_id and isinstance(params, dict):
            for container_key in ("metadata", "context", "tenant_context", "user"):
                container = params.get(container_key)
                if isinstance(container, dict):
                    executing_user_id = container.get("executing_user_id") or container.get("executingUserId")
                    if executing_user_id:
                        break
        if not executing_user_id and context is not None:
            executing_user_id = getattr(context, "executing_user_id", None) or getattr(context, "executingUserId", None)
        if isinstance(executing_user_id, (str, int)) and str(executing_user_id).strip():
            user_email = f"exec:{str(executing_user_id).strip()}@ccexpress.gupshup.io"
            synthesized_executing_user_identity = True

    # (function continues: falls back further to a shared acct:{user_id}:{name}
    # identity if user_id_val is set but nothing else resolved; returns
    # (trace_user_id, meta_dict) where meta_dict includes user_email,
    # user_name, user_id, and identity_source when a fallback fired.)
```

## Raw evidence (4 independently captured cases)

For each case: (a) what the calling browser/application actually sent over the network (captured via browser DevTools → Network tab → HAR export), and (b) what showed up in the corresponding backend telemetry trace for the `kb_answer` skill invocation shortly afterward.

### Case A — `superagent.gupshup.ai`, cookie-based login (`@gupshup.io` staff account)
**Sent (cookie, automatically attached by browser):**
```json
// sa_session cookie, JWT payload:
{"user_id": 43, "exp": 1785345527, "iat": 1785302327, "purpose": "access", "email": "adwit.sharma@gupshup.io"}
```
**Sent (POST /api/chat/stream body):**
```json
{"message": "...", "session_id": "...", "stream_id": "...", "conversation_id": 162463, "browser_mode": "off", "enable_skill_creator_tools": false, "enable_dashboard_tools": false, "enable_web_search": false}
```
(No explicit `user_email_id` in the body — identity is only in the cookie.)

**Resulting telemetry:** correct, real email attributed (`adwit.sharma@gupshup.io`).

### Case B — `superagent.gupshup.ai`, JWT-in-localStorage login (external Gmail account)
**`localStorage` for this origin contains** (confirmed via DevTools → Application → Local Storage):
```
auth_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNDgs... (JWT, not decoded)
ai_studio_tour_seen_148: 1
ai_studio_feature_launch_web_search_v1_148: snoozed
ai_studio_current_conversation: 162475
(no sa_session cookie exists for this session)
```
**Sent (POST /api/chat/stream — full request, verified header list, no Authorization/cookie header present):**
```
Headers present: :authority, :method, :path, :scheme, accept, accept-encoding,
accept-language, content-length, content-type, dnt, origin, priority, referer,
sec-ch-ua, sec-ch-ua-mobile, sec-ch-ua-platform, sec-fetch-dest, sec-fetch-mode,
sec-fetch-site, user-agent   [no Authorization header]

Cookies attached: none

Body:
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
A separate request in the same session, `GET /api/conversations/user/148?conversation_type=chat&limit=50&exclude_agent_chats=true`, was also observed — also with no cookie and no Authorization header on it either.

**Resulting telemetry:** no real email; falls back to a shared/generic identity.

### Case C — `concierge.gupshup.io` (CC Express widget, no login by design)
**Sent (POST /api/chat body, no cookies, no auth headers — expected, no login exists on this surface):**
```json
{
  "session_id": "9fdd6339-f218-40a3-ae86-367223c0a6fc",
  "message": "how to add templates for whatsapp"
}
```
**Resulting telemetry (aggregated over a 1-day sample of ~40 traces on this surface):**
- 36/40 traces: no identity resolved at all (no `session_id`-derived fallback triggered).
- 4/40 traces: `session_id`-derived fallback DID trigger, but using the literal string values `"anonymous"` or `"anonymous-session"` — not any real UUID like the one actually sent in the example above.

### Case D — `console.gupshup.io` → `plgapi.gupshup.io` (CC Express embedded in Console, logged in)
**Sent (POST /api/gupshup-ai-chat body, no cookies — auth via body fields + apiKey):**
```json
{
  "message": "@gupshup_guide show me how to add templates",
  "session_id": "1785343745647-29cenju2za3",
  "email_id": "plg@mailinator.com",
  "tenant_context": {"org_id": "31257006", "project_id": "31583675"},
  "apiKey": "4ripe43zxkpfg5sj1elrtj9s2kwk8zmz"
}
```
This request's SSE response stream shows it did call the `kb_answer` action (`execute_action` tool calls with label "Running kb answer" appear in the stream) — confirmed reaching the skill, not answered from the orchestrator's own knowledge.

**Resulting telemetry** (trace timestamped ~36 seconds after the request, same session_id era, matching query text about templates):
```
trace_env: PROD_EXT
user_email: sess:anon@ccexpress.gupshup.io
identity_source: session_id
```

## Questions for independent analysis

1. Based purely on the code and Case A/B, is the difference in outcome (real email vs. shared fallback) explainable by something in `_langfuse_user_context` itself, or does it require something outside this function (e.g., what the caller actually transmits)?

2. Case D is the most information-dense case. The request body contains a value (`"plg@mailinator.com"`) matching a key (`email_id`) that the code explicitly checks first in `_pick(...)`, and a `session_id` field the code also explicitly checks. Yet the resulting trace shows `sess:anon@ccexpress.gupshup.io` with `identity_source: session_id` — meaning the `session_id` fallback branch fired using the literal string `"anon"`, not the value `"1785343745647-29cenju2za3"` that was actually sent, and the `email_id` value was never used at all.
   - Can you construct any path through the `_langfuse_user_context` code above that would produce this exact output (`"anon"`, `session_id` fallback firing, real `email_id` ignored) from the literal input shown in Case D's request body? If not, what does that imply about where in the system this transformation is happening?

3. Cases C and D show two different literal placeholder strings (`"anonymous"`/`"anonymous-session"` in C, `"anon"` in D) being substituted for real session_id values across two different frontend surfaces (`concierge.gupshup.io` and `plgapi.gupshup.io`) that otherwise share no code with each other (different domains, different request shapes, different auth mechanisms). What's your hypothesis for why the same *category* of substitution (real value → generic placeholder) would appear independently on both?

4. Given all four cases, what do you conclude is the most likely location of the actual defect — front-end (each calling application), the skill (`kb_answer.py`), or some shared middle layer between the two (e.g. wherever SuperAgent's `execute_action` mechanism assembles the call to the skill)? What single additional piece of evidence (if any) would most decisively confirm or rule out your hypothesis?

5. Is there any alternative explanation for the pattern across all 4 cases that doesn't involve a shared backend bug — e.g., could this be explained by rate limiting, caching, a privacy/anonymization feature working as intended, or something else? If so, what evidence would distinguish that explanation from a bug?

Please answer in your own words based on the evidence, not by restating the setup. If you reach a confident conclusion, state it plainly along with your confidence level and what would change your mind.
