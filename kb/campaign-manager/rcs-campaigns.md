source_url: https://console-docs.gupshup.io/docs/rcs-campaigns

<!-- kb-golden:v10 -->
# RCS Campaigns

**Module**: Campaign Manager

## Definition

RCS campaigns enable brands to send rich, interactive messages at scale using the RCS (Rich Communication Services) channel. RCS campaigns combine the reach and scheduling capabilities of Campaign Manager with the advanced messaging features of RCS (rich media, interactive buttons, verified branding).

## When to Use

Use RCS campaigns when you need to:
- Send personalized promotional offers with interactive claim buttons
- Deliver order updates with rich tracking cards and suggested replies
- Run appointment booking campaigns with calendar integration
- Reach audiences with verified brand messaging and high engagement

**RCS campaigns vs other channels:**
- **WhatsApp campaigns:** RCS has higher delivery rates for authenticated brands but smaller user base
- **SMS campaigns:** RCS provides richer experience but requires RCS-enabled devices
- **Email campaigns:** RCS enables real-time, in-app delivery with high engagement

## Prerequisites

1. **RCS Agent registered** - Complete RCS agent registration via Channels module
2. **RCS templates approved** - All templates must be approved before use
3. **Campaign Manager access** - Access to create and schedule campaigns
4. **Target audience** - User database with phone numbers for RCS-enabled devices

## Setup Path

### 1. Register RCS Agent (One-time)

Go to **Channels → RCS** and complete RCS agent registration:
- Submit brand verification documents
- Configure agent branding (logo, name, colors)
- Receive RCS agent credentials

See: [RCS Agent Setup](../channels/rcs-agent-setup.md)

### 2. Create and Approve RCS Templates

In **Channels → RCS → Templates**:
- Design message templates with rich media and interactive elements
- Include fallback plain-text version for non-RCS devices
- Submit for approval (24-48 hour approval time)
- Wait for approval before campaigns can use them

See: [RCS Templates](../channels/rcs-templates.md)

### 3. Create RCS Campaign

In **Campaign Manager → Create Campaign**:
1. Select **Channel: RCS**
2. Choose **Template:** Select an approved RCS template
3. Configure **Recipients:** Upload phone number list or select segment
4. Set **Scheduling:** Immediate or scheduled send
5. Add **Personalization:** Map template variables to user data
6. Review and **Send**

### 4. Monitor Campaign Performance

In **Campaign Manager → Campaign → Analytics**:
- **Delivery rate:** % of messages successfully delivered
- **Displayed rate:** % of messages displayed in user's Messages app
- **Click rate:** % of users who clicked suggested action buttons
- **Reply rate:** % of users who replied to the campaign

## Examples

### Example 1: Order Confirmation with Tracking

```
Template: "Order Confirmation + Tracking"
Content:
  - Order number (variable)
  - Rich card with order summary
  - Tracking link with "Track Order" button
  - Suggested replies: "Track Order", "Contact Support", "Return Item"
```

### Example 2: Promotional Offer Campaign

```
Template: "Limited Time Offer"
Content:
  - Product image (rich media)
  - Offer headline and terms
  - "Claim Offer" button linking to store
  - "Learn More" button with detailed T&Cs
```

## Best Practices

1. **Use rich media wisely** - Images load faster on RCS; videos should be <10MB
2. **Keep CTAs clear** - 2-3 suggested action buttons per message
3. **Test with small audience first** - Send to 5-10% of audience, monitor metrics before full roll-out
4. **Optimize send times** - Check RCS analytics to find peak engagement windows
5. **Include fallback SMS** - For non-RCS devices, SMS fallback is automatic
6. **Monitor unsubscribe rates** - RCS requires easy opt-out mechanism

## Troubleshooting

### Campaign shows 0% delivery

**Check:** Are all recipients RCS-enabled? (Not all markets have 100% RCS adoption)

**Solution:** Verify audience location matches RCS carrier coverage

### Messages show as delivered but not displayed

**Check:** Did users see the message notification?

**Solution:** Check message timing; late-night sends have lower display rates

### Template approval pending >48 hours

**Check:** Did template include prohibited content?

**Solution:** Contact support if approval delays beyond SLA

## Field mapping / schemas

Campaign variables map to RCS template placeholders:

```
User CSV: [phone, name, order_id, amount]
Template: "Hi {name}, order {order_id} is ready! Amount: {amount}"
```

Ensure CSV column names match template variable names.

## Cross-module workflow docs

- **Channels:** RCS agent setup and template management
- **Campaign Manager:** Campaign scheduling and execution
- **Analytics:** RCS-specific metrics (delivery, display, click, reply rates)
- **Bot Studio:** Route incoming RCS replies to bot logic

## Module disambiguation

- **RCS channel (Channels module):** For 1-on-1 messaging and API integration
- **RCS campaigns (Campaign Manager):** For mass marketing campaigns with scheduling
- **Chatbot via RCS:** For conversation routing via Bot Studio

## Related docs

- [RCS Overview](../channels/rcs-overview.md)
- [RCS Templates](../channels/rcs-templates.md)
- [RCS Messaging API](../channels/rcs-messaging-api.md)
- [Campaign Manager Guide](./about-campaign-manager.md)
- [Campaign Analytics](./campaign-analytics.md)

## Reference (from source)

<!-- procedural:v2 -->
# RCS Campaigns

Send rich, interactive messages at scale using RCS through Campaign Manager's scheduling and analytics capabilities.
