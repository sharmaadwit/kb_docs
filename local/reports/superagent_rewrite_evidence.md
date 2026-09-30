# SuperAgent LLM Rewrite Evidence — Live Capture

> **Captured:** 2026-09-30  
> **Method:** Live queries fired via SuperAgent stream endpoint.  
> **For:** SuperAgent Engineering Team

Each sample shows:
1. **Original question** — what was typed (short, natural)
2. **Query kb_answer received** — what SuperAgent's LLM reformulated and sent to the skill
3. **Answer kb_answer generated** — the raw skill output before SuperAgent rewrites it
4. **Answer shown in UI** — what SuperAgent's LLM wrote to the user

---

## Sample 1

| Field | Value |
|-------|-------|
| Trace ID | `1ae1ddbb820648f98cd84011ccd4d71e` |
| Confidence | `1` |
| Top Source | `kb/agent-assist/user-management-business-hours.md` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Latency | `1563 ms` |
| Logic Version | `kb-answer-v4.15` |

### 1. Original Question (what the user typed)

> how do I set up business hours in agent assist

### 2. Query kb_answer Received (SuperAgent reformulation)

> *SuperAgent's LLM expanded this from the short original question above.*

```
How do I set up business hours in Agent Assist?
```

### 3. Answer kb_answer Generated (before SuperAgent rewrite)

> *Raw skill output. Compare with section 4 to see what SuperAgent changed.*

```markdown
To set this up, here's what you need to know.

- User Management: Business Hours
- Steps
- 1. Go to `Settings`.
- 2. Click `Business Hours`.
- 3. Click `Add New`.

Most common case: User Management: Business Hours

This also connects well with **Response Management: Auto Replies & Customer Satisfaction and Chat Management: Assignment Rules** — worth exploring if that's part of your setup.



---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Agent Assist Demo (Contact Center · VP of Support Team)
https://demoforge-ui.gupshup.io/shared/3274e01c-6fa6-4789-bfa0-4abf6773fbf6/autoplay

**Other Gupshup customers in Entertainment also use Bot Studio** — an entertainment company achieved *2X — Engagement and retention*. Worth exploring if you're looking to expand beyond your current setup.
```

### 4. Answer Shown in UI (after SuperAgent LLM rewrite)

> *This is what the user actually saw.*

```markdown
In Agent Assist, go to **Settings → Business Hours → Add New**. The available documentation doesn’t specify the fields to fill in after selecting **Add New**.

**See it in action:** [Agent Assist Demo](https://demoforge-ui.gupshup.io/shared/3274e01c-6fa6-4789-bfa0-4abf6773fbf6/autoplay)

**Other Gupshup customers in Entertainment also use Bot Studio** — an entertainment company achieved *2X — Engagement and retention*. Worth exploring if you're looking to expand beyond your current setup.
```

### Full kb_answer Trace Payload

```json
{
  "user_email": "exec:34@ccexpress.gupshup.io",
  "query": "How do I set up business hours in Agent Assist?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- User Management: Business Hours\n- Steps\n- 1. Go to `Settings`.\n- 2. Click `Business Hours`.\n- 3. Click `Add New`.\n\nMost common case: User Management: Business Hours\n\nThis also connects well with **Response Management: Auto Replies & Customer Satisfaction and Chat Management: Assignment Rules** \u2014 worth exploring if that's part of your setup.\n\n\n\n---\n*\u2026",
  "logic_version": "kb-answer-v4.15",
  "trace_env": "PROD",
  "answered": true,
  "top_score": 13.6,
  "top_source": "kb/agent-assist/user-management-business-hours.md",
  "source_count": 1,
  "latency_ms": 1563,
  "intent": "setup",
  "module": "Agent Assist",
  "explicit_module": "Agent Assist",
  "confidence": 1,
  "video_attached": true,
  "video_title": "Agent Assist Demo",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

## Sample 2

| Field | Value |
|-------|-------|
| Trace ID | `8e491c5c24444c35acb35c28ef2b2979` |
| Confidence | `0.6499999999999999` |
| Top Source | `kb/bot-studio/json-handler-instead-of-code-node.md` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Latency | `954 ms` |
| Logic Version | `kb-answer-v4.15` |

### 1. Original Question (what the user typed)

> what is JSON handler node

### 2. Query kb_answer Received (SuperAgent reformulation)

> *SuperAgent's LLM expanded this from the short original question above.*

```
What is the JSON Handler node in Bot Studio or Journey Builder?
```

### 3. Answer kb_answer Generated (before SuperAgent rewrite)

> *Raw skill output. Compare with section 4 to see what SuperAgent changed.*

```markdown
Here's what **JSON Handler instead of Code Node** means in this context.

- JSON Handler instead of Code Node
- Module: Bot Studio
- Parsing Using New JSON Handler Node (No-Code)
- With the new JSON Handler Node introduced in JB V2 (Upgraded Journey Builder), you can achieve this without code, via an intuitive UI that lets you define JSON paths for mapping.

Most common case: JSON Handler instead of Code Node

This also connects well with **API Node and Condition Node** — worth exploring if that's part of your setup.



---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Bot Studio (General · VP of Engineering)
https://demoforge-ui.gupshup.io/shared/adca6f42-7fc6-4f03-bf26-f5123e16071c/autoplay

**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.
```

### 4. Answer Shown in UI (after SuperAgent LLM rewrite)

> *This is what the user actually saw.*

```markdown
The **JSON Handler** is a no-code node in the upgraded Journey Builder (JB V2). It lets you define JSON paths in the UI to parse JSON data and map values, avoiding the need to write code for that task.

It’s commonly used instead of a Code Node. It can work alongside the **API Node** and **Condition Node** in a flow.

[See the Bot Studio demo](https://demoforge-ui.gupshup.io/shared/adca6f42-7fc6-4f03-bf26-f5123e16071c/autoplay)

**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.
```

### Full kb_answer Trace Payload

```json
{
  "user_email": "exec:34@ccexpress.gupshup.io",
  "query": "What is the JSON Handler node in Bot Studio or Journey Builder?",
  "answer_preview": "Here's what **JSON Handler instead of Code Node** means in this context.\n\n- JSON Handler instead of Code Node\n- Module: Bot Studio\n- Parsing Using New JSON Handler Node (No-Code)\n- With the new JSON Handler Node introduced in JB V2 (Upgraded Journey Builder), you can achieve this without code, via an intuitive UI that lets you define JSON paths for mapping.\n\nMost common case: JSON Handler instead \u2026",
  "logic_version": "kb-answer-v4.15",
  "trace_env": "PROD",
  "answered": true,
  "top_score": 12.5,
  "top_source": "kb/bot-studio/json-handler-instead-of-code-node.md",
  "source_count": 3,
  "latency_ms": 954,
  "intent": "definition",
  "module": "Bot Studio",
  "explicit_module": "Bot Studio",
  "confidence": 0.6499999999999999,
  "video_attached": true,
  "video_title": "Bot Studio",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

## Sample 3

| Field | Value |
|-------|-------|
| Trace ID | `2483836326d848689eeb252eb20ca0db` |
| Confidence | `0.865` |
| Top Source | `kb/campaign-manager/rcs-campaigns.md` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Latency | `961 ms` |
| Logic Version | `kb-answer-v4.15` |

### 1. Original Question (what the user typed)

> how do I create an RCS campaign

### 2. Query kb_answer Received (SuperAgent reformulation)

> *SuperAgent's LLM expanded this from the short original question above.*

```
How do I create an RCS campaign?
```

### 3. Answer kb_answer Generated (before SuperAgent rewrite)

> *Raw skill output. Compare with section 4 to see what SuperAgent changed.*

```markdown
To set this up, here's what you need to know.

- RCS Campaigns
- Setup Path
- 3. Create RCS Campaign
- In Campaign Manager → Create Campaign:
- 1. Select Channel: RCS

**Best practices:**
- 1. Use rich media wisely - Images load faster on RCS; videos should be <10MB
- 2. Keep CTAs clear - 2-3 suggested action buttons per message
- 3. Test with small audience first - Send to 5-10% of audience, monitor metrics before full roll-out

Most common case: RCS Campaigns

This also connects well with **Go Live with Instagram and Webhooks** — worth exploring if that's part of your setup.



---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

## Related success stories
- **Leading travel & hospitality company in India — marketing · 41.1% RCS Coverage** (Travel & Hospitality) — 41.1% — RCS Coverage · 26.1% — Read Rate — Marketing · RCS
- **Leading automobile company in India — marketing** (Automotive) — 2.4 Mn — + Total events 1 Mn+ Total — Marketing
- **Leading automobile company in India — ai · 14.3% Increase in lead** (Automotive) — 14.3% — Increase in lead · 10% — Lift in CPA — AI · Engagement · Marketing

_Up to 3 relevant examples. Some stories are anonymized for confidential clients._

**See it in action:** Campaign Manager Demo (Banking · Head of Marketing)
https://demoforge-ui.gupshup.io/shared/3deb4110-e216-4ef8-9082-d78c765ebc4a/autoplay

**Other Gupshup customers in Financial Services also use AI Admin** — a financial services company achieved *4.3X — productivity increase $20M*. Worth exploring if you're looking to expand beyond your current setup.
```

### 4. Answer Shown in UI (after SuperAgent LLM rewrite)

> *This is what the user actually saw.*

```markdown
In **Campaign Manager**, go to **Create Campaign** and select **RCS** as the channel. The available documentation doesn’t detail the remaining form fields or launch steps.

Best practices:
- Use rich media thoughtfully; images load faster, and videos should be under 10 MB.
- Keep calls to action clear, with 2–3 suggested action buttons.
- Test with a small audience first, then monitor results before rolling out more broadly.

[Watch the Campaign Manager demo](https://demoforge-ui.gupshup.io/shared/3deb4110-e216-4ef8-9082-d78c765ebc4a/autoplay)

**Other Gupshup customers in Financial Services also use AI Admin** — a financial services company achieved *4.3X — productivity increase $20M*. Worth exploring if you're looking to expand beyond your current setup.
```

### Full kb_answer Trace Payload

```json
{
  "user_email": "sess:anonymous-session@ccexpress.gupshup.io",
  "query": "How do I create an RCS campaign?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- RCS Campaigns\n- Setup Path\n- 3. Create RCS Campaign\n- In Campaign Manager \u2192 Create Campaign:\n- 1. Select Channel: RCS\n\n**Best practices:**\n- 1. Use rich media wisely - Images load faster on RCS; videos should be <10MB\n- 2. Keep CTAs clear - 2-3 suggested action buttons per message\n- 3. Test with small audience first - Send to 5-10% of audience, moni\u2026",
  "logic_version": "kb-answer-v4.15",
  "trace_env": "PROD",
  "answered": true,
  "top_score": 4.4,
  "top_source": "kb/campaign-manager/rcs-campaigns.md",
  "source_count": 4,
  "latency_ms": 961,
  "intent": "setup",
  "module": "Campaign Manager",
  "explicit_module": "Campaign Manager",
  "confidence": 0.865,
  "session_id": "anonymous-session",
  "video_attached": true,
  "video_title": "Campaign Manager Demo",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

## Sample 4

| Field | Value |
|-------|-------|
| Trace ID | `2208fac3b03c443d8355ac498f7b5f00` |
| Confidence | `0.44499999999999995` |
| Top Source | `kb/bot-studio/about-bot-studio.md` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Latency | `3765 ms` |
| Logic Version | `kb-answer-v4.15` |

### 1. Original Question (what the user typed)

> what does API node do in bot studio

### 2. Query kb_answer Received (SuperAgent reformulation)

> *SuperAgent's LLM expanded this from the short original question above.*

```
What does the API Node do in Bot Studio?
```

### 3. Answer kb_answer Generated (before SuperAgent rewrite)

> *Raw skill output. Compare with section 4 to see what SuperAgent changed.*

```markdown
Here's what the documentation says about this.

This can vary depending on your setup. The docs cover a few scenarios:
- Starting with Console 16.0, Gupshup has deprecated or replaced several legacy and dev-only nodes in Bot Studio to improve platform stability, performance, and user experience.
- API Node: HTTP Status Code Branching
- API Node

**Starting with Console 16.0, Gupshup has deprecated or replaced several legacy and dev-only nodes in Bot Studio to improve platform stability, performance, and user experience.**: About Bot Studio
**API Node: HTTP Status Code Branching**: API Node: HTTP Status Code Branching
**API Node**: API Node

**Best practices:**
- Always handle failure cases (e.g., 500, 404) by using fallback nodes.
- Test your journey using the Test Bot before going live.
- Use Global or Local Variables for dynamic values in API calls.

This also connects well with **JSON Handler and Condition Node** — worth exploring if that's part of your setup.



---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

## Related success stories
- **Leading automobile company in India — ai · 14.3% Increase in lead** (Automotive) — 14.3% — Increase in lead · 10% — Lift in CPA — AI · Engagement · Marketing
- **Leading automobile company in India — ai · Support** (Automotive) — AI · Support
- **Cars24** (Automotive) — 8% — Industry-leading · 60% — Lower agent effort — AI · Gen AI

_Up to 3 relevant examples. Some stories are anonymized for confidential clients._

**Watch:** [Bot Studio: Building a Journey](https://www.youtube.com/watch?v=cO21ibbcZnA&t=3&cc_load_policy=1&cc_lang_pref=en&hl=en)

**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.
```

### 4. Answer Shown in UI (after SuperAgent LLM rewrite)

> *This is what the user actually saw.*

```markdown
The **API Node** in Bot Studio lets your bot make an API call as part of a journey, so it can exchange data with an external service. You can use variables for dynamic values in the call, then handle the response in later steps—for example, with a **JSON Handler** or **Condition Node**.

Plan for failure paths (such as 404 or 500 responses) and test the journey with **Test Bot** before going live.

**Watch:** [Bot Studio: Building a Journey](https://www.youtube.com/watch?v=cO21ibbcZnA&t=3&cc_load_policy=1&cc_lang_pref=en&hl=en)

**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.
```

### Full kb_answer Trace Payload

```json
{
  "user_email": "sess:anonymous-session@ccexpress.gupshup.io",
  "query": "What does the API Node do in Bot Studio?",
  "answer_preview": "Here's what the documentation says about this.\n\nThis can vary depending on your setup. The docs cover a few scenarios:\n- Starting with Console 16.0, Gupshup has deprecated or replaced several legacy and dev-only nodes in Bot Studio to improve platform stability, performance, and user experience.\n- API Node: HTTP Status Code Branching\n- API Node\n\n**Starting with Console 16.0, Gupshup has deprecated\u2026",
  "logic_version": "kb-answer-v4.15",
  "trace_env": "PROD",
  "answered": true,
  "top_score": 4.4,
  "top_source": "kb/bot-studio/about-bot-studio.md",
  "source_count": 4,
  "latency_ms": 3765,
  "intent": "definition",
  "module": "Bot Studio",
  "explicit_module": "Bot Studio",
  "confidence": 0.44499999999999995,
  "session_id": "anonymous-session",
  "video_attached": true,
  "video_title": "Bot Studio: Building a Journey",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

## Observations

### Query Reformulation
Compare section 1 vs section 2 for each sample. SuperAgent's LLM:
- Expands short informal questions into structured, multi-clause queries
- Adds context clues (module names, Console navigation hints)
- Sometimes infers intent that wasn't explicitly stated

### Answer Reformulation
Compare section 3 vs section 4 for each sample. SuperAgent's LLM:
- Paraphrases bullet lists into prose
- Drops or compresses step-by-step formatting
- Preserves URLs and video links (governed by SKILL.md `never drop` rule)
- Cross-sell block is now preserved (SKILL.md v4.4 fix)
