# Meta Business Agent API Reference

Engineering reference for **Meta's native Business Agent API** — the underlying API that Gupshup's own wrapper product mirrors. Do not confuse this with [[bizai-api-endpoints]], which documents Gupshup's own **BizAI for Partners** API (the Gupshup-branded surface partners integrate against). This doc covers Meta's endpoints directly, grouped by lifecycle stage as they're organized in Meta's own reference docs. Full request/response schemas live on Meta's developer site (`https://developers.facebook.com/documentation/meta-business-agent/reference/...`); this doc is an index, not a spec replacement.

All endpoints sit under `https://api.facebook.com/{entity_id}/...` (one exception noted below) and use `X-API-Version: "2.0.0"` (also one exception). `entity_id` is almost always the WhatsApp Business Phone Number ID for the Meta Business Agent — two endpoint groups deviate from this, flagged below.

## Auth summary

Most endpoint groups accept **any of**: capability `bizai_wa_enterprise_api_3p_access`, or permission `whatsapp_business_messaging`. All require `Authorization: Bearer {token}` (OAuth). See **Inconsistencies** at the end for the groups that differ.

---

## Onboard

### Agent Onboarding
`POST https://api.facebook.com/{entity_id}/agent_onboarding`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Triggers AI agent onboarding for a given entity and channel (`whatsapp`, `instagram`, `messenger`, etc., passed as a required `channel` query param). Creates the underlying entities and kicks off async data-preparation jobs; returns an `agent_id` for the new agent settings object. Source: `reference_onboard_agent-onboarding.md`.

### Agent Allowlist
`GET / POST /` and `DELETE /{entry_id}` at `https://api.facebook.com/{entity_id}/agent_config/allowlist`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Manages the list of consumer WhatsApp phone numbers (E.164) the agent is allowed to talk to. Used together with `ai_audience: ALLOWLISTED_ONLY` on agent settings to restrict the agent to a known set of testers/consumers before wider rollout. Source: `reference_onboard_agent-allowlist.md`.

### Agent Settings
`GET / PUT /` at `https://api.facebook.com/{entity_id}/agent_config/settings`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Gets or fully replaces the agent's core rollout configuration: `rollout.enabled` (on/off), `handoff` (human handoff message + trigger behavior), `followup` (inactivity follow-up messaging), `ai_audience` (`EVERYONE` vs `ALLOWLISTED_ONLY`), and `never_say_phrases`. PUT is a full replace — disabling the agent stops it responding on all threads; re-enabling only makes it pick up new threads, not resume old ones. Accepts an optional `agent_id` query param to target a specific agent config. Source: `reference_onboard_agent-settings.md`.

*Note: `reference_onboard_agent-eligibility.md` exists in the source tree under this same "onboard" grouping but was not provided as a source file for this doc — see Inconsistencies/gaps below.*

---

## Configure

### Agent Budget
`GET / POST /` at `https://api.facebook.com/{entity_id}/agent_budget`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `business_management` **(differs from every other group — see Inconsistencies)**.
Reads or fully replaces token-usage budget caps for the agent. Each budget pairs a `time_window` (`one_day`/`seven_days`/`fourteen_days`/`thirty_days`) with a `max_budget` (tokens); an empty `budgets` array means unlimited usage. POST replaces the *entire* set — omitted budgets are removed. **`entity_id` here is the Business Manager ID (integer), not the WhatsApp Business Phone Number ID** used by nearly every other endpoint group. Source: `reference_configure_agent-budget.md`.

### Agent Knowledge — Business Info
`GET / PUT / DELETE /` at `https://api.facebook.com/{entity_id}/agent_config/business_info`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Stores structured business facts the agent draws on: payment methods, return policy, purchase info, delivery/shipping, a general business description, and contact info (email, hours, address). PUT is a full replace; DELETE resets to empty defaults. Source: `reference_configure_agent-knowledge-business-info.md`.

### Agent Knowledge — FAQs
Full CRUD (`GET`/`POST`/`PUT`/`DELETE`, list and by-id) at `https://api.facebook.com/{entity_id}/agent_config/faq`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Manages individual question/answer knowledge entries, each independently retrievable by the agent — answers should be self-contained since the agent doesn't chain FAQ entries together. Supports arbitrary string `metadata` per entry. Source: `reference_configure_agent-knowledge-faqs.md`.

### Agent Knowledge — Files
`GET`/`POST` (list/upload) and `GET`/`DELETE` by id at `https://api.facebook.com/{entity_id}/agent_config/files`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Uploads (multipart/form-data) documents into the agent's knowledge base — PDF, DOC/DOCX, PNG/JPG/JPEG, and conditionally CSV/XLSX when extraction is enabled for the WhatsApp asset. Max file size 100,000,000 bytes. No update endpoint; re-upload to replace. Source: `reference_configure_agent-knowledge-files.md`.

### Agent Knowledge — Websites
Full CRUD at `https://api.facebook.com/{entity_id}/agent_config/websites`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Registers URLs for the agent to crawl and ingest into its knowledge base; entries report `crawl_status`, `pages_crawled`, and `last_crawled_at`. Source: `reference_configure_agent-knowledge-websites.md`.

### Agent Skills
Full CRUD at `https://api.facebook.com/{entity_id}/agent_config/skills`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Defines free-text behavioral instructions ("skills") that tell the agent what to do and when — each skill has a `title`, a `description` (the trigger condition), and the `skill` body (the actual instructions, up to 20,000 chars). Conflicting skills that both claim priority for the same trigger are not resolved automatically and can produce inconsistent responses. `GET`/`POST` accept an optional `agent_id` query param. Source: `reference_configure_agent-skills.md`.

### Connectors
Full CRUD plus `GET /{connector_id}/logs` and credential-upsert actions (`upsertApiKey`, `upsertCertificate`, `upsertOAuth`) at `https://api.facebook.com/{entity_id}/agent_connectors`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Registers third-party API integrations the agent can call: base URL, auth type (`OAUTH2_CLIENT_CREDENTIALS`, `API_KEY`, or `NONE` currently supported; `OAUTH2`/`BASIC`/`CUSTOM` reserved), optional mTLS certificate, and optional user-auth token injection config. The `/logs` endpoint returns per-connector error logs (last 7 days only, max 7-day window per query) either as individual entries or, with `summary_only=true`, aggregated failure patterns with optional success-rate/latency stats. Source: `reference_configure_connectors.md`.

### Connector Tools
Full CRUD plus `POST /{tool_id}/run` at `https://api.facebook.com/{entity_id}/agent_connectors/{connector_id}/tools`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Defines individual callable actions (tools) under a connector: HTTP method/path/params/body schema for the outbound request, whether the call requires injected user auth, and (for login/refresh-type tools) how to extract tokens from the response. `POST /{tool_id}/run` executes the tool directly and returns the raw upstream response — useful for testing a tool definition outside a live conversation. Source: `reference_configure_connector-tools.md`.

### UI Skills
Full CRUD at `https://api.facebook.com/{entity_id}/agent-ui-skills`
Auth: permission `whatsapp_business_messaging` only — **no capability alternative listed (see Inconsistencies)**.
Configures rich, structured WhatsApp message types (`carousel_quick_reply`, `carousel_url`, `cta_url`, `flow`, `image`, `interactive_list`, `location`, `location_request`) the agent can send, each gated by an `instruction` describing when to use it. Flow-type skills require a `flow_id` and can't be enabled until the referenced flow is published. List endpoint is cursor-paginated (`before`/`after`/`limit`). Source: `reference_configure_ui-skills.md`.

---

## Operate

### Agent Eval
`GET /cases`, `GET /details`, `GET /summary`, `GET /run`, `POST /run` at `https://api.facebook.com/{entity_id}/agent-eval`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Runs offline evaluation of the agent against predefined scenarios. `POST /run` submits a combo job (simulation + evaluation + optional insights) across one or more `eval_case_ids` and returns a `job_id`; `GET /run` polls job status/progress/result. `GET /cases` lists configured eval scenarios (with `success_criteria` and `max_turns`); `GET /details` and `GET /summary` fetch per-conversation results and aggregated insight reports respectively, both by comma-separated ID lists. Source: `reference_operate_agent-eval.md`.

### Agent Event
`POST /` and `GET /{agent_event_id}` at `https://api.facebook.com/{entity_id}/agent_event`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Lets a partner system push an asynchronous, partner-defined event (e.g. `document_verified`, `payment_received`) into a specific consumer's conversation context — `to` (consumer phone), and an `event` object with `type`, `description`, and an opaque JSON `payload` (max 4096 chars). POST returns immediately with `status: accepted`; GET polls the event's processing status (`request_received` → `processing` → `sent`/`success`/`skipped`/`failed`). Source: `reference_operate_agent-event.md`.

### Agent Test
`POST /` at `https://api.facebook.com/{entity_id}/agent_test`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Sends a single test message through the full agent pipeline without needing a real consumer phone number — useful for interactive debugging during configuration. Pass `conversation_id` from a prior response to continue a multi-turn test conversation. Tokens consumed here are not billed. Response includes the agent's reply text plus metadata: handoff reason, no-response reason, quick replies, and referenced product variant IDs. Source: `reference_operate_agent-test.md`.

### Thread Control (Cloud API)
`POST /` at `https://api.facebook.com/business/whatsapp/phone_numbers/{phone_number_id}/thread_control` — **base URL pattern differs from every other group (see Inconsistencies)**.
Auth: permission `whatsapp_business_messaging` only, and **all three** of `access_token` (query), `oauth_token` (query), and `Authorization: Bearer` (header) are required together — the only endpoint in this set with multiple simultaneous auth requirements. Also uses `X-API-Version: "1.0.0"`, not `2.0.0`.
Transfers control of a consumer conversation thread between the Meta Business Agent and an external (human/escalation) system: `action: "release"` hands control back to the agent, `action: "take"` acquires control (restricted to the configured escalation partner), `action: "pass"` is reserved/not yet accepted. Optional `metadata` string is forwarded verbatim to the receiving app's `messaging_handovers` webhook. Source: `reference_operate_thread-control-cloud-api.md`.

---

## Insights

### Conversation Turns
`GET /` at `https://api.facebook.com/{entity_id}/insights/conversations/turns`
Auth: capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`.
Retrieves the ordered turns of the most recent conversation with a given consumer (`user_phone_number`, required, E.164), optionally bounded by `start_timestamp_ms`/`end_timestamp_ms` and cursor-paginated. Each turn includes `session_id`, end-to-end latency, and an ordered list of `steps` — `LLM_CALL` or `TOOL_CALL` entries with per-step latency, status (`SUCCESS`/`ERROR`/`TIMEOUT`), and, for tool calls, tool name/input/output. This is the primary endpoint for tracing what the agent actually did on a given turn. Source: `reference_insights_conversation-turns.md`.

---

## Delete

### Delete Agent
`DELETE /` at `https://api.facebook.com/{entity_id}/delete_agent`
Auth: permission `whatsapp_business_messaging` only — **no capability alternative listed (see Inconsistencies)**.
Removes the Meta Business Agent configuration from the specified WhatsApp phone number. When it's the last agent on the account, this also disconnects the integration entirely. Returns the `deleted_agent_id`, or null if there was nothing to remove. Source: `reference_delete-agent_delete-agent.md`.

---

## Inconsistencies observed across source docs

- **Auth requirement is not uniform.** Most groups (onboarding, allowlist, settings, all knowledge sub-resources, skills, connectors, connector tools, eval, event, test, conversation-turns) accept capability `bizai_wa_enterprise_api_3p_access` OR permission `whatsapp_business_messaging`. Three groups differ:
  - **Agent Budget** requires permission `business_management` instead of `whatsapp_business_messaging` (still OR'd with the same capability). This is the only group tied to Business Manager-level permissions rather than WhatsApp messaging permissions.
  - **UI Skills** and **Delete Agent** list only permission `whatsapp_business_messaging`, with no capability-based alternative documented.
  - **Thread Control (Cloud API)** lists only permission `whatsapp_business_messaging`, but additionally requires two API-key query params (`access_token`, `oauth_token`) *together with* the Bearer token — the only endpoint requiring three auth credentials simultaneously.
- **Base URL pattern is not uniform.** Every group uses `https://api.facebook.com/{entity_id}/...` except **Thread Control**, which uses `https://api.facebook.com/business/whatsapp/phone_numbers/{phone_number_id}/thread_control` — a structurally different path (no shared `{entity_id}` root segment, explicit `/business/whatsapp/phone_numbers/` prefix).
- **API version header is not uniform.** Every group uses `X-API-Version: "2.0.0"` except **Thread Control**, which uses `"1.0.0"`.
- **`entity_id` semantics differ for Agent Budget.** Every other group's `entity_id` is the WhatsApp Business Phone Number ID (string). Agent Budget's `entity_id` is the Business Manager ID (integer) that owns the agent — a different entity type entirely, despite reusing the same path-parameter name.
- **Coverage gap:** the task's grouping list for "Onboard" includes `agent-eligibility`, but `reference_onboard_agent-eligibility.md` was not among the source files provided for this doc, so it's omitted here (flagged as a placeholder note under Onboard rather than fabricated).

---

See also:
- [[bizai-api-endpoints]] — Gupshup's own BizAI for Partners API (the wrapper, not Meta's native API)
- [[meta-business-agent]] — Conceptual overview of the Meta Business Agent platform
- [[bizai-architecture]] — How Gupshup's wrapper maps to these underlying Meta endpoints
