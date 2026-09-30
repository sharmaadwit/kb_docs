source_url: https://console.gupshup.io/rcs/agent-setup

<!-- kb-golden:v10 -->
# RCS Agent Setup via Gupshup Console

**Module**: Channels

## Definition

How to create, verify, and launch an RCS agent from the Gupshup Console for postpaid accounts. The agent must reach Launched status before it can send live traffic through campaigns, Bot Studio, or Agent Assist.

---

## Prerequisites

Before creating the agent in Console:

- Console project exists with an RCS-enabled recipe (e.g. CX Standard + RCS)
- Org is on postpaid and upgraded to Golden Gate (GG)
- Enterprise RCS account has been mapped to the project by the onboarding team
- Assets ready to upload: brand logo, banner image, privacy policy URL, terms URL

**Information to collect from the client before kick-off**

- Brand name, agent (bot) name, logo, and banner image
- Agent description, website, support email and phone
- Privacy policy URL and terms & conditions URL
- Use case and traffic type: Transactional, Promotional, or OTP

---

## Steps in Console

1. Open **Channels > RCS** and click **Get Started** (shown when no agent exists yet).
2. Fill in the agent details and select carriers, then submit. Console shows that agent creation is in progress.
3. When the agent and its credentials (client ID and client secret) are generated, the **Agent Details** and **Test Devices** tabs appear.
4. Add test devices and verify the agent on real handsets.
5. Click **Submit for verification and launch**.
6. When the selected carriers approve, Console marks the agent **Launched**.

---

## Agent Status Reference

| Status | Meaning | What you can do |
|--------|---------|----------------|
| Created | Agent exists; credentials generated | Test on registered test devices only |
| Submitted | Sent for carrier verification and launch | Continue testing; wait for carrier approval |
| Launched | Live on all selected carriers | Send live traffic: campaigns, Bot Studio, Agent Assist, API |

---

## iOS Reach (India only)

In India, the agent that delivers to iOS devices is launched exclusively on Jio. This is configured during onboarding automation and is not a separate agent creation step.

Jio enables iOS traffic at its discretion, based on the brand's traffic volume and engagement metrics on its Android agent. A brand must first send substantial traffic through the Jio Android agent before becoming eligible for iOS delivery.

---

## Key Constraints

- **One RCS agent per Console project.** A project cannot have two RCS agents.
- **GG accounts only.** RCS and WhatsApp each have separate GG enterprise accounts. A client on a non-GG WhatsApp account must be migrated to GG before RCS can be enabled.
- Before the agent reaches Launched, messages can only be sent to registered test devices.

---

## Related docs

- rcs-overview.md for channel capabilities
- rcs-console-templates.md for creating templates after the agent is launched
- rcs-console-campaigns.md for sending broadcast campaigns
- rcs-prerequisites-checklist.md for the full onboarding checklist
