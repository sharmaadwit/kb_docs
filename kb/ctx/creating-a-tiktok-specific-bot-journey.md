source_url: https://console-docs.gupshup.io/docs/creating-a-tiktok-specific-bot-journey-copy
# CTX

## Creating a TikTok-specific Bot Journey

# Creating a TikTok-specific Bot Journey

# Link to download journey template

Please click on the link below to download the sample json journey template for TikTok: https://drive.google.com/drive/folders/1s_p6T89yDJWNf-hN1yUx9krqgHBcVPJ9?usp=sharing

# Creating a "user journey"

Step 1: Login to the Gupshup console

Step 2: In the left menu, click on "Bot Studio" -> Journeys

Step 3: Once on the journeys page, on the top-right corner, click on the "Import" button and upload the file downloaded from the above link. You can also rename the files (optional) as per your requirement.

Step 4: Under "User Journeys", open the imported journey.

Step 5: Click on the first node and select "user input" and in the expression choose "contains" and add "TikTok"

Step 6: In the second node, which includes the code below:

```
var_local.external_api_key = '{{ctx_external_app_id}}'

var_local.user_modified_message = 'TikTok ' + var_system.user_input.substring(var_system.user_input.indexOf(' ') + 1)
```

- In the code above, replace the CTX External App ID ONLY. To procure your app ID: Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.
- Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.
Step 7: Complete the journey basis the chatbot flow and click on "Save and Deploy"

# Converting user journey to TikTok "ad journey"

Step 1: Under "Bot Studio" -> Journeys, on the top-left under "User Journeys", there will be a drop-down.

Step 2: Click on the drop-down and select "Ad Journeys"

Step 3: If the ad journey will be imported while doing the previous journey setup, click on the journey to open it. If no ad journey is visible, click on "+Create Journey" on the right corner and choose "Start from scratch"

Step 4: Once the journey is opened, on the starting node at the right border, click on the blue dot and select "+Add"

Step 5: Choose "Actions" -> "Call and Return" and select the user journey created for TikTok from the drop-down.

Step 6: Click on "Save and Deploy"

Updated 10 months ago
