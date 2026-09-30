source_url: https://console.gupshup.io/rcs/faq

<!-- kb-golden:v10 -->
# RCS Console Operations — Troubleshooting and FAQ

**Module**: Channels

## Definition

Common issues and answers for RCS on Gupshup Console postpaid accounts. Covers delivery failures, agent setup problems, campaign issues, and iOS reach questions.

---

## Delivery Failure Codes

| Code | Reason | What to do |
|------|--------|-----------|
| 400 | Invalid template or parameter mismatch | Check the template code and verify every variable is passed |
| 404 | RCS not enabled on the user's device | Expected for non-RCS users; use fallback to SMS or WhatsApp |
| 409 | Template not approved and user is not in an active conversation | Get the template approved, or send only inside the 24-hour window after a user reply |
| 410 | User opted out | Do not resend; the user must send an opt-in keyword to re-subscribe |
| 429 | Promotional limit exceeded | Monthly per-user promotional limit reached; wait until the next month or the user replies |
| 451 | Outside permitted business hours | Promotional sends in India are only allowed between 7am and 10pm IST |
| 498 | Message expired before delivery | Retry if still within the conversation window |
| 501 | Agent not launched | Check agent status in Channels > RCS; before Launched, messages go only to test devices |
| 500 / 503 | Internal error or RCS service unavailable | Retry; escalate to support if it persists |

---

## Frequently Asked Questions

**How can a user check that their phone supports RCS?**
In the Messages app, go to Settings > Chat features. Status should show **Connected**. If the option is missing, install Google Messages, set it as the default SMS app, and turn on Chat features.

**Why does the RCS menu in Console show no agent?**
The agent has not been created yet. Click **Get Started** in Channels > RCS to begin the agent creation flow.

**Can one project have two RCS agents?**
No. Each Console project supports one RCS agent. Use separate projects if multiple agents are needed.

**Can the client use RCS and WhatsApp in the same project?**
Not yet in Console postpaid — this is planned. RCS and WhatsApp currently require separate projects or separate GG enterprise accounts.

**Why aren't iOS users receiving RCS messages? (India)**
In India, Jio launches the iOS RCS agent only after the brand has built sufficient traffic and engagement on its Jio Android agent. Until Jio approves iOS delivery for that agent, iOS users will not receive RCS messages.

**Which opt-out keyword works by default?**
STOP. Additional opt-out keywords can be configured at onboarding.

**Why is the campaign showing "no agent" in the account filter?**
The enterprise RCS account has not been mapped to the project. This is an onboarding step performed by the Gupshup onboarding team. Contact your CSM to complete the mapping.

**Can templates be sent before the agent is launched?**
No. Templates can only be sent to real users once the agent status is **Launched**. Before launch, messages can be sent only to registered test devices.

**What is the monthly promotional message limit per user?**
In India, the per-user cap is 2, 4, or 8 messages per month depending on the agent's reputation score (LOW, MEDIUM, or HIGH respectively), plus 2 additional messages each time the user replies.

---

## Related docs

- rcs-console-agent-setup.md for agent creation and launch steps
- rcs-console-templates.md for template creation and limits
- rcs-console-campaigns.md for campaign setup and analytics
- rcs-fallback-strategy.md for configuring SMS and WhatsApp fallback
