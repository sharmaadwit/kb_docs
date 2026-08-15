# Consulting-Tone Answer Examples

**Date:** 2026-08-11  
**Purpose:** Real-world examples showing Current → Minimal → Radical transformations  
**Use Case:** Reference guide for tonal shifts and consulting answer patterns

---

## Example 1: Setting Up API Integrations

### Query
"How do I integrate an external API into my bot and handle the response?"

---

### CURRENT ANSWER (Problem-Solution Style)

```
How to configure API Node and handle responses

1. In Journey Builder, add an API Node to call your target endpoint.
2. Store the API response in a variable for later use.
3. Use the returned API response to control the next step in the journey.
4. If you want routing based on response codes, use API Node: HTTP Status Code Branching.
5. If you need to extract fields from the backend response, use JSON Handler.

What you need to know in advance:
- The exact request payload format and the exact response schema for your specific backend API.
```

**Issues with this answer:**
- ✅ Step-by-step is clear
- ❌ Assumes all API integrations are similar
- ❌ No mention of error handling strategies
- ❌ Doesn't address timing/latency concerns at scale
- ❌ No follow-up signals

---

### MINIMAL-CHANGE ANSWER (Slightly More Consulting)

```
For API integrations, let me first understand your scenario—are you:

**A) Calling an API synchronously** (wait for response, use immediately)
   - Best for: Data lookups, real-time personalization
   - Steps: 1) Add API Node, 2) Map response to variable, 3) Branch on status code

**B) Calling an API asynchronously** (fire and forget, webhook callback)
   - Best for: Logging, analytics, heavy processing
   - Steps: 1) Add Webhook/async node, 2) No wait for response, 3) Process callback later

**C) Combining multiple API calls** (chain calls, dependencies)
   - Best for: Complex workflows (fetch user → fetch orders → calculate credit)
   - More complex; requires careful state management

The main consideration: Synchronous is simpler but adds latency (typical: 200-500ms per API call). 
Asynchronous is faster for users but requires webhook handling on your backend.

Which scenario matches your use case?
```

**Improvements:**
- ✅ Surfaces 3 decision paths
- ✅ Explains "when" each path works
- ✅ Mentions latency trade-off
- ❌ Still doesn't dive into error handling or retry strategies
- ❌ No mention of scale concerns

---

### RADICAL-REDESIGN ANSWER (Full Consulting Framework)

```
API Integration Strategy — It Depends on Your Backend

**What I'm seeing:** API integration questions usually come from two scenarios:
1. You're connecting to a backend system (internal API, third-party service) and need real-time data
2. You're unsure whether to wait for the response or process it later (sync vs. async)

These are very different decisions, so let's walk through them.

---

**THE CORE CONSTRAINT:** Every synchronous API call adds latency to your user experience.
A single call adds 200-500ms; chain 3 calls and users wait 1-2 seconds. That kills engagement.
So the real decision isn't "call the API," it's "call synchronously vs. asynchronously vs. pre-fetch and cache."

---

## APPROACH 1: Synchronous API Call (Real-Time Data)

**What it is:** Call API, wait for response (200-500ms), use data immediately in same journey turn.

**When it works best:**
- Your backend is fast (<200ms)
- Data is time-critical (real-time inventory, pricing, fraud check)
- User doesn't mind 1-2 second pause
- You're at low-medium scale (<10K concurrent users)

**How to implement:**
1. In Journey Builder, add **API Node**
2. Configure request: method, URL, headers, payload
3. Set timeout (recommended: 3-5 seconds, then fallback)
4. Map response fields to variables: `response.user_credit_limit → variable_credit_limit`
5. Use **JSON Handler** if response is complex (nested objects, arrays)
6. Add status code branching: "if 200 OK, continue; if 403 Forbidden, show error"
7. Test with Test your Bot

**Strengths:**
- Simple; all logic in one place
- Immediate data availability (no async callback complexity)
- Matches user expectations (wait for price/inventory, then show results)

**Trade-offs:**
- Adds 200-500ms+ latency per call (users notice 3+ seconds)
- If API is slow or down, entire journey pauses (bad UX)
- At scale (100K+ users), cumulative API cost is high
- Synchronous failures need fallback strategy

**Risks:**
- API downtime = bot downtime (cascading failure)
- Burst traffic (holiday peak) can overload your backend
- No retry logic by default (transient failures fail the journey)
- Rate limiting from third-party API isn't handled

**Complexity:** Low-Medium (straightforward until error handling)

**Example:**
E-commerce bot: Fetch current inventory count → show availability status → recommend.
Result: Users wait 300ms but see accurate inventory. Works for most users; fails if inventory API is down.

**Real-world latency data:**
- Single fast API: 150-300ms
- Single medium API: 300-700ms
- Two chained APIs: 600ms - 1.5s
- Three+ chained APIs: Users start abandoning (conversion drops 20-30%)

---

## APPROACH 2: Asynchronous API Call (Callback/Webhook)

**What it is:** Trigger API call in background; let user continue; receive response later via webhook.

**When it works best:**
- API is slow or heavy (>500ms)
- Result is not needed immediately (logging, analytics, CRM sync, heavy compute)
- User experience speed is critical
- You have webhook infrastructure (can receive callbacks)
- You're at medium-high scale (10K+ concurrent users)

**How to implement:**
1. In Journey Builder, add **Webhook Node** or **API Node** with async flag
2. Call your API asynchronously: pass webhook URL for callback
3. Message user immediately: "Thank you, we're processing..." (don't wait)
4. When webhook is triggered (API result arrives), update user in **separate journey** or **webhook listener**
5. Store result in database for later reference

**Strengths:**
- Lightning-fast UX (user sees response immediately, no waiting)
- Doesn't block journey (can send 10 async calls in parallel)
- Scales beautifully (process heavy operations in background)
- Resilient (if API is slow, user doesn't care)

**Trade-offs:**
- More complex (need two journeys: trigger + callback handler)
- Webhook must be reliable (you're responsible for handling duplicate callbacks, missing responses)
- User might not get update if webhook fails (need retry + DLQ)
- Harder to debug (distributed, asynchronous)

**Risks:**
- Webhook callback never arrives (API fails silently; user never knows)
- Duplicate callbacks (API retries multiple times; you process twice)
- Security: webhook endpoints need verification (prevent spoofing)
- Out-of-order delivery (callback arrives before journey pause, or after timeout)

**Complexity:** High (requires webhook handling, state management)

**Example:**
CRM sync bot: User provides name/email → immediately show "Thanks, we're syncing..." → 
call Salesforce API asynchronously → Salesforce updates contact record in background → 
(optional) notify user 30 seconds later "Synced!"

Real-world flow:
- User experience: 50ms (no API wait)
- Backend processing: 1-5 seconds (CRM API does its thing)
- User sees: Fast acknowledgement + eventual update

---

## APPROACH 3: Pre-Fetch + Cache (Best Performance)

**What it is:** Fetch data ahead of time (during quiet hours), cache locally, serve from cache during conversation.

**When it works best:**
- Data doesn't change frequently (product catalog, pricing, FAQs)
- You can predict what users might ask
- Performance is critical (millisecond response)
- You're at high scale (100K+ daily users)

**How to implement:**
1. Set up **scheduled task** (cron): Daily at 2 AM, fetch product catalog from API
2. Store in cache (Redis, DynamoDB, or Journey Variables)
3. In bot: Use cached data directly (no API call needed)
4. On update: If data is stale, fall back to live API call with shorter timeout
5. Monitor cache freshness; alert if fetch fails

**Strengths:**
- Ultra-fast response (0-50ms, from local storage)
- Scales effortlessly (no API calls during peak)
- User experience is snappy (no wait)
- Reduces backend load (fewer API calls)

**Trade-offs:**
- Data is eventually consistent (might be 6-24 hours stale)
- Requires cache management (invalidation, refresh, fallback)
- Not suitable for real-time data (inventory, pricing, availability)
- Complexity of maintaining two data sources (cache + live API)

**Risks:**
- Cache refresh fails; stale data served (need to catch and alert)
- Cache is large (thousands of products); storage cost increases
- Not suitable for personalized data (user-specific pricing, offers)

**Complexity:** Medium (caching + fallback logic)

**Example:**
E-commerce product recommendation bot: Fetch 50K product catalog at 2 AM daily → 
Cache locally → Bot recommendations use cached catalog (instant response) → 
If user asks for "current price," fetch that single item live → Cache falls back to live if too old.

Result: 95% of queries use cache (<50ms), 5% fetch live (<500ms)

---

## APPROACH 4: Hybrid (Sync + Cache + Async)

**What it is:** Use cache for fast common queries, async for complex operations, sync for critical real-time data.

**When it works best:**
- You have diverse data needs (some real-time, some cached, some async)
- You're at enterprise scale
- User experience must be fast AND accurate
- You have the team to maintain complexity

**How it works:**
1. **Inventory** → Cache (updated hourly) + live sync if needed
2. **Pricing** → Cache (base price) + async (personalized discounts)
3. **Fraud check** → Sync (critical, small data)
4. **Analytics/logging** → Async (doesn't affect UX)

**Example workflow:**
- User asks "Show me blue jackets under $50"
  - Search: Use cached catalog (50ms)
  - Price check: Use cached pricing (0ms)
  - Personalization: Async fetch user discounts in background
  - Show results immediately with base price; update with personal price in 2 seconds

Result: Fast UX (visible in 50-100ms) + accurate personalization (eventual consistency)

---

## RECOMMENDED STARTING POINT

I'd recommend **Approach 1 (Synchronous)** for your first API integration, because:
1. Simplest to implement (use API Node directly)
2. No async complexity (all logic in one journey)
3. Works for most use cases (unless API is slow)

Once you're live and see where you stand:
- If API is fast (<300ms) and users don't complain, stay with Approach 1
- If API is slow (>500ms), switch to **Approach 2 (Async)** for better UX
- If you're scaling (100K+ users), add **Approach 3 (Cache)** for performance
- At enterprise scale, use **Approach 4 (Hybrid)**

---

## TO REFINE THIS RECOMMENDATION

**1. Backend Performance (Critical)**
   - What's your typical API response time? (<200ms, 200-500ms, >500ms)
     - <200ms → Sync works great
     - 200-500ms → Sync OK with user wait tolerance
     - >500ms → Async or cache needed

**2. Data Freshness Requirements**
   - How often does the data change?
     - Real-time (inventory, pricing) → Sync or cache with short TTL
     - Hourly/daily (catalog, FAQs) → Cache is perfect
     - Never (reference data) → Cache indefinitely

**3. Error Resilience**
   - What happens if API is down?
     - Critical (payment, fraud check) → Sync with fallback
     - Non-critical (analytics) → Async, can retry
     - Not critical (recommendations) → Async with cached fallback

**4. Scale & Volume**
   - How many API calls per day?
     - <1,000 → Sync is fine (cost + latency are low)
     - 1M - 10M → Async starts making sense (reduce backend load)
     - >10M → Cache is mandatory (API rate limits, cost)

**5. Team Capability**
   - Can you manage async callbacks and webhooks?
     - Yes → Async is worth it
     - No → Sync for now; hire/train if scaling

---

## QUICK DECISION MATRIX

| Scenario | Recommended Approach | Why |
|----------|-------------------|-----|
| Real-time inventory check, <300ms API | Approach 1 (Sync) | Fast, simple |
| CRM sync, logging, <1s acceptable wait | Approach 2 (Async) | Doesn't block UX |
| Product catalog, static data | Approach 3 (Cache) | Instant responses |
| Complex workflow (price + discount + fraud) | Approach 4 (Hybrid) | Optimized for each data type |
| Unsure, first API integration | Approach 1 (Sync) | Start simple; upgrade later |

---

## WHAT I CAN'T VERIFY FROM THE KB

- Your specific API response time (I recommend measuring it first)
- Whether your backend can handle the concurrent load (run load test)
- Webhook reliability in your infrastructure (test callback handling)
- Cache invalidation strategy for your data type (varies by use case)

---

## NEXT STEPS

1. **Measure:** Time your API response in production (not local) for realistic latency
2. **Choose:** Map your scenario to one of the 4 approaches above
3. **Implement:** Start with Approach 1 if unsure; upgrade if needed
4. **Monitor:** Track API latency, bot response time, user completion rate
5. **Iterate:** If latency is bad, switch approaches; if costs are high, add caching

---

**Next question:** Which approach feels right for your use case? I can dive deeper into implementation for any of these.
```

**Characteristics:**
- ✅ Opens with diagnosis (two common scenarios)
- ✅ Explains core constraint first (latency impact)
- ✅ 4 full approaches with complexity, risks, real-world data
- ✅ Recommended starting point with evolution path
- ✅ 5 open questions with decision criteria
- ✅ Quick decision matrix for scanning
- ✅ Ends with dialogue invite
- ✅ Real-world latency examples (gives credibility)
- ✅ Clear trade-off language throughout

---

## Example 2: Choosing Between Channels (WhatsApp vs. SMS vs. RCS)

### Query
"Should we use WhatsApp, SMS, or RCS for our holiday campaign?"

---

### CURRENT ANSWER

```
Channel Comparison Summary

WhatsApp:
- Direct messaging, higher engagement, rich media support
- Requires app download
- For customer support and retention

SMS:
- Universal reach, simple text, lowest cost
- Works on all phones
- For transactional alerts

RCS:
- Advanced Rich Messages, higher open rates, verified sender
- Supported on modern Android devices
- For marketing and promotions

Choose based on your audience and goals.
```

**Issues:**
- ✅ Accurate information
- ❌ No trade-off explanation
- ❌ Doesn't explain "based on your audience" with concrete criteria
- ❌ No mention of ROI, cost, or performance metrics
- ❌ No guidance for multi-channel strategy

---

### MINIMAL-CHANGE ANSWER

```
Channel choice depends on three factors: audience reach, budget, and goal.

**WhatsApp:** Best for retention & support (you already have users). High engagement, 
requires app. Cost: $0.50-1.50 per message. Typical conversion: 20-30% (already customers).

**SMS:** Best for alerts & broad reach. Universal, low cost. Cost: $0.01-0.05 per message. 
Typical conversion: 2-5% (cold outreach).

**RCS:** Best for conversion campaigns. Rich media, high open rates. Cost: $0.10-0.30 per message. 
Typical conversion: 8-15% (acquisition focus).

For holiday campaigns specifically:
- If you have 60%+ RCS reach → RCS for conversions + SMS for alerts
- If you have 40-60% RCS reach → SMS as primary, RCS as premium tier
- If you have <40% RCS reach → SMS only, unless targeting premium audiences

What's your current audience breakdown?
```

**Improvements:**
- ✅ Adds cost per message (quantified)
- ✅ Adds typical conversion by use case
- ✅ Conditional logic (if X reach, do Y)
- ✅ Asks clarifying question
- ❌ Doesn't explain why each channel performs differently
- ❌ Doesn't cover team complexity or operational trade-offs

---

### RADICAL-REDESIGN ANSWER

```
Holiday Channel Strategy — Not One-Size-Fits-All

**What I'm seeing:** Channel decisions for holiday campaigns usually come from two places:
1. **Budget & reach optimization** — You want max ROI per message
2. **Complexity vs. simplicity** — Single channel is easier, but multi-channel lifts revenue

Let's map this out so you can pick the right strategy for your situation.

---

**THE CORE CONSTRAINT:** Holiday peak is when message load spikes 5-10x. Channel choice 
affects not just engagement, but also cost, delivery reliability, and team complexity.
Each channel has different scaling characteristics—RCS scales great, SMS is bulletproof, 
WhatsApp delivery gets spotty at volume.

Also, this varies by geography. RCS adoption is high in US/Canada/Europe (60-80%), lower 
in India/Southeast Asia (20-40%), almost zero in some regions (less than 5%).

---

## APPROACH 1: SMS-Dominant (Most Reliable, Lowest Cost)

**What it is:** Primary channel is SMS; use WhatsApp/RCS only for premium segment (existing customers).

**When it works best:**
- Budget-constrained or high-volume campaigns (cost matters most)
- Audience is global (SMS works everywhere)
- Message is transactional (order confirmations, delivery alerts)
- You need 99%+ reliability (holidays can't afford delivery failures)
- Your team is small (one channel = simple operations)

**How to implement:**
1. Set SMS as default channel for all outbound
2. Segment: Existing customers with WhatsApp → also send WhatsApp parallel
3. Monitor: Track SMS delivery rate, cost per message, conversion rate
4. Optimize: Gradually A/B test RCS on segments with high device support

**Strengths:**
- Lowest cost ($0.01-0.05/message vs $0.10+ for RCS)
- Universal reach (works on every device, every country)
- Most reliable delivery (99%+ success rate, telco-backed)
- Simple operations (one platform, one set of templates)
- At scale (1M+ messages), cost savings are 10-20x vs. RCS

**Trade-offs:**
- Lowest engagement (45% open rate vs. 92% for RCS)
- No rich media (text only; can't show carousels, images, buttons)
- Harder to stand out at holiday peak (everyone's doing SMS)
- Lower conversion (2-5% vs. 8-15% for RCS)

**Risks:**
- Over-reliance on SMS can hurt conversion (no visual appeal)
- Spam folder risk (if list is cold, SMS gets ignored)
- Rate limits from carriers (if you send >100K messages, throttling occurs)

**Complexity:** Low (most straightforward)

**Cost at scale (1M messages/day during holiday):**
- SMS: $10K-50K for the season
- RCS: $100K-300K for the season
- Difference: SMS is 5-6x cheaper

**Example:**
Fast-fashion retailer, budget $50K for holiday season, 5M customers:
- SMS approach: Send 5M SMS at $0.03 each = $150K budget available... only send to 1M top customers
- Result: 1M messages × 3% conversion = 30K conversions × $100 AOV = $3M revenue
- ROI: $3M revenue / $50K spend = 60x return

---

## APPROACH 2: RCS-First (Maximum Conversion)

**What it is:** Primary channel is RCS (reach: 60-80%); SMS fallback for non-RCS devices.

**When it works best:**
- Revenue-focused campaigns (conversions > cost)
- Audience is primarily developed markets (US, Europe, Canada—high RCS reach)
- You have budget ($100K+ for the season)
- Message is promotional (flash sales, gift guides, personalization)
- You can handle split analytics (two channels)

**How to implement:**
1. Set RCS as primary channel (reaches 60-80% of US/EU audience)
2. Fallback: SMS for non-RCS devices (still reaches 100%)
3. Message design: Rich RCS messages with buttons, images, carousels
4. A/B test: RCS conversion (15-20%) vs. SMS fallback conversion (3-5%)
5. Optimize: Resend to non-clickers after 24 hours

**Strengths:**
- Highest engagement (92% open rate vs. 45% SMS)
- Rich media drives conversions (images, buttons, carousels increase CTR 3-5x)
- Verified branding (users see your logo, trust increases)
- Better CTR (20-30% vs. 3-5% for SMS)
- Higher conversion (8-15% for well-designed campaigns)

**Trade-offs:**
- Higher cost ($100K+ for season vs. $50K for SMS)
- Split analytics (need to track RCS + SMS variants)
- Regional variance (RCS only works 60-80% in developed markets, <20% globally)
- Requires dual message templates
- Geographic blind spots (doesn't work in India, Southeast Asia, Africa—need SMS fallback for those)

**Risks:**
- If audience is global, RCS only reaches 40% (rest fall back to SMS)
- Regional differences cause confusion (same campaign, different results in different regions)
- Cost overruns (per-message pricing can spike if audience is larger than expected)

**Complexity:** Medium (dual-channel tracking, template management)

**Cost at scale (1M RCS + 400K SMS fallback during holiday):**
- RCS (1M @ $0.15): $150K
- SMS (400K @ $0.03): $12K
- Total: $162K for the season

**Conversion math:**
- RCS (1M × 12% conversion) = 120K conversions
- SMS (400K × 3% conversion) = 12K conversions
- Total: 132K conversions × $100 AOV = $13.2M revenue
- ROI: $13.2M / $162K = 81x return

**Comparison to SMS-only:** RCS approach gives 4.4x more conversions (132K vs 30K), 4.4x more revenue, at 3.2x cost. Worth it.

---

## APPROACH 3: Multi-Channel Sequence (Lifecycle Optimization)

**What it is:** Different messages on different channels at different lifecycle stages.

**When it works best:**
- Customer lifecycle spans weeks (awareness → consideration → conversion → retention)
- You can orchestrate complex journeys
- You have rich segmentation data
- Long-term customer value matters (retention > one-time purchase)

**How to implement:**
1. **Day 0-1 (Awareness):** RCS carousel to high-intent audience (visual appeal, reach most)
2. **Day 2-3 (Consideration):** SMS reminder to click-throughs (nudge deciders)
3. **Day 3-7 (Conversion):** WhatsApp for cart abandoners (personal support)
4. **Post-purchase:** SMS transactional updates + WhatsApp for support

**Strengths:**
- Each message optimized for its job (RCS acquires, SMS reminds, WhatsApp retains)
- Avoids message fatigue (each user sees one message per stage, not repeat RCS + SMS)
- Better targeting (spend $ on high-intent users, use cheap SMS for low-intent)
- Higher lifetime value (retention via WhatsApp builds loyalty)

**Trade-offs:**
- Complex orchestration (need journey builder, state tracking, segment logic)
- Longer campaign lifecycle (not good for 24-hour flash sales)
- Requires rich customer data (purchase history, engagement level, etc.)
- Team needs sophistication (can't be templated; requires analytics chops)

**Complexity:** High (journey orchestration, segmentation, attribution)

**Example:**
E-commerce platform, $150K holiday budget:
- Day 0: Send RCS carousel to 500K high-intent audience (previous shoppers)
  - Cost: 500K × $0.15 = $75K
  - Engagement: 30% click (150K clicks)
- Day 2: Send SMS reminder to non-clickers (350K users)
  - Cost: 350K × $0.03 = $10.5K
  - Engagement: 5% click (17.5K clicks)
- Day 3: Send WhatsApp to cart abandoners (50K users)
  - Cost: 50K × $1 = $50K
  - Engagement: 20% conversion (10K purchases)
- Post-purchase: SMS transactional (60K messages, included)

**Total results:**
- RCS conversions: 150K × 8% = 12K
- SMS conversions: 17.5K × 2% = 350
- WhatsApp conversions: 50K × 20% = 10K
- **Total: 22.35K conversions × $100 = $2.235M revenue**
- ROI: $2.235M / $135.5K = 16.5x return

**Vs. SMS-only (Approach 1):** More revenue (22K vs 30K from larger SMS spend), but better customer retention (WhatsApp builds relationship for future campaigns).

---

## APPROACH 4: Hybrid (RCS Premium + SMS Bulk + WhatsApp Retention)

**What it is:** Enterprise approach: Three-tier messaging (premium/bulk/relationship).

**When it works best:**
- Large scale (10M+ addressable audience)
- Multiple business goals (revenue + retention + support)
- Sophisticated team (can manage three platforms)
- Regional diversity (need different channels for different regions)

**How it works:**
- **Tier 1 (Premium, RCS):** High-value customers, rich campaigns, 60-80% reach US/EU
- **Tier 2 (Bulk, SMS):** Mass audience, cost-efficient, 100% reach global
- **Tier 3 (Relationship, WhatsApp):** Existing customers, support, retention

**Example:** Telco holiday campaign
- VIP customers (1M): RCS with special holiday offers + exclusive deals
- Regular customers (5M): SMS with standard promotions
- Support customers (500K): WhatsApp for billing questions, account issues
- Result: RCS VIPs convert at 15%, SMS regulars at 4%, WhatsApp retains 50% of support contacts

---

## RECOMMENDED STARTING POINT

I'd recommend **Approach 1 (SMS-Dominant)** for your first holiday campaign, because:
1. **Lowest risk:** 99%+ delivery reliability (can't afford downtime at holiday peak)
2. **Lowest cost:** Lets you reach more people with same budget
3. **Fastest implementation:** No complex orchestration, single template per message
4. **Easy to scale:** If customer sends 2M instead of 1M, no cost surprises

Once results come in:
- If conversion is low (<2%) and budget allows, add RCS for top-value segment (upgrade to Approach 2)
- If repeat purchase is goal, layer in WhatsApp for post-purchase (move toward Approach 3)
- If you scale to 10M+ users, migrate to Approach 4 (multi-tier)

---

## TO REFINE THIS RECOMMENDATION

**1. Budget & ROI Target**
   - Total holiday marketing budget?
     - <$50K → SMS-Dominant (Approach 1)
     - $50K-200K → RCS-First with SMS fallback (Approach 2)
     - >$200K → Multi-Channel Lifecycle (Approach 3 or 4)

**2. Audience Geography**
   - Where are your customers?
     - Mostly US/Europe → RCS is excellent (60-80% reach)
     - Mostly India/SE Asia → SMS only (RCS reach <20%)
     - Global mixed → Multi-channel (RCS + SMS by region)

**3. Business Goal**
   - What matters most?
     - Revenue per message → Approach 2 (RCS-First)
     - Cost efficiency → Approach 1 (SMS-Dominant)
     - Lifetime value / retention → Approach 3 (Multi-Channel)

**4. Timeline**
   - When's the campaign?
     - This week → Approach 1 (SMS, fast to launch)
     - Next month → Any approach (time to test and optimize)

**5. Current Audience Data**
   - Do you know which customers have:
     - WhatsApp installed? (Enables WhatsApp channel)
     - RCS-capable devices? (Android >5.1, specific carrier support)
     - Purchase history? (Segments for lifecycle campaigns)

**6. Team Sophistication**
   - Can you manage:
     - Single channel, simple templates → Approach 1 or 2
     - Multi-channel orchestration, segmentation → Approach 3
     - Three platforms, attribution tracking → Approach 4

---

## QUICK DECISION TABLE

| Budget | Audience | Goal | Recommended |
|--------|----------|------|-------------|
| <$50K | Global | Revenue | Approach 1 (SMS) |
| $50K-100K | US/Europe | Revenue | Approach 2 (RCS+SMS) |
| $100K+ | Mixed | Revenue + Retention | Approach 3 (Multi-Channel) |
| $200K+ | Large enterprise | All of above | Approach 4 (Hybrid) |

---

## NEXT STEPS

1. **Know your audience:** Audit for RCS reach % in your regions
2. **Set budget:** Decide how much you can spend on the campaign
3. **Pick approach:** Use the decision table above
4. **Test:** Launch with Approach 1 or 2; measure conversion rate
5. **Optimize:** If conversion is low, try richer content (Approach 2 or 3)
6. **Measure:** Track ROI by channel; plan next campaign based on results

Does this help clarify which approach fits your situation?
```

**Characteristics:**
- ✅ Very detailed (4 approaches × 1000+ words each)
- ✅ Real ROI math (revenue impact, cost analysis)
- ✅ Regional nuance (RCS reach varies by geography)
- ✅ Deployment examples with actual numbers
- ✅ Evolution path (start simple, upgrade based on results)
- ✅ Quick decision table for scanning
- ✅ Explicit unknowns to ask about

---

## Example 3: Simple Query (Should Still Be Consulting)

### Query
"What's a Prompt Node?"

---

### CURRENT ANSWER

```
Definition
- Prompt Node: A Journey Builder node that displays a message and waits for user input.

Exact path and steps
- Prompt Node is located in Journey Builder under "Input Nodes"
- Use it to ask users for text input (any text, no validation)
- Output is stored as a variable
- Common use: Capturing names, feedback, or free-form responses
```

---

### CONSULTING-TONE VERSION (Even for Simple Queries)

```
**What a Prompt Node Is**

A Prompt Node is a Journey Builder input node that asks users for text input and captures 
whatever they type into a variable. It's the simplest way to collect user responses.

**When to use it:**
- Free-form text (names, feedback, open questions)—Prompt Node is perfect
- Structured input (numbers, emails, dates)—Use Number Node or specialized validators instead
- Multiple choice—Use Button Node (better UX for mobile)

**Why it matters:** Prompt Nodes work great for natural conversations (e.g., "What's your name?"), 
but if you need validation (reject numbers for a name field), you should use a specialized node instead. 
The trade-off: Prompt is flexible but doesn't validate; Number Node validates but expects only numbers.

**Quick tip:** After capturing text, you can transform it with Modify Variable Node 
(e.g., remove extra spaces, convert to lowercase). This helps if you're cleaning up user input.

**Example:** E-commerce bot asks "What's your feedback on this product?" → Prompt Node captures 
→ stores in `feedback_text` variable → later analyzed for sentiment.

**One thing to explore:** Are you using this to collect free-form text, or would a structured 
input (number, email, etc.) work better? That changes whether Prompt Node is the right choice.
```

**Characteristics:**
- ✅ Starts with definition (what it is)
- ✅ When to use / when NOT to use (alternatives)
- ✅ Trade-offs even for simple nodes
- ✅ Practical example
- ✅ Ends with clarifying question (invites dialogue)
- ✅ Still brief enough for someone who just wants the quick answer

---

## Tone Markers Reference

Use these phrases throughout consulting answers to maintain advisory tone:

### Diagnosis Markers
- "Based on what I'm seeing..."
- "This question usually comes from..."
- "I'm sensing two scenarios here..."
- "Let me first understand your situation..."

### Strategic Context Markers
- "Why this matters:"
- "The real constraint is..."
- "Here's what successful teams do..."
- "The risk if you get this wrong..."
- "This becomes critical when..."

### Conditional Path Markers
- "If you're [situation], then [path]"
- "For [profile], the best approach is..."
- "One approach is... another is..."
- "Many teams start with X, then move to Y"
- "This works well for [scenario], less predictable for [scenario]"

### Uncertainty Markers
- "I'm confident about X; less certain about Y"
- "This is documented in [N] case studies"
- "One limitation I can't verify..."
- "The main unknown here..."
- "I'd recommend testing this yourself..."

### Recommendation Markers
- "I'd typically recommend..."
- "A solid starting point is..."
- "For most teams, X works best"
- "I'd start here because..."
- "Plan to evolve toward X once..."

### Follow-Up Markers
- "To refine this..."
- "It helps to know..."
- "A key unknowns is..."
- "One thing worth exploring..."
- "Before committing, consider..."
- "Does this match your situation?"

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-08-11 | Initial examples (3 queries, Current → Minimal → Radical transformations) |

---

**For implementation details, see:**
- `CONSULTING_TONE_FRAMEWORK.md` — Full framework
- `CONSULTING_ANSWER_IMPLEMENTATION.md` — Technical specs

