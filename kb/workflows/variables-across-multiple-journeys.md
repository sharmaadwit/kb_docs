source_url: https://console-docs.gupshup.io/docs/manage-variables

<!-- kb-golden:v5 -->
# Workflow: Use variables across multiple journeys (Journey Builder)

**Module**: Workflows

## Definition
This page explains how to **store data in Journey Builder variables** and **reuse it across multiple journeys** (including multi-journey setups). The key is choosing the right **variable scope/lifecycle** (Local vs Global vs Constant) and validating the data is available where you need it.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Manage Variables  
Gupshup Console → Bot Studio → Modify Variable Node  
Gupshup Console → Bot Studio → Multi-Journey - User Journeys

### Where to configure it
- **Manage Variables**: define/create variables and pick the variable type.
- **Modify Variable node**: write/update variables at runtime (from user input/API responses).
- **Multi-Journey**: orchestrate journeys (call sub-journeys from a main journey).

### Prerequisites
- You can edit journeys in **Bot Studio**.
- You know what key you’ll use to identify the user (channel/user id) if you need persistence.

### Setup path
- Bot Studio → open a journey → **Manage Variables**
- Bot Studio canvas → add **Modify Variable** node to set/update values

### Steps
1. Decide what “across journeys” means for your use case:
   - **Same session / same conversation window** → Local may be sufficient.
   - **Persistent across sessions for the same user** → use **Global**.
   - **Same value for all users across all journeys** → use **Constant/Bot Constants**.
2. In **Manage Variables**, create/select the variable and choose the correct type (Local/Global/Constant).
3. In the journey where you first capture the value:
   - Use a prompt/API node to get data, then
   - Use **Modify Variable** to store it in the chosen variable.
4. In another journey (or a sub-journey), reference the same variable to reuse the value.

### Save/publish/deploy behavior
- Use **Save** while editing.
- Use **Save & Deploy** to ensure the updated journey is live on the channel.

### Validation
- In a test conversation, set the variable in Journey A, then route into Journey B and confirm the value is present.
- If you restart the conversation or wait beyond the session window, confirm the behavior matches the variable type:
  - Local may reset; Global should persist; Constant is always available.

## Available options
- Variable types: **Local**, **Global**, **System**, **Constant**, **CDP**
- Operations (Modify Variable): string/number/JSON operations depending on the target variable type

## Notes
- Global variables persist against the user’s **channel ID**; Local variables persist until the conversation context resets.

## Troubleshooting
- Variable is empty in the next journey:
  - Confirm you stored it to the correct type (Local vs Global).
  - Confirm the journey that sets the variable was **deployed**.
  - Confirm you’re testing in the same conversation context (for Local).

## Field mapping / schemas
- For “System variables” (like user/channel identifiers), refer to the system variable list/table in Manage Variables.

## Cross-module workflows
- CTX → Bot Studio → variables set from ad payload → multi-journey routing

## Module disambiguation
- **Multi-journey** orchestrates flow; **variable type** determines persistence/availability across journeys and time.

## Reference (from source)
- `kb/bot-studio/manage-variables.md`
- `kb/bot-studio/modify-variable-node.md`
- `kb/bot-studio/multi-journey-user-journeys.md`
