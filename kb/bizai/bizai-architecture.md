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

## Integration Points

- **Agent Configuration** — Define knowledge sources, instructions, connectors
- **Message Routing** — Automatic routing to BizAI or partner module based on rules
- **Escalation** — Seamless handoff to human agents when needed
- **Session Context** — Full conversation history available for resolution

See also:
- [[bizai-value-add]] — What makes Gupshup's BizAI different
- [[bizai-api-endpoints]] — API endpoints for agent management
- [[bizai-onboarding]] — How to get started
