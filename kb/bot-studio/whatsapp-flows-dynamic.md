source_url: https://console-docs.gupshup.io/docs/whatsapp-flows-enhancement-dynamic-flow-support
# BOT STUDIO

## WhatsApp Flows - Dynamic

# WhatsApp Flows - Dynamic

# Introduction:

The Journey Builder WhatsApp Flow Node now supports triggering dynamic flows, even for flows that begin with the first screen in dynamic mode. This enhancement ensures end-to-end support for triggering both static and dynamic WhatsApp flows from Journey Builder, allowing seamless integration and execution for all Bot Studio users.

# Key Aspects of the Feature

- Support for Dynamic and Static Flows: With the addition of First Screen type option, developers can now decide if the Flow triggered should be of type Navigate (static) or Data Exchange (dynamic) for routing the flow to the next screens.
- Dynamic Flow Initialization: Supports triggering flows that start with a dynamic first screen, allowing for customized and adaptive user experiences right from the beginning.
# How to Use:

- On WhatsApp Flow node click on the First Screen Dropdown to view the options
- Select the type of First Screen that will be sent
- Incase of Dynamic Flow select Data Exchange and for Static Flow select Navigate
- Continue configuring the node as required and the Flow will be triggered with the same config during runtime
- For Dynamic Flows make sure you have the Data Channel mapping done on the Meta BM while creating the Flow JSON
- To receive the responses submitted on the WA Flows on Console/WhatsApp Flow Journey, the Dynamic Channel have to send back the payload on the nfm reply at the Terminal Screen to use the same on the WhatsApp Flow Journey\
# Implementing Dynamic Flows

## Define the Flow Structure:

Create a JSON structure that outlines the sequence of screens and interactions within your flow. Each screen represents a step in the conversation and can include various interactive elements.

## Set Up the Data Channel:

For dynamic flows, establish a data channel that facilitates communication between the WhatsApp client and your server. This involves specifying the endpoint_uri when creating or updating your flow via the Flows API. Contact Gupshup Support to update your endpoint for your WhatsApp Flows.

## Configure the Server Endpoint:

Develop a server endpoint that can process incoming requests from the WhatsApp client. This endpoint should be capable of receiving user inputs, processing them, and responding with appropriate data to guide the flow's progression.

To know more on Implementing Endpoints for Dynamic Flow/Data Exchange: Meta Doc

## Handling User Responses and Webhook Integration

To capture and utilize user responses within your WhatsApp Flow Journey, follow these steps:

Receive User Inputs: As users interact with the flow, their inputs are sent to your server via the data channel. Your server should be prepared to handle these inputs appropriately.

Process and Respond: Upon receiving user inputs, your server processes the data and determines the subsequent steps in the flow. It then sends back the necessary information to the WhatsApp client to continue the interaction.

Send Payload to Webhook: At the terminal screen of the flow, ensure that your dynamic channel sends back the payload . This action, often referred to as an "nfm reply," is crucial for transmitting the collected data back to your system.

Integrate with WhatsApp Flow Journey: The data received at the webhook can now be utilized within your WhatsApp Flow Journey. This integration allows for seamless utilization of user responses, enabling you to tailor subsequent interactions or trigger specific actions based on the collected data. The submit action of the WA Flow will update the data sent from your Data Channel in the message_metadata system variable of the WhatsApp Flow journey

# How to setup Data Channel?

For setting up the Data Channel for Dynamic Flows, refer to the Meta Documentation or reach out to Gupshup Support or Customer Success Team for hosting and pricing details.

Updated 10 months ago
