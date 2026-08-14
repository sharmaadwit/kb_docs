# Campaign Segmentation Paths

## Diagnosis
**How do I segment my audience?**

Segmentation is the difference between personalization (relevant message to right person) and spam (irrelevant blast to everyone). Most teams skip segmentation because it requires thinking: "Who are our distinct customer types? What does each type need?"

Without segmentation, your campaigns are like broadcasting the same dinner invitation to everyone—vegetarians get the steak dinner, carnivores get salad, and everyone deletes it.

Good segmentation creates distinct audience paths. Each segment sees different creative, offer, or timing because they have different needs. The result: 3-5x higher engagement, lower unsubscribe rates, and better brand perception.

## Context

### Segmentation Dimensions

**Demographics**
- Age, geography, company size, industry
- Static, easy to collect, moderate predictive power
- Best for: Awareness, regional campaigns
- Example: "Send product A to Tech/Finance, product B to Healthcare/Retail"

**Behavioral**
- Purchase history, feature adoption, engagement frequency, browsing patterns
- Dynamic, requires event tracking, highest predictive power
- Best for: Engagement, conversion, retention
- Example: "Send feature tutorial to users who opened welcome email but haven't used the feature"

**Value / RFM (Recency, Frequency, Monetary)**
- How recently purchased, how often, how much spent
- Dynamic, calculated from transaction history, very predictive
- Best for: Retention, high-value campaigns
- Example: "Send VIP offer only to top 20% by spending, with enhanced service tier"

**Intent / Lifecycle**
- Where customer is in their journey (awareness, evaluation, purchasing, onboarding, established, churn-risk)
- Hybrid, requires behavioral + business logic
- Best for: Targeted retention, feature adoption
- Example: "Send conversion offer to free trial users in week 2 of trial, send adoption tips to paying customers in month 1"

**Engagement**
- Email open rate, link click rate, form submission, inactive duration
- Dynamic, easy to calculate, directly predictive of campaign success
- Best for: All campaigns
- Example: "Send to high-engagement segment (opens 50%+ emails), use different creative for low-engagement segment"

## Recommended Approach

**Start with: Rule-Based + Behavioral Segmentation**

This combination is simple to execute and highly effective:

### Step 1: Define 3-5 Core Segments
```
- High-Value Active: Purchased in last 30 days, spent >$500 lifetime
- Engaged Growth: Opened >50% of emails, uses features 2+ days/week
- Trial/Onboarding: Signed up <30 days ago, incomplete setup
- At-Risk: Last purchase 90+ days ago, opened <20% of recent emails
- Dormant: No login >180 days
```

### Step 2: Assign Business Rules
- **High-Value Active**: VIP offers, early access, 1:1 support messaging
- **Engaged Growth**: Feature announcements, advanced use cases, community content
- **Trial/Onboarding**: Welcome series, feature tutorials, objection handling
- **At-Risk**: Win-back offer, personalized re-engagement, feedback request
- **Dormant**: Simple reactivation offer, clear value prop

### Step 3: Automate with Tool
- Use CDP (Segment, mParticle), email platform (HubSpot, Klaviyo), or data warehouse
- Calculate segment membership weekly or daily
- Assign each user to exactly one primary segment (prevent overlap confusion)
- Test for accuracy: sample 50 users per segment, verify they match the rules

### Why This Works
- **Simple**: Only requires customer data you already have (purchase history, email engagement)
- **Scalable**: Rules can be updated without touching code
- **Predictive**: Behavioral signals are 10x more predictive than demographics alone
- **Measurable**: Each segment's performance isolated for A/B testing

### When to Evolve to ML-Based Segmentation
Once rule-based segmentation is mature (3+ months of data):
- Churn prediction models (predict which customers will leave in 30 days)
- Next-best-action models (recommend which offer each segment should get)
- Lookalike modeling (find new prospects similar to high-value customers)
- Investment: Data science effort, but 2-3x ROI improvement possible

## Follow-Up Questions

1. **Core Metrics**: What behavior signals are most predictive in your business? (Purchase frequency? Feature adoption? Engagement? Retention days?)
2. **Data Availability**: Can you reliably track these behaviors today? (Or do we need to improve event tracking first?)
3. **Segment Size**: Are you OK with 5 segments, or do you want more granular (10+)? (More segments = higher complexity)
4. **Frequency**: How often should segment membership be recalculated? (Weekly recommended, daily if highly dynamic business)

## See Also
- [Campaign Strategy Diagnosis](campaign-strategy-diagnosis.md) — High-level campaign type choice
- [Campaign A/B Testing Framework](campaign-ab-testing-framework.md) — How to test different segment strategies
- [Campaign Performance Monitoring](campaign-performance-monitoring.md) — How to measure segment-level performance
