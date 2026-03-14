source_url: https://console-docs.gupshup.io/docs/campaign-analytics

<!-- kb-golden:v11 -->
# Campaign Analytics

**Module**: Campaign Manager

## Definition
- Use **Campaign Analytics** to measure how a sent campaign performed.
- This page shows campaign delivery and engagement metrics such as **Targeted**, **Sent**, **Delivered**, **Read**, **Dropped**, **Failed**, and **Click Analysis**.
- If you are asking **“Where can I see campaign analytics?”** -> open **Campaign Manager -> Campaign Analytics**.

## Procedure
### Exact UI path
Gupshup Console -> Campaign Manager -> Campaign Analytics

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Open **Campaign Analytics**.
4. Select a campaign that is already **Sent**.
5. Review **Targeted**, **Sent**, **Delivered**, **Read**, **Dropped**, and **Failed**.
6. Open **Click Analysis** if you need **Total Clicks**, **Unique Clicks**, or **Click Through Rate**.
7. Download the **Response file** if you need recipient-level delivery outcomes.
8. Download the **Link tracking report** if you need click-level detail.

### Validation / where to check
- Send a small test campaign and confirm counts update in **Campaign Analytics**.
- If delivery webhooks are enabled, compare the response file with webhook delivery records for the same campaign.

### Save / publish / deploy behavior
- Campaign Analytics is a reporting view; there is no save action here.

### Troubleshooting
- If delivery totals look wrong, download the **Response file** and inspect recipient-level statuses.
- If users are not converting even though the campaign was delivered, compare **Campaign Analytics** with **Goal Analytics** instead of assuming the send failed.
- If clicks are present but conversions are not, campaign delivery worked; continue troubleshooting in **Goals** / **Goal Analytics**.

### Prerequisites
- A campaign already sent from **Campaign Manager**.
- Access to the relevant campaign analytics view.

## Options / variants
- **Response file**: timewise delivery events for recipients.
- **Link tracking report**: click-level report with URL and device metadata.
- **Click Analysis**: Total Clicks, Unique Clicks, CTR.

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
- **Goal Analytics** is for conversion tracking after the user enters the bot or completes the target journey path.
- Use **Campaign Analytics** to answer **“Was the campaign delivered/read/clicked?”**
- Use **Goal Analytics** to answer **“Did the user complete the intended conversion?”**
