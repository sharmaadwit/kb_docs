source_url: https://console-docs.gupshup.io/docs/webhooks

<!-- kb-golden:v12 -->
# Webhooks

**Module**: Integrations

## Definition
The Webhooks feature lets you subscribe to real-time events triggered by the Gupshup platform and receive updates on your callback URL.

## How To Configure
1. Log into Gupshup Console.
2. Navigate to `App > Integration > Webhooks`.
3. Add your `Callback URL` and save.
4. Choose the module and respective events:
   - `WhatsApp Profile (Account)`
   - `Template`
   - `Campaign Manager`
   - `API Delivery events`
5. Click `Create Webhook`.

## Important Note
- You can configure only `1 URL` for `Delivery Events`.
- Additional webhooks created for delivery events update the URL, and events are sent to the latest URL saved.

## Event Categories
### Delivery Events
Delivery webhooks notify you in real time about message delivery statuses for Campaigns and API-sent WhatsApp messages.

The source page lists:
- `SENT`
- `DELIVERED`
- `READ`
- `FAILED`

Key parameters explained in the source:
- `externalId`
- `eventType`
- `srcAddr`
- `destAddr`
- `conversation.id`
- `conversation.expiration_timestamp`
- `pricing.category`

### Template Events
Template events notify you of template status or category changes.

Examples listed in the source:
- `status-update`
- `category-update`
- `quality-update`

### Profile Events (Account Events)
Profile or Account events are triggered when a change occurs in the WhatsApp Business Account.

Examples listed in the source:
- `review-event`
- `status-event`
- `pndn-event`
- `tier-event`
- `capability-event`

## Delivery Payload Example
The source page includes this example:

`{ "srcAddr": "919898989898", "channel": "WHATSAPP", "hsmTemplateId": "6330963", "externalId": "4873914210717831261-128116432999904428", "cause": "SENT", "errorCode": "025", "destAddr": "91XXXXXXXXXX", "eventType": "SENT", "eventTs": 1680527479000, "conversation": { "expiration_timestamp": 1680613560, "origin": { "type": "marketing" }, "id": "072a7f95683c6c2bffef5655c706c50d" }, "pricing": { "category": "marketing" } }`
