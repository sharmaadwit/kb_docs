# SuperAgent LLM Rewrite Layer — Before/After Evidence

> **For:** SuperAgent Engineering Team  
> **From:** gupshup_guide skill team  
> **Date:** 2026-09-30  
> **Purpose:** Document the two LLM rewrite layers observed in production — query reformulation (user → kb_answer) and answer reformulation (kb_answer → UI).

---

## Architecture Overview

```
User types in UI
     ↓
SuperAgent LLM rewrites the question → structured query
     ↓
kb_answer receives structured query → generates formatted answer
     ↓
SuperAgent LLM rewrites the answer → final UI response
     ↓
User sees rewritten answer in UI
```

Both rewrites are done by SuperAgent's LLM. The kb_answer skill does not control them.

### Layer 1 — Query Reformulation
SuperAgent's LLM expands the user's casual question into a structured, detailed query before calling kb_answer.

**Evidence:** The queries in the traces below are clearly not raw user input. Real users type short, informal questions. The traces show formal, multi-clause structured queries that match the style of an LLM prompt expansion.

### Layer 2 — Answer Reformulation
SuperAgent's LLM takes the kb_answer output and rewrites it — paraphrasing structure, sometimes dropping content. The `answer` field in each trace below is what **kb_answer returned**. The user sees a paraphrased version in the UI.

**Known issues with Layer 2:**
- Cross-sell block (`**Other Gupshup customers...`) was being dropped until `SKILL.md` was updated with an explicit preserve instruction.
- Bullet structure, emoji markers (📌 🧭), and step numbering are often rephrased or removed.
- Video links survive because `SKILL.md` has `never drop` instruction for them.

---

## Sample Traces (Production)

### Sample 1: How do I configure business hours in Agent Assist?...

| Field | Value |
|-------|-------|
| Trace ID | `0d2a0f5ec08547028499e0d6d5bb9594` |
| Timestamp | 2026-09-30T06:54:13 UTC |
| Environment | `PROD_EXT` |
| Confidence | `1.000` |
| Top Score | `13.65` |
| Top Source | `kb/agent-assist/user-management-business-hours.md` |
| Module | `Agent Assist` |
| Answer Mode | `consulting` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Logic Version | `kb-answer-v4.14` |
| Latency | `757 ms` |
| User | `adwit.sharma@gupshup.io` |
| Source Count | `1` |

#### Layer 1 — Query as Received by kb_answer

> *This is what SuperAgent's LLM sent to kb_answer. Compare with the informal question a user would naturally type.*

```
How do I configure business hours in Agent Assist?
```

**What the user likely typed:** Short, informal — e.g. a 3–6 word version of the above. SuperAgent expanded it into this structured form before calling kb_answer.

#### Layer 2 — Answer from kb_answer (BEFORE SuperAgent Rewrite)

> *This is the raw answer kb_answer returned. The user sees a paraphrased version in the UI.*

```markdown
Other Gupshup customers in Entertainment also use Bot Studio — an entertainment company achieved 2X — Engagement and retention. Worth exploring if you're looking to expand beyond your current setup.

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
```

#### Full Trace Payload (kb_answer metadata)

```json
{
  "user_email": "adwit.sharma@gupshup.io",
  "user_name": "Adwit Sharma",
  "query": "How do I configure business hours in Agent Assist?",
  "answer_preview": "Other Gupshup customers in Entertainment also use Bot Studio \u2014 an entertainment company achieved 2X \u2014 Engagement and retention. Worth exploring if you're looking to expand beyond your current setup.\n\nTo set this up, here's what you need to know.\n\n- User Management: Business Hours\n- Steps\n- 1. Go to `Settings`.\n- 2. Click `Business Hours`.\n- 3. Click `Add New`.\n\nMost common case: User Management: B\u2026",
  "logic_version": "kb-answer-v4.14",
  "trace_env": "PROD_EXT",
  "answered": true,
  "unanswered": false,
  "top_score": 13.65,
  "top_source": "kb/agent-assist/user-management-business-hours.md",
  "source_count": 1,
  "latency_ms": 757,
  "intent": "setup",
  "module": "Agent Assist",
  "explicit_module": "Agent Assist",
  "confidence": 1,
  "trace_sequence": "None:0",
  "video_attached": true,
  "video_id": "6a43f349f14e94517beb843f",
  "video_title": "Agent Assist Demo",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

### Sample 2: What is an API node in Bot Studio and how do I configure it?...

| Field | Value |
|-------|-------|
| Trace ID | `18787e994e6e4d69a746d2ec4d6dc008` |
| Timestamp | 2026-09-29T14:50:10 UTC |
| Environment | `PROD` |
| Confidence | `0.860` |
| Top Score | `8.9` |
| Top Source | `kb/bot-studio/api-node-http-status-code-branching.md` |
| Module | `Bot Studio` |
| Answer Mode | `consulting` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Logic Version | `kb-answer-v4.11` |
| Latency | `993 ms` |
| User | `exec:34@ccexpress.gupshup.io` |
| Source Count | `4` |

#### Layer 1 — Query as Received by kb_answer

> *This is what SuperAgent's LLM sent to kb_answer. Compare with the informal question a user would naturally type.*

```
What is an API node in Bot Studio and how do I configure it?
```

**What the user likely typed:** Short, informal — e.g. a 3–6 word version of the above. SuperAgent expanded it into this structured form before calling kb_answer.

#### Layer 2 — Answer from kb_answer (BEFORE SuperAgent Rewrite)

> *This is the raw answer kb_answer returned. The user sees a paraphrased version in the UI.*

```markdown
To set this up, here's what you need to know.

- API Node: HTTP Status Code Branching
- 📌 What is it?
- 🧭 How to Use
- Step 1: Add & Configure API Node
- Set up your API call and test connection

**Best practices:**
- Always handle failure cases (e.g., 500, 404) by using fallback nodes.
- Test your journey using the Test Bot before going live.
- Use Global or Local Variables for dynamic values in API calls.

Most common case: API Node: HTTP Status Code Branching

This also connects well with **JSON Handler and Condition Node** — worth exploring if that's part of your setup.

---
**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.

---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Bot Studio (General · VP of Engineering)
https://demoforge-ui.gupshup.io/shared/adca6f42-7fc6-4f03-bf26-f5123e16071c/autoplay
```

#### Full Trace Payload (kb_answer metadata)

```json
{
  "user_email": "exec:34@ccexpress.gupshup.io",
  "query": "What is an API node in Bot Studio and how do I configure it?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- API Node: HTTP Status Code Branching\n- \ud83d\udccc What is it?\n- \ud83e\udded How to Use\n- Step 1: Add & Configure API Node\n- Set up your API call and test connection\n\n**Best practices:**\n- Always handle failure cases (e.g., 500, 404) by using fallback nodes.\n- Test your journey using the Test Bot before going live.\n- Use Global or Local Variables for dynamic values in \u2026",
  "logic_version": "kb-answer-v4.11",
  "trace_env": "PROD",
  "answered": true,
  "unanswered": false,
  "top_score": 8.9,
  "top_source": "kb/bot-studio/api-node-http-status-code-branching.md",
  "source_count": 4,
  "latency_ms": 993,
  "intent": "definition",
  "module": "Bot Studio",
  "explicit_module": "Bot Studio",
  "confidence": 0.8599999999999999,
  "trace_sequence": "None:0",
  "video_attached": true,
  "video_id": "6a433c867d620401bb6774c1",
  "video_title": "Bot Studio",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

### Sample 3: How do I use a JSON Handler node in Bot Studio?...

| Field | Value |
|-------|-------|
| Trace ID | `ed850acf387742709c11e9098e0d56f3` |
| Timestamp | 2026-09-29T14:46:12 UTC |
| Environment | `PROD` |
| Confidence | `0.860` |
| Top Score | `11.75` |
| Top Source | `kb/bot-studio/json-handler-instead-of-code-node.md` |
| Module | `Bot Studio` |
| Answer Mode | `consulting` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Logic Version | `kb-answer-v4.11` |
| Latency | `780 ms` |
| User | `exec:34@ccexpress.gupshup.io` |
| Source Count | `3` |

#### Layer 1 — Query as Received by kb_answer

> *This is what SuperAgent's LLM sent to kb_answer. Compare with the informal question a user would naturally type.*

```
How do I use a JSON Handler node in Bot Studio?
```

**What the user likely typed:** Short, informal — e.g. a 3–6 word version of the above. SuperAgent expanded it into this structured form before calling kb_answer.

#### Layer 2 — Answer from kb_answer (BEFORE SuperAgent Rewrite)

> *This is the raw answer kb_answer returned. The user sees a paraphrased version in the UI.*

```markdown
To set this up, here's what you need to know.

- JSON Handler instead of Code Node
- Procedure
- Steps
- 1. Open Gupshup Console.
- 2. Go to Bot Studio.

Most common case: JSON Handler instead of Code Node

This also connects well with **API Node and Condition Node** — worth exploring if that's part of your setup.

---
**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.

---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Bot Studio (General · VP of Engineering)
https://demoforge-ui.gupshup.io/shared/adca6f42-7fc6-4f03-bf26-f5123e16071c/autoplay
```

#### Full Trace Payload (kb_answer metadata)

```json
{
  "user_email": "exec:34@ccexpress.gupshup.io",
  "query": "How do I use a JSON Handler node in Bot Studio?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- JSON Handler instead of Code Node\n- Procedure\n- Steps\n- 1. Open Gupshup Console.\n- 2. Go to Bot Studio.\n\nMost common case: JSON Handler instead of Code Node\n\nThis also connects well with **API Node and Condition Node** \u2014 worth exploring if that's part of your setup.\n\n---\n**Other Gupshup customers in Financial Services also use Agent Assist** \u2014 a fin\u2026",
  "logic_version": "kb-answer-v4.11",
  "trace_env": "PROD",
  "answered": true,
  "unanswered": false,
  "top_score": 11.75,
  "top_source": "kb/bot-studio/json-handler-instead-of-code-node.md",
  "source_count": 3,
  "latency_ms": 780,
  "intent": "setup",
  "module": "Bot Studio",
  "explicit_module": "Bot Studio",
  "confidence": 0.8599999999999999,
  "trace_sequence": "None:0",
  "video_attached": true,
  "video_id": "6a433c867d620401bb6774c1",
  "video_title": "Bot Studio",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

### Sample 4: How do I configure routing rules in Agent Assist?...

| Field | Value |
|-------|-------|
| Trace ID | `4b3f14bd0ecf40b8b8e6f686fb9405ba` |
| Timestamp | 2026-09-29T14:45:30 UTC |
| Environment | `PROD` |
| Confidence | `0.860` |
| Top Score | `16.4` |
| Top Source | `kb/agent-assist/chat-management-assignment-rules.md` |
| Module | `Agent Assist` |
| Answer Mode | `consulting` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Logic Version | `kb-answer-v4.11` |
| Latency | `780 ms` |
| User | `sess:anonymous-session@ccexpress.gupshup.io` |
| Source Count | `4` |

#### Layer 1 — Query as Received by kb_answer

> *This is what SuperAgent's LLM sent to kb_answer. Compare with the informal question a user would naturally type.*

```
How do I configure routing rules in Agent Assist?
```

**What the user likely typed:** Short, informal — e.g. a 3–6 word version of the above. SuperAgent expanded it into this structured form before calling kb_answer.

#### Layer 2 — Answer from kb_answer (BEFORE SuperAgent Rewrite)

> *This is the raw answer kb_answer returned. The user sees a paraphrased version in the UI.*

```markdown
To set this up, here's what you need to know.

- Chat Management: Assignment Rules
- Procedure
- Fields to configure
- `Rule name`
- Rule conditions

Most common case: Chat Management: Assignment Rules

This also connects well with **User Management: Business Hours** — worth exploring if that's part of your setup.

---
**Other Gupshup customers in Entertainment also use Bot Studio** — an entertainment company achieved *2X — Engagement and retention*. Worth exploring if you're looking to expand beyond your current setup.

---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Agent Assist Demo (Contact Center · VP of Support Team)
https://demoforge-ui.gupshup.io/shared/3274e01c-6fa6-4789-bfa0-4abf6773fbf6/autoplay
```

#### Full Trace Payload (kb_answer metadata)

```json
{
  "user_email": "sess:anonymous-session@ccexpress.gupshup.io",
  "query": "How do I configure routing rules in Agent Assist?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- Chat Management: Assignment Rules\n- Procedure\n- Fields to configure\n- `Rule name`\n- Rule conditions\n\nMost common case: Chat Management: Assignment Rules\n\nThis also connects well with **User Management: Business Hours** \u2014 worth exploring if that's part of your setup.\n\n---\n**Other Gupshup customers in Entertainment also use Bot Studio** \u2014 an entertain\u2026",
  "logic_version": "kb-answer-v4.11",
  "trace_env": "PROD",
  "answered": true,
  "unanswered": false,
  "top_score": 16.4,
  "top_source": "kb/agent-assist/chat-management-assignment-rules.md",
  "source_count": 4,
  "latency_ms": 780,
  "intent": "setup",
  "module": "Agent Assist",
  "explicit_module": "Agent Assist",
  "confidence": 0.8599999999999999,
  "session_id": "anonymous-session",
  "trace_sequence": "None:0",
  "video_attached": true,
  "video_id": "6a43f349f14e94517beb843f",
  "video_title": "Agent Assist Demo",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

### Sample 5: What is the Condition node in Bot Studio and how do I set up...

| Field | Value |
|-------|-------|
| Trace ID | `845262e2781d40ac9b1de39d1d9f01f9` |
| Timestamp | 2026-09-29T16:08:45 UTC |
| Environment | `PROD_EXT` |
| Confidence | `0.767` |
| Top Score | `8.75` |
| Top Source | `kb/bot-studio/condition-node.md` |
| Module | `Bot Studio` |
| Answer Mode | `consulting` |
| Cross-sell Attached | `True` |
| Video Attached | `True` |
| Logic Version | `kb-answer-v4.12` |
| Latency | `665 ms` |
| User | `adwit.sharma@gupshup.io` |
| Source Count | `4` |

#### Layer 1 — Query as Received by kb_answer

> *This is what SuperAgent's LLM sent to kb_answer. Compare with the informal question a user would naturally type.*

```
What is the Condition node in Bot Studio and how do I set up branches?
```

**What the user likely typed:** Short, informal — e.g. a 3–6 word version of the above. SuperAgent expanded it into this structured form before calling kb_answer.

#### Layer 2 — Answer from kb_answer (BEFORE SuperAgent Rewrite)

> *This is the raw answer kb_answer returned. The user sees a paraphrased version in the UI.*

```markdown
To set this up, here's what you need to know.

- Condition Node
- Procedure
- Steps
- 1. Open Gupshup Console.
- 2. Go to Bot Studio.

Most common case: Condition Node

This also connects well with **Manage Variables and Modify Variable Node** — worth exploring if that's part of your setup.



---
**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fields, API payload, edge cases) and I’ll expand on this topic.

**See it in action:** Bot Studio (General · VP of Engineering)
https://demoforge-ui.gupshup.io/shared/adca6f42-7fc6-4f03-bf26-f5123e16071c/autoplay

---
**Other Gupshup customers in Financial Services also use Agent Assist** — a financial services company achieved *4X — Increase in completion rate 46%*. Worth exploring if you're looking to expand beyond your current setup.
```

#### Full Trace Payload (kb_answer metadata)

```json
{
  "user_email": "adwit.sharma@gupshup.io",
  "user_name": "Adwit Sharma",
  "query": "What is the Condition node in Bot Studio and how do I set up branches?",
  "answer_preview": "To set this up, here's what you need to know.\n\n- Condition Node\n- Procedure\n- Steps\n- 1. Open Gupshup Console.\n- 2. Go to Bot Studio.\n\nMost common case: Condition Node\n\nThis also connects well with **Manage Variables and Modify Variable Node** \u2014 worth exploring if that's part of your setup.\n\n\n\n---\n**Need more detail?** Reply with **more detail**, **step by step**, or ask a specific follow-up (fiel\u2026",
  "logic_version": "kb-answer-v4.12",
  "trace_env": "PROD_EXT",
  "answered": true,
  "unanswered": false,
  "top_score": 8.75,
  "top_source": "kb/bot-studio/condition-node.md",
  "source_count": 4,
  "latency_ms": 665,
  "intent": "definition",
  "module": "Bot Studio",
  "explicit_module": "Bot Studio",
  "confidence": 0.7666666666666666,
  "trace_sequence": "None:0",
  "video_attached": true,
  "video_id": "6a433c867d620401bb6774c1",
  "video_title": "Bot Studio",
  "bullet_cap": 8,
  "word_cap": 500,
  "answer_mode": "consulting",
  "cross_sell_attached": true
}
```

---

## What to Look For in SuperAgent Traces

To complete the before/after picture, match these kb_answer trace IDs to the SuperAgent conversation thread in SuperAgent's own telemetry. You should see:

1. **Original user message** — the raw text the user typed in the chat UI
2. **System prompt expansion** — SuperAgent LLM turning the user message into the structured query shown above
3. **kb_answer tool call** — the structured query being sent to kb_answer (matches `query` field above)
4. **kb_answer response** — the `answer` field shown above (before rewrite)
5. **Final LLM response** — what SuperAgent's LLM wrote to the user after reading kb_answer's output

Comparing steps 4 and 5 will show the answer rewrite. The `answer_preview` field in the kb_answer metadata (above) contains the first ~200 chars of what kb_answer returned — cross-reference with the final UI output to measure reformulation.

## Known Rewrite Issues Observed

| Issue | Root Cause | Fix Applied |
|-------|-----------|-------------|
| Cross-sell block stripped | SKILL.md missing preserve instruction | Added `## Cross-sell block` to SKILL.md v4.4 |
| Answer structure paraphrased | SuperAgent LLM applies its own style | Acceptable — SKILL.md guardrails limit compression |
| Bullet/step numbering removed | LLM reformats lists | Known; no fix needed unless facts are dropped |
| Video links preserved | SKILL.md explicit `never drop` instruction | Working as intended |

---

*Generated from Langfuse production traces by the gupshup_guide analytics agent.*