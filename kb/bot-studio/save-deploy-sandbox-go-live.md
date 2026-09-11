> Source: https://console-docs.gupshup.io/docs/save-save-deploy
> Last updated: 2026-09-11

# Save, Deploy to Sandbox, and Go Live

## Overview

Save a User Journey, test selected journeys with WhatsApp sandbox testers, and promote all sandbox journeys to production when you are ready.

Sandbox applies only to **User Journeys** in Bot Studio. It does not apply to Campaign Journeys or Ad Journeys.

## Prerequisites

- Open **Manage Project** → **Sandbox Users**.
- Add at least one WhatsApp sandbox tester and set the tester status to **Active**.
- Create or open a User Journey in Bot Studio.

<br />

<Callout icon="fa-info-circle" theme="info">
  Sandbox testers are external WhatsApp testers. They do not need Gupshup Console login access and receive messages only in the sandbox environment.
</Callout>

## Steps

### 1. Add Sandbox Testers

1. Open **Manage Project** → **Sandbox Users**. The Sandbox Users page lists your testers and their status.
2. Click **Add Sandbox Tester**. The Add Sandbox Tester dialog opens.
3. Enter the tester name. This identifies the tester in the Sandbox Users list.
4. Select **WhatsApp** as the channel. The dialog shows the WhatsApp number field.
5. Select the country code and enter the tester's WhatsApp number. The tester can receive sandbox messages at this number.
6. Set **Status** to **Active** and click **Save Tester**. The tester is ready to test sandbox journeys.

![](https://files.readme.io/5f1e2cbd6a792839ba915ed4ed13d3f256670be698d5c7a6729184b14770fb22-image_23.png)

![](https://files.readme.io/bb0b288b266ade8bcf9177c423054dd5f86eccecfa6414b893d1392c7ef3088c-image_24.png)

You can change a tester between **Active** and **Inactive** from **Sandbox Users**. Inactive testers do not receive sandbox messages.

### 2. Save the Journey

1. Build or edit a User Journey on the Bot Studio canvas. Your changes remain in the editor until you save them.
2. Click **Save**. Bot Studio stores the journey in the system without deploying it to sandbox or production.

Save your work regularly while you build the journey.

### 3. Deploy Selected Journeys to Sandbox

1. Open the **User Journeys** tab on the Journeys page. The page displays **Deploy to Sandbox** and **Go Live**.
2. Click **Deploy to Sandbox**. The **Sandbox Changes** dialog lists User Journeys that are ready to deploy.
3. Select the journeys that you want to test. Only selected journeys are included in this sandbox deployment.
4. Click **Confirm**. Bot Studio deploys the selected journeys to the sandbox environment.

Your active sandbox testers can now interact with the selected User Journeys on WhatsApp. Saved journeys that you did not select remain unchanged.

![](https://files.readme.io/c3f3e25baa3d18898bc91874b239d0c051b967dbbebc9352a9ff39f01b11bb49-image_25.png)

![](https://files.readme.io/67748b37e5e0b6e4f681638989d5d34c3e1a907b6e2e19db687147ba4efd5371-image_26.png)

<br />

### 4. Go Live

1. Finish testing each journey in the sandbox. Confirm that the expected WhatsApp messages and journey paths work for your testers.
2. Click **Go Live** from the **User Journeys** tab. The **Deploy Changes** dialog lists the sandbox journeys that will deploy to production.
3. Review the listed journeys. The dialog includes every journey currently deployed to sandbox.
4. Click **Confirm**. Bot Studio deploys all sandbox journeys to production.

![](https://files.readme.io/a1b2e4da47f90bb91896d2fe51f52564786d116c8731108b1e3cb56e2cc6e0c8-image_27.png)

<br />

<Callout icon="fa-exclamation-triangle" theme="warning">
  **Go Live** deploys every User Journey currently in sandbox. You cannot select individual journeys at this stage. Review the **Deploy Changes** list before you confirm.
</Callout>

## Expected Result

- **Save** stores your User Journey without exposing it to testers or production users.
- **Deploy to Sandbox** makes only the selected User Journeys available to active WhatsApp sandbox testers.
- **Go Live** deploys all User Journeys currently in sandbox to production.

## Troubleshooting

### A tester does not receive sandbox messages

Open **Manage Project** → **Sandbox Users** and confirm that the tester has the correct WhatsApp number and an **Active** status. Then confirm that you selected the intended User Journey in the **Sandbox Changes** dialog.

### A saved journey is not available for testing

Click **Deploy to Sandbox**, select the saved User Journey, and click **Confirm**. Saving a journey does not deploy it automatically.

### A journey is not ready for production

Do not click **Go Live** until every journey listed in **Deploy Changes** is ready. **Go Live** promotes all sandbox journeys together.

## Related Links

- [Getting Started with Bot Studio](https://console-docs.gupshup.io/v2.0/docs/create-a-new-journey)
- [How to Trigger a User Journey](https://console-docs.gupshup.io/v2.0/docs/how-to-trigger-a-user-journey)