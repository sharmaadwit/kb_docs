source_url: https://console-docs.gupshup.io/docs/campaign-analytics

<!-- kb-golden:v12 -->
# Campaign Analytics

**Module**: Campaign Manager

## Definition
- `Campaign Analytics` is available for campaigns that are `sent`.
- This page provides a preview of the campaign and high level analytics.

## Procedure
### Exact UI path
Gupshup Console -> Campaign Manager -> Campaign Analytics

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Open **Campaign Analytics**.
4. Open a campaign that is already `sent`.
5. Review the analytics on the screen.
6. Generate the `Response file` for additional campaign details.
7. Use the `Link tracking Report` if you need click details.

### Validation / where to check
- Check the campaign analytics screen for the campaign preview and high level analytics.
- Use the generated reports for advanced stats.

### Save / publish / deploy behavior
- Campaign Analytics is a reporting view; there is no save action here.

### Prerequisites
- A campaign already sent from **Campaign Manager**.
- Access to the relevant campaign analytics view.

## Options / variants
- `Response file`: timewise summary of all delivery events for all phone numbers.
- `Link tracking Report`: timewise summary of clicks with original URL, Gupshup URL, click time, IP address, device, and OS.
- `Click Analysis`: `Total Clicks`, `Unique Clicks`, and `Click Through Rate`.

## Field mapping / schemas
- Key delivery and engagement metrics on this page include:
  - **Targeted**
  - **Sent**
  - **Delivered**
  - **Read**
  - **Dropped**
  - **Failed**
  - **Total Clicks**
  - **Unique Clicks**
  - **Click Through Rate**

## Cross-module workflow docs
- Campaign Manager send -> Campaign Analytics for delivery/engagement
- Campaign Manager send -> Bot Studio journey -> Goal Analytics for conversion
- Delivery Webhooks -> Response file reconciliation

## Module disambiguation docs
- **Campaign Analytics** is for campaign send, delivery, read, failure, and click performance.
- **Goal Analytics** is for goal tracking after a goal is created and implemented within a journey.
