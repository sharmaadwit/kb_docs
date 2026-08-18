<!-- kb-golden:v10 -->
# WhatsApp Messaging Best Practices (Evidence-Based)

**Module**: WhatsApp

## Definition

These are operational and messaging best practices for running WhatsApp Business API on Gupshup — template usage, message quality and opt-in, API integration, and onboarding-to-production practices. Every practice is grounded in real internal KB content: the WhatsApp error-codes troubleshooting guide, the WhatsApp pricing/quality-rating and API-reference docs, the WABA setup guide, the promotional-restrictions guidelines, and specific customer case studies. Campaign *strategy* (CTWA lead-gen, segmentation, cart recovery, contests) is intentionally excluded here — see `kb/campaign-manager/campaign-best-practices.md`. Nothing here is generic industry advice; unsupported claims are called out in the final section.

## Opt-In & Message Quality

- **Require explicit opt-in before any promotional message; treat unsolicited sends as spam** — repeated unwanted contact and bulk automated messaging without consent violate WhatsApp's Messaging Guidelines and can trigger account restrictions or suspension (source: kb/whatsapp/whatsapp-promotional-restrictions.md — "Users must have opted in to receive promotional messages. Sending unsolicited promotional messages constitutes spam"; enforcement includes account suspension and message blocking).
- **Provide an easy opt-out mechanism and stop messaging opted-out users** — repeat messages to opt-out users violate guidelines (source: kb/whatsapp/whatsapp-promotional-restrictions.md — "Users can opt-out, and repeat messages to opt-out users violate guidelines").
- **Protect your account quality rating — it directly governs throughput and cost** — rating moves Green → Yellow → Red based on complaint rate, message rejection rate, and spam reports; Yellow throttles throughput, Red risks rate increases and bans (source: kb/whatsapp/whatsapp-pricing.md — quality-rating table; kb/whatsapp/whatsapp-api-reference.md — Green 80 msg/sec, Yellow 40 msg/sec + 50% slow, Red 1 msg/sec major throttling).
- **Keep spam-complaint rate below 0.1% and track "Report" clicks with a feedback loop** — a rising complaint rate is what pushes accounts toward rejection (Error 131002) and quality downgrades (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — "Monitor spam complaint rate: maintain <0.1% across all recipients"; "Implement feedback loop: track which messages get Report clicks").
- **Avoid spam-trigger content: no "URGENT!!!", no URL shorteners, no multiple/suspicious links** — these get messages actively rejected by WhatsApp filters, not just throttled (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — Error 131002 prevention: "Avoid: URGENT!!!, multiple links, URL shorteners (use full URLs)").

## Template Usage & Approval

- **Use pre-approved templates for all campaign/broadcast sends** — sending non-template content in broadcast contexts causes rejections; templates are also 5–10x cheaper than service messages (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — "Use pre-approved message templates for campaigns"; kb/whatsapp/whatsapp-pricing.md — "Use templates whenever possible — 5-10x cheaper than service messages").
- **Fill every template variable and use the correct placeholders** — missing variables or wrong placeholders is a template violation that gets messages rejected (Error 131002) (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — "For templates: verify all variables filled, correct placeholders used"; kb/whatsapp/whatsapp-api-reference.md — template send requires ordered body parameters).
- **Always provide fallback text and avoid prohibited content at submission time** — the two most common causes of approval delay/rejection are missing fallback text and prohibited content (source: kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md — troubleshooting: "Template approval delayed → Check for prohibited content, ensure fallback text provided").
- **Test template content with a small group before full broadcast** — validate before scaling to catch content/format issues while blast radius is small (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — "Test template content with small group before full broadcast"; "Test with small batch before scaling").
- **Handle template lifecycle states in your integration** — react to `APPROVED`, `PENDING_REVIEW`, `REJECTED`, and `DISABLED` (a DISABLED template means a violation was detected and the template can no longer send) (source: kb/whatsapp/whatsapp-api-reference.md — Template statuses; note Meta approval typically 2–4 hours per kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md).

## Message Category & Cost Discipline

- **Match message type to the correct WhatsApp category** — Template, Service (outside 24h window), Authentication/OTP, and Marketing each have distinct rules and costs; marketing requires opt-in and is highest cost, authentication is lowest (source: kb/whatsapp/whatsapp-pricing.md — message categories).
- **Prefer templates over service messages for cost, batch non-urgent updates, and use self-serve AI to cut escalations** — documented cost-optimization levers (source: kb/whatsapp/whatsapp-pricing.md — cost-optimization strategies: use templates, batch non-urgent updates, optimize with BizAI agent to reduce escalations).
- **Respect the 24-hour customer-initiated window** — template and marketing messages can only be sent within 24 hours of customer initiation; sends after the window fall into the higher-cost service-message category (source: kb/whatsapp/whatsapp-pricing.md — "Can only be sent within 24 hours of customer initiation").

## API Integration & Delivery Reliability

- **Normalize phone numbers to `+[country_code][number]` before sending** — the single most common critical error (131000) is a malformed number (missing `+`, leading zeros, missing country code); validate against known country codes and implement double opt-in to confirm the number (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — Error 131000 prevention).
- **Don't send to landlines, business numbers, or numbers without WhatsApp** — these always fail with 131000; ask the recipient to message you first to confirm an active account (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — FAQ: "WhatsApp only works with personal mobile numbers"; Error 131004 for undeliverable/no-WhatsApp).
- **Implement exponential backoff, never aggressive 1-second retries** — aggressive retries themselves get the account throttled (131003); back off 1s → 2s → 4s → 8s and wait 60s after a throttle before retrying (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — Error 131003 fix/prevention).
- **Rate-limit to your quality tier and stay under ~100 messages/minute per recipient without a high-speed tier** — bursting past your tier causes send failures and throttling; request the high-speed tier from Gupshup sales for legitimately high volume (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — Error 131001/131003; kb/whatsapp/whatsapp-api-reference.md — per-tier msg/sec limits).
- **Validate media before sending** — enforce image <16MB (JPG/PNG) and video <100MB (MP4/3GP), and ensure media URLs are publicly accessible; failing this causes Error 131005 (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — Error 131005; kb/whatsapp/whatsapp-api-reference.md — supported media types).
- **Consume delivery-status and error webhooks to close the loop** — subscribe to `accepted`/`sent`/`delivered`/`read`/`failed` status events and parse `errors[].code` on failures so you fix root causes instead of symptoms (source: kb/whatsapp/whatsapp-api-reference.md — message status update and delivery error webhooks; kb/p2-content-gaps/whatsapp-error-codes-guide.md — "Fix the root cause: Not just the symptom").
- **Set error-rate alerts as an operational tripwire** — 131000 >1% signals a data-quality problem, 131001 >5% an API/network problem, 131002 >0.5% a spam-content problem, any 131003 means you need rate limiting; run a monthly error audit grouped by code (source: kb/p2-content-gaps/whatsapp-error-codes-guide.md — "Advanced: Monitoring & Prevention").

## Onboarding to Production (WABA Setup)

- **Complete WABA prerequisites before starting** — Meta Business Account with admin access, a Gupshup project, and a verifiable business phone number; plan for a 24–48 hour approval timeline (source: kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md — Prerequisites).
- **Verify phone ownership and business ownership early** — the two documented go-live blockers are "phone number stuck pending" (resolve by SMS-verifying in Meta, then waiting 24h) and "WABA connection failed" (resolve by re-checking the phone code and verifying business ownership in Meta) (source: kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md — Troubleshooting table).
- **Know your phone-number limit** — a WABA includes 5 phone numbers; request more from support before you hit the cap rather than during a launch (source: kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md — "Can't add phone number → Check WABA limits (5 included), request more from support").
- **Set up incoming-message webhooks and templates as part of go-live, not after** — the documented next steps after connecting a WABA are configuring webhooks for incoming messages and message templates before sending begins (source: kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md — Next Steps).

## Operational Messaging Patterns (Case-Grounded)

- **Use automated transactional reminders to drive acknowledgment and reduce cycle time** — automated payment/premium reminders on WhatsApp measurably improve completion (case: financial-services-4.md — automated reminder messages achieved a 98% acknowledgment rate and shortened the collection cycle; financial-services-3.md — WhatsApp used for policy updates and premium-payment reminders with transaction alerts and receipts).
- **Send completion-nudge notifications for multi-step flows** — track completion status and re-nudge users who dropped off (case: food-restaurant-2.md — chatbot tracks rider onboarding completion status and sends "regular nudges for riders who didn't complete onboarding via WhatsApp notifications").
- **Offer self-serve journeys with live-agent handoff to deflect support load** — combining bot self-service with escalation to a human agent measurably reduces call volume (case: pureit.md — interactive WhatsApp bot for inquiry/demo/order/complaint plus live-agent chat cut support calls 50%; healthcare-2.md — Click-to-WhatsApp Ads with live-agent support for appointment booking; ride-hailing-2.md — WhatsApp message connects the user to a live agent for onboarding queries).
- **Go multilingual to widen accessibility once live** — adding regional-language support after the initial launch improves reach (case: financial-services-13.md — bank launched WhatsApp banking in Nov '23, then "added multilingual (Hindi) capabilities in 2024 using Azure Cloud translation services"; ride-hailing-2.md — ads sent on WhatsApp "in regional languages").
- **Keep integration data fresh so the bot never messages on stale state** — sync backing catalogs/inventory on a schedule to avoid sending offers for unavailable items (case: cars24.md — "To avoid recommending cars that are already sold, the catalog is synced every few hours").

## What the Evidence Does NOT Support

- **No case-study evidence for WhatsApp Business API *onboarding-to-production* practices specifically.** In the case-study corpus, "onboarding" almost always means *customer/rider/student* onboarding journeys (food-restaurant-2.md, ride-hailing-2.md, financial-services-3.md), not WABA provisioning. All go-live/setup practices above are grounded in the setup doc (kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md), not in case studies — do not cite case studies for WABA setup.
- **No evidence for specific message-quality-rating *recovery* playbooks.** The pricing and API-reference docs describe what quality rating affects (throughput, cost) but neither the docs nor any case study describes a concrete Green-recovery procedure beyond reducing complaints/rejections. Do not invent step-by-step "rehabilitate a Red account" content.
- **No case-study evidence for conversation-based *pricing optimization* as a lived outcome.** Cost-optimization levers are grounded only in kb/whatsapp/whatsapp-pricing.md (use templates, batch updates, self-serve deflection); no case study quantifies a WhatsApp cost reduction from category optimization. Do not attribute pricing wins to specific customers.
- **No evidence for opt-in *mechanics* detail (double opt-in UX, consent-capture UI).** Case studies confirm opt-ins are collected (general-5.md, cpg-1.md, retail-d2c-4.md) but describe none of the mechanics; the only mechanical guidance ("double opt-in: confirm number before adding to send list") comes from kb/p2-content-gaps/whatsapp-error-codes-guide.md. Do not fabricate consent-flow UX best practices.

## Related Docs

- [Campaign Manager Best Practices (campaign strategy — excluded here)](../campaign-manager/campaign-best-practices.md)
- [WhatsApp Error Codes: Troubleshooting & Prevention](../p2-content-gaps/whatsapp-error-codes-guide.md)
- [WhatsApp Pricing](./whatsapp-pricing.md)
- [WhatsApp API Reference](./whatsapp-api-reference.md)
- [WhatsApp Promotional Restrictions](./whatsapp-promotional-restrictions.md)
- [WABA Setup in Gupshup](./setup-whatsapp-business-account-waba-in-gupshup.md)
