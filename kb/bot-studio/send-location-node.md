source_url: https://console-docs.gupshup.io/docs/send-location-node

<!-- kb-golden:v10 -->
# Send Location Node

**Module**: Bot Studio

## Definition
The Location Node (Message Node) feature allows businesses to share location details with end users via WhatsApp, making it easier to inform them about the business's serviceable locations. This feature is ideal for businesses that need to communicate precise location information to their end users.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Send Location Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Send Location Node**.
4. Add Location Node: Insert the Location Node (Message Node) into your flow at the desired point where you need to share location information with the user.
5. Configure Latitude and Longitude: Enter numeric values manually or map a number variable for Latitude and Longitude. Ensure that only valid number/integer values are used for these fields.
6. Enter numeric values manually or map a number variable for Latitude and Longitude.
7. Ensure that only valid number/integer values are used for these fields.
8. Save and Deploy: Once the node is configured, save your journey and deploy it. The location will now be sent to users when they reach this node in the flow.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Send Location Node**.

## Options / variants
- Enter numeric values manually or map a number variable for Latitude and Longitude.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Send Location Node

**Module**: Bot Studio

## Overview
The Location Node (Message Node) feature allows businesses to share location details with end users via WhatsApp, making it easier to inform them about the business's serviceable locations. This feature is ideal for businesses that need to communicate precise location information to their end users.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction

The Location Node (Message Node) feature allows businesses to share location details with end users via WhatsApp, making it easier to inform them about the business's serviceable locations. This feature is ideal for businesses that need to communicate precise location information to their end users.

# Key Aspects of the Feature

## Functionality

- Address and Location Name (Optional): These fields are optional and can accept either string or number variables, providing flexibility in the data sent.
- Latitude and Longitude Fields (Required): These fields require number values or numeric variables. Only valid number/integer inputs can be mapped to ensure accurate location data. Fill the Latitude and Longitude of the required location to be shared.
# How to Use

- Access the Journey Builder: Navigate to the Journey Builder in your platform and select the flow where you want to add the Location Node.
- Add Location Node: Insert the Location Node (Message Node) into your flow at the desired point where you need to share location information with the user.
- Configure Latitude and Longitude: Enter numeric values manually or map a number variable for Latitude and Longitude. Ensure that only valid number/integer values are used for these fields.
- Enter numeric values manually or map a number variable for Latitude and Longitude.
- Ensure that only valid number/integer values are used for these fields.
- Optional: Configure Address and Location Name: If needed, enter a string or map a string/number variable to the Address and Location Name fields. These fields are optional and can be left blank if not required.
- If needed, enter a string or map a string/number variable to the Address and Location Name fields.
- These fields are optional and can be left blank if not required.
- Save and Deploy: Once the node is configured, save your journey and deploy it. The location will now be sent to users when they reach this node in the flow.
# Use Cases

### Service Area Notifications

- Scenario: A delivery service wants to inform customers about their delivery areas by sending the exact coordinates of serviceable zones.
- Benefit: By using the Location Node, businesses can efficiently communicate geographical information, ensuring that end users know whether they are within a serviceable area.
### Store Location Sharing

- Scenario: A retail chain wants to share the exact coordinates of a new store location with customers on WhatsApp.
- Benefit: The Location Node allows the business to send accurate latitude and longitude details, along with optional store names and addresses, making it easy for customers to locate the store.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Save and Deploy: Once the node is configured, save your journey and deploy it. The location will now be sent to users when they reach this node in the flow.

**Last updated (from source)**: Updated 10 months ago
