source_url: https://console-docs.gupshup.io/docs/webhooks

<!-- kb-golden:v11 -->
# Webhooks

**Module**: Integrations

## Definition
- Use **Webhooks** to send platform events to your **Callback URL**.
- For delivery reporting and troubleshooting, focus on **Delivery Events** only.
- If you are asking:
  - **How do I set up delivery webhooks?** -> create a webhook for **Delivery Events** and save the **Callback URL**.
  - **What fields/statuses should I store?** -> use the **Delivery Events** payload fields, not Profile or Template events.
  - **Why are message IDs missing?** -> inspect the delivery payload reaching your endpoint and validate your downstream parser/mapping.

## Procedure
### Exact UI path
Gupshup Console -> Integrations -> Webhooks

### Steps
1. Open Gupshup Console.
2. Go to **Integrations**.
3. Open **Webhooks**.
4. Click **Create Webhook**.
5. Select **Delivery Events** if your goal is delivery tracking.
6. Enter the **Callback URL**.
7. Save the webhook.
8. Trigger a test send and confirm delivery callbacks reach your endpoint.

### Validation / where to check
- Confirm the receiver endpoint returns **HTTP 2xx**.
- Confirm a delivery payload reaches your endpoint after a test send.
- Confirm the event family is **Delivery Events**, not **Profile Events** or **Template Events**.

### Fields to configure
- **Callback URL**
- Event family: **Delivery Events**

### Save / publish / deploy behavior
- Saving the delivery webhook updates the active callback URL for that event family.
- Only **one active URL** is supported for delivery events; saving another delivery-event webhook can overwrite the previous one.

### Troubleshooting
- If callbacks are missing, verify the **Callback URL** is reachable and returns **2xx** quickly.
- If a new webhook seems to replace the old one, confirm whether another delivery-event webhook was saved later.
- If message IDs or identifiers are missing downstream, inspect the raw payload first, then validate parser logic and field mapping in your receiver.
- If you are seeing unrelated WABA/account/template data, you are likely consuming the wrong event family instead of **Delivery Events**.

## Options / variants
- **Delivery Events**: for sent, delivered, read, and failed message status tracking.
- **Profile / Account Events**: for WABA/account state changes.
- **Template Events**: for template status/category updates.

## Field mapping / schemas
### Delivery-only fields to store
- **eventType**: delivery lifecycle status such as `SENT`, `DELIVERED`, `READ`, `FAILED`
- **cause**: status/cause value from the delivery event
- **eventTs**: event timestamp
- **destAddr**: recipient address
- **srcAddr**: source address
- **externalId**: message/external identifier for dedupe or reconciliation
- **errorCode**: failure code when present

### Delivery statuses to expect
- **SENT**
- **DELIVERED**
- **READ**
- **FAILED**

### What not to mix into delivery schema answers
- **review-event**
- **status-event** for WABA/account state
- **pndn-event**
- **capability-event**
- **template-event**
- generic **account-event** payloads

## Field/payload examples
- Delivery payload example:
  - `{ "srcAddr": "919898989898", "channel": "WHATSAPP", "externalId": "4873914210717831261-128116432999904428", "cause": "SENT", "errorCode": "025", "destAddr": "91XXXXXXXXXX", "eventType": "SENT", "eventTs": 1680527479000 }`

## Cross-module workflow docs
- Integrations -> Delivery Webhooks -> downstream system / warehouse / CRM
- Integrations -> Delivery Webhooks -> Campaign Analytics response-file reconciliation

## Module disambiguation docs
- **Delivery Events** are for message lifecycle tracking.
- **Profile / Account Events** are for WABA/account changes and should not be mixed into delivery schema answers.
- **Template Events** are for template approval/category/status changes and should not be used as delivery-status evidence.
