source_url: https://console-docs.gupshup.io/docs/faqs-of-bot-studio

<!-- kb-golden:v11 -->
# Save Vs Save & Deploy

**Module**: Bot Studio

## Definition
- Use **Save** when you want to keep draft changes in Bot Studio without pushing them to live channels.
- Use **Save & Deploy** when you want the latest Bot Studio journey changes to become active for live traffic.
- If you are asking **“What is the difference between Save and Save & Deploy?”**: **Save** stores draft work; **Save & Deploy** publishes the latest journey to the live bot experience.

## Procedure
### Exact UI path
Gupshup Console -> Bot Studio -> Journey Builder

### Where to configure it
- Open the target journey in **Bot Studio**.
- Use the action buttons at the top right of the journey builder.

### Prerequisites
- Access to the bot/project in Gupshup Console.
- A journey with changes ready to test or publish.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Open the target journey in **Journey Builder**.
4. Make the required edits.
5. Click **Save** if you only want to keep the draft in Bot Studio.
6. Click **Save & Deploy** if the change must affect live users on connected channels.

### Validation / where to check
- After **Save**, reopen the journey and confirm the draft changes are present in Bot Studio.
- After **Save & Deploy**, run a live channel test and confirm the updated journey behavior is active.

### Save / publish / deploy behavior
- **Save** updates the draft journey only.
- **Save & Deploy** pushes the latest saved journey to the live bot experience.
- If the live bot still behaves like the old version, confirm you used **Save & Deploy**, not just **Save**.

### Troubleshooting
- If Bot Studio shows the change but live traffic does not, the journey was likely only **Saved** and not **Deployed**.
- If the wrong live behavior continues after **Save & Deploy**, confirm you edited the correct journey and test the correct channel entry path.

## Options / variants
- **Save**: use for draft work, internal review, or changes you are not ready to expose to live traffic.
- **Save & Deploy**: use for production updates that must affect live channels immediately.

## Cross-module workflow docs
- Bot Studio draft update -> **Save** -> draft retained in Journey Builder only
- Bot Studio live update -> **Save & Deploy** -> live channels use the new journey version

## Module disambiguation docs
- **Save / Save & Deploy** belongs to **Bot Studio** publishing behavior.
- **Campaign Analytics**, **Goal Analytics**, and **Webhooks** help you observe outcomes after deployment; they do not publish Bot Studio changes.
