source_url: https://console-docs.gupshup.io/docs/gupshup-journey-builder-legacy-vs-v2-vs-pro

<!-- kb-golden:v4 -->
# Gupshup Journey Builder: Legacy vs V2 vs Pro

**Module**: Bot Studio

## Definition
Gupshup’s Journey Builder (JB) platform has evolved through multiple versions to address different user segments and technical requirements. The three key versions are:

## Procedure
### Exact path
Gupshup Console → Bot Studio → Gupshup Journey Builder: Legacy vs V2 vs Pro

### Where to configure it
Gupshup Console → Bot Studio → Gupshup Journey Builder: Legacy vs V2 vs Pro

### Prerequisites
- Gupshup’s Journey Builder (JB) platform has evolved through multiple versions to address different user segments and technical requirements. The three key versions are:

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Gupshup Journey Builder: Legacy vs V2 vs Pro**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- Test Bot and Inline Message Logs: Enable debugging directly within the canvas.

## Available options
- 3.1 JB Legacy
- 3.2 JB V2
- 3.3 JB Pro

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Gupshup Journey Builder: Legacy vs V2 vs Pro

**Module**: Bot Studio

## Overview
Gupshup’s Journey Builder (JB) platform has evolved through multiple versions to address different user segments and technical requirements. The three key versions are:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## 1. Overview

Gupshup’s Journey Builder (JB) platform has evolved through multiple versions to address different user segments and technical requirements. The three key versions are:

Version

Description

Target User

JB Legacy (Deprecated)

Original version supporting Code Node and developer-oriented flexibility.

Developers, technical users.

JB V2

Current default version with a modern no-code/low-code interface focused on simplicity and automation.

Business users, GTM teams, DIY builders.

JB Pro

Developer-grade version designed for internal Gupshup teams building complex, enterprise-grade bot workflows.

Internal Gupshup Bot Solutions developers.

Each version is designed to balance usability and flexibility based on the type of project being built.

Journey Builder (JB) Legacy is officially deprecated and should not be used for any new projects going forward.

Starting with Console 16.0 and subsequent releases, all new projects are provisioned on JB V2 by default.

Projects created on the Legacy version and containing code node will eventually require manual migration to JB V2 or JB Pro, depending on their feature usage.

Continuing to use JB Legacy will lead to additional rework, migration overhead, and potential downtime in the future.

To ensure long-term platform compatibility, maintainability, and access to the latest features, all new bot journeys must be built using JB V2 (or JB Pro for managed enterprise deployments).

## 2. Key Differentiators

## 3. Platform Intent and Use Cases

### 3.1 JB Legacy

Who it was for: Developers and technical teams building advanced bots using JavaScript and backend logic.

Key Features:

- Direct use of Code Node for writing JavaScript.
- Support for Database Node (RQ Lite), Send Message, Clear Context, and Dynamic Image nodes.
- Developer Mode for custom node configurations.
Limitations:

- High maintenance and risk of performance inconsistencies.
- Deprecated in favor of JB V2 and JB Pro.
Best suited for:

- Highly customized bots with backend integrations.
- Complex use cases involving external databases or logic layers.
Status: Being phased out after Console 17.0. Projects using no code nodes are automatically migrated to JB V2.

### 3.2 JB V2

Who it’s for: Business users, marketing teams, and GTM teams who want to build bots independently with minimal or no coding.

Core Philosophy: To enable no-code journey design with powerful data handling through visual interfaces and expression-based logic.

Key Features:

- Expression Library: Over 170 built-in expressions for data manipulation, conditions, and operations inside the Modify Variable node.
- JSON Handler Node: Simplifies parsing of API responses without code.
- Dedicated Message Nodes: Supports message types like Audio, Sticker, Send Location, and Address.
- Block Templates: Allows reusable components across projects.
- Test Bot and Inline Message Logs: Enable debugging directly within the canvas.
- Support for AI-based journey triggers and multilingual design.
- Bot Constants: Define global constants like pricing, discounts, and dates that can be used across journeys.
Limitations:

- Does not support Function Nodes or database integrations.
- Not intended for highly technical or logic-intensive workflows.
Best suited for:

- DIY bot builders and business teams.
- Lead generation, appointment booking, customer support automation, or campaign bots.
Access: Default for all new Console projects and available to clients and GTM teams.

### 3.3 JB Pro

Who it’s for: Internal Gupshup developers building managed, enterprise-grade solutions that require backend logic, integrations, and custom handling.

Core Philosophy: Combines the simplicity of JB V2 with developer-grade capabilities through the Solutions Platform.

Key Features:

- Includes all features from JB V2.
- Function Node: Replaces Code Node for advanced backend logic and computation.
- Database Access: Supports SQL database integration.
- Send Message and Clear Context Nodes: Available and fully supported.
- Full integration with the Solutions Platform for scalable and secure backend logic.
- Designed for projects that require API chaining, dynamic data handling, or transactional workflows.
Limitations:

- Not available for client self-serve access.
- Only used by internal Gupshup Bot Solutions teams.
- Downgrade to JB V2 is not supported once upgraded.
Best suited for:

- Enterprise solutions requiring complex data manipulation and external integrations.
- Managed service projects handled by Gupshup developers.
Access: Available only to internal Gupshup development teams via Solutions Platform.

## 4. Migration Path and Rules

## 5. Choosing the Right Journey Builder Version

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 4 months ago
