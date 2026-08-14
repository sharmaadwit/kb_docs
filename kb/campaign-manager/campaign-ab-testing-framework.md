# Campaign A/B Testing Framework

## Diagnosis
**How do I A/B test campaigns?**

A/B testing is the difference between guessing what works and knowing. Most teams skip testing because it feels slow or complex. But untested campaigns leave 20-50% of potential revenue on the table. A single untested subject line decision could be costing you thousands per month.

A/B testing doesn't have to be complicated. The most effective test is often the simplest: split your audience into two groups, show them different versions, measure which performs better. Statistical rigor comes later—start with valid isolation of variables.

## Context

### Common Testing Variables

**Subject Line Testing**
- Which subject line drives higher open rate?
- Typical lift: 5-20% improvement possible
- Duration: 2-7 days (until sufficient sample size)
- Best for: Email campaigns
- Example: "Introducing X" vs. "You've been invited to X" vs. "Limited time: X"

**Send Time Testing**
- When should we send to maximize open rate?
- Typical lift: 10-30% improvement possible
- Duration: 2-4 weeks (need variation by day, by hour-of-day, by timezone)
- Best for: Email campaigns
- Example: Tuesday 9am vs. Wednesday 2pm vs. Thursday 6pm

**Content Testing**
- Which content/offer drives higher click-through or conversion?
- Typical lift: 15-50% improvement possible
- Duration: 2-7 days for email, 1-4 weeks for landing pages
- Best for: Both email and web
- Example: Product A pitch vs. Product B pitch vs. Competitor comparison

**Audience Split Testing**
- Should we send to segment A or segment B? Who responds better?
- Typical lift: Defines segment strategy going forward
- Duration: 2-4 weeks (ensure statistical significance)
- Best for: Segmentation validation
- Example: Test "high-value" segment definition vs. alternative definition

**Channel Testing**
- Which channel drives better response: email vs. SMS vs. push?
- Typical lift: Varies wildly (20-200% channel effects possible)
- Duration: 2-4 weeks
- Best for: Multi-channel orchestration decisions
- Example: Email-only vs. Email + SMS retargeting

### Statistical Rigor (Simplified)

**Sample Size**
- Minimum: 1,000 users per variation (2,000 total for A/B test)
- Recommended: 5,000-10,000 per variation for reliable results
- Rule of thumb: More users = shorter test duration, clearer winner

**Significance Threshold**
- Statistical significance = 95% confidence the result isn't random chance
- In practice: Look for 2-5% difference in conversion/engagement as meaningful
- If you see >10% difference, test is likely conclusive in 2-7 days

**Duration Considerations**
- Too short: Might not capture day-of-week or timezone effects
- Too long: Opportunity cost, delayed winning version rollout
- Sweet spot: 3-7 days for email, 2-4 weeks for retention campaigns

## Recommended Approach

**Start with: Audience Split Testing**

This is the cleanest isolation of variables:

### Setup
1. **Define One Variable**: Pick ONE thing to test (subject line, send time, content, audience split, etc.)
2. **Split Audience 50/50**: Randomly divide audience into Control (current) and Test (new) groups
3. **Send Simultaneously**: Send both variations at the same time to eliminate time-of-day effects
4. **Run Duration**: Let test run for 3-7 days (or until >5,000 per group have opened/clicked)

### Analysis
- **Metric**: Choose primary metric (open rate for subject line test, conversion rate for offer test)
- **Winner**: Does Test outperform Control by 5%+ and hit 95% statistical significance?
- **Guardrails**: Check secondary metrics (unsubscribe rate, complaint rate) to ensure no negative effects
- **Rollout**: If Test wins, send winning version to remaining unsegmented audience

### Why This Works
- **Simple**: No complex statistics required, just count opens/clicks
- **Reliable**: Eliminates confounding variables (day-of-week, timezone, etc.)
- **Actionable**: Clear winner emerges in 3-7 days
- **Scalable**: Can run multiple tests in parallel on different audiences

### Example: Subject Line Test
```
Audience: 10,000 users who clicked purchase page but didn't convert
Split: 5,000 Control, 5,000 Test

Control (Current): "Complete your order"
Test (New): "You're 1 click away from $50 savings"

Metric: Click-through rate (link to complete purchase)
Run Time: 3 days

Result:
Control: 12% click rate = 600 clicks
Test: 15% click rate = 750 clicks
Lift: +25% = +150 additional conversions at $100 AOV = +$15K revenue

Decision: Rollout new subject line to remaining 100,000 dormant audience
Expected value: 15,000 additional conversions = +$1.5M revenue (annualized if repeated)
```

## Follow-Up Questions

1. **Test Frequency**: How often can you test? (Weekly? Monthly? Continuous?)
2. **Variance Tolerance**: How much conversion variance can you tolerate? (±5%, ±10%, ±20%?)
3. **Minimum Lift**: What's the minimum lift needed to justify changing creative/strategy? (e.g., 5% improvement, 10% improvement)
4. **Sample Size**: How many users can you spare for a test group? (Impacts test duration and reliability)

## See Also
- [Campaign Strategy Diagnosis](campaign-strategy-diagnosis.md) — Choose campaign type before testing
- [Campaign Segmentation Paths](campaign-segmentation-paths.md) — Validate segmentation strategy with audience split tests
- [Campaign Performance Monitoring](campaign-performance-monitoring.md) — Monitor test results in real-time dashboard
