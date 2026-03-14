source_url: https://console-docs.gupshup.io/docs/webhooks

<!-- kb-golden:v12 -->
# Webhooks To Delivery Analytics

**Module**: Workflows

## Definition
Use this page when you need to connect the delivery-event webhook configuration with the delivery information available in Campaign Analytics.

## Webhooks Side
From the `Webhooks` page:

1. Log into Gupshup Console.
2. Navigate to `App > Integration > Webhooks`.
3. Add the `Callback URL` and save.
4. Choose the relevant events, including `API Delivery events`.
5. Click `Create Webhook`.

Important note from the source:
- Only `1 URL` can be configured for `Delivery Events`.
- Additional delivery-event webhooks update the URL, and events are sent to the latest saved URL.

## Delivery Data Available From Webhooks
The source page lists these delivery statuses:
- `SENT`
- `DELIVERED`
- `READ`
- `FAILED`

The source page also lists these key parameters:
- `externalId`
- `eventType`
- `srcAddr`
- `destAddr`
- `conversation.id`
- `conversation.expiration_timestamp`
- `pricing.category`

## Campaign Analytics Side
From the `Campaign Analytics` page:

- `Response file` gives a timewise summary of all delivery events for all phone numbers.
- The analytics page includes:
  - `Targeted`
  - `Sent`
  - `Delivered`
  - `Read`
  - `Dropped`
  - `Failed`

## Source Notes
- Webhooks source: `https://console-docs.gupshup.io/docs/webhooks`
- Campaign Analytics source: `https://console-docs.gupshup.io/docs/campaign-analytics`
