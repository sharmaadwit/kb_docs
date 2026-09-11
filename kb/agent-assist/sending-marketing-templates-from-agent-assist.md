> Source: https://console-docs.gupshup.io/docs/sending-marketing-templates-from-agent-assist
> Last updated: 2026-09-11

As brands increasingly prioritize WhatsApp for their sales operations, one of the most requested features is enabling agents to send WhatsApp-approved templates to customers, facilitating seamless communication. This functionality allows agents to initiate conversations with customers by selecting a pre-approved template, entering the customer's phone number, and then sending the template with a simple click.

## Overview

<Cards columns={2}>
  <Card title="For Agents" icon="fa-user-tie">
    Send approved WhatsApp templates directly to customers from the Agent Assist interface
  </Card>
  <Card title="For Administrators" icon="fa-cog">
    Configure agent campaigns, set up journeys, and manage user permissions
  </Card>
</Cards>

---

## Configuration Setup

<Tabs>
  <Tab title="Create Agent Campaigns">

### Step 1: Navigate to Campaign Creation
Go to **Settings > Workflow & Automation > Agent Campaigns > Create Campaign**

### Step 2: Configure Campaign Details
When you create a campaign, a popup will request:
- **Campaign name**: Choose a descriptive name for your campaign
- **Template**: Select from your approved WhatsApp templates
- **Test phone number**: Provide an internal number for testing (a template message will be sent to this number upon creation)

### Step 3: Automatic System Actions
Once you create an agent campaign, the following happen automatically:

<Accordion title="Campaign Manager Integration" icon="fa-chart-line">
All analytics associated with the campaign will be visible under campaign analytics in the Campaign Manager.
</Accordion>

<Accordion title="Bot Studio Journey Creation" icon="fa-robot">
An interactive journey with an agent handover node is created in Bot Studio. When customers reply to agent-sent campaigns, they'll be routed through this newly created journey before agent assignment. You can edit this journey after creation if needed.
</Accordion>

  </Tab>
  
  <Tab title="Beta Feature Setup">

### Enable Beta Features
> **Note**: This is currently a beta feature

To activate this functionality:
1. Send an email to [console-support@gupshup.io](mailto:console-support@gupshup.io)
2. Request configuration for your brand
3. Once enabled, navigate to Journey Builder within Campaign Journey
4. A journey named "Agent Assist" will be created automatically

When customers respond to templates sent by agents, they will enter this journey, allowing you to:
- Assign chats to agents
- Route conversations to other journeys

![Campaign Journey Setup](https://files.readme.io/3639b5c-image.png)

  </Tab>
  
  <Tab title="Campaign Properties">

### Configure Access and Settings
After setting up the journey, navigate to **Agent Assist > Agent Campaigns > Campaign Properties** to configure:

![Campaign Properties Interface](https://files.readme.io/7ea8a7f-image.png)

<Accordion title="Stickiness Settings" icon="fa-clock">
**Chat Stickiness** determines the time period within which returning customers will be assigned to the same agent who sent the original template.

**Additional Options**:
- Choose whether chats should be assigned to the same agent even if unavailable
- Set up fallback team routing based on team policy
</Accordion>

<Accordion title="User Restrictions" icon="fa-users">
**Agent Selection**: Use the dropdown menu to restrict this feature to specific agents, providing granular control over who can send marketing templates.
</Accordion>

  </Tab>
</Tabs>

---

## Using the Feature

### For Agents: Sending Templates

<Columns layout="auto">
  <Column>
    
#### Step 1: Access Template Sending
1. In the Chat Inbox, locate the **WhatsApp icon** next to views
2. Click the icon to open the template selection popup

![WhatsApp Template Access](https://files.readme.io/3078b6f-image.png)

  </Column>
  <Column>
    
#### Step 2: Send to Customer
1. Choose your desired template
2. Enter the customer's phone number with country code
3. Check the opt-in box if the customer's number is opted in
4. Click send

![Template Sending Interface](https://files.readme.io/7340d50-image.png)

  </Column>
</Columns>

### Troubleshooting Common Issues

<Accordion title="Template Sending Error" icon="fa-exclamation-triangle">
If an agent encounters an error while sending a template, it may be due to an existing open chat with the same customer that isn't assigned to the sending agent.

**Solution**: The agent needs to assign the existing chat to themselves before attempting to send the message.
</Accordion>

### Managing Customer Responses

When customers reply to marketing templates:

1. **System Notification**: Agents will see a system message indicating the conversation contains a marketing message
2. **Template Identification**: Click on the marketing message or use the campaign context button in the right panel
3. **Template History**: View all templates sent to the customer for context

![Customer Response Management](https://files.readme.io/514f3ba-image.png)

---

## Key Benefits

<Cards columns={3}>
  <Card title="Streamlined Communication" icon="fa-comments">
    Enable agents to initiate WhatsApp conversations with pre-approved templates
  </Card>
  <Card title="Compliance Ready" icon="fa-shield-alt">
    Use only WhatsApp-approved templates to ensure messaging compliance
  </Card>
  <Card title="Analytics Integration" icon="fa-chart-bar">
    Track campaign performance through integrated analytics and reporting
  </Card>
</Cards>

---

## Next Steps

After setting up marketing templates in Agent Assist:
- Monitor campaign analytics in the Campaign Manager
- Adjust journey flows in Bot Studio as needed
- Train your agents on the new functionality
- Review and optimize stickiness and routing settings based on performance