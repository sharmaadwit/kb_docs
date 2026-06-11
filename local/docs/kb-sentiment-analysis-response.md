# KB Update Spec: Sentiment Analysis in Bot Analytics

**For:** Skill code change agent  
**Purpose:** Add sentiment analysis documentation to Bot Studio Analytics section  
**Priority:** High (improves user support for a feature that's not well documented)

---

## 🎯 Context

**Trace ID:** `kb-kb_answer-8cf9a2dfde30458d`

**User Query:** "Where in Gupshup Console can I check sentiment analysis of bots? It was previously in Bot analytics but I can't see it now."

**Current KB Response:** "I don't know based on the current docs."

**Issue:** Users are asking about sentiment analysis but the KB has no documentation on where to find it or how to access it.

---

## 📝 Polished Response

Use this polished version as the answer:

```
Sentiment analysis is available through the Custom Bot Analytics extension in Gupshup Console.

To access sentiment analysis:

1. Contact your Delivery team to activate the Custom Bot Analytics extension for your console project
2. Once the extension is activated, all sentiment analysis data will be automatically visible in Bot Studio Analytics

If the extension is not yet activated for your project, reach out to your Delivery team to enable it.
```

---

## 📍 Where to Add This

### Primary Location
**File:** `kb/bot-studio-analytics/dashboard.md`

**Section to Update:** Add a new subsection under the existing content

**Placement:** After the "Live Metrics" section (around line 78), add:

```markdown
### Sentiment Analysis

Sentiment analysis is available through the Custom Bot Analytics extension in Gupshup Console.

#### How to access sentiment analysis

To access sentiment analysis data:

1. Contact your Delivery team to activate the Custom Bot Analytics extension for your console project
2. Once the extension is activated, all sentiment analysis data will be automatically visible in Bot Studio Analytics

If the Custom Bot Analytics extension is not yet activated for your project, reach out to your Delivery team to enable it.

#### Prerequisites

- **Custom Bot Analytics extension** must be activated for your console project (request from Delivery team)
- Access to **Gupshup Console → Bot Studio Analytics → Dashboard**

```

### Secondary Location (Recommended)
**File:** Create a new file `kb/bot-studio-analytics/sentiment-analysis.md`

This would be better long-term as sentiment analysis might have its own configuration/features. Template:

```markdown
source_url: https://console-docs.gupshup.io/docs/sentiment-analysis

# Sentiment Analysis

**Module**: Bot Studio Analytics

## Definition

Sentiment analysis monitors and evaluates the emotional tone of customer interactions with your bot. This feature is available through the Custom Bot Analytics extension.

## Procedure

### Exact UI path
Gupshup Console → Bot Studio Analytics → Dashboard → Sentiment Analysis (when Custom Bot Analytics extension is activated)

### Prerequisites
- **Custom Bot Analytics extension** must be activated for your console project
- Access to Gupshup Console → Bot Studio Analytics

### How to access

1. Contact your Delivery team to activate the Custom Bot Analytics extension for your console project
2. Once the extension is activated, all sentiment analysis data will be automatically visible in Bot Studio Analytics
3. Navigate to Bot Studio Analytics → Dashboard to view sentiment trends

### Troubleshooting

If you don't see sentiment analysis data:
- Confirm that the Custom Bot Analytics extension has been activated for your console project
- Contact your Delivery team if the extension is not yet enabled
- Data may take some time to populate after activation

## Related docs
- Dashboard
- Custom Bot Analytics Extension
```

---

## 🔍 Related Questions to Update

These similar questions should also get the sentiment analysis response:

1. **"How do I see sentiment analysis in my bot analytics?"**
   → Same answer applies
   
2. **"Where is sentiment analysis in Bot Studio Analytics?"**
   → Same answer applies
   
3. **"Can I access sentiment data in my dashboard?"**
   → Same answer applies
   
4. **"I'm looking for sentiment metrics for my bot."**
   → Same answer applies
   
5. **"How do I enable sentiment analysis?"**
   → Same answer applies (mention the extension + Delivery team)

**Implementation note:** The KB scoring algorithm will naturally surface the answer to these queries once the content is in place. No additional changes needed beyond updating the above files.

---

## ✅ Implementation Checklist

- [ ] **Option A (Recommended):** Create new file `kb/bot-studio-analytics/sentiment-analysis.md` with the template provided above
- [ ] **Option B:** Add sentiment analysis subsection to existing `kb/bot-studio-analytics/dashboard.md`
- [ ] Verify the response addresses the original query
- [ ] Test with a sample query: "Where in Gupshup Console can I check sentiment analysis of bots?"
- [ ] Confirm the answer appears in the KB results
- [ ] Consider adding cross-references in other analytics files (ai-analytics.md, filters-in-bot-analytics.md) pointing to this new content

---

## 📊 Success Criteria

✅ **Implementation is successful when:**

1. User query "Where in Gupshup Console can I check sentiment analysis of bots?" returns the polished response
2. The response clearly explains:
   - Sentiment analysis is available via Custom Bot Analytics extension
   - How to request activation from Delivery team
   - What happens after activation
3. Confidence score for similar questions improves significantly (should be > 8.0)
4. Related queries automatically surface the same answer

---

## 📝 Notes

- **No skill code changes needed** — This is purely KB content authoring
- **No infrastructure changes** — Users can access the feature immediately once extension is activated
- **No breaking changes** — This is additive documentation only
- **Test thoroughly** — Verify queries about sentiment analysis now receive proper answers instead of "I don't know"

---

**Status:** READY FOR IMPLEMENTATION  
**Created:** 2026-06-11  
**Assigned to:** Skill code change agent  
