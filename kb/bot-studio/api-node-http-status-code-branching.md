source_url: https://console-docs.gupshup.io/docs/api-node-http-status-code-branching
# BOT STUDIO

## API Node: HTTP Status Code Branching

# API Node: HTTP Status Code Branching

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
Updated 10 months ago
