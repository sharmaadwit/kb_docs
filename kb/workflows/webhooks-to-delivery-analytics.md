source_url: https://console-docs.gupshup.io/docs/webhooks

<!-- kb-golden:v11 -->
# Webhooks To Delivery Analytics

**Module**: Workflows

## Definition
- Use this workflow when you want **Delivery Events** from **Webhooks** to feed downstream systems and be reconciled against **Campaign Analytics**.
- This workflow is useful for:
  - delivery-status tracking
  - webhook validation
  - response-file reconciliation
  - duplicate or missing event troubleshooting

## Procedure
### Exact UI path
Gupshup Console -> Integrations -> Webhooks
Gupshup Console -> Campaign Manager -> Campaign Analytics

### Steps
1. Open **Integrations -> Webhooks**.
2. Create or update a webhook for **Delivery Events**.
3. Enter the **Callback URL** and save it.
4. Trigger a test send or use a sent campaign to generate delivery events.
5. Confirm the receiver endpoint logs the delivery payload.
6. Open **Campaign Manager -> Campaign Analytics** for the same campaign.
7. Compare aggregate statuses in Campaign Analytics with the delivery events received by your system.

### Validation / where to check
- Confirm webhook callbacks are received by the endpoint.
- Confirm the callback payload contains delivery fields such as status, identifiers, and timestamps.
- Confirm Campaign Analytics shows matching sent/delivered/read/failed counts for the same campaign.

### Save / publish / deploy behavior
- Saving a new delivery webhook updates the active callback URL for delivery events.
- Delivery events support only one active callback URL; a later save can overwrite the previous delivery-event URL.

### Troubleshooting
- If duplicate delivery events appear, dedupe using message/external identifier plus status and timestamp.
- If message IDs are missing downstream, inspect the raw webhook payload before debugging analytics.
- If Campaign Analytics has delivery data but your endpoint does not, re-check the callback URL and endpoint response.
- If your answer or downstream schema includes WABA/account/template fields, you are using the wrong webhook event family.

## Field mapping / schemas
- Recommended delivery fields to store:
  - **eventType**
  - **cause**
  - **eventTs**
  - **externalId**
  - **destAddr**
  - **srcAddr**
  - **errorCode** when present

## Module disambiguation docs
- **Webhooks** gives you near-real-time event delivery.
- **Campaign Analytics** gives you the console view and response files for delivery outcomes.
- Use **Webhooks** for ingestion and troubleshooting.
- Use **Campaign Analytics** for verification and reporting.
