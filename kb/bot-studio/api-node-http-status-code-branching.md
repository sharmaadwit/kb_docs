source_url: https://console-docs.gupshup.io/docs/api-node-http-status-code-branching

<!-- kb-golden:v4 -->
# API Node: HTTP Status Code Branching

**Module**: Bot Studio

## Definition
Lets you route bot logic differently based on API's HTTP response codes (e.g., 200 OK vs 500 Error).

## Procedure
### Exact path
Gupshup Console → Bot Studio → API Node: HTTP Status Code Branching

### Where to configure it
Gupshup Console → Bot Studio → API Node: HTTP Status Code Branching

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → API Node: HTTP Status Code Branching**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- Set up your API call and test connection

## Available options
- 🧭 How to Use
- Set up your API call and test connection
- Toggle ON the “HTTP Status Code” switch
- Add connectors and tag them with codes like 200, 400, 401, 503

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Lets you route bot logic differently based on API's HTTP response codes (e.g., 200 OK vs 500 Error).
- Customize error response (400/500)

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
# API Node: HTTP Status Code Branching

**Module**: Bot Studio

## Overview
Lets you route bot logic differently based on API's HTTP response codes (e.g., 200 OK vs 500 Error).

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## 📌 What is it?

Lets you route bot logic differently based on API's HTTP response codes (e.g., 200 OK vs 500 Error).

### 🧭 How to Use

#### Step 1: Add & Configure API Node

- Set up your API call and test connection
#### Step 2: Enable Status Code Branching

- Toggle ON the “HTTP Status Code” switch
- Add connectors and tag them with codes like 200, 400, 401, 503
#### Step 3: Connect Branches

- Route connectors to different nodes
- Untagged responses follow fallback
### 🧩 Use Cases

- Retry payment (503/504)
- Handle auth failure (401)
- Customize error response (400/500)

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
