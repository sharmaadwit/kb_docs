# Three RCS Setup Paths — Choose Your Implementation Approach

## Diagnosis: Which Setup Path Is Right for You?

Consider:
- Expected daily volume (<10K, 10K-100K, or >100K)
- Engineering time available
- Launch timeline
- Existing SMS/WhatsApp scale

**Rule of thumb:**
- **<10K/day → Path 1 (Manual)**
- **10K-100K/day → Path 2 (API-Driven)**
- **>100K/day → Path 2 with advanced optimization**

## Context: Three Paths Compared

| Factor | Path 1 (Manual) | Path 2 (API) | Path 3 (Hybrid) |
|--------|-----------------|--------------|-----------------|
| Setup Effort | 10-50 hours | 60-150 hours | 70-180 hours |
| Timeline | 4-7 weeks | 5-9 weeks | 5-9 weeks |
| Max Volume | <10K/day | 10K-100K+/day | Scales with API |
| Team Size | 1 person | 2-3 people | 2-3 people |
| Maintenance | 30min/week | 2-3 hours/week | 3-5 hours/week |
| Cost (Monthly) | $200-500 | $500-2000+ | $500-2000+ |

## Options: Three Implementation Approaches

### Path 1: Manual/UI-Based Setup
**Setup Process:**
1. Access Gupshup Console
2. Fill metadata (name, logo, description)
3. Upload compliance docs
4. Submit approval
5. Monitor approval status (4-6 weeks wait)
6. Receive credentials
7. Configure webhook
8. Create templates via Console
9. Test with sample users
10. Launch to production

**Best for:** <10K/day, minimal engineering, validation phase

### Path 2: API-Driven Setup
**Setup Process:**
1-7. Same as Path 1 (approval gate)
8. API client initialization (Node.js, Python, Go)
9. Message sending via SDK
10. Webhook handler for delivery callbacks
11. Retry logic (exponential backoff)
12. Monitoring & alerting
13. Load testing
14. Launch to production

**Best for:** 10K-100K+/day, production-scale, scaling needs

### Path 3: Hybrid Setup
**Setup Process:** Start Path 1, migrate to Path 2 at scale

**Best for:** Teams that want to validate RCS first, then scale

## Recommended Approach

**Start Path 1. Migrate to Path 2 when you hit 10K/day threshold.**

Most teams benefit from starting simple (manual), validating RCS ROI, then upgrading to API when volume justifies engineering effort.

## Follow-Up Questions

- What's your expected volume?
- When do you need to launch?
- Do you already send SMS at scale?
- Can you commit 4-7 weeks for carrier approval?
