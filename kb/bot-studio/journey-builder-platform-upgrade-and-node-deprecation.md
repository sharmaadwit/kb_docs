source_url: https://console-docs.gupshup.io/docs/journey-builder-platform-upgrade-node-deprecation

<!-- kb-golden:v9 -->
# Journey Builder Platform Upgrade & Node Deprecation

**Module**: Bot Studio

## Definition
As part of our efforts to enhance the Journey Builder platform, Gupshup is transitioning all projects to a more modern and scalable infrastructure. This document outlines upcoming node updates, deprecations, user-facing changes, and next steps for all customers and partners.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journey Builder

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Journey Builder**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Once migrated, projects cannot be reverted to JB V2

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Journey Builder**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Journey Builder Platform Upgrade & Node Deprecation

**Module**: Bot Studio

## Overview
As part of our efforts to enhance the Journey Builder platform, Gupshup is transitioning all projects to a more modern and scalable infrastructure. This document outlines upcoming node updates, deprecations, user-facing changes, and next steps for all customers and partners.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
As part of our efforts to enhance the Journey Builder platform, Gupshup is transitioning all projects to a more modern and scalable infrastructure. This document outlines upcoming node updates, deprecations, user-facing changes, and next steps for all customers and partners.

## 📅 Effective From: Post Console 19.0 Release

A deprecation notice will begin appearing in the Console UI Journey listing page for the following legacy nodes:

These nodes will continue to work temporarily, but will be fully deprecated in a future release. (Tentative Dates will be notified on the UI once decided). Sufficient time will be provided for migration.

## Sample Screenshots of the Notice:

Notice on the Journey Listing Page

After Clicking View Effected Journeys

Journey Canvas with deprecated node

Project that doesn't contain any deprecated node(s)

Note: The notice will show on reload of the page even if the Project doesn't contain any deprecated nodes. Please ignore for such cases.

## 🔄 Migration Pathways

### 🧩 Use Alternate Nodes in JB V2

If your journey uses simple logic or API integrations, you can refactor your journeys using:

- Expression Library in Modify Variable node for manipulating runtime data
- JSON Handler node for parsing API responses or JSON Objects
- New Message-Type Nodes (Audio, Sticker, etc.) for sending WA specific message types
These features are available within JB V2(Newer Version) and require no code or migration support. Reach out to console-support@gupshup.io for upgrading your project to JB V2.

## 🚀 Upgrading to JB Pro (For Advanced Use Cases)

Projects that rely on custom logic or backend execution (via Code Node) can be migrated to JB Pro.

### Key Notes:

- JB Pro supports Function Nodes built on Gupshup's Solutions Platform
- Migration is done only for projects managed by Gupshup Devs
- A migration script will be used to replace Code Nodes with Function Nodes
- Manual pre- and post-migration testing will be conducted by the Bot Solutions team
- Once migrated, projects cannot be reverted to JB V2
- JB Pro projects will be maintained and upgraded by Gupshup Bot Solutions only
- 📩 If your project is managed by Gupshup, please contact your Project Manager or CSM to initiate the JB Pro upgrade.
- ⚠️ Projects managed by customers directly are not eligible for JB Pro migration at this time.
## ✅ Next Steps for Users

- Review your journeys: Check for usage of deprecated nodes.
- Refactor using JB V2 nodes: Use Expression Library, JSON Handler, and message-type nodes wherever possible.
- Contact Support: If you require help with identifying deprecated node usage or migration options.
Stay updated: Final deprecation timeline and enforcement dates will be shared soon!

### 📘 Need Help?

Contact: console-support@gupshup.io

For JB Pro upgrades: Reach out to your Project Manager or Customer Success Manager (CSM)

We encourage you to begin reviewing and refactoring your journeys now to avoid last-minute migration or journey failures when the final deprecation goes live.

Thank you for your continued support.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 7 months ago
