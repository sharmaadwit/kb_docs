# BizAI Reference Architecture

## How BizAI Fits Into Your Integration

The Gupshup BizAI reference architecture positions Gupshup as the orchestration layer between the WABA number, the BizAI engine, and the partner's own module.

### Architecture Points

**1. Message Flow**
- End-user traffic flows over WhatsApp to the WABA number as today
- AI-bound messages reach BizAI through Gupshup
- Regular messages are handled by the partner's module as before

**2. Agent Operating Modes**
BizAI can operate in different modes depending on your use case:

- **Autonomous** — Full agent control; agent responds directly to customer
- **Human-in-the-loop** — Agent recommends, human confirms before sending
- **Hybrid** — Agent escalates to human when uncertain or for complex issues

**3. Session State Management**
- Session state and conversation history are stored in Gupshup
- Surfaced to both BizAI and the partner's system
- Enables context-aware handoffs and multi-turn conversations

### Data Flow Diagram

```
┌─────────┐
│ Customer│ ← WhatsApp Message
│ (WhatsApp)
└────┬────┘
     │ WABA Number
     ▼
┌──────────────────┐
│  Gupshup         │ (Orchestration Layer)
├──────────────────┤
│ ┌──────────────┐ │
│ │ Session Mgmt │ │ (Stores conversation context)
│ │ & History    │ │
│ └──────────────┘ │
└──────┬──────┬────┘
       │      │
    ┌──▼──┐  │
    │ BizAI│  │
    │Engine│  │
    └──▼──┘  │
       │      │
       │      └────────────────┐
       │                       │
       ▼                       ▼
┌──────────────┐        ┌──────────────┐
│Partner Module│        │Human Support │
│(Handle msgs) │        │(Handle escalations)
└──────────────┘        └──────────────┘
```

## How BizAI Integrates with Your Partner API

BizAI doesn't replace your Partner API — it **extends it** with new endpoints for agent management.

### Your Current Partner API Integration
You have:
- Authentication (Bearer token)
- WABA setup (phone number ID, business account ID)
- Message send/receive working
- Webhook handling for incoming messages

### BizAI Adds New Endpoints
On top of your existing integration, BizAI provides:

```
POST /agents                    Create and configure agents
POST /agents/{id}/knowledge     Add knowledge sources
POST /agents/{id}/connectors    Register third-party connectors
POST /messages/agent            Send message to agent
GET /agents/{id}/metrics        Get performance analytics
GET /sessions/{id}              Retrieve conversation history
```

### Message Routing
When a customer message arrives:

1. **Parse the message** (existing Partner API webhook)
2. **Determine routing** (new BizAI logic):
   - If BizAI agent is enabled → `POST /messages/agent`
   - If regular partner module → handle as before
3. **Return response** (agent response or partner module response)
4. **Store context** (Gupshup stores conversation in session)

### No Code Migration Required
Your existing Partner API code keeps working. You add BizAI configuration separately:

```javascript
// Your existing code still works
app.post('/webhooks/whatsapp', (req, res) => {
  const message = req.body.message;
  // ... your code
});

// Add BizAI agent config (new)
const agent = await fetch('POST /agents', {
  headers: { 'Authorization': 'Bearer ' + token },
  body: {
    name: 'support-agent',
    knowledge_sources: [...],
    escalation_rules: {...}
  }
});
```

### Connector Integration
Third-party integrations (CRM, order API, payment processor) are configured via BizAI's connector system, not via your Partner API integration:

```
POST /agents/{agent_id}/connectors
{
  "connectors": [
    {"name": "salesforce", "endpoint": "..."},
    {"name": "order-api", "endpoint": "..."}
  ]
}
```

The agent calls these connectors directly — no changes to your Partner API code needed.

## Integration Points

- **Agent Configuration** — Define knowledge sources, instructions, connectors via BizAI endpoints
- **Message Routing** — Automatic routing to BizAI or partner module based on agent rules
- **Escalation** — Seamless handoff to human agents when needed (handled by agent config)
- **Session Context** — Full conversation history available for resolution (stored in Gupshup)
- **Connector Calls** — Third-party integrations happen at the agent level, not the Partner API level

## Key Concept: "New Endpoints on Existing API"

BizAI is delivered as **new endpoints** on your existing Partner API, not a separate platform. This means:

✅ **Keep** your auth tokens, WABA setup, webhook handlers  
✅ **Add** BizAI agent endpoints for configuration and management  
✅ **No migration** of existing message handling code  
✅ **Incremental adoption** — start with one agent, scale gradually

See also:
- [[bizai-value-add]] — What makes Gupshup's BizAI different
- [[bizai-api-endpoints]] — Complete endpoint reference
- [[bizai-onboarding]] — Step-by-step integration guide
