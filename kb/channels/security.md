source_url: https://console-docs.gupshup.io/docs/web-security

<!-- kb-golden:v1 -->
# Security

**Module**: Channels

## Definition
You can secure your Web chat widget by whitelisting domains in the Preferences tab.

## Procedure
### Where to configure it
Gupshup Console → Channels → Security

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Channels → Security**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

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
