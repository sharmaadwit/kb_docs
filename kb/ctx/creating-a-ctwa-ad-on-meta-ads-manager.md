source_url: https://console-docs.gupshup.io/docs/creating-a-ctwa-ad-on-meta-ads-manager

<!-- kb-golden:v9 -->
# Creating a CTWA Ad on Meta Ads Manager

**Module**: Ctx

## Definition
Meta's guide to creating CTWA ads: https://www.facebook.com/business/help/447934475640650?id=371525583593535

## Procedure
### Exact UI path
Gupshup Console → CTX → Creating a CTWA Ad on Meta Ads Manager

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Creating a CTWA Ad on Meta Ads Manager**.
4. Enter the desired names for your ad campaign, Ad set, and ads.
5. Select the performance goal as: Maximize number of conversations.
6. Add the audience filtration, if any basis your target audience. You may also use traditional campaign audience.
7. Select the placement for the ads and where you want your ads to appear in the feed.
8. Choose the ad creative and enter the headline, description and CTWA to be displayed.
9. Select the Message template (icebreaker message) that the users will send the brand to trigger the journey once they reach the WhatsApp environment. You can either customize the template or choose one from the existing templates.
10. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- names for your ad campaign, Ad set, and ads
- headline, description and CTWA
- Message content

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **CTX**.
- Go to **Creating a CTWA Ad on Meta Ads Manager**.

## Options / variants
- Enter the desired names for your ad campaign, Ad set, and ads
- Select the performance goal as: Maximize number of conversations
- Add the audience filtration, if any basis your target audience. You may also use traditional campaign audience
- Select the placement for the ads and where you want your ads to appear in the feed
- Choose the ad creative and enter the headline, description and CTWA to be displayed

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- CTX campaign → Bot Studio journey → Goal measurement

## Module disambiguation docs
- CTX covers ad-to-WhatsApp campaign flows; bot conversation logic still lives in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Creating a CTWA Ad on Meta Ads Manager

**Module**: Ctx

## Overview
Meta's guide to creating CTWA ads: https://www.facebook.com/business/help/447934475640650?id=371525583593535

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Meta's guide to creating CTWA ads: https://www.facebook.com/business/help/447934475640650?id=371525583593535

Best Practices for creating CTWA Campaigns:

- Campaign Objective to be selected as “Engagement”
- Performance goal to be selected as “Maximize number of conversations”
- Please make sure that the ads communication headline and pre-filled text seamlessly tie-down to the actions being taken in the bot journey.
- Under Conversions, please select “Messaging Apps”
- Under Messaging Apps, please select “WhatsApp" and de-select Instagram and Messenger
- Please make sure the correct WhatsApp number is being selected to redirect users. This WhatsApp number should match the WhatsApp number onboarded to Gupshup Console
Step-by-step Process:

- Campaign level: Create a new campaign from Ads Manager and select Campaign Objective as Engagement Enter the desired names for your ad campaign, Ad set, and ads
- Create a new campaign from Ads Manager and select Campaign Objective as Engagement
- Enter the desired names for your ad campaign, Ad set, and ads
- Ad-set level: Under Conversions, please select the Conversion Location as “Messaging Apps” Under Messaging Apps, please select “WhatsApp” as the platform and un-check Messenger and Instagram Please ensure that the WhatsApp number shown in the drop-down is the WhatsApp number linked to console. Select the performance goal as: Maximize number of conversations Add the audience filtration, if any basis your target audience. You may also use traditional campaign audience Select the placement for the ads and where you want your ads to appear in the feed Check that the FB page and Instagram account have been correctly mapped.
- Under Conversions, please select the Conversion Location as “Messaging Apps”
- Under Messaging Apps, please select “WhatsApp” as the platform and un-check Messenger and Instagram
- Please ensure that the WhatsApp number shown in the drop-down is the WhatsApp number linked to console.
- Select the performance goal as: Maximize number of conversations
- Add the audience filtration, if any basis your target audience. You may also use traditional campaign audience
- Select the placement for the ads and where you want your ads to appear in the feed
- Check that the FB page and Instagram account have been correctly mapped.
- Ad level: Choose the ad creative and enter the headline, description and CTWA to be displayed Select the Message template (icebreaker message) that the users will send the brand to trigger the journey once they reach the WhatsApp environment. You can either customize the template or choose one from the existing templates.
- Choose the ad creative and enter the headline, description and CTWA to be displayed
- Select the Message template (icebreaker message) that the users will send the brand to trigger the journey once they reach the WhatsApp environment. You can either customize the template or choose one from the existing templates.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 6 months ago
