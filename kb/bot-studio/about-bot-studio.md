source_url: https://console-docs.gupshup.io/docs/about-bot-studio

<!-- kb-golden:v4 -->
# About Bot Studio

**Module**: Bot Studio

## Definition
Bot Studio is Gupshup’s visual, no-code/low-code platform that empowers users to design, build, and deploy intelligent conversational journeys across messaging channels like WhatsApp, Web, and Instagram.

## Procedure
### Exact path
Gupshup Console → Bot Studio → About Bot Studio

### Where to configure it
Gupshup Console → Bot Studio → About Bot Studio

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → About Bot Studio**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- 1. Journey Builder (V2)
- 2. Journey Builder Pro
- JB Pro is not available for self-serve users.
- ❌ Deprecated / Replaced Nodes:
- ⚙️ Other Changes:
- Developer Mode toggle → Removed

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
# About Bot Studio

**Module**: Bot Studio

## Overview
Bot Studio is Gupshup’s visual, no-code/low-code platform that empowers users to design, build, and deploy intelligent conversational journeys across messaging channels like WhatsApp, Web, and Instagram.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## What is Bot Studio

Bot Studio is Gupshup’s visual, no-code/low-code platform that empowers users to design, build, and deploy intelligent conversational journeys across messaging channels like WhatsApp, Web, and Instagram.

With an intuitive drag-and-drop canvas, users can craft dynamic bots using modular nodes for messages, prompts, API calls, and conditional logic—without writing a single line of code.

Bot Studio supports:

- Self-serve (DIY) use cases
- Advanced enterprise solutions via internal developer tooling
It is versatile enough for:

- Lead generation
- Customer support
- Campaign automation
- Transactional flows
Whether you're a business user or a developer, Bot Studio provides the tools to deliver scalable, personalized, and engaging customer experiences.

## Bot Studio Versions

Bot Studio is available in two versions depending on the user’s needs and offering type:

### 1. Journey Builder (V2)

Journey Builder V2 is Gupshup’s intuitive, no-code/low-code platform for business teams and GTM users.

Key Features:

- Drag-and-drop builder
- Message, prompt, API, and logic nodes
- Expression Library for advanced data ops
- JSON Handler for parsing API responses
- Rapid setup and deployment
Best suited for:

- Lead capture
- Appointment booking
- Support automation
- Teams looking for self-serve, go-live-fast capabilities
### 2. Journey Builder Pro

Journey Builder Pro is the developer-grade version of JB V2, exclusively for Gupshup’s internal Bot Solutions team.

Includes everything in JB V2, plus:

- Access to Function Node via the Solutions Platform
- Supports custom logic, complex integrations, and real-time data handling
Best suited for:

- Enterprise use cases
- Transactional workflows
- Fully managed projects with internal developer support
### JB Pro is not available for self-serve users.

## ⚠️ Note on Deprecated Nodes and Features

### Starting with Console 16.0, Gupshup has deprecated or replaced several legacy and dev-only nodes in Bot Studio to improve platform stability, performance, and user experience.

### ❌ Deprecated / Replaced Nodes:

- Code Node → Replaced by Function Node (JB Pro only)
- Database Node (RQ Lite) → Deprecated, SQL-based access available via JB Pro
- Send Message Node (generic) → Replaced by dedicated message-type nodes like: Audio Sticker Send Location Address
- Audio
- Sticker
- Send Location
- Address
### ⚙️ Other Changes:

- Clear Context Node → Available on JB Pro
- Dynamic Image URL Node → Available on JB Pro
- Developer Mode toggle → Removed
These changes ensure a simplified, robust experience for JB V2 users, while giving JB Pro developers controlled access to powerful tooling via the Solutions Platform.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
