  
**BizAI for Partners**

**API Strategy White Paper**

**Audience:** Internal Gupshup stakeholders (product, engineering, partnerships, GTM)  
**Status:** Draft for review  
**Date:** 2026-06-30

# **Executive Summary**

Gupshup’s partner ecosystem is built on a mature set of Partner APIs that today drive WhatsApp Business messaging at scale. BizAI — the agentic AI layer that turns a WhatsApp number into an autonomous business agent — represents the next surface our partners can build on, resell, and embed. This white paper sets out the strategy for delivering BizAI to partners as an extension of the APIs they already use, not as a separate platform they must learn from scratch.

The strategy rests on two complementary bets:

* **Meta-parity plus value-add.** We mirror Meta’s BizAI API surface as closely as possible so that partners and their developers face a familiar, well-documented contract — then we layer differentiating Gupshup capabilities on top (simplified handoff, an eval-and-optimize loop, a connectors ecosystem, and conversation analytics) that Meta’s raw APIs do not provide.

* **Partner enablement and monetization.** Every design choice is filtered through a single question: does this make it easier for a partner to launch, operate, and grow an AI agent business with lower engineering and operational burden? The add-on layer is where partners differentiate their offering and where new monetizable surface is created.

The result is a low-friction adoption path — reuse of existing authentication and onboarding, delivery as new endpoints on the existing Partner API — paired with a set of higher-order capabilities that make BizAI significantly more valuable through Gupshup than through Meta directly.

*Assumption flagged for review: This paper treats the Meta BizAI API surface as the parity baseline and the endpoints listed in api-strategy.md (the /api/nma/\* family) as the planned Gupshup contract. Endpoint names and onboarding APIs are still in flux per the source doc.*

# **1\. Strategic Context**

## **1.1 Where partners are today**

Partners integrate with Gupshup through the existing Partner API endpoints: provisioning WABA IDs, sending and receiving messages, managing templates, and handling the operational plumbing of WhatsApp conversations. They have already absorbed the cost of integrating our authentication, our onboarding flow, and our message-handling model. That integration is an asset we should not ask them to rebuild.

## **1.2 The opportunity**

BizAI changes what a WhatsApp number is. Instead of a channel that a partner’s bot drives, the number can host an autonomous agent that answers FAQs, references a catalog, calls into external systems, hands off to humans, and improves over time. Meta exposes a BizAI API surface for this; partners could, in principle, integrate against it directly.

Our opportunity is to make Gupshup the better place to consume BizAI — by removing the operational burden Meta leaves on the integrator, and by adding capabilities (eval, analytics, reusable connectors and skills) that no raw API provides.

## **1.3 Two strategic pillars**

**Pillar 1 — Meta-parity \+ value-add:** Mirror Meta BizAI API surface → familiar contract, low learning cost → Gupshup add-on layer on top.

**Pillar 2 — Partner enablement \+ monetization:** Reuse existing auth & onboarding → remove operational burden → new monetizable surface.

These pillars reinforce each other. Parity lowers the cost of adoption (Pillar 2’s goal), and the value-add layer is what creates the differentiated, monetizable surface (Pillar 1’s payoff).

## **1.4 Reference Architecture**

The partner-facing architecture places Gupshup as the orchestration layer between the WABA number, the BizAI engine, and the partner’s own module. The partner never talks to BizAI directly — they talk to Gupshup, which orchestrates BizAI on their behalf.

![Reference architecture diagram][image1]

Reading the diagram:

* **Users ↔ WABA Number:** end-user traffic flows over WhatsApp as today.

* **WABA Number ↔ Gupshup / ↔ BizAI:** the WABA number is fronted by Gupshup. AI-bound messages (AI\*) reach BizAI; the rest are handled as ordinary messages. Message echoes are absorbed at the Gupshup layer, not pushed onto the partner.

* **Gupshup core modules:** the orchestration layer is composed of an Orchestrator, AI, Analytics, Connector Manager (Conn Mgr), and Optimiser. These are the engines behind the value-add layer in Section 6\.

* **Gupshup ↔ BizAI:** internal control planes: Handoff, Agent Management, and Connectors.

* **Gupshup ↔ Partner Module:** the partner-facing contract: Agent APIs, Traces, Connectors, and Test/Eval.

The strategic point the diagram makes visually: the partner integrates against a single Gupshup surface that abstracts BizAI, message echoes, and handoff — which is exactly the friction-removal and “seamless, future-proof BizAI integration” the partner notes call for.

# **2\. Design Principles**

The strategy is governed by two principles carried directly from api-strategy.md:

* **Stay as close as possible to Meta’s BizAI APIs**, adding only APIs that deliver clear value on top. Familiarity is a feature: it reduces partner integration time, lowers our documentation and support load, and protects partners against lock-in anxiety.

* **Deliver BizAI APIs as an extension of the existing Gupshup Partner API endpoints.** No new authentication domain, no parallel onboarding stack, no separate SDK. BizAI is a set of new capabilities reachable through the contract partners already hold.

From these two principles, three operational commitments follow:

* Reuse, don’t reinvent, authentication. (Section 4\)

* Meet partners where their integration already is. New endpoints, same envelope.

* Differentiate above the parity line. The vanilla Meta-mirrored APIs are table stakes; Gupshup’s add-on layer is the product.

# **3\. What We Deliver to Partners**

Beyond the APIs themselves, a successful partner offering requires the surrounding enablement assets called out in the source strategy:

| Deliverable | Purpose |
| :---- | :---- |
| **API documentation** | Endpoint and parameter reference for every BizAI API, so developers can integrate without hand-holding. |
| **Cookbook** | Task-oriented recipes (“enable BizAI on a number,” “wire a Shopify connector,” “run an eval loop”) that compress time-to-first-value. |
| **Sandbox environment** | A rate-limited, hands-on environment for partners to experiment safely before touching production traffic. |

Documentation and a sandbox are not afterthoughts — for an internal audience, they are the difference between a strategy that converts partners and one that generates support tickets. They should be resourced as first-class deliverables alongside the APIs.

# **4\. Authentication — Zero New Surface**

BizAI introduces no new authentication model. It reuses the existing Gupshup Partner API authentication end to end.

* BISU tokens are created, fetched, and stored in the Gupshup system exactly as they are for any other WABA ID today.

* A partner already authenticated for messaging is, by construction, authenticated for BizAI.

* There is no separate credential lifecycle for partners to manage, rotate, or secure.

This is the single largest friction-remover in the strategy. It means a partner’s path from “we use Gupshup messaging” to “we offer BizAI agents” does not pass through a security and credentials review — the most common stall point in API adoption.

**Auth flow:** Partner system → (existing Gupshup auth) → Gupshup Partner API → (BISU token, per WABA ID) → BizAI APIs (/api/nma/\*). Same credential domain as WhatsApp/WABA.

# **5\. The Core BizAI API Surface (Meta-Parity Line)**

These APIs constitute the parity baseline — the surface that mirrors Meta’s BizAI capabilities and forms the foundation every partner builds on.

## **5.1 Onboarding (forthcoming)**

The onboarding APIs are not yet available but are expected to follow the existing manual process. The anticipated functions are:

* First-time enablement of BizAI on a number.

* Enabling message echoes and message events.

  *Open item: Onboarding API shape is undefined. Because it gates every other API, it should be sequenced first on the roadmap (Section 9).*

## **5.2 Configuration & Identity**

| API | What it does | Typical endpoint |
| :---- | :---- | :---- |
| **Settings** | Toggle BizAI on/off per number; configure inactivity nudges; enable/disable human handoff; manage allowed/testing numbers. | /api/nma/settings |
| **Business Info** | Manage business name, address, branding, hours of operation, policies, and support info. | /api/nma/business\_info |

## **5.3 Knowledge & Behavior**

| API | What it does | Typical endpoint |
| :---- | :---- | :---- |
| **Instructions** | Create and update named behavioral rules that steer agent responses (tone, escalation, edge-cases); prioritize and organize them. | /api/nma/instructions |
| **FAQ** | Add/edit/remove Q\&A pairs for instant responses; bulk import/export. | /api/nma/faq |
| **Catalog** | CRUD over products/services with categories, images, metadata; pagination for large catalogs. | /api/nma/catalog |
| **Websites** | Register crawlable URLs to augment the agent’s knowledge base; trigger refresh; remove stale URLs. | /api/nma/websites |

## **5.4 External Integration**

| API | What it does | Typical endpoint |
| :---- | :---- | :---- |
| **Connectors** | Register external API integrations the agent can call. | /api/nma/agent\_connectors |
| **Connector Tools** | Define individual callable operations on a connector, with parameter annotations and sample payloads. | /api/nma/agent\_connectors/{cid}/tools/{tid} |

## **5.5 Runtime Control & Quality**

| API | What it does | Typical endpoint |
| :---- | :---- | :---- |
| **Thread Control** | Take or release control of a conversation thread for smooth AI↔human handover. | /api/nma/thread\_control/take, /release |
| **Agent Test** | Dry-run agent responses to sample queries without sending real messages; expose intermediate reasoning. | /api/nma/agent\_test |
| **Agent Event** | Push proactive events/notifications (updates, reminders, system messages) as arbitrary JSON payloads. | /api/nma/agent\_event |
| **Agent Eval** | List evaluation cases, run eval jobs, pull historical run data for regression tracking. | /api/nma/agent-eval/cases, /run |

## **5.6 How the core surface fits together**

The four capability groups — Configure, Teach, Integrate, Operate — all feed the BizAI Agent. Operate produces feedback that flows back to Teach, closing the loop. Everything in Section 6 sits above this parity line and is where Gupshup differentiates.

# **6\. The Value-Add Layer — Where Gupshup Wins**

The add-on layer is the strategic core of the partner offering. It is what a partner gets through Gupshup that they would have to build themselves on top of Meta’s raw APIs — and it is the surface most likely to support premium positioning and monetization.

## **6.1 Simplified Handoff, Echoes & Events**

### **The problem it removes**

With raw BizAI, every partner system must manage handoff between AI and human, plus the bookkeeping of message echoes and message events. That is undifferentiated, error-prone work that every partner re-implements.

### **What Gupshup provides**

A layer built after WDS that absorbs this entirely:

* Incoming user messages are passed to the partner’s existing systems only when BizAI is not in control. When the agent is driving, the partner system simply does not see the traffic it would otherwise have to route and suppress.

* Partner systems no longer have to handle message echoes or message events at all.

* Partners retain full control: existing systems can still issue /pass and /take to hand a conversation to or reclaim it from BizAI.

The handover layer must: track message echoes and events emitted by BizAI; route incoming user messages to the correct system (BizAI or the partner) based on who holds the conversation; and maintain the state of which system is in control of each conversation as control passes back and forth via /pass and /take.

*This is a genuinely new system Gupshup must build. The strategic payoff is that this complexity is solved once, centrally — so no connecting system has to handle the new message types or implement the complex handoff checks themselves.*

**Why it matters strategically.** This is the clearest “buy vs. build” argument in the offering. It converts a recurring, error-prone engineering cost on the partner side into a single Gupshup-managed capability — directly serving the partner-enablement pillar and reducing partner operational burden.

## **6.2 Eval & Optimization Loop**

**Three evaluation modes:** 

* **BizAI eval:** evaluates the BizAI agent in isolation.

* **Hybrid test:** lets partners test a hybrid agent — the partner’s bot and the BizAI agent working together — against standard test scenarios.

* **Hybrid eval:** evaluates the combined hybrid agent, while BizAI eval remains scoped to the BizAI agent alone.

This distinction matters: most partners will run BizAI alongside, not instead of, their existing bot. Giving them a way to test and evaluate the combination is something only an integrator positioned where Gupshup sits can offer.

**The optimization loop:** Roleplay scenarios → Benchmark → Score (judge agent) → Improve agent → loop back. When benchmark is met, produce release candidate.

Supporting capabilities:

* Versioning and rollback of agent configurations.

* View results across runs, with tags and notes for tracking experiments.

* Generate scenarios and scoring mechanisms from simple descriptions, lowering the expertise needed to run rigorous evals.

**Why it matters strategically.** Building an agent has become easy; getting it right has not. The bulk of a bot developer’s time is no longer spent on creation — it goes into the loop of testing, evaluating, and optimizing skills and tools. An automated optimizer is the key unlock, and it only works with the surrounding rigor: versioning of every agent configuration, clear rollback to any prior version, and reproducibility. Quality is the durable differentiator for AI agents, and this is where partners spend their hardest hours.

## **6.3 Connectors Ecosystem**

**Two connector types, with an important trade-off:**

* **Gupshup connectors:** route BizAI → Gupshup → external system. Because the call passes through Gupshup, tool-call traces are available (see 6.4).

* **BizAI connectors:** call external systems directly. They are simpler but traces are not available for these calls.

  *This trade-off should be made explicit to partners: choosing Gupshup connectors buys observability.*

**Ecosystem capabilities:**

* **Prebuilt connectors** for common systems — Shopify, Zendesk, Salesforce, and other APIs — available in both Gupshup and BizAI connector flavors.

* **Connector versioning** with rollback to previous versions.

* **Custom connector templates** that can be built once and reused across WABA IDs — a force-multiplier for partners managing many businesses.

**Why it matters strategically.** Reusable, versioned, prebuilt connectors turn integration from a per-customer project into a catalog a partner draws from. The reuse-across-WABA-IDs property is especially valuable to partners operating at scale across many end-customers.

## **6.4 Conversation Analytics & Traces**

**Conversation Analytics:**

* Templated and customizable, and re-runnable on past sessions — so a new analytics definition can be applied retroactively.

* Produces structured output per conversation based on a schema, stored in the database, and re-runnable if analytics settings change.

* The output schema can be built from a simple description, reviewed and approved by the user, then stored, managed, and versioned.

* Uses an external LLM, with a cost implication; open-source models can be used as a cheaper option.

**Traces / agent logs:**

* Traces cover tool calls and assistant messages, available both in real time and in bulk.

* Full tool-call traces assume Gupshup connectors; for non-Gupshup (direct) connectors, traces contain only user and agent messages (consistent with the connector trade-off in 6.3).

**Why it matters strategically.** Analytics and traces close the loop between running agents and improving them (6.2). They are also a natural metered/monetizable surface given the LLM cost, and the open-source-model option gives partners a cost lever rather than a fixed tax.

## **6.5 Reusable Instructions (Skills)**

Complementing connectors, the Instructions / Skills add-on layer provides:

* Versioning and rollback of instruction updates.

* A library of templated Gupshup skills/instructions to reuse.

* Custom skills reusable across WABA IDs.

* Generation of full-fledged instructions from a skeleton the partner provides, applying best practices.

This mirrors the connector ecosystem’s “build once, reuse across many businesses” model on the behavior side, and lowers the skill required to author high-quality agent behavior.

## **6.6 Multi-Channel Support (RCS & Web)**

The vanilla BizAI API wrappers carry an additional attribute to support RCS and Web chat agents, extending the same agent model beyond WhatsApp. This positions BizAI as a channel-flexible agent platform rather than a WhatsApp-only feature — relevant as partners’ channel mix broadens. The notes frame this more broadly as multi-channel orchestration (e.g., RCS driven by Gupshup AI), consistent with the orchestrator-centric architecture in Section 1.4.

## **6.7 Consolidated Partner Value-Add Inventory**

The full partner value-add surface — what a partner gets through Gupshup above the Meta-parity line:

| Value-add | What it gives the partner | Covered in |
| :---- | :---- | :---- |
| **Conversation analytics / traces** | Conversation analytics \+ tool-call/message traces, real-time and bulk | 6.4 |
| **Service / token cost optimization** | Lever on LLM spend (open-source model option, routing) rather than a fixed AI tax | 6.4, new |
| **BizAI / WAME orchestration** | Gupshup orchestrates BizAI against the WABA number; partner integrates one surface | 1.4 |
| **Seamless, future-proof BizAI integration** | Insulates the partner from BizAI/Meta API churn behind the Gupshup contract | 1.4, 4 |
| **Gupshup agent library** | Templated agents (e.g., translation) ready to reuse | 6.5, new |
| **Pre-built connector library** | Shopify, Zendesk, Salesforce, etc., versioned | 6.3 |
| **Agent lifecycle management** | Versioning, rollback, tags/notes across the agent’s life | 6.2, 6.3, 6.5 |
| **Async messages & triggers in BizAI** | Proactive events, scheduled/triggered agent actions | 5.5 (Agent Event), new |
| **Copy / clone across multi-business** | Reuse skills, connectors, analytics across the partner’s customers (WABA IDs) | 6.3, 6.5, new |
| **Multi-channel orchestration** | RCS \+ Web alongside WhatsApp under one agent model | 6.6 |
| **Design-time configurator (UI)** | Visual setup of agents, skills, connectors before runtime; APIs also available | 6.8, new |
| **Raw user/agent conversation trace log** | Unprocessed transcript log, distinct from structured analytics | 6.4 |
| **Sandbox** | Rate-limited hands-on environment | 3 |
| **Agent optimizer** | Closed-loop optimization driven by traces \+ analytics | 6.2 |
| **Payments** | Payment flows surfaced through the agent | new |

*New surfaces flagged for scoping (not in api-strategy.md): service/token cost optimization, async messages & triggers, copy/clone across multi-business, design-time configurator, Gupshup agent library (translation/templated agents), and payments. These came from discussion notes and need product definition before they enter the roadmap.*

## **6.8 Design-Time Configurator (UI)**

Partners today are API-first: they integrate Gupshup through endpoints, not screens. The design-time configurator is a deliberate departure — a UI for setting up agents, skills, connectors, and analytics before runtime.

* APIs remain available for everything the configurator does, so partners who prefer to stay fully programmatic can. The UI does not replace the API contract; it sits on top of it.

* The UI exists because it makes BizAI easier to understand and adopt. For a capability surface this broad — skills, connectors, instructions, analytics schemas, eval scenarios — a visual configurator dramatically shortens the learning curve compared to reading API docs alone.

* It is most valuable at the top of the adoption ladder (Section 9.1), where partners author and manage their own reusable templates: seeing and shaping these objects visually is far faster than constructing them blind through API calls.

**Why it matters strategically.** The configurator is an adoption accelerant for an audience that is new to building agents, not just calling messaging APIs. It lowers the barrier to the high-value rungs (build-your-own templates, eval, optimize) without forcing partners off the API path they know.

# **7\. How the Pieces Reinforce Each Other**

The value-add layer is not a grab-bag of features; the components compound:

* **Handoff** produces clean, well-scoped conversation traffic.

* **Gupshup connectors** make that traffic observable via traces and analytics.

* **Analytics** feed the eval-and-optimize loop with real-world signal.

* **The loop** produces better skills and connector configurations, which are reused across WABA IDs.

A partner who adopts the full stack gets a flywheel; a partner who adopts only the parity line gets Meta’s capabilities with Gupshup’s auth convenience. Both are valid entry points — and the upgrade path between them is the monetization story.

# **8\. Partner Enablement & Monetization Lens**

Mapping capabilities to the partner-enablement thesis:

| Capability | Partner benefit | Monetization signal |
| :---- | :---- | :---- |
| Reused auth & onboarding | Near-zero integration friction | Faster activation, higher conversion |
| Simplified handoff | Removes recurring engineering/ops burden | “Buy vs. build” — strong willingness to pay |
| Eval & optimize loop | Provable agent quality | Premium/quality tier; recurring use |
| Connectors ecosystem | Reuse across customers; faster delivery | Catalog/marketplace surface |
| Analytics & traces | Visibility \+ improvement signal | Metered (LLM cost), tiered analytics |
| Reusable skills | Faster, higher-quality agent authoring | Template library value |
| RCS / Web channels | Broader reach from one agent model | Expanded addressable surface |

The consistent theme: each add-on either removes a cost the partner would otherwise carry or creates new surface the partner can resell. That is the dual engine of enablement and monetization.

# **9\. Adoption Ladder, Phasing & Open Questions**

## **9.1 Partner adoption ladder**

The add-ons are not all-or-nothing. A partner climbs a ladder of increasing sophistication and value, each rung building on the last. This doubles as the monetization staircase — higher rungs justify higher tiers.

| Rung | Partner capability | Maps to |
| :---- | :---- | :---- |
| 0 | **Simplified handoff** — extend existing bots/agents into a hybrid setup with BizAI; Gupshup absorbs handoff, echoes & events so partner-side changes are minimal | 6.1 |
| 1 | Versioned templated skills & connectors (consume Gupshup’s library) | 6.3, 6.5 |
| 2 | Get the traces | 6.4 |
| 3 | Simple conversational analytics | 6.4 |
| 4 | Build own templates for skills, connectors & analytics, reused across clients and managed by the partner | 6.3, 6.5, copy/clone (6.7) |
| 5 | Automated testing (standard scenarios, hybrid test) | 6.2 |
| 6 | Agent eval | 6.2 |
| 7 | **Optimizer** (closed loop via traces \+ analytics) | 6.2 |

The ladder runs from coexist (rung 0\) to consume (rungs 1–3) to build & operate (rung 4\) to measure & improve (rungs 5–7). Rung 0 is the on-ramp: simplified handoff lets a partner keep their existing bots/agents and run BizAI alongside them in a hybrid model, with Gupshup absorbing handoff, message echoes, and events so the partner-side change is minimal. Rung 4 is the inflection point: a partner who starts authoring and managing their own reusable templates across customers has moved from a BizAI user to a BizAI platform operator — the stickiest, highest-value relationship.

## **9.2 Suggested build sequencing**

A pragmatic ordering, given dependencies:

* **Phase 0 — Onboarding APIs \+ Sandbox \+ Docs:** Unblocks everything. Onboarding APIs are still undefined and gate enablement; sandbox and docs are prerequisites for partner self-service.

* **Phase 1 — Core parity surface \+ reused auth:** Delivers the familiar parity surface on reused auth — the lowest-friction adoption milestone.

* **Phase 2 — Simplified handoff layer:** Highest buy-vs-build value.

* **Phase 3 — Connectors \+ Traces:** Unlocks analytics and eval.

* **Phase 4 — Analytics \+ Eval/Optimize loop.**

* **Phase 5 — Reusable skills \+ RCS/Web.**

  *Sequencing is a recommendation for discussion, not a committed roadmap.*

## **9.3 Open questions for internal review**

* **Onboarding API shape:** undefined; needs definition before Phase 0 can close.

* **Endpoint naming:** /api/nma/\* names in api-strategy.md are marked “typical”; confirm the committed contract.

* **Analytics LLM cost model:** how is external-vs-open-source model choice surfaced to partners, and how is cost metered/billed?

* **Connector trace gap:** how prominently do we steer partners toward Gupshup connectors given the observability trade-off, and what’s the messaging when partners need direct connectors?

* **Hybrid agent boundary:** clarify partner expectations on what hybrid eval covers vs. BizAI-only eval.

* **Sandbox limits:** define the rate/quota limits that make the sandbox useful without becoming a free production tier.

* **Payments:** what payment flows does BizAI surface (in-conversation checkout, partner billing, both), and what is Gupshup’s role vs. the partner’s?

* **New value-add surfaces:** scope service/token cost optimization, async messages & triggers, copy/clone across multi-business, design-time configurator, and the Gupshup agent library; none are defined in api-strategy.md.

# **10\. Conclusion**

The BizAI partner strategy is deliberately conservative at the contract layer and ambitious above it. By mirroring Meta’s BizAI APIs and delivering them as an extension of the Partner APIs partners already use — over the authentication they already hold — we make adoption almost frictionless. By layering simplified handoff, an eval-and-optimize loop, a reusable connectors ecosystem, and conversation analytics on top, we give partners capabilities they cannot easily build themselves and a clear reason to consume BizAI through Gupshup rather than Meta directly.

***Parity earns the integration. The value-add layer earns the margin.***

*This white paper is derived from and should be read alongside [**api-strategy.md**](http://api-strategy.md) **([https://docs.google.com/document/d/18GuiNy0lyXI6\_WOgxLUWaJZcM5uMScCmcJs9C1USU\_c/edit?usp=sharing](https://docs.google.com/document/d/18GuiNy0lyXI6_WOgxLUWaJZcM5uMScCmcJs9C1USU_c/edit?usp=sharing) )**. Assumptions and open items are flagged inline for internal review.*

[image1]: <data:image/png;base64,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>