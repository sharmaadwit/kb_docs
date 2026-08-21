# Meta Business Agent — Official Overview (Meta-native product)

**Purpose of this doc:** give sales/presales an accurate, source-traceable picture of what Meta's own Meta Business Agent product actually supports today, so deals aren't closed on capabilities it doesn't have.

> **This is Meta's own native product, not Gupshup's.** Meta Business Agent is built, hosted, and operated by Meta through the Meta Business Agent Platform APIs. It is **distinct from Gupshup's "BizAI for Partners"** (see `kb/bizai/bizai-overview.md`), which is Gupshup's own product that mirrors Meta's API surface on top of Gupshup's Partner API. Do not conflate the two — see [See also](#see-also) below for how they relate.

## What Meta Business Agent is

Meta Business Agent is an enterprise AI agent that engages customers on WhatsApp in the business's brand voice. Once enabled, it acts as the **primary responder** — answering questions from the business's own knowledge, taking actions through the business's own systems (e.g., looking up an order or booking an appointment), and handing off to the business's app when needed.

Businesses set up, configure, and enable the agent through the Meta Business Agent Platform APIs. Configurable surfaces are:

- **What it knows** — business information, FAQs, websites, and files, so the agent answers from the business's content.
- **How it responds** — "skills" that set the agent's tone, priorities, and brand voice.
- **What it can do** — connectors to the business's own APIs, plus webhook subscriptions, so the agent can take actions and listen to events (e.g., booking an appointment, confirming a payment).
- **Handoff** — passing control between the agent and the business's app for specific events or flows.
- **Testing** — sending test messages and evaluating agent performance before and after go-live.

## Eligibility

Meta Business Agent is **available only in approved countries and verticals**. Only businesses based in an approved country, operating in one of the approved verticals, can onboard.

**Supported verticals (exactly 5, per the official overview — do not paraphrase or add to this list):**
- Automotive
- Consumer Packaged Goods (CPG)
- Professional Services
- Retail and Ecommerce
- Travel

**Supported countries:** 182 countries are currently supported. See Meta's official docs (Overview → Availability) for the full country list — it is not reproduced here to avoid drift from the source of truth.

To check whether a **specific phone number** is eligible programmatically, use the [Eligibility](https://developers.facebook.com/documentation/meta-business-agent/reference/onboard/agent-eligibility) endpoint (`GET /{entity_id}/agent_eligibility`), which returns a simple `is_eligible: true/false` for that WhatsApp Business Phone Number ID. This is the authoritative, per-number check — verticals/countries lists above are necessary but not sufficient for eligibility confirmation.

## Requirements

To use Meta Business Agent, a business needs:

- A **WhatsApp Business Account (WABA)** with a WhatsApp Business phone number
- A **Meta app** with the **`whatsapp_business_messaging`** permission
- A business that operates in a supported country and vertical (see [Eligibility](#eligibility) above)

## High-level setup flow

The confirmed, documented onboarding path (from Meta's "Get started with Meta Business Agent APIs") is:

1. **Set up Meta Business Agent in WhatsApp Manager** — the business goes to WhatsApp Manager, and if any of its phone numbers are eligible, a "Meta Business Agent" tab appears. This is where the business accepts the Meta Business Agent Terms of Service and sets up the agent for eligible numbers. (BSPs/Tech Providers must additionally accept the Tech Provider Terms of Service.) The agent does not reply to customers yet at this point — knowledge/skills need to be configured first.
2. **Create a system user** in Meta Business Suite (skip if one already exists).
3. **Assign the app** to the system user.
4. **Assign the WABA** to the system user, with "View and manage phone numbers" permission.
5. **Generate an access token** — either a system user token (for direct integrators) or a BISU token (for BSPs/Tech Providers), each requiring `whatsapp_business_messaging` and `whatsapp_business_management` permissions.
6. **Subscribe the app to the WABA** via the Subscribed Apps API.
7. **Subscribe to webhook fields** — `messages`, `standby`, and `messaging_handovers` — so the business's app stays in sync with what the agent is doing (conversation routing/control is tracked via these fields; control can be handed back to the agent via the Thread Control endpoint's `pass` action).

After the app is connected, the business configures the agent across three stages — **Onboard** (eligibility, onboarding, settings/enable, allowlist), **Configure** (skills, business info, FAQs, websites, files, connectors), and **Operate** (thread control, agent events, test, eval). Not every API is required — only the ones the use case needs.

## Currently WhatsApp-only

**Important for sales/presales:** the documented, confirmed-live onboarding path is set up through **WhatsApp Manager**, and the Prerequisites/Get Started docs frame this entire flow around a WhatsApp Business Account, WhatsApp phone numbers, and the `whatsapp_business_messaging` permission. **Today, this is a WhatsApp-only product.**

There are signals in the underlying API schema that suggest Meta may be building toward multi-channel support in the future:
- The eligibility and onboarding response schemas are named `BizAIOmniChannelEligibilityResponse` and `BizAIOmniChannelOnboardingResponse`.
- The onboarding API's `channel` query parameter accepts one of: `email`, `instagram`, `line`, `messenger`, `sms`, `tiktok`, `unknown`, `webchat`, `whatsapp`.

**Do not read this as multi-channel availability.** These are naming/schema artifacts, not a confirmed product capability. The overview, get-started guide, and eligibility docs only describe a WhatsApp Business phone number flow through WhatsApp Manager. Nothing in the source docs confirms that email, Instagram, Line, Messenger, SMS, TikTok, or webchat onboarding is actually live or supported for customers today. Treat "OmniChannel" naming as a forward-looking hint at best, not a sellable feature.

## For Sales/Presales

**Do:**
- Confirm the prospect's vertical is one of the 5 supported: Automotive, CPG, Professional Services, Retail and Ecommerce, or Travel.
- Confirm the prospect's business is based in one of the 182 supported countries (point them to Meta's official docs for the current list, or use the Eligibility endpoint to check a specific number).
- Position Meta Business Agent as a **WhatsApp-only** capability today.
- Clarify to the prospect whether they are asking about **Meta's native Meta Business Agent** or **Gupshup's BizAI for Partners** — the two have different ownership, delivery models, and capability sets. If the prospect wants multi-channel (SMS, email, web) AI agents today, that is a BizAI for Partners conversation, not a Meta Business Agent one (see `kb/bizai/bizai-overview.md`).
- Use the per-number Eligibility endpoint (or point technical stakeholders to it) before making firm commitments — vertical/country match alone does not guarantee a given phone number is eligible.

**Don't:**
- Don't promise Meta Business Agent for verticals outside the 5 listed above (e.g., no BFSI, healthcare, telecom, government, etc. — these are not in the supported list per the official overview).
- Don't promise availability in countries outside the 182 supported, and don't guess at country coverage — refer to Meta's official docs.
- Don't promise or imply channels beyond WhatsApp (no email, Instagram, Messenger, SMS, TikTok, Line, or webchat) — the "OmniChannel" naming in the API schema is not evidence of a live, sellable multi-channel product.
- Don't conflate Meta Business Agent with Gupshup's BizAI for Partners in customer-facing conversations — they are different products with different owners.

## Open questions / not covered by source docs

- The source docs do not state a timeline or roadmap for multi-channel (non-WhatsApp) support — only the schema/parameter naming hints exist. Do not commit to a timeline.
- Pricing details are referenced in the overview but not reproduced here; see Meta's WhatsApp pricing docs for non-template messages for current rates.

## See also

- `kb/bizai/bizai-overview.md` — Gupshup's **BizAI for Partners**, which mirrors Meta's BizAI API surface on top of Gupshup's own Partner API. This is the Gupshup-owned wrapper/value-add product — not the same as this doc's subject.
- `kb/bizai/bizai-architecture.md` — How Gupshup's BizAI wrapper integrates with the Partner API, session management, and connectors. Useful for explaining to prospects how Gupshup's offering differs from onboarding directly with Meta.
