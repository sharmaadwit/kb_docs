source_url: internal

<!-- kb-golden:v10 -->
# CC Express vs Conversation Cloud (Console)

**Module**: Overview

## Definition

CC Express and Gupshup Console (Conversation Cloud) are the same underlying platform. They are not different products — the difference is billing model, target customer, and which advanced features are enabled.

## Billing model

- **CC Express**: prepaid wallet billing only. Customers recharge a wallet balance and usage is deducted from it.
- **Console (Conversation Cloud)**: postpaid billing by default (invoiced). Console no longer supports wallet billing as a standard option — going forward, all prepaid/wallet customers are provisioned on CC Express.
  - Exception: an existing Console client that specifically needs wallet billing can have it enabled on request. This is a manual, case-by-case exception, not the default for Console.

## Target audience

- **CC Express**: SME (small/medium business) and self-serve customers who sign up and configure their own account without a managed onboarding process.
- **Console (Conversation Cloud)**: enterprise customers, typically with a managed relationship (Sales, Solutions, or Customer Success involvement).

## Feature availability

CC Express does **not** include features gated behind:

- **JB Pro (Journey Builder Pro)** — the developer-grade Journey Builder tier. JB Pro is not self-serve; it's only provisioned for internal Gupshup Bot Solutions teams building managed/enterprise bot workflows (Function Node, database/SQL access, Clear Context Node, Dynamic Image URL Node, and similar advanced nodes are JB Pro–only). See [Gupshup Journey Builder: Legacy vs V2 vs Pro](../bot-studio/gupshup-journey-builder-legacy-vs-v2-vs-pro.md).
- **Developer access / Developer Mode–gated features** — advanced AI Admin capabilities (Settings, AI Agents, AI Agent Guardrails, Skills, Agent Personality, Website Re-training Scheduler, Skill Prompt Enhancer, and similar) that require Gupshup Support or a Sales representative to enable.

**CC Express includes JB V2**, referred to interchangeably as **"JB Lite"** in some places — this is the standard no-code/low-code Journey Builder available to self-serve customers, and is the same JB V2 documented elsewhere in this KB.

## Quick comparison

| | CC Express | Console (Conversation Cloud) |
|---|---|---|
| Billing | Prepaid wallet | Postpaid (invoiced) by default; wallet only on request |
| Audience | SME / self-serve | Enterprise / managed |
| Journey Builder | JB V2 ("JB Lite") | JB V2 by default; JB Pro available only via internal Gupshup Bot Solutions provisioning |
| Developer Mode features | Not available | Available on request via Gupshup Support / Sales |

## Module disambiguation docs

- CC Express and Console are the same product family (Conversation Cloud) — do not treat them as separate platforms with separate documentation. Module-level docs (Bot Studio, Channels, Campaign Manager, etc.) apply to both unless a feature is explicitly called out as JB Pro–only or Developer Mode–only, in which case it is Console-only (and even then, only when specifically provisioned).
