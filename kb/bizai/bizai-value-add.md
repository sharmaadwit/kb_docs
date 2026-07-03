# Gupshup BizAI Value-Add Capabilities

Gupshup delivers differentiated value on top of Meta's BizAI API. These four capabilities are **not available** in Meta's raw APIs.

## 1. Simplified Handoff

**Seamless transition** between automated BizAI agent and human support teams, abstracted from the partner.

- Agent routes customers to humans without partner code changes
- Human agents see full conversation context and agent analysis
- Whichever team handles the issue (agent or human), customer experience is consistent
- No custom integration needed; handled transparently by Gupshup

**Use case:** Customer asks for something outside agent scope → agent recommends escalation → human agent takes over with full context.

## 2. Eval-and-Optimize Loop

**Continuous improvement pipeline** so partners can measure agent accuracy, identify failure modes, and iterate on prompts and knowledge.

- Performance metrics dashboard (resolution rate, escalation rate, customer satisfaction)
- Automated failure mode detection (what types of questions cause escalation?)
- Iteration recommendations from Gupshup's ML models
- A/B testing support for prompts and knowledge updates

**Use case:** Monitor agent performance weekly, identify top 5 failure modes, update knowledge base, measure improvement in next iteration.

## 3. Multi-Channel Deployment

**Deploy once, run everywhere.** Partners author an agent once and deploy it across multiple channels with minimal changes.

Supported channels:
- WhatsApp
- SMS
- Email
- Web widget

Same agent logic, same knowledge base, same escalation rules — just different transport layers.

**Use case:** Train agent on WhatsApp, then instantly activate it on SMS for emergency notifications and email for follow-ups.

## 4. Extensibility via Connectors

**Plug in custom data sources and third-party tools** without Gupshup becoming the integration bus.

Partners can connect:
- Custom APIs and internal systems
- CRM systems (Salesforce, HubSpot)
- Helpdesk platforms (Zendesk, Jira Service Management)
- Payment processors (Stripe, Razorpay)
- Custom data sources (knowledge bases, product catalogs)

**How it works:**
- Partner defines connectors in agent config
- Agent can call connectors to fetch data, execute actions, trigger workflows
- Responses are fed back to agent for synthesis

**Use case:** Agent answers "What's my order status?" by calling your order API, then "When does it arrive?" by calling your shipping provider's API.

## Why This Matters

Meta's BizAI is powerful but generic. Gupshup adds the **operational layer** that partners need:
- Real people still exist in your business → handoff must be effortless
- Agents need to improve over time → visibility + iteration tools are essential
- Partners sell to multiple channels → reuse is critical
- Partners have existing systems → integration must be flexible, not invasive

See also:
- [[bizai-api-endpoints]] — How to configure these capabilities
- [[bizai-onboarding]] — Getting started
- [[meta-business-agent]] — What Meta's BizAI offers
