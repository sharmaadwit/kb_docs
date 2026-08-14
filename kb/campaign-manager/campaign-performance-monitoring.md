# Campaign Performance Monitoring

## Diagnosis
**How do I know if my campaign is working?**

Most teams run campaigns and check results manually, days or weeks later. By then, the damage is done: a failing campaign has burned budget, damaged brand trust, and wasted team resources. Meanwhile, winning campaigns are already stale, and they don't learn why they won.

Real-time monitoring answers three questions:
1. **Is it working?** (Campaign converging to expected KPIs or underperforming?)
2. **Should I adjust?** (Stop it, pause it, optimize it, or let it run?)
3. **Why?** (Which segments, creatives, offers drove success or failure?)

Without monitoring, campaigns are black boxes. With it, they become learning machines.

## Context

### Core Campaign KPIs

**Awareness Campaigns**
- Primary: Impression count, reach, frequency
- Secondary: Brand lift (survey), consideration lift
- Alert threshold: 20% below target impressions at Day 1

**Engagement Campaigns**
- Primary: Open rate (email), click-through rate, engagement rate (SMS/push)
- Secondary: Unsubscribe rate, complaint rate, repeat engagement
- Alert threshold: >2% unsubscribe rate, <20% of target engagement rate

**Conversion Campaigns**
- Primary: Conversion rate (purchase, signup, form completion)
- Secondary: Cost per conversion, revenue per email sent
- Alert threshold: Conversion rate <50% of expected baseline

**Retention Campaigns**
- Primary: Win-back rate (% of dormant users who re-engage), churn reduction
- Secondary: Revenue per re-engaged user, 90-day retention of re-engaged cohort
- Alert threshold: Win-back rate <10% expected rate

### Monitoring Cadence

**Real-Time Dashboard**
- Update: Every 15-30 minutes
- Audience: Campaign managers, marketing ops, VP marketing
- Purpose: Catch catastrophic failures early (>80% unsubscribe rate, >50% bounce rate)
- Action: Pause campaign immediately if critical threshold breached

**Daily Email Report**
- Update: 9am daily
- Audience: Campaign manager, performance analyst
- KPIs: Campaign performance vs. expected (% variance), top performers, anomalies
- Purpose: Spot trends early (underperformance, surprising winners)
- Action: Adjust send times, creative, targeting, or pause underperformers

**Weekly Business Review**
- Update: Every Monday
- Audience: Marketing leadership, stakeholders
- KPIs: Week-over-week trends, segment performance, ROI, recommendations
- Purpose: Strategic learning (what's working, what to double down on)
- Action: Double-budget winners, kill persistent underperformers, adjust strategy

## Recommended Approach

**Start with: Real-Time Dashboard + Daily Anomaly Alerts**

This combination catches problems fast without requiring complex automation:

### Real-Time Dashboard (Technical Setup)
**Source**: Email platform API (HubSpot, Klaviyo, Braze) or data warehouse (Snowflake, BigQuery)
**Refresh**: Every 15-30 minutes
**Key Metrics**:
- Emails sent (cumulative)
- Bounce rate (hard/soft)
- Open rate (trending, by hour)
- Click rate (trending, by hour)
- Unsubscribe rate (real-time alert if >1%)
- Conversion rate (if e-commerce tracked)
- Cost per open, cost per conversion (if budget tracked)

**Setup Tool**:
- Looker, Tableau, or data studio (1-2 days to build)
- Or use platform's native dashboard (HubSpot, Klaviyo, Braze all have dashboards)
- Or hire agency to build (cheapest time-to-value)

### Daily Anomaly Alerts (Automation)
**Process**:
1. Calculate expected performance for each campaign type (based on historical baseline)
2. Each morning, compare yesterday's results to expected
3. If variance >20% below expected, send alert to campaign manager
4. Alert includes: Campaign name, metric, expected vs. actual, potential causes, recommended action

**Example Alert**:
```
🚨 ANOMALY ALERT: Welcome Email Campaign
Expected open rate: 35%
Actual open rate: 18% (48% below expected)
Potential causes: Bounce rate spike (8% vs. 2% baseline)
Recommended action: Check email list quality, verify DKIM/SPF, contact deliverability vendor
```

### Weekly Business Review (Manual Analysis)
**Timing**: Every Monday 10am
**Duration**: 30 minutes
**Attendees**: Campaign manager, marketing analyst, VP marketing

**Agenda**:
1. **Week-over-week trends** (5 min): Which campaigns outperformed? Which underperformed?
2. **Segment performance** (5 min): Which segments engaged most? Any segments to deprioritize?
3. **Learnings** (10 min): Why did top campaigns win? Can we repeat?
4. **Adjustments** (5 min): Which campaigns to double down on? Which to pause?
5. **Forecast** (5 min): Expected revenue/engagement for next 2 weeks based on current trends

## Follow-Up Questions

1. **KPI Priority**: What's your #1 success metric? (Revenue, engagement, acquisition, retention?)
2. **Monitoring Frequency**: Can your team check dashboard daily, or does it need to be automated?
3. **Alert Sensitivity**: How much variance triggers action? (5% below expected, 10%, 20%?)
4. **Tools Available**: What platform do you send campaigns from? (HubSpot, Klaviyo, Braze, custom?)

## See Also
- [Campaign Strategy Diagnosis](campaign-strategy-diagnosis.md) — Define campaign type and expected KPIs
- [Campaign Segmentation Paths](campaign-segmentation-paths.md) — Monitor performance by segment
- [Campaign A/B Testing Framework](campaign-ab-testing-framework.md) — Use monitoring data to power testing insights
