source_url: https://console-docs.gupshup.io/docs/cta-url-support-on-reply-button

<!-- procedural:v2 -->
# CTA URL Button Node

**Module**: Bot Studio

## Overview
The CTA URL Button Node is a new addition to the Message Category in Journey Builder, designed to enhance WhatsApp messaging capabilities. This feature allows businesses and bot designers to share clickable links directly through a Call-To-Action (CTA) button, eliminating the need for sending lengthy URLs as text messages. It simplifies user interactions, offering a seamless way to direct users to external websites, promotions, or resources.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Navigate to Message Nodes in Journey Builder and select the CTA URL Button Node.

## Step-by-step configuration
# Introduction

The CTA URL Button Node is a new addition to the Message Category in Journey Builder, designed to enhance WhatsApp messaging capabilities. This feature allows businesses and bot designers to share clickable links directly through a Call-To-Action (CTA) button, eliminating the need for sending lengthy URLs as text messages. It simplifies user interactions, offering a seamless way to direct users to external websites, promotions, or resources.

# Key Features

- WhatsApp-Only Support This node is specifically designed for WhatsApp and does not support other channels.
- This node is specifically designed for WhatsApp and does not support other channels.
- Single Button Restriction The CTA URL Button supports only a single button, with no provision to add or remove additional buttons.
- The CTA URL Button supports only a single button, with no provision to add or remove additional buttons.
- Dynamic URL Support URLs can be passed dynamically using variables, allowing personalized links for each user.
- URLs can be passed dynamically using variables, allowing personalized links for each user.
- URL Validation Directly entered URLs are validated during design time to ensure correctness. For variable-mapped URLs, designers must ensure the runtime values are valid, as no design-time validation is performed.
- Directly entered URLs are validated during design time to ensure correctness.
- For variable-mapped URLs, designers must ensure the runtime values are valid, as no design-time validation is performed.
- Media Header Support Similar to the Reply Button Node, the CTA URL Button supports media headers, allowing rich media content alongside the link.
- Similar to the Reply Button Node, the CTA URL Button supports media headers, allowing rich media content alongside the link.
- No Inactivity Timer Required This node functions similarly to a standard text message on WhatsApp, without requiring a Wait For Event or Inactivity Timer.
- This node functions similarly to a standard text message on WhatsApp, without requiring a Wait For Event or Inactivity Timer.
- Multi-Lingual Support Both the Button Name and URL fields support multiple languages, enhancing accessibility for diverse audiences.
- Both the Button Name and URL fields support multiple languages, enhancing accessibility for diverse audiences.
# Key Benefits

- Streamlined User Experience Simplifies the process of sharing links on WhatsApp, making it easier for users to access external resources.
- Simplifies the process of sharing links on WhatsApp, making it easier for users to access external resources.
- Enhanced Engagement Clickable CTA buttons improve user interaction rates compared to traditional text links.
- Clickable CTA buttons improve user interaction rates compared to traditional text links.
- Dynamic and Personalized Messaging The ability to pass dynamic URLs allows for personalized user experiences, increasing relevance and engagement.
- The ability to pass dynamic URLs allows for personalized user experiences, increasing relevance and engagement.
- Multi-Lingual Capability Supports multiple languages, making it suitable for global audiences and localized campaigns.
- Supports multiple languages, making it suitable for global audiences and localized campaigns.
# How to Use

- Add the CTA URL Button Node Navigate to Message Nodes in Journey Builder and select the CTA URL Button Node.
Add the CTA URL Button Node

- Navigate to Message Nodes in Journey Builder and select the CTA URL Button Node.
- Configure the URL Enter a direct URL for validation during design time, or use variables to pass dynamic URLs.
Configure the URL

- Enter a direct URL for validation during design time, or use variables to pass dynamic URLs.
- Set Button Name Provide a name for the CTA button, ensuring it is clear and action-oriented. Utilize multi-lingual support if needed.
Set Button Name

- Provide a name for the CTA button, ensuring it is clear and action-oriented. Utilize multi-lingual support if needed.
- Add Media Header (Optional) If desired, add a media header similar to the Reply Button Node for a richer message experience.
Add Media Header (Optional)

- If desired, add a media header similar to the Reply Button Node for a richer message experience.
- Save and Deploy Once configured, save the node and deploy the journey to start using the CTA URL Button in your WhatsApp messages.
Save and Deploy

- Once configured, save the node and deploy the journey to start using the CTA URL Button in your WhatsApp messages.
# Use Cases

- Promotional Campaigns Scenario: Share links to special offers, discounts, or new product launches. Benefit: Increases click-through rates and customer engagement with direct access to promotional content.
- Scenario: Share links to special offers, discounts, or new product launches.
- Benefit: Increases click-through rates and customer engagement with direct access to promotional content.
- Event Registrations Scenario: Direct users to registration pages for webinars, events, or appointments. Benefit: Simplifies the registration process, improving attendance rates.
- Scenario: Direct users to registration pages for webinars, events, or appointments.
- Benefit: Simplifies the registration process, improving attendance rates.
- Customer Support Scenario: Provide links to support articles, FAQs, or live chat options. Benefit: Enhances customer service by offering quick access to helpful resources.
- Scenario: Provide links to support articles, FAQs, or live chat options.
- Benefit: Enhances customer service by offering quick access to helpful resources.
- Feedback Collection Scenario: Share links to feedback forms or surveys. Benefit: Encourages user feedback, helping businesses improve their services.
- Scenario: Share links to feedback forms or surveys.
- Benefit: Encourages user feedback, helping businesses improve their services.
# Error Handling

- Invalid URL Entries Direct URLs are validated during design time to ensure they are correct.
- Direct URLs are validated during design time to ensure they are correct.
- Variable-Mapped URL Issues Designers must ensure runtime values are valid, as no design-time validation is provided for variable-mapped URLs.
- Designers must ensure runtime values are valid, as no design-time validation is provided for variable-mapped URLs.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Save and Deploy Once configured, save the node and deploy the journey to start using the CTA URL Button in your WhatsApp messages.
- Save and Deploy
- - Once configured, save the node and deploy the journey to start using the CTA URL Button in your WhatsApp messages.

**Last updated (from source)**: Updated 10 months ago
