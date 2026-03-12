source_url: https://console-docs.gupshup.io/docs/json-response-attribute-mapping-in-api-node

<!-- kb-golden:v4 -->
# JSON Handler

**Module**: Bot Studio

## Definition
The JSON Handler Node is a powerful new addition to the Journey Builder Canvas in the Bot Studio platform. It allows bot designers to effortlessly extract information from simple to complex JSON objects without requiring coding expertise. This feature simplifies handling JSON responses from APIs or channel messages, making the platform more accessible, especially for non-technical users.

## Procedure
### Exact path
Gupshup Console → Bot Studio → JSON Handler

### Where to configure it
Gupshup Console → Bot Studio → JSON Handler

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Navigate to Action Nodes in Journey Builder and select JSON Handler.\

### Steps
1. Open Gupshup Console.
2. Navigate to Action Nodes in Journey Builder and select JSON Handler.\
3. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Select from Local, Global, and System variables containing JSON responses.
- Add the JSON Handler Node Navigate to Action Nodes in Journey Builder and select JSON Handler.\
- Select JSON Variable Choose the variable containing the JSON response from the dropdown (Local, Global, or System).\
- Choose the variable containing the JSON response from the dropdown (Local, Global, or System).\

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Transform & Validation Transform Button reformats JSON for easier viewing. Real-time error handling for invalid JSON inputs.
- Real-time error handling for invalid JSON inputs.
- Error-Free Data Mapping Built-in validation ensures that only correct mappings are applied, reducing runtime errors.
- ## Error Handling
- Invalid JSON Inputs Real-time error messages appear in the editor if JSON is invalid.
- Real-time error messages appear in the editor if JSON is invalid.

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
# JSON Handler

**Module**: Bot Studio

## Overview
The JSON Handler Node is a powerful new addition to the Journey Builder Canvas in the Bot Studio platform. It allows bot designers to effortlessly extract information from simple to complex JSON objects without requiring coding expertise. This feature simplifies handling JSON responses from APIs or channel messages, making the platform more accessible, especially for non-technical users.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Navigate to Action Nodes in Journey Builder and select JSON Handler.\

## Step-by-step configuration
## Introduction

The JSON Handler Node is a powerful new addition to the Journey Builder Canvas in the Bot Studio platform. It allows bot designers to effortlessly extract information from simple to complex JSON objects without requiring coding expertise. This feature simplifies handling JSON responses from APIs or channel messages, making the platform more accessible, especially for non-technical users.

## Key Features

- Intuitive JSON Parsing Provides a user-friendly interface to parse JSON responses and map attributes to variables.
- Provides a user-friendly interface to parse JSON responses and map attributes to variables.
- Flexible Variable Selection Select from Local, Global, and System variables containing JSON responses. Encrypted JSON variables are excluded from selection to ensure security.
- Select from Local, Global, and System variables containing JSON responses.
- Encrypted JSON variables are excluded from selection to ensure security.
- Sample JSON Input & Editor Input a sample JSON to visualize and map data. Use the Open Editor to modify or map elements within the JSON. Split-panel editor with code view (left) and formatted JSON with mapping capabilities (right).
- Input a sample JSON to visualize and map data.
- Use the Open Editor to modify or map elements within the JSON.
- Split-panel editor with code view (left) and formatted JSON with mapping capabilities (right).
- Hover-to-Map Feature Hover over keys and values in the formatted JSON to quickly map them to variables.
- Hover over keys and values in the formatted JSON to quickly map them to variables.
- Transform & Validation Transform Button reformats JSON for easier viewing. Real-time error handling for invalid JSON inputs.
- Transform Button reformats JSON for easier viewing.
- Real-time error handling for invalid JSON inputs.
- Mapping Capabilities Create up to 10 mappings per node. Support for nested JSON structures and arrays. Enforce values as stringified objects using the Enforce String option.
- Create up to 10 mappings per node.
- Support for nested JSON structures and arrays.
- Enforce values as stringified objects using the Enforce String option.
- Data Persistence Sample JSON and mappings are saved with the journey upon Save or Deploy actions. Runtime validation ensures correct data types; failures will prevent updates to the destination variable.
- Sample JSON and mappings are saved with the journey upon Save or Deploy actions.
- Runtime validation ensures correct data types; failures will prevent updates to the destination variable.
## Key Benefits

- Simplified JSON Handling Eliminates the need for custom code, allowing non-technical users to manage JSON data effortlessly.
- Eliminates the need for custom code, allowing non-technical users to manage JSON data effortlessly.
- Enhanced Flexibility Supports a wide range of JSON structures, from simple key-value pairs to deeply nested objects.
- Supports a wide range of JSON structures, from simple key-value pairs to deeply nested objects.
- Increased Efficiency Reduces the time and effort required to handle JSON responses within journeys.
- Reduces the time and effort required to handle JSON responses within journeys.
- Error-Free Data Mapping Built-in validation ensures that only correct mappings are applied, reducing runtime errors.
- Built-in validation ensures that only correct mappings are applied, reducing runtime errors.
## How to Use

- Add the JSON Handler Node Navigate to Action Nodes in Journey Builder and select JSON Handler.\
Add the JSON Handler Node

- Navigate to Action Nodes in Journey Builder and select JSON Handler.\
- Select JSON Variable Choose the variable containing the JSON response from the dropdown (Local, Global, or System).\
Select JSON Variable

- Choose the variable containing the JSON response from the dropdown (Local, Global, or System).\
- Input Sample JSON Click on the Map JSON Attribute to add sample JSON for parsing Paste your sample JSON and click on Format
Input Sample JSON

- Click on the Map JSON Attribute to add sample JSON for parsing
- Paste your sample JSON and click on Format
- Map JSON Attributes Use the hover functionality in the right panel to map JSON keys/values to variables. You can also Map JSON objects by collapsing the JSON Object and then hovering on the collapsed line. Review mappings in the Path to Attribute -> Set to Variable section.
Map JSON Attributes

- Use the hover functionality in the right panel to map JSON keys/values to variables.
- You can also Map JSON objects by collapsing the JSON Object and then hovering on the collapsed line.
- Review mappings in the Path to Attribute -> Set to Variable section.
- Save and Deploy Click Save to store your mappings and JSON structure. Deploy the journey to apply the JSON Handler Node in live scenarios.
Save and Deploy

- Click Save to store your mappings and JSON structure.
- Deploy the journey to apply the JSON Handler Node in live scenarios.
## Use Cases

- API Response Handling Scenario: Extract user data (e.g., name, email) from API responses. Benefit: Simplifies parsing API responses without custom code.
- Scenario: Extract user data (e.g., name, email) from API responses.
- Benefit: Simplifies parsing API responses without custom code.
- Channel Message Parsing Scenario: Process structured JSON messages received from messaging platforms. Benefit: Quickly extract and utilize key message details in the journey.
- Scenario: Process structured JSON messages received from messaging platforms.
- Benefit: Quickly extract and utilize key message details in the journey.
- Nested Data Extraction Scenario: Handle complex nested JSON objects from third-party integrations. Benefit: Supports deep JSON structures, making complex data extraction seamless.
- Scenario: Handle complex nested JSON objects from third-party integrations.
- Benefit: Supports deep JSON structures, making complex data extraction seamless.
## Error Handling

- Invalid JSON Inputs Real-time error messages appear in the editor if JSON is invalid.
- Real-time error messages appear in the editor if JSON is invalid.
- Mapping Errors Validation errors are triggered if mappings are incorrectly set. Runtime validation ensures data type compatibility; failures prevent incorrect data storage.
- Validation errors are triggered if mappings are incorrectly set.
- Runtime validation ensures data type compatibility; failures prevent incorrect data storage.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Sample JSON and mappings are saved with the journey upon Save or Deploy actions.
- - Save and Deploy Click Save to store your mappings and JSON structure. Deploy the journey to apply the JSON Handler Node in live scenarios.
- Save and Deploy
- - Click Save to store your mappings and JSON structure.
- - Deploy the journey to apply the JSON Handler Node in live scenarios.

**Last updated (from source)**: Updated 9 months ago
