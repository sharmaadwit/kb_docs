# BizAI for Partners Onboarding

## Prerequisites

Before onboarding to BizAI, you must have:

1. **Existing Gupshup Partner API integration**
   - Valid auth token
   - WABA setup complete
   - Message sending/receiving working

2. **BizAI Premium tier** enabled in your account
   - Tier-based access (contact sales)

## Step-by-Step Onboarding

### 1. Create an Agent

Define your agent via API or dashboard:

```bash
curl -X POST https://api.gupshup.io/agents \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "customer-support",
    "instructions": "You are a helpful support agent...",
    "escalation_rules": {...}
  }'
```

Response includes `agent_id`.

### 2. Load Knowledge Sources

Upload documents, FAQs, product catalogs:

```bash
curl -X POST https://api.gupshup.io/agents/{agent_id}/knowledge \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "knowledge=@faq.pdf" \
  -F "knowledge=@products.json"
```

Knowledge indexing is **asynchronous**; expect 2-5 minutes.

### 3. Define Escalation Rules

Specify when to hand off to humans:

```bash
curl -X PATCH https://api.gupshup.io/agents/{agent_id} \
  -d '{
    "escalation_rules": {
      "keywords": ["complaint", "refund", "error"],
      "confidence_threshold": 0.65,
      "escalation_queue": "support_team"
    }
  }'
```

### 4. Configure Connectors (Optional)

Connect external systems:

```bash
curl -X POST https://api.gupshup.io/agents/{agent_id}/connectors \
  -d '{
    "connectors": [
      {
        "name": "order-api",
        "endpoint": "https://api.partner.com/orders",
        "auth_token": "..."
      }
    ]
  }'
```

Test connector connectivity:

```bash
curl -X GET https://api.gupshup.io/agents/{agent_id}/connectors/order-api/health
```

### 5. Test in Sandbox

Use test WABA numbers to validate agent behavior:

```bash
# Test a customer query
curl -X POST https://api.gupshup.io/messages/agent \
  -d '{
    "agent_id": "{agent_id}",
    "phone_number": "+1234567890",  # Test number
    "message": "What is my order status?"
  }'
```

Check response quality, connector calls, escalation logic.

### 6. Request Production Approval

When ready, request production access:

```bash
curl -X POST https://api.gupshup.io/agents/{agent_id}/request_production_approval \
  -d '{
    "reason": "Agent tested and validated in sandbox",
    "expected_volume": "10k messages/month"
  }'
```

Gupshup reviews for:
- Safety (no harmful instructions)
- Compliance (data privacy, regulatory)
- Quality (escalation logic, knowledge quality)

Approval typically takes **24-48 hours**.

### 7. Go Live with Gradual Rollout

Once approved, roll out incrementally:

**Week 1:** Route 5% of customer numbers to agent
```bash
curl -X PATCH https://api.gupshup.io/agents/{agent_id} \
  -d '{ "rollout_percentage": 5 }'
```

**Week 2:** Monitor metrics
```bash
curl -X GET https://api.gupshup.io/agents/{agent_id}/metrics?period=week
```

Response:
```json
{
  "resolution_rate": 0.85,
  "escalation_rate": 0.15,
  "customer_satisfaction": 4.1
}
```

**Week 3+:** Increase to 25%, 50%, 100% based on metrics

## No Migration Required

Partners do not need to re-integrate authentication or message handling. BizAI seamlessly routes AI-bound messages through your existing Partner API without disrupting production traffic.

## Support & Iteration

During and after onboarding:

- **Eval-and-optimize dashboard** shows what's working and what's not
- **Weekly metric reviews** with Gupshup support team
- **Prompt iteration** recommended based on failure mode detection
- **Knowledge base updates** deployed without re-approving the agent

---

See also:
- [[bizai-api-endpoints]] — API reference
- [[bizai-value-add]] — What you get at each stage
- [[bizai-pricing]] — Costs
