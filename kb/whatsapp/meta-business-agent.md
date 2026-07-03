# Meta Business Agent

Meta Business Agent is an **enterprise AI platform** that automates customer interactions on WhatsApp.

## What It Does

The Meta Business Agent acts as a **first-point-of-contact agent** that:
- Answers customer questions automatically
- Executes transactions and workflows
- Routes complex issues to humans with full context
- Operates 24/7 without human intervention

It's designed to handle high-volume, repetitive customer queries while escalating anything outside its scope.

## Core Capabilities

### 1. Knowledge-Based Responses

Load business information to inform agent responses:
- FAQ documents and knowledge bases
- Website content and product information
- Structured data (product catalogs, pricing tables)
- Customer account information

The agent synthesizes knowledge into natural-language responses.

### 2. Action Execution

Connect external APIs and tools so the agent can:
- Fetch data (order status, account balance, shipping info)
- Process transactions (refunds, password resets, bookings)
- Trigger workflows (send confirmation email, create support ticket)
- Call third-party services (payment processors, logistics, CRM)

### 3. Intelligent Escalation

Automatically detect when an issue exceeds agent scope:
- Confidence scoring on agent responses
- Keyword-based escalation triggers (refund, complaint, error)
- Route to human agents with full conversation context
- Prevent escalation of repetitive, resolvable issues

## Customization

Each agent can be customized with:
- **Business-specific instructions** — "You are a bank support agent, prioritize account security"
- **Tone guidelines** — Professional, friendly, formal, casual
- **Allowed actions** — Refunds up to $500, password resets only, etc.
- **Language** — Multi-language support built-in
- **Operating scope** — Which topics the agent handles vs. escalates

## Multi-Number Support

A single Meta Business Agent can operate across:
- Multiple WhatsApp phone numbers managed by one business account
- Consistent behavior and knowledge base across all numbers
- Unified analytics and session history

## How It Differs from ChatGPT

| Aspect | Meta Business Agent | Generic LLM (ChatGPT) |
|--------|-------------------|----------------------|
| **Knowledge** | Business-scoped (FAQs, product data, customer info) | General knowledge only |
| **Actions** | Can execute transactions, call APIs | Can only provide information |
| **Escalation** | Automatic handoff to humans | No human integration |
| **Compliance** | Built for regulated industries (banking, healthcare) | Not designed for compliance |
| **Cost** | Pay-per-token (cheap at scale) | Variable, often expensive |
| **Customization** | Business rules, tone, scope | Prompt engineering only |

## Use Cases

**Financial Services**
- Check account balance or transaction history
- Request account statements or tax documents
- Reset passwords and update security settings
- Escalate fraud disputes to specialized teams

**E-Commerce**
- Check order status and shipping updates
- Process returns and refunds (within policy)
- Answer product questions and recommendations
- Handle customer complaints escalation

**Telecom**
- Check bill and usage
- Activate/deactivate features
- Update contact information
- Escalate billing disputes

**Customer Support**
- Triage incoming issues
- Provide self-service solutions
- Route high-priority issues to specialists
- Handle follow-ups on resolved tickets

---

See also:
- [[bizai-value-add]] — How Gupshup adds value to Meta's agent
- [[whatsapp-pricing]] — Meta's pricing for agent messages
- [[bizai-onboarding]] — Getting started with BizAI for Partners
