source_url: https://console-docs.gupshup.io/docs/api-node-http-status-code-branching

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
