# Meta Business Agent vs. BizAI for Partners: Which One Am I Asking About?

These are two different products with similar names. This doc disambiguates them.

## Meta Business Agent (Meta's product)

Meta Business Agent is **Meta's own** enterprise AI agent that engages customers on WhatsApp in your brand's voice, acting as the primary responder to conversations. You configure what it knows (business info, FAQs, websites, files), how it responds (skills/tone), and what it can do (connectors to your own APIs), plus handoff rules back to your app. It's set up via the Meta Business Agent Platform APIs, requires a WABA, a Meta app with `whatsapp_business_messaging` permission, and is limited to approved countries/verticals.

See: `kb/bizai/meta-business-agent-official-overview.md` and `kb/bizai/meta-business-agent-api-reference.md`.

## BizAI for Partners (Gupshup's product)

BizAI for Partners is **Gupshup's own** strategy for delivering an agentic AI layer on top of Gupshup's existing Partner API. It's built as **new endpoints on the existing Partner API** — not a separate platform — so partners adopt it without migrating off their current integration (auth, WABA setup, message send/receive, webhooks all stay unchanged). Its API surface deliberately mirrors Meta's ("Meta-parity plus value-add"): partners get a familiar contract plus Gupshup-specific capabilities Meta's raw APIs don't offer — simplified human handoff, an eval-and-optimize loop, multi-channel deployment (WhatsApp, SMS, email, web), and connector extensibility.

See: `kb/bizai/bizai-overview.md`, `kb/bizai/bizai-architecture.md`, `kb/bizai/bizai-value-add.md`.

## When to ask about which

| If the question is about... | Ask about |
|---|---|
| Meta Business Agent Platform APIs, WABA-level agent setup directly with Meta, Meta's eligibility/country-vertical rules | **Meta Business Agent** |
| Gupshup Partner API endpoints, adopting AI agents without migrating your Gupshup integration, resale/multi-channel/handoff/eval features | **BizAI for Partners** |

## The relationship

BizAI does not replace or compete with Meta Business Agent — it **mirrors and wraps** Meta's API surface on top of Gupshup's existing Partner API, then adds Gupshup-specific value (handoff, eval-and-optimize, multi-channel, connectors) that Meta's raw APIs don't provide. If you're already a Gupshup partner, BizAI is how you get Meta Business Agent-equivalent capability without a separate integration.

See also:
- [[bizai-overview]]
- [[bizai-architecture]]
- [[bizai-value-add]]
