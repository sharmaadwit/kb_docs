source_url: https://console-docs.gupshup.io/docs/tools-beta

<!-- kb-golden:v10 -->
# Tools (Developer Mode)

**Module**: Ai Admin

## Definition
Introduction: Tools enable your AI Agent to perform dynamic actions, fetch real-time data, or integrate with external systems. They act as functional extensions of the agent’s capabilities—helping it go beyond static responses and enabling task execution, data retrieval, or logic-driven behavior.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Tools (Developer Mode)

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Tools (Developer Mode)** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Tools (Developer Mode)**.
4. Provide Tool Name & Description: Provide a clear and descriptive name for the tool along with a description that captures its purpose and variables to be used in the tool schema.
5. Add API Specification (Optional) You can configure how the tool connects to an external system by sharing a sample API request & response OR adding OpenAPI endpoint.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Tool Testing:Users can run a test tool code with sample input values to validate output. Save the tool which provides valid output.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **Tools (Developer Mode)**.

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
# Tools (Developer Mode)

**Module**: Ai Admin

## Overview
Introduction: Tools enable your AI Agent to perform dynamic actions, fetch real-time data, or integrate with external systems. They act as functional extensions of the agent’s capabilities—helping it go beyond static responses and enabling task execution, data retrieval, or logic-driven behavior.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Note: AI Agent is available in developer mode through our Gupshup’s internal Bot Solutions Team. To access the latest AI Agent modules in Bot Studio please contact Gupshup support or your respective Sales representative.

Introduction: Tools enable your AI Agent to perform dynamic actions, fetch real-time data, or integrate with external systems. They act as functional extensions of the agent’s capabilities—helping it go beyond static responses and enabling task execution, data retrieval, or logic-driven behavior.

Type of Tools:Users have provision to use available system tools or configure custom tools

- System Tools: Built-in pre-configured, non-editable tools. Example
- get_faq_answer_content_tag: Tool to get answers from specific content tags trained using the organization's knowledge base
- Custom Tools: Related by users to extend the agent’s capabilities based on business-specific needs Ex. Users can create a tool to fetch order status, generate OTPs, calculate interest rates etc.
Tool Usage in Skills:Tools are referenced inside the skill instructions, where their purpose and tool call logic are described. During runtime:

- The agent calls the tool when specified conditions are met.
- Tool responses can be used to generate dynamic replies.
- Multiple tools can be used in a single skill if needed.
Steps to Create a Custom Tool:

- Provide Tool Name & Description: Provide a clear and descriptive name for the tool along with a description that captures its purpose and variables to be used in the tool schema
- Define Input & Output Schema: Schema defines how data is sent to & received by the tool
- Add API Specification (Optional) You can configure how the tool connects to an external system by sharing a sample API request & response OR adding OpenAPI endpoint
- Generate Tool Code:Based on tool input & output Schema LLM generates the tool code.
Note: When tool code is generated Safety checks are run on the generated tool code to ensure code doesn't contain any harmful coding patterns, risky system-level commands, unsafe read/write actions and more. A tool that fails the safety checks can not be saved.

- Tool Testing:Users can run a test tool code with sample input values to validate output. Save the tool which provides valid output.
Updated 10 months ago

- Settings

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Tool Testing:Users can run a test tool code with sample input values to validate output. Save the tool which provides valid output.
