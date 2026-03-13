source_url: https://console-docs.gupshup.io/docs/whatsapp-flows-static-2-way

<!-- kb-golden:v9 -->
# WhatsApp Flows - Static/Dynamic

**Module**: Bot Studio

## Definition
The WhatsApp Flows feature enhances the platform's capabilities by enabling two-way messaging triggered from the JB WhatsApp Flow node. With this feature, you can seamlessly initiate WhatsApp Flows at any point during a conversation, ensuring dynamic interaction and real-time engagement.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → WhatsApp Flows - Static/Dynamic

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **WhatsApp Flows - Static/Dynamic**.
4. Ensure the WABA is hosted on Cloud API of WhatsApp.
5. Ensure the Console Project is using V3 version of WhatsApp Service - Contact Support to confirm incase required.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Ensure the Console Project is using V3 version of WhatsApp Service - Contact Support to confirm incase required.
- Draft Toggle: Use this toggle to test Flow IDs in draft state on Meta BM (not yet published).

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **WhatsApp Flows - Static/Dynamic**.

## Options / variants
- Draft Toggle: Use this toggle to test Flow IDs in draft state on Meta BM (not yet published).

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# WhatsApp Flows - Static/Dynamic

**Module**: Bot Studio

## Overview
The WhatsApp Flows feature enhances the platform's capabilities by enabling two-way messaging triggered from the JB WhatsApp Flow node. With this feature, you can seamlessly initiate WhatsApp Flows at any point during a conversation, ensuring dynamic interaction and real-time engagement.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Introduction:

The WhatsApp Flows feature enhances the platform's capabilities by enabling two-way messaging triggered from the JB WhatsApp Flow node. With this feature, you can seamlessly initiate WhatsApp Flows at any point during a conversation, ensuring dynamic interaction and real-time engagement.

Ref: Meta Documentation

## Key aspects of this feature include:

- Triggering WhatsApp Flows: Initiate WhatsApp Flows at any time during a two-way conversation using the WhatsApp Flows Node, enhancing the flexibility and responsiveness of your messaging strategy.
- Handling Responses: Efficiently manage responses from WhatsApp Form submissions within the WhatsApp Flows Journey, ensuring that collected information is processed and utilized effectively.
- Information Passing: Pass required information to different journeys for diverse use case handling, enabling complex workflows and comprehensive user interaction scenarios.
This feature is designed to optimize your communication strategies, allowing for more personalized and timely interactions with your users through WhatsApp.

## Use Cases:

WhatsApp Flows can significantly enhance business communication and operational efficiency across various industries. Here are several use cases that demonstrate the potential applications of WhatsApp Flows:

### 1. Customer Support and Service:

Scenario: A customer contacts support for help with a product issue. WhatsApp Flow: Trigger a diagnostic form to gather detailed information about the issue. Benefit: Streamlines the support process, enabling quicker resolution.

Scenario: Post-resolution feedback collection. WhatsApp Flow: Send a feedback form to the customer after resolving their issue. Benefit: Gathers valuable customer feedback, improving service quality.

### 2. Sales and Marketing

Scenario: Lead qualification. WhatsApp Flow: Trigger a questionnaire to qualify leads during initial contact. Benefit: Automates lead qualification, ensuring sales teams focus on high-potential leads.

Scenario: Promotional campaign engagement. WhatsApp Flow: Send promotional offers or surveys to engage customers during a campaign. Benefit: Enhances customer engagement and drives conversions.

### 3. Appointment Scheduling

Scenario: Medical or service appointments. WhatsApp Flow: Send an appointment scheduling form when a user requests a booking. Benefit: Simplifies the booking process, reducing administrative overhead.

Scenario: Appointment reminders and confirmations. WhatsApp Flow: Send reminders and allow users to confirm or reschedule their appointments. Benefit: Reduces no-show rates and improves operational efficiency.

### Pre-Checks:

- Ensure the WABA is hosted on Cloud API of WhatsApp
- Ensure the Console Project is using V3 version of WhatsApp Service - Contact Support to confirm incase required.
- Create your Flow using the Meta Business Manager and ensure its working by Testing it from Meta BM
- Make sure to Publish the flow or use Draft Mode on the WhatsApp Flow Node while testing
### What's supported ?

- Sending of WhatsApp Flows (Static/Dynamic) is supported from Bot Studio
- Developers have to create the Flow JSON/Flow Screens using the Meta Business Manager only and ensure that the runtime information which are required are properly mapped during Flow creation time
- WhatsApp Flows can only be sent during an open session in the current phase.
### What's not supported?

- Triggering WhatsApp Flows via a Template Node is not supported
- No default Data Channel is provided for Dynamic WhatsApp Flows. Contact Support/CSM for Data Channel hosting and pricing details.
- Flow creation on Console, Importing of existing flows are not supported
## Functional Elements of the Feature:

- WhatsApp Flow Message Node
- WhatsApp Flow Journey
- Flow Starting Node
- Flow Terminal Nodes
### 1. WhatsApp Flow Message Node:

The WhatsApp Flow Node is now available in the Journey Builder (JB) Canvas under the Message Nodes category. This feature enables you to send pre-approved WhatsApp Flows seamlessly. You can create these Flows in Meta Business Manager and use the corresponding Flow ID to trigger the WhatsApp Flow Message directly from the platform.

Fields Available in the WhatsApp Flow Node:

- Flow ID: This is generated in the Business Manager after drafting a WhatsApp Flow. You can find the list of available Flows IDS once the Flow Journey is created.
- Draft Toggle: Use this toggle to test Flow IDs in draft state on Meta BM (not yet published).
- Message: You can send a free-form message along with the Flow CTA Button to inform the user about the Flow.
- Footer: An optional footer message can be added if required.
- Button Title: The name of the CTA Button that will be displayed on the WhatsApp application after clicking the Form.
- First Screen Type: Provides the option to select between 'Navigate' or 'Data Exchange' based on the Flow type - 'Static' or 'Dynamic,' respectively.
- First Screen: This is the ID of the screen that needs to be shown as the first screen to the user. Businesses can render different first screens for different end users based on their requirements. Not applicable if the Flow Type is Dynamic/Data Exchange
- Additional Data: WhatsApp Flows also allow the passing of additional information on the first screen, which can be defined during the flow creation. Flow JSON designers can create the keys for which values can be passed during the flow sending time. Bot designers can pass JSON key-value pairs in the Additional Data field of the WhatsApp Flow Node to leverage this feature. Not applicable if the Flow Type is Dynamic/Data Exchange
More Details on Meta Doc: https://developers.facebook.com/docs/whatsapp/flows/gettingstarted/sendingaflow

Note: The WhatsApp Flow Node is a non-continuity enabled node on JB Canvas, meaning bot designers cannot connect any node after it. This is because the response of the WhatsApp Flow requires handling in a separate Flows Journey. To manage the response of WhatsApp Flows, bot designers need to configure the WhatsApp Flow Journey by navigating to Bot Studio > WhatsApp Flows.

### 2. WhatsApp Flows Journey:

The WhatsApp Flows Journey is an integral part of the WhatsApp Flow runtime process. Designers must create a WhatsApp Flow Journey corresponding to each Flow ID used in the User Journeys to receive and handle the Flow Responses.

Bot designers must enter the Flow ID generated at Meta’s end before creating the Flow Journey. Flow Journeys ensure that the Flow ID used is sent to the user, and once the flow is submitted, the Flow Journey containing the respective Flow ID to which the user has responded will receive the Flow Response payload. This payload will be saved as a JSON in the system variable system_var.message_meta

Sample Payload for the Flows Response: The payload differs based on the Flow Components and number of screens.

```
{
  "screen_3_TextArea_0": "Excellent ",
  "screen_2_RadioButtonsGroup_0": "0_Yes",
  "screen_2_RadioButtonsGroup_1": "0_Yes",
  "screen_2_TextArea_2": "E-Retail ",
  "screen_1_RadioButtonsGroup_0": "0_5",
  "screen_1_TextInput_1": "John",
  "screen_1_TextInput_2": "john@gupshup.io",
  "flow_token": "d2FmbC9maWQvMTYyNTAzMDI4NDk0NDQ5Ni93YWJhL3VuZGVmaW5lZC9jaWQvOTE4NzIzMDYyMjY1L2ZtaWQvMTczNzEwMTc0MTA3Mz9kYXRhPSIi"
}
```

This journey receives the Flow Response JSON, which contains the parameters filled in by the end user on the Flows form. The bot designer can parse this JSON to fetch the values entered by the user and call APIs to transfer the data to other systems if required.

### 3. Flow Starting Node

Flow Starting Node is a default node on Flow Journey and the Flow ID entered while creating the Flow Journey will be prefilled on the Flow Starting Node. The Flow Starting Node is non-editable.

Currently, there is provision for using the API, Code, and Modify Variable nodes in the Flows Journey to parse and use the Flow Response before reaching the Terminal Node to pass on the context to a different journey

### 4. Flow Terminal Node

The Terminal Node is the final node for any Flow Journey. Bot designers must ensure that every Flow Journey ends with a Terminal Node for proper handling of the Flow submission. Multiple Terminal Nodes can be used based on the conditions under which designers want to continue the journey after Flow submission.

Terminal Node consists of optional parameters that can be configured to handle the post flow submission action.

Trigger Journey:

Bot designers can configure to trigger a User Journey by passing the Flow Variables to a different journey and continue the conversation with the same context.

There is also a provision to map the variables of the User Journey to those of the Flow Journey to pass the Flow response values .

Terminal Message:

Designers can choose to just send an acknowledgement message to the end user and post submission of the form using the optional Terminal Message. This allows bot designers to complete the Flow within the Flow Journey if the data is already sent to client CRM or other Databases using the API and Code node.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Make sure to Publish the flow or use Draft Mode on the WhatsApp Flow Node while testing

**Last updated (from source)**: Updated 10 months ago
