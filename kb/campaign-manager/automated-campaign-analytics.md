source_url: https://console-docs.gupshup.io/docs/automated-campaign-analytics

<!-- kb-golden:v9 -->
# Automated Campaign analytics

**Module**: Campaign Manager

## Definition
Use **Automated Campaign analytics** to measure automated campaign performance at two levels:
- **Message Analytics** (aggregate across multiple WhatsApp Template nodes)
- **Template node analytics** (template-level stats per message step)

**Where to see campaign analytics for automated campaigns**: open **Campaign Manager → Automated Campaign analytics**.

## Procedure
### Exact UI path
Gupshup Console → Campaign Manager → Automated Campaign analytics

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Go to **Automated Campaign analytics**.
4. Select the automated campaign execution you want to analyze.
5. Review **Message Analytics** (aggregate delivery and engagement metrics).
6. Drill down into a **WhatsApp Template node** to view template-level stats.
7. (Optional) Download response files at the aggregate level (About section) and template level.

### Validation / where to check
- Run a small automated campaign and confirm analytics populate after completion.

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- No save action is required; this is a reporting/analytics view.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Campaign Manager**.
- Go to **Automated Campaign analytics**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).

## Reference (from source)
<!-- procedural:v2 -->
# Automated Campaign analytics

**Module**: Campaign Manager

## Overview
For each completed Automated Campaign we show analytics in 2 levels:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
For each completed Automated Campaign we show analytics in 2 levels:

- Message Analytics: This shows aggregate analytics across multiple WhatsApp Template nodes
- WhatsApp Template node analytics: For each WhatsApp message used while the Automated Campaign is created we can see Template level stats.
Response files can also be downloaded at an aggregate (About section) and Template level.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
