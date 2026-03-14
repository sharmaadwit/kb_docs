source_url: https://console-docs.gupshup.io/docs/custom-document-name

<!-- kb-golden:v10 -->
# Custom Document Name

**Module**: Bot Studio

## Definition
Document node allows businesses to send a ‘custom file name’ for the documents sent to users. The file name is an optional field with a limit of 20 characters. The original file name will be replaced by the custom name if provided

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Custom Document Name

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Custom Document Name**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Custom Document Name**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

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
# Custom Document Name

**Module**: Bot Studio

## Overview
Document node allows businesses to send a ‘custom file name’ for the documents sent to users. The file name is an optional field with a limit of 20 characters. The original file name will be replaced by the custom name if provided

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Introduction

Document node allows businesses to send a ‘custom file name’ for the documents sent to users. The file name is an optional field with a limit of 20 characters. The original file name will be replaced by the custom name if provided

## Variable Name functionality:

This file name can be provided manually or the field also has the ‘Add Variable’ feature to use variables for naming. This is also an indirect way to overcome the 20 characters limit. Further applications can be understood by reading the use cases below.

## Use Cases:

Here are some use cases that demonstrate the potential applications of the custom document name feature:

1. Personalized Invoices

Scenario: A business sends invoices to customers after a purchase. Custom Document Name: Use the variables in the custom document name field to send invoices with personalized file names, such as "{{var_local.CustomerName}}". Benefit: Enhances the professional appearance and personalization of communication, making it easier for customers to identify their documents.

2. Customized Contracts and Agreements

Scenario: A legal firm sends contracts or agreements to clients. Proactive Persistent Message: Utilize the variables in the custom document name field to label documents with client-specific names, like "{{var_local.ClientName}}". Custom Document Name: Simplifies document management for clients and increases the perceived value of the service through tailored communication.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
