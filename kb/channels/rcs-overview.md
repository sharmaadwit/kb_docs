source_url: https://api.dotgo.com/rcs

<!-- kb-golden:v10 -->
# RCS (Rich Communication Services) Overview

**Module**: Channels

## Definition

RCS (Rich Communication Services) is Gupshup's advanced messaging channel for capturing attention in the SMS inbox with rich, 2-way and engaging conversation. Built on the Dotgo RBM (Rich Business Messaging) platform, RCS is the natural upgrade path from SMS—offering your brand visibility with verification badges, logo displays, and interactive messaging capabilities that drive higher engagement and ROI.

RCS enables brands to send rich media messages (images, videos, carousels), interactive suggestions (replies, action buttons, QR codes), and track delivery and engagement in real-time across 90+ global carriers and 2 billion+ RCS-enabled users.

**Marketing value prop:** Capture attention, drive engagement, reduce friction, and track ROI—all in the familiar Messages app (Android) and iMessage (iPhone).

## Key Capabilities

- **Verified Branding**: Your logo + brand name + verification badge display in user's Messages app (builds trust, prevents spoofing)
- **Rich Media Messaging**: Send images, videos, GIFs, PDFs (up to 100MB) with high-quality thumbnails
- **Rich Card Templates**: Single or carousel cards with title, description, media, and interactive action buttons
- **Interactive Suggestions**: Suggested replies, URL actions (web/deep link), dialer actions (phone), calendar actions (event add), map actions (location share)
- **Dynamic Templates**: Pre-approved message templates with variable placeholders for personalization
- **In-depth Analytics**: Track delivery rate, view rate (message read), interaction rate (click-through), and engagement metrics
- **Real-time Webhooks**: Receive instant notifications for incoming messages, user interactions, and message status changes
- **Global Reach**: 2 billion+ RCS users across 90+ carriers (USA, India, Brazil, Germany, Europe, APAC)
- **Flexible API Standards**: Support for both GSMA Chatbot MaaP and Google Business Messages (RBM) API specifications
- **Fallback & Compliance**: Built-in SMS fallback for non-RCS devices; template approval workflow ensures regulatory compliance

## When to Use

Use RCS when you need to:
- **Increase engagement** — Rich media (images, videos, carousels) drives 3-5x higher interaction vs SMS
- **Drive conversions** — Interactive suggestion buttons (reply, URL, phone, calendar, map) reduce friction and boost click-through rates
- **Build brand trust** — Verification badge and logo display differentiate your brand from phishing and spam
- **Enable 2-way conversation** — Receive customer replies in real-time via webhooks
- **Track detailed analytics** — Delivery, displayed, read, click, and reply metrics for ROI measurement
- **Reduce support costs** — Suggested actions (book appointment, check status, claim offer) enable self-service
- **Support global reach** — 2 billion users across 90+ carriers worldwide
- **Personalize at scale** — Dynamic templates with custom variables for each customer
- **Ensure compliance** — Template approval workflow prevents spam and regulatory violations

**Use cases:**
- Order confirmations + delivery tracking with tracking links
- Flight + hotel bookings with calendar adds and map links
- Promotional offers with direct claim buttons
- Account security alerts with 2FA verification options
- Customer support with suggested reply options
- E-commerce product catalogs with carousel cards

## Setup Path

1. **Register as RBM Agent** — Submit brand details, business information, and verification documents
2. **Configure Bot/Agent** — Create an RCS bot with branding (logo, colors, name, description)
3. **Create Templates** — Design and submit message templates for approval
4. **Integrate APIs** — Implement GSMA or Google RBM APIs in your application
5. **Set Up Webhooks** — Register webhook endpoints for message events and callbacks
6. **Test & Deploy** — Validate in sandbox, then go live

## RCS Architecture

**Server Root**: `https://api.dotgo.com/rcs`

**API Styles**:
- **GSMA Chatbot MaaP APIs** — Per GSMA MaaP Chatbot API specifications
- **Google RBM APIs** — Per Google Business Messages specifications

**Authentication**: OAuth2 SSO via Dotgo Auth service (Bearer tokens)

## Supported Carriers & Regions

- **Global reach**: 90+ RCS-enabled carriers
- **Primary markets**: India, USA, Europe, APAC
- **Regional variations**: Carrier support varies by region; check carrier list before deploying

## Compliance & Guidelines

- All templates must be approved before use
- Fallback SMS messages required for template failures
- Confidentiality flags control message visibility in sensitive contexts
- Rate limits apply per agent (default: 60 TPM = transactions per minute)
- Message expiration handling for TTL scenarios

## Field mapping / schemas

Detailed field specifications are documented in API reference sections for each endpoint (agent creation, template submission, message sending).

## Cross-module workflow docs

- **Channels**: RCS agent registration and bot setup
- **Campaign Manager**: [Use RCS as a channel for multi-channel campaigns](../../campaign-manager/rcs-campaigns.md)
- **Bot Studio**: Route RCS messages via connected bots
- **Analytics**: Track RCS message metrics and delivery rates

## Module disambiguation docs

RCS is a messaging channel managed at the Channels level. Message logic and routing rules are configured separately in Bot Studio or Campaign Manager based on your use case.

## Reference (from source)

<!-- procedural:v2 -->
# RCS Overview

RCS provides rich communication capabilities with advanced templating, media support, and interactive elements for modern messaging experiences.
