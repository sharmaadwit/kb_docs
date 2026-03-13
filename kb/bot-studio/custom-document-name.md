source_url: https://console-docs.gupshup.io/docs/custom-document-name

<!-- kb-golden:v7 -->
# Custom Document Name

**Module**: Bot Studio

## Definition
Document node allows businesses to send a ‘custom file name’ for the documents sent to users. The file name is an optional field with a limit of 20 characters. The original file name will be replaced by the custom name if provided

## Procedure
### Exact path
Gupshup Console → Bot Studio → Custom Document Name

### Where to configure it
Gupshup Console → Bot Studio → Custom Document Name

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Custom Document Name**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Custom Document Name**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
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
