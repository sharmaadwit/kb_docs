source_url: https://console-docs.gupshup.io/docs/webhooks

<!-- kb-golden:v9 -->
# Webhooks To Delivery Analytics

**Module**: Workflows

## Definition
Use this workflow when you want **delivery event data** (sent/delivered/read/failed) to flow from **delivery webhooks** into your downstream systems (warehouse/CRM) and/or be validated against **delivery analytics** in **Campaign Manager**.

**Where to see delivery analytics**: open **Campaign Manager → Campaign Analytics** (delivery analytics dashboard + response files).

If you’re asking **“After configuring delivery webhooks, where do I see delivery analytics?”** → use **Campaign Manager → Campaign Analytics** (and optionally download the response file for per-recipient delivery status).

## Procedure
### Exact UI path
Gupshup Console → Integrations → Webhooks
Gupshup Console → Campaign Manager → Campaign Analytics

### Where to configure it
- Configure delivery webhooks in **Integrations → Webhooks**.
- Validate results in **Campaign Manager → Campaign Analytics** (and/or response files).

### Prerequisites
- A project/app in Gupshup Console with delivery events enabled for the relevant channel/campaign.
- A reachable **Callback URL** (HTTPS endpoint) to receive webhook POSTs.
- At least one sent campaign (or test traffic) to generate delivery events.

### Setup path
- Go to **Integrations → Webhooks**.
- Create/Update a webhook for **Delivery Events** and set your **Callback URL**.
- Go to **Campaign Manager → Campaign Analytics** to review delivery metrics (and download response files if needed).

### Steps
1. Open Gupshup Console.
2. Go to **Integrations → Webhooks**.
3. Click **Create Webhook**.
4. Select the module/events for **Delivery Events**.
5. Enter the **Callback URL** and **Save**.
6. Trigger a **test send** (or use an existing campaign) to generate delivery events.
7. Go to **Campaign Manager → Campaign Analytics** and confirm delivery analytics metrics (Sent/Delivered/Read/Failed).
8. If you need per-recipient status, download the **response file** from Campaign Analytics.

### Save/publish behavior
- Saving the webhook updates the active callback URL for those events.

### Validation
- Confirm webhook callbacks are received by your endpoint (HTTP 2xx at receiver).
- Confirm the campaign shows expected delivery counts in **Campaign Analytics**.

## Available options
- Event types/modules vary by channel and feature (e.g., campaign delivery events vs account/template events).

## Notes
- Delivery Events typically allow **only one active URL**; saving a new one can override the previous URL.

## Troubleshooting
- If you’re not receiving callbacks, verify the **Callback URL** is reachable and returns **2xx** quickly.
- If delivery counts don’t match, use the **response file** to find failed/dropped reasons per recipient.

## Field mapping / schemas
- See `kb/integrations/webhooks.md` for event keys and sample payloads.

## Cross-module workflows
- Integrations (Webhooks) → Campaign Manager (Campaign Analytics / response files) → downstream analytics/CRM

## Module disambiguation
- **Delivery webhooks** are the event stream (near real-time).
- **Campaign Analytics** is the console UI view (aggregate + downloadable response files).

## Reference (from source)
- Webhooks: `kb/integrations/webhooks.md`
