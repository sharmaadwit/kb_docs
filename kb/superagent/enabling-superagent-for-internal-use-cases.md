---
source_url: internal
---

# Enabling SuperAgent for Internal Use Cases

**Module**: SuperAgent

## What this page covers
How to enable SuperAgent for a customer's **internal** use cases when the
deployment involves connecting to their internal systems, building data
pipelines on their side, and running agent-driven actions safely.

## 1) What SuperAgent should do
For internal use cases, SuperAgent should sit as an **AI orchestration layer over the customer's existing systems**.
It is not meant to replace their warehouse, CRM, ticketing, or internal APIs. Instead, it uses those systems through controlled integrations.

Typical internal use cases:
- Internal ops copilot
- Campaign operations assistant
- Template management assistant
- Support / Agent Assist admin helper
- Analytics / troubleshooting assistant
- Internal workflow automation via APIs / webhooks

## 2) Recommended architecture
A safe and scalable setup usually looks like this:

- **Customer data stays in customer-controlled systems** — CRM, CDP, DB, BI tools, ticketing tools, internal dashboards, etc.
- **Customer exposes only what is needed** — secure APIs, webhooks, scheduled exports, middleware / iPaaS layer, read-only service endpoints where possible.
- **SuperAgent uses skills to interact with those systems** — each skill handles a narrow task (e.g. fetch open tickets, create a campaign draft, check template status, sync analytics, trigger webhook).
- **Secrets stay in skill settings** — API keys, tokens, base URLs, client credentials should be stored in Skill Settings / secrets, not pasted into prompts.

## 3) How to build this in SuperAgent

### Step A: Define the use case clearly
Before building, lock these:
- Who will use it?
- What questions / actions should it support?
- Which systems will it read from?
- Which systems will it write to?
- What actions require confirmation?

Good first use cases:
- "Show campaign performance for the last 7 days"
- "Fetch failed WhatsApp templates and suggest next steps"
- "Create a draft response for support escalation"
- "Trigger a webhook when a lead reaches a stage"

Avoid starting with:
- "Connect everything"
- "Let the AI access all internal data"

## 4) Using the Build Skills & Recipes button
If you want custom internal workflows, this is the main entry point.

Use **Build Skills & Recipes** when you need to:
- Create a custom skill for an internal API
- Add logic for a private workflow
- Build a reusable internal automation
- Standardize a multi-step operational flow

### When to create a Skill
Create a skill when you need the agent to:
- Call an API
- Read or update structured data
- Trigger a webhook
- Perform a repeatable business action
- Validate inputs before acting

Examples: `get_open_tickets`, `fetch_internal_kpi`, `create_campaign_approval_request`, `sync_customer_status`, `trigger_internal_incident_webhook`.

### When to create a Recipe
Create a recipe when you need:
- A guided workflow using one or more skills
- Best-practice orchestration
- A repeatable process with business rules

Examples: campaign launch checklist, lead qualification workflow, escalation handling flow, delivery request orchestration.

## 5) Best practice for Skill Secrets
For internal use cases, credentials should be stored in **skill secrets / settings**, not hardcoded and not shared in chat.

Store things like:
- API base URLs
- Client ID / client secret
- API keys
- Bearer tokens
- Service account values
- Project IDs / Workspace IDs

Why use skill secrets:
- Keeps auth separate from chat
- Prevents users from seeing credentials
- Makes the skill reusable across sessions
- Easier to rotate credentials later
- Safer than embedding tokens in prompts or code comments

Important rules:
- Never ask end users to paste passwords or raw secrets into chat
- Keep secrets per skill if scopes differ
- Use least-privilege credentials
- Prefer short-lived tokens where possible
- Rotate keys periodically

## 6) Suggested pattern for custom internal skills
A strong internal skill usually follows this pattern:

- **One clear purpose** (e.g. "Fetch open finance approvals")
- **Defined inputs** (date range, team, status, campaign ID, template name, etc.)
- **Secure auth from skill secrets** (the skill reads credentials from settings)
- **Validation** — reject missing / invalid inputs, prevent unsafe writes
- **Clear output** — structured, short, reliable; avoid dumping raw backend payloads
- **Confirmation for sensitive actions** — especially if creating, updating, deleting, sending, or publishing

## 7) What the customer team usually needs to provide
For internal enablement, the customer's engineering / data team should usually provide:

**Data access layer** — at least one of:
- Internal API endpoints
- Middleware service
- Webhook receiver / sender
- Read-only reporting endpoint
- Export pipeline into an accessible system

**Authentication model**, for example:
- API key
- OAuth client credentials
- JWT / Bearer token flow
- Basic auth if unavoidable
- IP allowlisting if required by their infra

**Data contract** — define:
- Input parameters
- Output fields
- Error states
- Rate limits
- Pagination
- Freshness / SLA expectations

**Ownership** — someone must own:
- API uptime
- Schema changes
- Credential rotation
- Incident handling
- Access approval

## 8) Recommended rollout plan

- **Phase 1: Discovery** — document use case, users, systems involved, inputs / outputs, permissions, approval needs, expected business value.
- **Phase 2: Build a thin slice** — one skill, one API, one clear result, one user persona.
- **Phase 3: Add guardrails** — read-only vs write access, approval-required actions, who can invoke what, allowed environments, logging / audit expectations.
- **Phase 4: Pilot** — run with a small internal team, verify answers, test edge cases, refine prompts and outputs, improve error handling.
- **Phase 5: Expand** — add more skills, multi-step recipes, scheduled automations, analytics / reporting helpers.

## 9) Good internal use-case examples

**Read-heavy, low-risk starters** (best for first deployment):
- Fetch analytics summaries
- Check WABA health
- List templates by status
- Find delivery issues
- Summarize campaign performance
- List open support items
- Retrieve goal / journey status

**Medium-complexity:**
- Draft campaign setup from inputs
- Create internal review summaries
- Map template variables
- Segment / customer lookup helpers
- Support routing recommendations

**Higher-risk** (add only after controls are clear):
- Publish campaigns
- Update production journeys
- Modify live configs
- Create users / access
- Write back to internal systems
- Trigger customer-facing outbound actions

## 10) Guardrails to define upfront
For internal deployments, define these explicitly:
- Who can use it
- What systems it can access
- Which actions are read-only
- Which actions require confirmation
- What data must never be exposed
- What logs / audits are needed
- What happens on auth failure or bad input

A simple rule:
- Start with read-only
- Add writes later
- Require confirmation for destructive or customer-impacting actions

## 11) How to explain this to a customer
You can position it like this:

> SuperAgent can support internal workflows, but the recommended model is to
> connect it to your existing systems through secure APIs, webhooks, or
> controlled data services. For custom workflows we use **Build Skills &
> Recipes** to create reusable capabilities. Authentication should be stored
> securely in skill secrets / settings, not passed through chat. We usually
> start with a narrow use case, pilot it with read-only access, and then
> expand once the data contracts and controls are stable.

## 12) Practical implementation checklist
Use this as an onboarding checklist:
- Identify one internal use case
- List source systems involved
- Define read / write scope
- Ask customer team for API or webhook access
- Define request / response schema
- Build a custom skill using **Build Skills & Recipes**
- Store auth in Skill Settings / secrets
- Test with sample inputs
- Add confirmation for sensitive actions
- Pilot with a small user group
- Review failures and edge cases
- Expand to more workflows only after stability

## 13) What not to do
- Don't ask users to paste credentials in chat
- Don't hardcode secrets inside prompts
- Don't start with broad production write access
- Don't connect the agent to every internal system at once
- Don't skip schema and ownership discussions
- Don't let the AI invent unsupported actions against internal tools

## 14) Suggested first pilot
A very practical first pilot is:
- One read-only internal API
- One reporting or troubleshooting workflow
- One or two user personas
- One custom skill
- Secrets stored in skill settings
- No production writes

That usually drives adoption faster and avoids data-pipeline complexity early.
