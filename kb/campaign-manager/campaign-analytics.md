source_url: https://console-docs.gupshup.io/docs/campaign-analytics

<!-- kb-golden:v9 -->
# Campaign Analytics

**Module**: Campaign Manager

## Definition
- Use **Campaign Analytics** to view **campaign performance** and **delivery analytics** for campaigns that are **Sent**.
- **Where to see campaign analytics**: open **Campaign Manager → Campaign Analytics** (campaign analytics dashboard + response files).
- It shows a preview plus aggregate metrics (Sent/Delivered/Read/Failed/Dropped) and lets you download response files for detailed delivery events.
-
- If you’re asking **“Where can I see campaign analytics?”** → open **Campaign Manager → Campaign Analytics**.
- Following numbers are displayed on this screen - Targeted - Total number of phone numbers to whom the campaign was targeted. Sent - Number of phone numbers to whom the campaign was sent. Delivered - Number of phone numbers to whom the campaign was delivered. Read - Number of phone numbers who read the message. Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers. Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Targeted - Total number of phone numbers to whom the campaign was targeted.
- Sent - Number of phone numbers to whom the campaign was sent.
- Delivered - Number of phone numbers to whom the campaign was delivered.
- Read - Number of phone numbers who read the message.
- Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers.
- Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Click Analysis - Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4. Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1. Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4.
- Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1.
- Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Reports Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out. Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.
- Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out.
- Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.

## Procedure
### Exact UI path
Gupshup Console → Campaign Manager → Campaign Analytics

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Go to **Campaign Analytics** (campaign analytics dashboard).
4. Select the campaign (only campaigns with status **Sent** will have analytics).
5. Review key metrics: **Targeted**, **Sent**, **Delivered**, **Read**, **Dropped**, **Failed**.
6. (Optional) Open **Click Analysis** to review **Total Clicks**, **Unique Clicks**, and **Click Through Rate**.
7. (Optional) Download:
   - **Response file** (timewise delivery events per phone number; useful for retargeting failures)
   - **Link tracking report** (timewise clicks with URL + device/IP metadata)

### Validation / where to check
- Send a small test campaign and confirm counts update in Campaign Analytics.
- If you’re using webhooks, validate delivery events against the response file for the same campaign.

### Fields to configure
- Message content

### Save / publish / deploy behavior
- No save action is required; this is a reporting/analytics view.

### Troubleshooting
- Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out.

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Campaign Manager**.
- Go to **Campaign Analytics**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).
- **Campaign Analytics** is where you view **campaign delivery performance**; Bot Studio analytics are for journey execution, not campaign sends.

## Reference (from source)
<!-- procedural:v2 -->
# Campaign Analytics

**Module**: Campaign Manager

## Overview
- The campaign analytics is available for all the campaigns which are ‘sent’.
- This page provides a preview of the campaign and high level analytics and in order to get to advanced stats, you can generate a response file that provides additional details regarding the campaign.
- Following numbers are displayed on this screen - Targeted - Total number of phone numbers to whom the campaign was targeted. Sent - Number of phone numbers to whom the campaign was sent. Delivered - Number of phone numbers to whom the campaign was delivered. Read - Number of phone numbers who read the message. Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers. Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Targeted - Total number of phone numbers to whom the campaign was targeted.
- Sent - Number of phone numbers to whom the campaign was sent.
- Delivered - Number of phone numbers to whom the campaign was delivered.
- Read - Number of phone numbers who read the message.
- Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers.
- Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Click Analysis - Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4. Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1. Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4.
- Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1.
- Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Reports Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out. Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.
- Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out.
- Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
- The campaign analytics is available for all the campaigns which are ‘sent’.
- This page provides a preview of the campaign and high level analytics and in order to get to advanced stats, you can generate a response file that provides additional details regarding the campaign.
- Following numbers are displayed on this screen - Targeted - Total number of phone numbers to whom the campaign was targeted. Sent - Number of phone numbers to whom the campaign was sent. Delivered - Number of phone numbers to whom the campaign was delivered. Read - Number of phone numbers who read the message. Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers. Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Targeted - Total number of phone numbers to whom the campaign was targeted.
- Sent - Number of phone numbers to whom the campaign was sent.
- Delivered - Number of phone numbers to whom the campaign was delivered.
- Read - Number of phone numbers who read the message.
- Dropped - Number of phone numbers which got a validation failure which can be due to invalid phone number, duplication, breach of frequency capping rule. The campaign will not get sent to these phone numbers.
- Failed - Number of phone numbers for which we got a failure which can be due to many reasons including phone number not available on WhatsApp, template variable mismatch, etc. All failures are mentioned here for reference.
- Click Analysis - Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4. Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1. Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4.
- Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1.
- Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Reports Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out. Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.
- Response file - It gives timewise summary of all the delivery events for all phone numbers. If you want to retarget users for which campaign got failed, this file will help you out.
- Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
