source_url: https://console-docs.gupshup.io/docs/salient-features

<!-- kb-golden:v10 -->
# Salient Features

**Module**: Personalize

## Definition
Unified Profile of your users

## Procedure
### Exact UI path
Gupshup Console → Personalize → Salient Features

### Prerequisites
- Access to **Gupshup Console → Personalize → Salient Features** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Personalize**.
3. Go to **Salient Features**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Personalize**.
- Go to **Salient Features**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Distinguish this page from adjacent modules/settings before troubleshooting elsewhere.

## Reference (from source)
<!-- procedural:v2 -->
# Salient Features

**Module**: Personalize

## Overview
Unified Profile of your users

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Unified Profile of your users

- Personalize builds a unified profile of your users based on events and properties.
- You can import users to CDP manually using lists or as when a new user is created on Shopify
- Events performed by the user on Shopify are automatically recorded on Personalize platform
- There are some primary properties that can be added manually through CSV or fetched from Shopify
- Phone number or E-mail is considered as unique identifier for each profile and at least 1 of them is a must for every profile
- You can view each individual user, their properties and events in all contacts section of Personalize platform
Unique profile view

Lists & Segments

- Lists is one of the ways one can import new users manually into the CDP platform
- Download the sample file which has pre-filled column names with all properties (both primary and custom)
- The values of properties for the users can be populated in the CSV and uploaded
Uploading CSV to create list

- Segments can be created by defining conditions on events and properties
- Using segments you can perform different actions (eg: running a campaign), to users who dynamically match a specific condition
Adding conditions to create a segment

Custom Attributes

- There is plenty of data that can be automatically fetched from Shopify, etc., but in case you need to define custom property for a user you can use custom attributes
- On the profile properties section on Personalize platform you can create a new property along with defining it's name and data type
- Once the custom attribute is created a column is automatically added to the download sample file and now the values for the property can be populated and uploaded
List of profile properties

- One can also add custom attributes on a single users profile
Integration with E-commerce

- Within the Personalize platform you can seamlessly integrate your Shopify store with our CDP, increase engagement and boost sales
- Automate marketing and transactional communication across multiple messaging platforms like WhatsApp
- Deliver personalized and interactive messages to nurture leads, boost sales, and enhance customer satisfaction
- Streamline your customer communication with welcome messages, real-time order updates, and timely reminders for abandoned checkouts

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 4 months ago
