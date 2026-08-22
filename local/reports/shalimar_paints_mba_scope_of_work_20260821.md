# Shalimar Paints × Meta Business Agent — Scope of Work & Phased Plan

*Sent to client (Archna, Nikhil, Rahul) by Adwit Sharma, 2026-08-21 12:34 PM. Based on call transcript, 2026-08-20 12:30 IST.*

## 1. What we heard — two distinct tracks

**Track A — Customer-facing WhatsApp bot (Meta Business Agent, as pitched).**
An AI agent on WhatsApp talking to Shalimar's end customers (homeowners) for:
- Sales & lead generation (shade card downloads, "what paint should I use", qualifying to an in-store/consult appointment)
- Product discovery (paint types, wallpaper options — grounded in your catalog/docs)
- Customer support (post-purchase issues you define)

**Track B — Internal sales-force diagnostic tool (Venkatesh's idea, raised mid-call).**
An AI tool for your own salespeople to resolve the ~25% of dealer complaints that are actually tinting/usage errors (e.g. curdled paint from incorrect colorant-machine temperature), using photos/voice from the dealer plus your R&D knowledge base and SAP data.

## 2. For Track A

**Clearly supported out of the box:**

| Item | Status |
|---|---|
| WhatsApp text conversation, English | ✅ Standard |
| Hindi input/output (typed Hindi or Hindi-in-English-script) | ✅ Confirmed doable |
| Bengali (East market) | ✅ Same mechanism, no additional lift |
| Product/catalog grounding via Facebook catalog or your own docs | ✅ Agent knowledge sources support business info, FAQs, websites, and uploaded files |
| Connect to your own systems via API (e.g. lead capture, appointment booking) | ✅ "Connectors" with configurable tools; 2 connectors is the practical ceiling for a 4-week build |
| 7-8 message conversation cap, 2-3 user turns before drop-off | ✅ This is a design constraint we'll build to, not a platform limitation |

**Requires custom setup:**

| Item | Status |
|---|---|
| Photo/image input from customers (e.g. "photo of my wall" or "photo of curdled paint") | ⚠️ While we can accept incoming messages, Meta's AI systems are not currently tuned for images. Gupshup can bring in its own AI systems for image recognition. Deployment within 4 weeks may not be feasible. |
| Voice input/output | ⚠️ Same caveat. Requires custom AI from Gupshup. |
| SAP/ERP as a live data source | ⚠️ High risk for a 4-week timeline. Depends entirely on whether your ERP vendor exposes usable APIs — if not, on-prem/custom integration work that cannot land in 4 weeks (as discussed live on the call). Needs to be confirmed by your team before we scope Phase 1, not assumed. |

## 3. Phased plan

Before we lock Phase 1 scope, we need from your side:
- Confirm the Phase 1 use case — recommend starting with product discovery + lead generation for end customers (lowest technical risk, matches Meta's recommended starting pattern, doesn't depend on your ERP).
- Confirm data sources for that use case — what's the catalog/product info source? Facebook catalog, a spreadsheet, existing website content? (Not SAP — see above.)
- Confirm the 2 connectors you want in v1 (e.g. "capture lead → push to CRM/Salesforce" and one more).
- Confirm language scope for v1.
- For maximum ROI and extracting benefit from Meta's funding pattern, we need to pick use cases that can bring in ~100 real users/day.

**Phase 2 — Analysis window (no new code)**
- Review 2-4 weeks of live conversation data with your team
- Identify what's working, what's not, where users drop off
- Decide jointly whether to extend to the customer support use case, add more languages, add custom AI features, or address the dealer/painter track

## 4. What Shalimar's team needs to confirm readiness for

- [ ] Sign-off on Phase 1 use case (product discovery + lead gen, recommended)
- [ ] Confirmed data source for product/catalog info (not SAP)
- [ ] Confirmed 2-3 connectors/integration points for v1
- [ ] Confirmed commitment to 100 users/day testing post-launch
- [ ] Internal check: does your ERP vendor expose API access at all? (Needed before any SAP-dependent phase can be scoped, in Phase 1 or Phase 2+)
- [ ] Decide whether Track B (internal-facing use cases) is included in Phase 1 or deferred to Phase 2+

## 5. On Track B (internal sales-force tool)

This is a genuinely good idea and the 25%-of-complaints-are-usage-errors data point is a strong case for it — but it needs its own scoping conversation, because:
- Photo/voice diagnostic input isn't a standard Meta Business Agent capability, but Gupshup can augment the capability with its own special-purpose AI.
- It depends on SAP/R&D knowledge base integration, which needs its own feasibility check independent of the 4-week Track A timeline.

Recommend treating this as a Phase 2/3 discussion once we have real usage data from Track A, or as a fully separate parallel workstream if your team wants to move on it sooner — happy to have that conversation once you've had a chance to explore internally, as Venkatesh mentioned.

---

## Revision notes (vs. earlier internal draft)

The sent version made these deliberate edits from the pre-send draft:
- **Photo/voice reframed as an upsell, not a hard "not supported."** Draft said "not documented as a supported input type." Sent version: "Meta's AI systems are not currently tuned for images... Gupshup can bring in its own AI systems for image recognition" — turns the gap into a Gupshup value-add conversation rather than a dead end. Same underlying fact (not in Meta's docs), different framing.
- **100 users/day reframed as an ROI/funding lever, not just a Meta-imposed constraint** — ties it to "extracting benefit from Meta's funding pattern," giving the client a reason to want it rather than just comply with it.
- **Track B's "own separate initiative" framing loosened** — the readiness checklist now explicitly asks the client to *decide* whether Track B lands in Phase 1 or Phase 2+, rather than asserting it belongs in a later phase by default.
- Section numbering/heading style tightened for an email format (numbered top-level sections instead of markdown H2 report style).
