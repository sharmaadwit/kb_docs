<!-- kb-golden:v10 -->
# RCS Best Practices & Optimization Guide

**Module**: Channels

## Definition

Best practices for RCS messaging maximize engagement, compliance, and ROI by following proven design patterns, audience segmentation strategies, and performance optimization techniques. This guide covers message design, template approval, personalization, timing, media handling, and analytics interpretation to help brands achieve peak performance on RCS channels.

## Message Design Best Practices

### Text Content Guidelines

- **Keep messages concise** — Limit main text to under 500 characters for optimal readability
- **Lead with value** — First line should immediately communicate benefit or action required
- **Use short sentences** — Break long content into 2-3 sentence blocks for mobile readability
- **Avoid urgency language** — Don't use "Act now!", "Limited time!", "Urgency" tactics (triggers spam filters and lowers trust)
- **Include brand voice** — Maintain consistent tone and personality across all messages
- **Test on mobile** — Always preview messages on actual Android device before sending

### Rich Media Strategy

- **Images improve engagement 3x** — Use high-quality product images, brand imagery, or data visualizations
- **Use media strategically** — Don't add images just for decoration; every image should support the message goal
- **Video for complex info** — 10-30 second videos explain processes (delivery flow, how to use, product demo) better than text
- **Avoid wall-of-text** — Use rich cards to break up content into scannable chunks (title + image + description)
- **Carousel for choices** — Use multi-card carousels to show multiple products or options (max 5-10 cards)
- **GIFs for engagement** — Animated GIFs (under 5MB, looping) increase click rates 20-30%

### Interactive Elements Guidelines

- **Limit buttons to 2-3 per message** — More than 3 buttons confuses users; prioritize top 2 actions
- **Use descriptive button labels** — Instead of "Click here" or "Yes/No", use "Track Order", "View Receipt", "Claim Offer"
- **Action buttons as conversation starters** — Use suggested replies for customer input (Yes/No, feedback, next steps)
- **URL actions for conversion** — Drive traffic to landing page, claim link, or product detail page
- **Calendar actions for booking** — Add events directly to user's calendar (appointment, delivery date, event)
- **Map actions for locations** — Share store location, delivery address, or meeting point
- **Fallback text for all rich cards** — Always include plain-text version of card content for non-RCS devices

## Template Approval Best Practices

### Pre-Submission Checklist

- **Clear business value** — Template description should explain what customer gets (offer, update, request)
- **No spam language** — Avoid words like "Free money", "Guaranteed", "Risk-free", "Best", "Exclusive"
- **No urgency tactics** — Don't use "Act now", "Limited time", "Only X left", "Expires soon"
- **Fallback text matches rich content** — Plain-text version should convey same message as rich card
- **Media URLs public and accessible** — Test all image/video URLs; ensure no expired/private links
- **Test in sandbox first** — Send test messages to RCS numbers before approval submission

### Template Structure

- **Title** — Under 200 characters, clear and specific
- **Description** — Under 400 characters, concise value proposition
- **Media** — Minimum 500x500px, ideally 1080x1080px, JPG/PNG format
- **Button labels** — Clear, action-oriented, under 30 characters each
- **Suggested replies** — Plain-text only, 2-3 options maximum

### Common Approval Delays

- **Prohibited content** — Templates with affiliate links, gambling, unverified health claims, investment offers
- **Unclear business purpose** — Generic templates without specific use case
- **Unresolved media URLs** — Links that return 404 or require authentication
- **Deceptive formatting** — Using special characters to hide content or spam indicators
- **Solution** — Contact support if approval takes >48 hours beyond SLA

## Audience & Compliance Best Practices

### Consent & Legal

- **Obtain explicit opt-in before messaging** — Document user consent (checkbox, SMS opt-in code, web form)
- **Honor opt-out requests within 24 hours** — Implement unsubscribe immediately; maintain opt-out list
- **Include unsubscribe link in marketing messages** — Every promotional message should have "Unsubscribe" button or link
- **Segment by preference** — Keep separate lists: marketing (promotions), transactional (orders), support (help)
- **Privacy compliance** — Follow GDPR, CCPA, TCPA, and local regulations for your regions

### Brand & Identity

- **Use brand name consistently** — RCS displays your logo, brand name, and verification badge; maintain consistency
- **Verification badge requirement** — Only verified brands show badge; unverified messages are marked "unregistered business"
- **Logo quality** — Use high-resolution logo (square format, 512x512px minimum) for display
- **Color consistency** — Ensure brand colors render consistently across Android Messages and iMessage

## Personalization Best Practices

### Variable Substitution

- **Customer first name** — Use `{{first_name}}` for greeting when available (increases engagement 15-20%)
- **Order ID for transactional** — Reference specific order number, booking ID, or delivery ID
- **Purchase history context** — "Based on your recent purchase of X, here's Y" feels relevant, not spammy
- **Segment-based content** — Different templates for VIP vs new customer vs churn risk
- **Last interaction reference** — "Following up on your support ticket #123" adds context

### Testing & Iteration

- **A/B test message variations** — Test same offer with different subject lines, images, buttons
- **Test send times** — When do your customers engage most? 9am vs noon vs 5pm can differ 2-3x
- **Test button labels** — "Learn More" vs "See Details" vs "Get Offer" can change click rate 20%
- **Test with small audience first** — Send to 5-10% of audience, monitor metrics before full rollout
- **Avoid excessive personalization** — Don't use too many variables or dynamic content (feels spammy and breaks trust)

## Timing & Frequency Best Practices

### Send Timing Strategy

- **Transactional messages immediately** — Send order confirmations, delivery updates, alerts without delay
- **Marketing during business hours** — Send between 9am-5pm in user's timezone for higher display rates
- **Avoid early morning/late night** — Don't send before 8am or after 9pm (lower engagement, annoying)
- **Test peak hours** — Analyze your analytics; some audiences engage better at 1pm vs 3pm
- **Respect user timezone** — Use user's local timezone for scheduling; personalization of timing drives 2x higher engagement

### Frequency Guidelines

- **Limit marketing to 1-2 per week per customer** — Frequency >2/week causes 30-40% unsubscribe spike
- **Space campaigns 2-3 days apart** — Don't send back-to-back campaigns (users perceive as spam)
- **Daily transactional is OK** — Order updates, alerts, support messages can be frequent (they expect these)
- **Monitor unsubscribe rate** — If >1% of audience unsubscribes after campaign, frequency is too high
- **Seasonal adjustment** — Holiday campaigns can be more frequent (Black Friday, Diwali); adjust post-season

## Media Best Practices

### Image Specifications

- **Format** — JPG or PNG only (not WebP, GIF, or BMP)
- **Size** — Under 100MB total file size; typically 2-5MB for optimal load
- **Dimensions** — 1080x1080px is optimal; minimum 500x500px to avoid pixelation
- **Aspect ratio** — Square (1:1) works best for cards; 16:9 for fullscreen video
- **Alt text** — Always include descriptive alt text for accessibility ("Order confirmation photo of product X")
- **Compression** — Optimize images to reduce load time; under 1 second load target

### Video Specifications

- **Format** — MP4 or WebM (H.264 codec)
- **Size** — Under 100MB total file size; typically 10-50MB for 10-30 second video
- **Duration** — 10-30 seconds ideal (longer videos have lower completion rates)
- **Dimensions** — 1080x1920px vertical or 1920x1080px horizontal
- **Codec** — H.264 for compatibility; ensure audio is AAC codec
- **Preview thumbnail** — Provide static image to show before video plays
- **Captions** — Add captions for accessibility (many watch without sound)

### GIF Specifications

- **Size** — Under 5MB; 2-5MB is typical for high-quality GIFs
- **Duration** — 3-5 seconds ideal; looping GIFs should feel natural
- **Dimensions** — 1080x1080px or 1080x1920px
- **Optimization** — Use tools to reduce file size (ImageMagick, Gifsicle)
- **Animation rate** — 8-10 frames per second for smooth motion without file bloat

## Rich Card Best Practices

### Content Structure

- **Title** — Under 200 characters, benefit-focused ("15% Off Fresh Groceries" vs "New Promo")
- **Description** — Under 400 characters, include key details and CTA hint ("Tap below to claim")
- **Media always included** — Visual element is crucial; cards without media have 50% lower engagement
- **Action buttons** — 2-3 buttons maximum; prioritize top 1-2 actions
- **Suggested replies** — Plain-text quick replies for follow-up questions or feedback

### Carousel Best Practices

- **Multi-product showcase** — Use carousels to show 3-5 product options (not more than 5)
- **Sequential storytelling** — Use carousel to walk through process steps (delivery journey, onboarding)
- **Consistent card design** — All cards in carousel should have similar structure and layout
- **Navigation clear** — Users should understand they can swipe left/right through cards
- **Call-to-action clarity** — Each card should have a primary action button (not just text)

## Analytics & Optimization

### Key Metrics to Track

- **Delivery rate** — % of messages successfully delivered (95%+ is healthy)
- **Display rate** — % of delivered messages that were displayed in user's Messages app (70-80% typical)
- **Click rate** — % of users who clicked on suggested action buttons (15-30% varies by CTA quality)
- **Reply rate** — % of users who replied to message (5-15% for interactive elements)
- **Conversion rate** — % of recipients who completed desired action (claim offer, book appointment, purchase)
- **Unsubscribe rate** — % of recipients who opted out after campaign (<1% is target)

### Performance Benchmarks by Use Case

**Order Confirmations:**
- Delivery: 98%+
- Display: 85%+
- Click rate: 30%+ (tracking link)
- Reply rate: 5%+ (support questions)

**Promotional Offers:**
- Delivery: 95%+
- Display: 75%+
- Click rate: 20-25% (offer claim)
- Reply rate: 3-5%

**Account Alerts (Security, Status):**
- Delivery: 99%+
- Display: 90%+
- Click rate: 10-15% (follow-up action)
- Reply rate: 2-3%

**Customer Support:**
- Delivery: 99%+
- Display: 95%+
- Click rate: 35%+ (quick replies)
- Reply rate: 60%+ (conversation)

### Optimization Process

1. **Baseline** — Send campaign to 10% audience; measure all metrics
2. **Identify bottleneck** — Which metric is lowest? (Delivery, display, click, or reply?)
3. **Test improvement** — Vary one element (time, image, button label, personalization)
4. **Measure impact** — Compare new campaign metrics to baseline
5. **Scale winner** — Roll out improved version to full audience
6. **Iterate** — Repeat process to compound improvements over time

## Common Mistakes to Avoid

- **❌ Not testing on actual device** — Always preview on real Android phone; emulators don't show true rendering
- **❌ Sending to non-opted audiences** — Will result in high unsubscribe, spam complaints, and brand damage
- **❌ Overloading with buttons** — More than 3 buttons causes decision paralysis; users abandon
- **❌ Using unrelated images** — Stock photos that don't match message confuse users and lower trust
- **❌ Ignoring opt-out requests** — Compliance violation; always honor unsubscribe within 24 hours
- **❌ Spammy language** — "Free money", "Act now", "Risk-free" triggers filters and damages brand
- **❌ Not providing customer value** — Every message should benefit customer (offer, update, solution), not just brand
- **❌ Sending during odd hours** — Late-night/early morning sends have 40% lower display rates
- **❌ Insufficient personalization** — Generic "Hi Customer" vs "Hi Sarah" can reduce engagement 20%
- **❌ Media URL expiration** — Links that break after campaign goes live create negative experience
- **❌ No fallback text** — Non-RCS devices see blank if no plain-text version; causes confusion
- **❌ Ignoring analytics** — Send, hope for best; instead analyze and iterate every campaign

## RCS vs WhatsApp Comparison

| Factor | RCS | WhatsApp |
|--------|-----|----------|
| **Best for** | Rich media, verified branding, reach campaigns | Conversations, support, retention |
| **Reach** | 2 billion+ RCS users (90+ carriers) | 1.5+ billion WhatsApp users |
| **Media support** | Rich cards, carousels, images, video, GIF | Limited rich cards; mostly media + text |
| **Interactive elements** | Suggested replies, URL buttons, calendar, map | Reply buttons, call buttons |
| **Verification** | Verified brand badge, logo display | Verified checkmark (green badge) |
| **Template approval** | 24-48 hour approval | 24-48 hour approval |
| **Cost model** | Per message + delivery | Conversation-based pricing |
| **2-way capability** | Yes (webhooks for replies) | Yes (native conversations) |
| **Analytics depth** | Delivery, display, click, reply rates | Read receipts, message status |
| **Device requirement** | RCS-enabled Android (or iPhone) | WhatsApp app installed |
| **Use RCS for** | Campaigns, marketing, announcements, offers | Ongoing conversations, support tickets |
| **Use WhatsApp for** | One-time high-value offers (supplements) | Customer service, retention, loyalty |

**Dual-channel strategy:** Use RCS for campaign reach with rich media; use WhatsApp for support and relationship building. Users who reply on RCS can be moved to WhatsApp for ongoing conversation.

## Performance Benchmarks

### Industry Standards (Typical Performance)

**Delivery Metrics:**
- Healthy delivery rate: 95%+
- Poor delivery (<90%): Check audience location matches RCS coverage (not all markets have 100% RCS adoption)
- Great delivery (98%+): Verified brand, clean audience, valid phone numbers

**Display Metrics:**
- Healthy display rate: 70-80%
- Poor display (<60%): Check send timing; late-night sends have lower rates
- Great display (85%+): Optimal timing + compelling preview text

**Click Metrics:**
- Healthy click rate: 15-30% (depends heavily on CTA quality)
- Poor click (<10%): Button label unclear; wrong audience; weak offer
- Great click (30%+): Clear CTA; relevant audience; compelling button text

**Reply Metrics:**
- Healthy reply rate: 5-15% (only if message asks for response)
- Poor reply (<3%): Audience doesn't engage; check sentiment
- Great reply (15%+): Strong suggested replies; personalized message

### Segmentation Impact

- **VIP customers** — 40-50% higher engagement rates than general audience
- **Repeat customers** — 25-30% higher click rates than new customers
- **Personalized messages** — 15-20% higher display and click rates vs generic
- **Targeted offers** — 20-25% higher conversion vs generic campaigns
- **Previous non-engagers** — 10% lower performance; consider re-engagement strategy or exclusion

## Compliance Checklist

Use this checklist before sending any RCS campaign:

- **✓ Opt-in documented** — Record of user consent (email, SMS opt-in, web form signup)
- **✓ Brand verified** — RCS agent is verified; display badge will show
- **✓ Unsubscribe option available** — Marketing messages include "Unsubscribe" button/link
- **✓ Templates approved** — All templates used have passed approval (not custom/ad-hoc)
- **✓ No spam content** — Language, frequency, and timing comply with best practices
- **✓ Rate limits respected** — Frequency within guidelines (1-2/week marketing; transactional flexible)
- **✓ Media URLs valid** — All image/video links tested and public (no 404s or expired URLs)
- **✓ Fallback text present** — All rich cards have plain-text version for non-RCS devices
- **✓ Legal review done** — Message complies with GDPR, CCPA, TCPA for target regions
- **✓ Analytics planned** — Know what metrics to track and improvement plan for next iteration

## Related Docs

- [RCS Overview](./rcs-overview.md)
- [RCS Agent Setup](./rcs-agent-setup.md)
- [RCS Templates](./rcs-templates.md)
- [RCS Messaging API](./rcs-messaging-api.md)
- [RCS Webhooks & Callbacks](./rcs-webhooks-and-callbacks.md)
- [RCS FAQ](./rcs-faq.md)
- [RCS Campaigns (Campaign Manager)](../campaign-manager/rcs-campaigns.md)
