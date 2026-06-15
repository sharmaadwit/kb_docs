source_url: https://docs.gupshup.io/docs/campaigns-overview

<!-- kb-golden:v10 -->
# Getting Started with Gupshup Campaigns

**Module**: Overview

## What Are Campaigns?

Campaigns let you send personalized, bulk messages to your customers across multiple channels (WhatsApp, RCS, SMS) simultaneously. Unlike one-off messages, campaigns help you reach thousands of people at scale while tracking engagement and managing compliance.

**Key benefits:**
- **Scale & Speed** — Send to thousands of recipients in seconds
- **Personalization** — Use customer data to customize each message
- **Scheduling** — Choose when messages are delivered for maximum impact
- **Analytics** — Track sent, delivered, failed, and read rates in real time
- **Compliance** — Built-in opt-in verification and audit trails

---

## Getting Started with Campaigns

**New to campaigns? Start here.**

### Step 1: Create Your First Campaign
Once you've connected a channel (WhatsApp, RCS, or SMS) and have message templates approved, creating your first campaign takes about 10 minutes.

**Read:** [Creating Your First Campaign](../campaign-manager/creating-your-first-campaign.md)

This guide covers:
- What you need before you start (channel setup, templates, audience list)
- Step-by-step walkthrough of the Campaign Manager interface
- How to upload your audience and personalize messages
- How to schedule and launch your campaign
- How to monitor delivery in real time

### Step 2: Build Confidence with Best Practices
Every channel has unique rules and optimal strategies. Understanding these upfront saves time and improves engagement.

**Read:** [RCS Best Practices & Optimization Guide](../channels/rcs-best-practices.md)

This guide helps you:
- Design messages that get approved (avoid spam triggers)
- Use rich media (images, videos, buttons) effectively
- Structure interactive elements for maximum engagement
- Understand timing and personalization strategies
- Interpret analytics to refine future campaigns

### Step 3: Explore Channel-Specific Features
Different channels support different message types and capabilities.

**Browse by channel:**
- **RCS Campaigns** — [RCS Campaigns Overview](../campaign-manager/rcs-campaigns.md) — Understand RCS-specific features like rich cards and carousels
- **WhatsApp Campaigns** — [How to Access Campaign Manager](../campaign-manager/how-to-access-campaign-manager.md) — Get oriented in the UI and find campaign tools
- **Bot Studio Integration** — [Campaign & Journey Integration](../bot-studio/campaign-journey.md) — Connect campaigns to automated workflows

---

## Channel Best Practices

Each messaging channel has unique strengths. Choose the right channel and strategy for your use case.

### WhatsApp Best Practices

**Why WhatsApp?**
- Highest engagement rates
- Direct, 1-to-1 conversation feel
- Reliable delivery across regions
- Great for time-sensitive alerts (orders, deliveries, OTPs)

**Key practices:**
- Keep messages short and scannable
- Use personalization (names, order details) to build trust
- Segment audiences by intent and history
- A/B test send times to find your audience's peak window

**Learn more:** [Creating a New Campaign](../campaign-manager/creating-a-new-campaign.md)

### RCS Best Practices

**Why RCS?**
- Rich media built in (images, videos, interactive buttons)
- Higher click rates than SMS
- Native Android experience
- Perfect for product catalogs and rich experiences

**Key practices:**
- Use rich cards to showcase products or offers
- Carousels for multiple options or product galleries
- Interactive buttons for surveys, feedback, or CTAs
- Always include fallback text for non-RCS devices

**Learn more:** [RCS Best Practices & Optimization Guide](../channels/rcs-best-practices.md)

### SMS Best Practices

**Why SMS?**
- Universal reach (doesn't require app installation)
- Highest delivery rates globally
- Perfect for short, urgent messages
- Ideal for audiences without smartphone access

**Key practices:**
- Keep messages under 160 characters to avoid splits
- Use shortcodes for better brand recognition
- Include clear call-to-action (link, phone, or reply)
- Test across carriers for formatting consistency

---

## Optimize Engagement

After you've sent your first campaign, use these tips to increase open rates, click rates, and conversions.

### Timing Strategies

**Send at the right moment:**
- **Test send times** — Every audience has a peak engagement window. Use analytics to find yours (usually 10am–2pm, 7pm–9pm by time zone)
- **Consider time zones** — Segment audiences by geography if you span multiple regions
- **Avoid quiet hours** — Don't send between midnight–6am unless it's an urgent alert
- **Schedule for holidays** — Adjust timing around holidays and cultural events

### Personalization

**Make messages feel personal:**
- **Use customer names** — Messages with names have 15–25% higher open rates
- **Reference past interactions** — "Your recent order #12345 is on the way"
- **Segment by behavior** — Send different messages to VIP customers, first-time buyers, and churned customers
- **Dynamic content** — Use customer data (purchase history, preferences, location) to customize copy

### A/B Testing

**Improve with data:**
- **Test subject lines/openers** — Try different greeting styles (friendly vs. professional)
- **Test media types** — Some audiences prefer images, others respond to video
- **Test button labels** — "Track Order" vs. "View Delivery Status" may have different click rates
- **Test segment sizes** — 10% test + 90% rollout to validate before full send
- **Track what matters** — Focus on conversions, not just opens

### Message Design for Engagement

**Structure for success:**
- **Lead with benefit** — First line should make the reader want to continue
- **Keep it scannable** — Use short paragraphs and white space
- **Clear call-to-action (CTA)** — One primary action per message (link, button, reply)
- **Build urgency (ethically)** — Create genuine scarcity ("Last 3 seats") rather than false urgency
- **Use power words** — "Exclusive", "Unlock", "Discover", "Save" tend to outperform generic language

### Analytics & Iteration

**Use data to improve:**
- **Monitor delivery rates** — If >5% fail, check channel configuration or audience list quality
- **Track engagement** — Compare open, click, and conversion rates against benchmarks
- **Segment by channel** — RCS may outperform SMS for your audience; optimize allocations accordingly
- **Create feedback loop** — Review successful campaigns and replicate their structure
- **Watch for fatigue** — If engagement drops after repeated sends, increase time between campaigns or rotate messaging

---

## Advanced Topics

Ready to level up? Explore these specialized features.

### Automated Campaigns

**Set it and forget it:**
- [Sending an Automated Campaign](../campaign-manager/sending-an-automated-campaign.md) — Schedule recurring campaigns or trigger-based sends
- [Automated Campaign Analytics](../campaign-manager/automated-campaign-analytics.md) — Track performance of autopilot campaigns over time

### Analytics & Reporting

**Measure what matters:**
- [Campaign Analytics Dashboard](../campaign-manager/campaign-analytics.md) — Deep dive into sent, delivered, failed, read, and click metrics
- [Campaign Listing Page](../campaign-manager/campaign-listing-page.md) — View campaign history, status, and quick stats

### Integration with Journeys

**Connect campaigns to customer workflows:**
- [Campaign & Journey Integration](../bot-studio/campaign-journey.md) — Trigger campaigns from Bot Studio journeys or send campaigns as journey steps

### Click-to-WhatsApp Ads

**Drive campaign traffic:**
- [Click-to-WhatsApp Campaign](../ctx/creating-and-analysing-a-click-to-whatsapp-campaign.md) — Run ads that open WhatsApp conversations at scale

---

## Next Steps

1. **Connect a channel** — Ensure your WhatsApp, RCS, or SMS channel is active and configured
2. **Create your first campaign** — Follow [Creating Your First Campaign](../campaign-manager/creating-your-first-campaign.md) to send your first bulk message
3. **Monitor & optimize** — Check analytics after launch and apply insights from [Channel Best Practices](../channels/rcs-best-practices.md)
4. **Explore automation** — Once comfortable, try [automated campaigns](../campaign-manager/sending-an-automated-campaign.md) to scale further

**Questions?** Refer to [Campaign Manager Overview](../campaign-manager/about-campaign-manager.md) or explore the full [Console Navigation Guide](./console-navigation-guide.md) to find any feature in the UI.

---

## Reference (from source)

<!-- procedural:v2 -->
# Gupshup Campaigns: Getting Started Guide

A comprehensive index for new users learning to create, optimize, and scale bulk messaging campaigns across WhatsApp, RCS, and SMS channels.
