source_url: https://console.gupshup.io/rcs/google-search-p2a

<!-- kb-golden:v10 -->
# RCS Google Search Entry Point (Search to Chat / P2A)

**Module**: Channels

## Definition

Search to Chat (also called P2A — Person to Agent) lets users start an RCS conversation with a brand directly from Google Search results. When a user searches for a brand on Google, a chat button appears that opens the brand's RCS agent in the native Messages app.

---

## What is a P2A Conversation?

A P2A conversation is user-initiated. It starts when the brand's RCS agent responds (within 24 hours) to a P2A message that arrived through an entry point — such as a QR code, a deeplink URL, or a Google Search surface — outside any existing conversation.

---

## Prerequisites

To enable Search to Chat, the following must be in place:

1. RCS agent status is **Launched**
2. Console postpaid onboarding complete (GG enterprise account, project mapped)
3. A conversational journey built in Bot Studio (Journey Builder)
4. CX Analytics enabled

Google review and go-live takes approximately **4–5 business days** after submission.

---

## Typical P2A Workflows by Vertical

| Vertical | Priority P2A workflows |
|----------|----------------------|
| Retail | Product discovery and browsing, personalised recommendations, direct in-thread purchasing |
| Professional services | Automated service inquiries, appointment booking, re-engagement campaigns |
| Auto | Test drive booking, real-time dealer inventory checks, automated follow-ups |
| Finance | Product comparisons, lead qualification and applications, account protection alerts |

---

## Setting Up the RCS Journey (via Superagent)

Gupshup's RCS Journey Generator (available in AI Admin and Superagent) can generate a complete RCS conversational flow from a brand brief or requirement document.

1. Migrate the project to Console if it is not already there.
2. Upgrade Bot Studio > Journeys to JB Pro.
3. Open [superagent.gupshup.ai](https://superagent.gupshup.ai/) and enter a prompt describing the brand's journey requirement. Upload the brand's journey document.
4. Superagent generates the RCS conversational flow and rich messaging artifacts.
5. Add a Goal node to the deployed journey.
6. Enable CX Analytics.

**Example prompt:**
> `Create an end-to-end RCS journey for "Zigly" based on the attached journey document. AI Admin Project ID: 31575126`

Note: The AI Admin Project ID is the same as the Console project ID.

---

## Why This Matters

- 96% of mobile searches start on Google Search — a Search to Chat button gives brands a direct conversation entry point at the moment of intent.
- Users stay in their native Messages inbox, with no app download required.
- Brands live with Search to Chat in India include CARS24, Swiggy, and MamaEarth.

---

## Related docs

- rcs-console-agent-setup.md for launching the RCS agent
- rcs-overview.md for RCS channel capabilities
- rcs-best-practices.md for conversational design guidance
