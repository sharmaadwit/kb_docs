source_url: https://console-docs.gupshup.io/docs/connecting-ad-to-bot-in-gupshup-console
# CTX

## Connecting ad to bot in Gupshup Console

# Connecting ad to bot in Gupshup Console

Best Practices:

- Please make sure that the journey that needs to be run for CTWA is converted from a user journey to an ad journey. Only Ad journeys can be connected to CTWA ads
- As a best practice, run the FB preview link generated from Meta Ads Manager to check if the journey is working correctly and if the bot is portraying normal behaviour.
- (Get started by creating a user journey)
Converting a User Journey to Ad Journey:

- Click on Bot Studio -> Journeys
- The main page lists all the User Journeys. On the user journey tab, click on the drop-down and select "Ad Journeys"
- Click on "+Create Ad Journey" button on the top right corner and select "Start from scratch"
- In the journey builder screen that opens, click on the blue dot on the right border of the starting node and select "Actions"
- Under the "Actions" tab, select "Call and Return" as the option:
- Click on the "Call and Return" node and this will get added in the journey. Click on the node and select the desired user journey that needs to be connected to CTWA ads.
- Once the journey is selected, close the node settings and click on "Save and Deploy". Your ad journey is now ready.
Step-by-step Process: Connecting Ad Journey to CTWA Ad

- Click on Click to Chat Ads -> Ad Management
- Click on "View Campaigns"
- For the campaign name that is configured for CTWA, click on "View Ads"
- On the ads page, click on "Connect Bot" and in the pop-up that opens for verification, click on "Confirm"
- Select the Ad journey from the list of journeys that appear and click on "Connect Bot". Disclaimer: Only Ad Journeys are visible in this list, so as a best practice please ensure your user journey has been converted to an ad journey, following the steps shown in section 2.
Updated 6 months ago
