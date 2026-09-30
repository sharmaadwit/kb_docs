source_url: https://console.gupshup.io/rcs/campaigns

<!-- kb-golden:v10 -->
# RCS Broadcast Campaigns in Gupshup Console

**Module**: Campaign Manager

## Definition

How to create and send RCS broadcast campaigns from the Gupshup Console using approved RCS templates. Supports text, standalone rich card, and rich card carousel templates. Campaign analytics are available per campaign after sending.

---

## Prerequisites

- RCS agent status is **Launched** (see rcs-console-agent-setup.md)
- At least one approved RCS template exists (see rcs-console-templates.md)
- Enterprise RCS account is mapped to the Console project

---

## Steps in Console

1. Open **Broadcast Campaigns** and select the RCS account using the account filter.
2. Click **Create** and enter the campaign name. Channel and account are pre-filled.
3. Select a template. The list shows each template's name and type.
4. Map template variables (for example `[NAME]`, `[AMOUNT]`) to upload-file columns, C360 properties, or fallback values.
5. Review the channel-specific RCS preview, then launch the campaign.
6. Track results in the campaign's analytics tab after sending.

---

## Campaign Analytics

| View | Metrics available | Downloadable report |
|------|------------------|-------------------|
| Campaign funnel | Targeted, sent, delivered, read, failed, dropped | Response report |
| Click analysis | Total clicks, unique clicks, CTR | Link click report (phone number, URL clicked, timestamp, postback text) |
| Button click analysis | Total clicks, unique clicks, clicks per button | Button click report (phone number, button clicked, timestamp, postback text) |

---

## Channel-Level Analytics

In addition to per-campaign analytics, a full RCS channel analytics view is available under **Channels > RCS > Analytics**. It includes:

- Unified traffic dashboard: submitted, sent, delivered, read, failed, revoked, responses, and unsubscribes — with delivery rate (DR%) and read rate (RR%) at a glance
- Trend analysis: traffic, response, and unsubscribe trends over time with hour or day granularity and period-over-period comparison
- Top N insights: top-performing templates, bots, countries, and failure reasons ranked by key metrics
- Template-level analytics: delivery, read, and engagement per template
- Button click analytics: top CTA labels and click distribution by action type

---

## Sending Rules (India)

- Outside an active conversation window, only **approved templates** can be sent. After the user replies, non-template messages can be sent within a 24-hour window.
- Promotional agents in India can send only between **7am and 10pm IST**.
- Per-user promotional limit: at most 4 A2P messages per brand per user per month, plus 2 more each time the user replies. The exact monthly cap (2, 4, or 8) depends on the agent's reputation score (LOW, MEDIUM, or HIGH).

---

## Fallback and Failover

RCS to SMS or WhatsApp fallback is available in solution mode only — a one-time account-level setup by the TechSupport team. The Smart cPaaS module is added as a channel extension so you can map channel-specific templates against each other.

Automated WhatsApp-to-RCS and RCS-to-WhatsApp failover in Broadcast, Automated, and API campaigns is planned.

---

## Related docs

- rcs-console-templates.md for creating and managing RCS templates
- rcs-console-agent-setup.md for launching the RCS agent
- rcs-fallback-strategy.md for fallback channel configuration
