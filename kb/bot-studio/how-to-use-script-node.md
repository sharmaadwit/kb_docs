> Source: https://console-docs.gupshup.io/docs/how-to-use-script-node
> Last updated: 2026-09-11

<br />

# Overview

The Script Node is available in Journey Builder V2 for bot designers who need to perform lightweight custom scripting inside a conversational journey.

![](https://files.readme.io/4eb19869204163f7835aea2eff4b89821a8849b1365c065a82eb56657ebf8f22-image.png)

<br />

It can be used for scenarios where the required logic is difficult to implement using standard Journey Builder nodes such as the JSON Handler Node, Expression Library, Modify Variable Node, or other low-code alternatives.

The Script Node allows bot designers to write JavaScript that can modify variables, transform data, prepare payloads, or perform other supported lightweight logic during journey execution.

***

# Where to Find the Script Node

The Script Node is available under the **Action Nodes** category in the Journey Builder node panel.

![](https://files.readme.io/6c50d271179ce954ab6977a010154dff24027dde82e10c873c9e9f3f3e8189c0-image.png)

<br />

![](https://files.readme.io/48ee67ca9fa067b5f3344c036096bdfea9d01131d34c4ccc083ee34ebd55845a-image.png)

<br />

## To add a Script Node

1. Open the required journey in Journey Builder V2.
2. Go to the node panel.
3. Open the **Action Nodes** category.
4. Drag and drop the **Script Node** onto the canvas.
5. Connect it to the required point in the journey flow.

Once added, the Script Node becomes part of the journey execution path and will run when the end user reaches that node during runtime.

***

# Opening the Script Node

## To configure the Script Node

1. Click the Script Node on the canvas.
2. A right-side configuration panel will open.
3. The panel will show the currently available script for the node, if any.

If a script already exists in the node, bot designers can view it in a read-only format from the right-side panel.

This allows users to review the script without accidentally modifying it.

***

# Viewing an Existing Script

When a Script Node already contains code:

1. Click the Script Node on the canvas.
2. View the existing script in the right-side panel.
3. The script will be displayed in read-only mode.

<br />

![](https://files.readme.io/ce3b9edb1de7a4a555844fedf23ae4cc4fd401b3138d5c8152234744f3ca9d95-image.png)

<br />

Read-only mode helps prevent accidental edits while still allowing bot designers to inspect the logic configured in the node.

***

# Editing or Adding a Script

## To add a new script or edit an existing one

1. Click the Script Node on the canvas.
2. In the right-side panel, locate the script text box.
3. Click the **Edit** button above the code text box.
4. The Script Editor will open.
5. Write or update the required JavaScript logic in the editor.

![](https://files.readme.io/ee1e55db2dc727cef63912420d1c7e39837a2037827fd383522c55e9c1232d6f-image.png)

<br />

The Script Editor provides a larger editing experience where bot designers can write, review, and update their script more comfortably.

***

# Referring to Variables in the Script

Bot designers can refer to Journey Builder variables inside the script.

Variables can be added or referenced manually in the script, or inserted using the variable selector.

## To add a variable

1. Open the Script Editor.
2. Click the **Add Variable** icon.
3. The Add Variable icon is available near the script text box, at the bottom-left area of the editor.
4. Select the required variable.
5. The selected variable reference will be inserted into the script.

## Example Variable Reference

```javascript
var_local.customerName
```

<Callout icon="📘" theme="info">
  **Bot designers should ensure that the required variables are already created in the journey before referring to them in the script**.
</Callout>

***

# Saving the Script

Once the script is written or updated:

1. Click the **Save** button in the Script Editor.
2. The script will be saved for the selected Script Node.
3. After saving, the script becomes usable in the node.

During runtime, the saved script will execute when the end user reaches this Script Node in the journey.

If the script modifies variables, those updated values can be used in subsequent nodes in the journey.

***

# Runtime Execution

The Script Node executes when the conversation reaches that specific node in the journey flow.

## At Runtime

1. The end user reaches the Script Node.
2. The saved script is executed.
3. Any supported variable updates or transformations are performed.
4. The journey proceeds to the next connected node if execution is successful.
5. If execution fails, the configured fallback path is triggered, where applicable.

Bot designers should keep scripts concise and optimized to ensure smooth runtime execution.

***

# Using Libraries in Script Node

If a bot designer wants to use a supported library inside the Script Node, they can manage libraries from the Script Node settings.

## To open library settings

1. Open the Script Node.
2. Click the **Edit** button to open the Script Editor.
3. Click the **Settings** button.
4. The Settings modal will open.
5. Go to the **Manage Library Version** tab.

![](https://files.readme.io/26d0f493c99ccbd824161686e330cd7efebc4e9d8e875c58670cd5ceb878c718-image.png)

<br />

From this tab, bot designers can view, add, edit, or delete supported libraries for the project.

***

# Adding a Library

## To add a new library

1. Open the Script Node editor.
2. Click the **Settings** button.
3. Go to the **Manage Library Version** tab.
4. Click **Add Row**.
5. In the new row, use the dropdown on the left side of the table to select a library.
6. Enter the required library version.
7. Click **Save**.

<br />

![](https://files.readme.io/9fb57d300fec7ac8678c05a87ab2a23bfcb0d5593fd42a99ffe1efdc6d187052-image.png)

<br />

Once saved, the selected library version will be imported and made available on the backend.

The library can then be used across all Script Nodes available in that particular project.

***

# Library Version Guidelines

When adding or updating a library version:

* Enter a valid version number.
* Ensure the version is available and supported.
* Avoid using incorrect or incomplete version values.
* Use only the libraries available in the dropdown.
* Do not assume that unsupported libraries can be imported manually.

If the library or version is invalid, the import may fail.

***

# Project-Level Library Availability

Libraries added from the **Manage Library Version** tab are available at the project level.

## This Means

* A library added once can be used across all Script Nodes in the same project.
* The same library does not need to be added separately for every Script Node.
* Library changes may affect other Script Nodes in the same project if they depend on the updated library version.

Bot designers should review usage carefully before deleting or updating a library version.

***

# Legacy Libraries in Migrated Projects

If the project has been migrated from Legacy Journey Builder, some older libraries may be visible in the **Manage Library Version** tab.

These libraries will be marked as `legacy` libraries.

<Image align="center" src="https://files.readme.io/4cdad739e410b860c2ce29a6eaf310ec5e7e909454f14d6cb485eec07823b777-image.png" />

## Legacy Libraries

* Were available in the earlier Legacy Code Node setup.
* Are available only for that migrated project.
* Cannot be used in other projects.
* May not be editable.
* May not be available in the library dropdown for new projects.
* Are retained only to support migration compatibility.

These libraries are shown so that migrated scripts can continue to function without requiring immediate manual rewriting.

<Callout icon="📘" theme="info">
  **Note: Bot designers are advised to switch to alternate supported libraries or approaches for the unsupported libraries if possible.**
</Callout>

***

# Deleting a Library

## To delete a library

1. Open the Script Node editor.
2. Click the **Settings** button.
3. Go to the **Manage Library Version** tab.
4. Locate the library that needs to be removed.
5. Click the **Delete** icon.
6. Confirm the deletion, if prompted.

Before deleting a library, ensure that no Script Node in the project depends on it.

<Callout icon="📘" theme="info">
  **Deleting a library that is being used by a script may cause execution failures**.
</Callout>

***

# Editing or Updating a Library Version

## To update the version of an existing library

1. Open the Script Node editor.
2. Click the **Settings** button.
3. Go to the **Manage Library Version** tab.
4. Locate the library that needs to be updated.
5. Click the **Edit** icon.
6. Enter the updated library version.
7. Click **Save**.

Once saved, the updated version will be imported and made available for Script Nodes in the project.

Bot designers should validate affected scripts after updating a library version.