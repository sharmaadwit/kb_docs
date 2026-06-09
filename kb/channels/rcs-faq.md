source_url: https://api.dotgo.com/rcs/faq

<!-- kb-golden:v10 -->
# RCS Frequently Asked Questions

**Module**: Channels

## Definition

Quick answers to common questions about RCS (Rich Communication Services) business messaging, capabilities, setup, and best practices.

---

## What is RCS?

**Q: What does RCS stand for?**

A: **Rich Communication Services**. It's the GSMA-defined standard for an IP messaging solution that offers a natural upgrade path from SMS. RCS enables rich, interactive messaging with images, videos, suggested actions, and real-time delivery tracking—all in the native Messages app (Android) and iMessage app (iPhone).

**Q: How is RCS different from SMS?**

A: | Feature | SMS | RCS |
|---|---|---|
| **Message length** | 160 chars | 2,500 chars |
| **Media** | Text only | Images, videos, GIFs, PDFs (up to 100MB) |
| **Interactivity** | None | Suggested replies, action buttons, carousels |
| **Verification** | No | Brand logo + verification badge |
| **Delivery tracking** | Limited | Delivery, displayed, read status |
| **Cost** | Lower | Higher engagement ROI |

**Q: Who uses RCS?**

A: Over **2 billion users globally** across:
- **USA**: 250+ million
- **India**: 500+ million
- **Brazil**: 100+ million
- **Germany**: 50+ million
- Plus coverage in 90+ carriers worldwide

---

## Why Should I Use RCS?

**Q: What business problems does RCS solve?**

A: RCS helps you:
- **Capture attention** in the SMS inbox with your brand's logo and verification badge
- **Increase engagement** with rich media (images, videos, interactive carousels)
- **Reduce friction** with suggested replies and action buttons (no typing needed)
- **Drive conversions** via direct links (URLs, phone calls, calendar adds, map locations)
- **Track ROI** with in-depth analytics on delivery, views, clicks, and replies
- **Build trust** with verified branding and reduced phishing risk

**Q: What's the ROI of RCS vs SMS?**

A: Customers typically see:
- **3-5x higher engagement** (rich media drives interaction)
- **2-3x better conversion** (clickable actions reduce friction)
- **Higher customer satisfaction** (faster, richer responses)
- **Reduced support costs** (self-service via suggested actions)

**Q: When should I use RCS instead of SMS?**

A: Use RCS when:
- **High engagement matters** — Promotions, flight confirmations, order tracking
- **Visual content helps** — Product catalogs, travel itineraries, event tickets
- **User action is needed** — Booking, claiming offers, selecting options
- **Brand trust is critical** — Financial alerts, account security, identity verification

Use SMS when:
- **Simple notification only** — System alerts, OTPs (though RCS supports OTP templates)
- **Lowest cost matters** — Bulk notifications where interaction isn't needed
- **Very old devices** — Basic phones without RCS support

---

## Getting Started

**Q: How long does RCS setup take?**

A: End-to-end:
- **Agent registration**: 24-48 hours for Dotgo approval
- **Template submission**: 2-4 hours for template approval
- **First message**: Immediately after template approval
- **Total**: ~24-48 hours from start to sending live messages

**Q: What information do I need to register?**

A: - Company name and website
- Brand logo (224x224px JPG/PNG, <90KB)
- Privacy policy URL
- Terms & conditions URL
- Support contact email
- Expected monthly message volume

**Q: Can I test before going live?**

A: Yes. After agent registration:
1. Dotgo provides a **sandbox environment** for testing
2. Test with your own phone number or small test group
3. No approval needed for template testing in sandbox
4. Production messages require template approval

**Q: Do I need to write code?**

A: Yes, basic API integration is required:
- REST API calls (POST/GET) to send messages and check status
- OAuth2 token management (1-line per request)
- Webhook setup to receive incoming messages
- Use our SDKs or any HTTP client (cURL, Postman, Python requests, etc.)

See rcs-quickstart.md for a 5-minute setup guide.

---

## Features & Capabilities

**Q: What types of messages can I send?**

A: **Text messages** — Plain text up to 2,500 chars

**Template messages** — Pre-approved formats:
- Text + PDF
- Rich card (image + title + description)
- Rich card carousel (multiple cards)
- With suggested replies, action buttons, etc.

**File messages** — Direct images, videos, GIFs (up to 100MB)

See rcs-messaging-api.md for examples.

**Q: What are suggested replies and action buttons?**

A: Interactive suggestions that appear below the message:
- **Reply buttons** — Text suggestions user can tap (e.g., "Yes", "No")
- **URL action** — Open a website (e.g., "Shop Now")
- **Dialer action** — Call a phone number (e.g., "Call Support")
- **Calendar action** — Add event to calendar (e.g., "Add to Calendar")
- **Map action** — Show location on map (e.g., "Get Directions")

User taps a button → instant postback to your webhook (no typing needed).

**Q: Can I send the same message to multiple users?**

A: Yes, in two ways:
1. **Loop over recipients** — Make individual API calls for each phone number (simple, good for <1000 users)
2. **Campaign Manager** — Use Gupshup Campaign Manager to send at scale with scheduling and analytics

**Q: What's the rate limit?**

A: Default: **60 TPM (transactions per minute)** per agent.
- 1 message = 1 transaction
- 60 messages per minute = ~3,600 per hour
- Contact support to increase limits

---

## Delivery & Status

**Q: What does "delivered" mean?**

A: Message status progression:
- **pending** — Queued, not yet sent
- **sent** — Reached carrier network
- **delivered** — Arrived on user's phone
- **displayed** — User opened the message
- **failed** — Delivery failed (no RCS support, opt-out, etc.)
- **cancelled** — You revoked the message before delivery

**Q: Why did my message fail?**

A: Common reasons:
- User's device doesn't support RCS (no Android Messages or iMessage update)
- Carrier doesn't support RCS in that region
- User opted out of RCS messaging
- Invalid phone number format
- Message quota/rate limit exceeded
- Invalid template or parameters

See rcs-api-reference.md error codes section.

**Q: Can I see who read my message?**

A: Yes. Message status includes:
- **delivered** — Confirmed on device
- **displayed** — Confirmed user opened it

Webhooks notify you in real-time when status changes. Use this for analytics dashboards.

---

## Compliance & Security

**Q: Are there compliance requirements?**

A: Yes:
- **Templates must be approved** before use (no spam, misleading content)
- **Fallback SMS required** — If RCS delivery fails, have SMS as backup
- **Carrier guidelines** — Some carriers restrict promotional content
- **GDPR/privacy** — Follow local consent and data retention rules
- **Rate limits** — Comply with carrier and platform limits

**Q: Is RCS secure?**

A: RCS is more secure than SMS:
- **HTTPS encryption** for all API calls
- **Bearer token auth** (OAuth2) — no plain passwords
- **Verification badge** — Users see your verified brand (not spoofed)
- **End-to-end encryption** on RCS carriers (carrier-dependent)
- **No sensitive data in URLs** — Use postback callbacks instead

Store credentials in environment variables or secure vaults, never hardcoded.

---

## Troubleshooting

**Q: Template submission keeps getting rejected.**

A: Check:
- Media URLs are publicly accessible (not internal/localhost)
- Image dimensions and file sizes match requirements (see rcs-templates.md)
- Text content doesn't contain profanity, spam, or misleading info
- Fallback text is provided for rich cards

**Q: My messages aren't being delivered.**

A: Verify:
- Phone number is in E.164 format: `+1234567890`
- User's carrier supports RCS (see supported carriers list)
- User's device has RCS enabled (Android Messages, iMessage on iPhone)
- Template is approved (not in sandbox)
- You have quota/balance remaining

**Q: How do I receive incoming messages?**

A: Set up webhooks in your agent config (see rcs-webhooks-and-callbacks.md):
1. Register your webhook URL (HTTPS only)
2. When users reply, webhook is called with message content
3. Parse the webhook and respond via sending API

**Q: Can I integrate with my existing chatbot?**

A: Yes:
- Receive user messages via webhooks
- Process in your bot logic
- Send responses back via RCS messaging API
- See rcs-webhooks-and-callbacks.md for webhook payload details

---

## Integrations & Ecosystem

**Q: Does RCS work with Google Wallet?**

A: Yes. RCS messages can include:
- **Google Wallet link** — Users add passes directly from message
- **Google Pay integration** — Payment buttons for e-commerce
- **Google Maps integration** — Location sharing in maps action

This integrates RCS into the broader Google ecosystem.

**Q: Can I use RCS with Bot Studio?**

A: Yes:
1. Create RCS agent in Channels
2. In Bot Studio, add RCS as a delivery channel
3. Design journeys that send RCS messages
4. Use webhooks to receive user replies
5. Route to next node based on interaction

**Q: Can I send RCS from Campaign Manager?**

A: Yes. Campaign Manager supports RCS as a channel:
1. Create campaign → select RCS channel
2. Choose template or compose message
3. Select audience/recipient list
4. Schedule and send
5. Track delivery and engagement in analytics

---

## Analytics & Reporting

**Q: How do I track message performance?**

A: **Via API:**
- Query message status for individual messages
- Track delivery, displayed, and read counts
- Use webhook events for real-time tracking

**Via Dashboard (Analytics):**
- View delivery rate, engagement rate, conversion rate
- Filter by template, time period, carrier
- Export reports for analysis

See analytics documentation for detailed metrics.

**Q: Can I track clicks on action buttons?**

A: Yes. When users click an action button:
1. Webhook is sent with `suggestionResponse` data
2. Includes the postback data you set
3. You can track conversion in your system

---

## Pricing & Billing

**Q: How is RCS priced?**

A: Gupshup pricing typically:
- Per-message cost (varies by region and volume)
- Monthly agent fee (flat or tiered)
- Premium features (templates, webhooks, analytics)

Contact sales for pricing details.

**Q: Can I try RCS for free?**

A: Yes:
- **Sandbox environment** — Free testing with limited messages
- **Free tier** — Limited production quota (contact support)
- **Pilot program** — Often available for new brands

---

## Cross-module workflow docs

- **RCS Agent Setup** — Detailed registration (rcs-agent-setup.md)
- **RCS Templates** — All template types and approval process (rcs-templates.md)
- **RCS Messaging API** — Send messages, check status, handle webhooks (rcs-messaging-api.md)
- **RCS Authentication** — OAuth2 token management (rcs-authentication.md)
- **RCS Webhooks** — Receive incoming messages and events (rcs-webhooks-and-callbacks.md)
- **RCS API Reference** — Full endpoint documentation (rcs-api-reference.md)

## Reference (from source)

<!-- procedural:v2 -->
# RCS FAQ

Answers to common questions about RCS capabilities, setup, delivery, compliance, and integrations.
