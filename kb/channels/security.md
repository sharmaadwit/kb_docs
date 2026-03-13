source_url: https://console-docs.gupshup.io/docs/web-security

<!-- kb-golden:v9 -->
# Security

**Module**: Channels

## Definition
You can secure your Web chat widget by whitelisting domains in the Preferences tab.

## Procedure
### Exact UI path
Gupshup Console → Channels → Security

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Security**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **Security**.

## Options / variants
- You can switch on the Enable Security toggle for restricting the messaging to the whitelisted domains.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Security

**Module**: Channels

## Overview
You can secure your Web chat widget by whitelisting domains in the Preferences tab.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
You can secure your Web chat widget by whitelisting domains in the Preferences tab.

### By default, security is disabled i.e. messaging will be functional in the chat widget on all domains.

You will need to enable security in the Security settings to restrict messaging.

- You can switch on the Enable Security toggle for restricting the messaging to the whitelisted domains.
- You can enter the domain you wish to whitelist and click Add. The added domain will appear in the List Of Domains table.
- If you add a page URL or link, the domain of that page will be extracted and whitelisted automatically.
All subdomains (for example, console.gupshup.io) will be whitelisted along with the domain (gupshup.io).

- You can delete an added domain using the delete icon under the Action column in the List Of Domains table.
Updated 10 months ago

- Retain Customer Chat History

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
