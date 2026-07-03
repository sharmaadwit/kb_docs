# BizAI for Partners API Endpoints

BizAI for Partners introduces new API endpoints for agent configuration, knowledge management, and session control.

## Agent Management

### Create/Update Agent
```
POST /agents
```

**Body:**
```json
{
  "name": "customer-support-agent",
  "instructions": "You are a helpful customer support agent...",
  "knowledge_sources": ["faq.pdf", "product-catalog.json"],
  "escalation_rules": {
    "keywords": ["complaint", "refund"],
    "confidence_threshold": 0.7
  }
}
```

**Returns:**
- `agent_id` — Unique agent identifier
- `status` — "active" or "paused"

---

## Knowledge Management

### Upload/Link Knowledge Sources
```
POST /agents/{id}/knowledge
```

**Body:**
```json
{
  "sources": [
    {
      "type": "document",
      "url": "s3://bucket/faq.pdf"
    },
    {
      "type": "structured",
      "data": {
        "products": ["SKU-001", "SKU-002"],
        "prices": [9.99, 19.99]
      }
    }
  ]
}
```

**Returns:**
- `knowledge_id` — Indexed knowledge base identifier
- `indexing_status` — "complete" or "in_progress"

---

## Connector Configuration

### Register Third-Party Connectors
```
POST /agents/{id}/connectors
```

**Body:**
```json
{
  "connectors": [
    {
      "name": "order-api",
      "type": "rest",
      "endpoint": "https://api.partner.com/orders",
      "auth": "bearer_token",
      "methods": ["GET /orders/{customer_id}", "POST /orders"]
    },
    {
      "name": "crm",
      "type": "salesforce",
      "instance_url": "https://instance.salesforce.com",
      "oauth_token": "..."
    }
  ]
}
```

**Returns:**
- `connector_id` — Unique connector identifier
- `status` — "active" or "error"
- `health_check` — Last connection test result

---

## Message Processing

### Send Message to Agent
```
POST /messages/agent
```

**Body:**
```json
{
  "agent_id": "customer-support-agent",
  "phone_number": "+1234567890",
  "message": "What's the status of my order?",
  "session_id": "sess_123abc"
}
```

**Returns:**
```json
{
  "response": "Your order #ORD-789 is in transit...",
  "escalated": false,
  "connector_calls": [
    {
      "connector": "order-api",
      "method": "GET /orders/12345",
      "result": {...}
    }
  ]
}
```

---

## Performance & Analytics

### Get Agent Metrics
```
GET /agents/{id}/metrics
```

**Query Parameters:**
- `period` — "day", "week", "month"
- `group_by` — "hour", "day", "intent"

**Returns:**
```json
{
  "resolution_rate": 0.87,
  "escalation_rate": 0.13,
  "avg_response_time": 1.2,
  "customer_satisfaction": 4.2,
  "top_failure_modes": [
    {
      "intent": "refund_request",
      "escalation_rate": 0.45
    }
  ]
}
```

---

### Retrieve Session History
```
GET /sessions/{id}
```

**Returns:**
```json
{
  "session_id": "sess_123abc",
  "customer_phone": "+1234567890",
  "messages": [
    {
      "role": "customer",
      "content": "...",
      "timestamp": "2026-07-03T10:30:00Z"
    },
    {
      "role": "agent",
      "content": "...",
      "timestamp": "2026-07-03T10:30:05Z"
    }
  ],
  "escalation_notes": "Transferred to human agent due to refund request",
  "resolved_by": "human_agent_id"
}
```

---

## Error Handling

All endpoints return standard error responses:

```json
{
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent 'invalid-id' does not exist",
    "details": {}
  }
}
```

Common error codes:
- `AGENT_NOT_FOUND` — Agent ID doesn't exist
- `KNOWLEDGE_INDEXING_FAILED` — Failed to index knowledge source
- `CONNECTOR_UNREACHABLE` — Third-party connector is down
- `RATE_LIMIT_EXCEEDED` — Too many requests
- `INVALID_REQUEST` — Malformed request body

---

See also:
- [[bizai-value-add]] — What these endpoints enable
- [[bizai-onboarding]] — Step-by-step setup
- [[bizai-pricing]] — Cost structure
