# Gate C Validation — kb_search.py post-Patch 9

Run each query below using the `kb_search` action. Report the top result's source path for each.

> **DO NOT touch any code. This is a read-only validation step.**

## Search ranking (top result source should contain the expected slug)

| # | Query | Expected slug in top result source |
|---|-------|------------------------------------|
| S1 | `condition node` | `condition-node` |
| S2 | `api node in journey builder` | `api-node` |
| S3 | `business hours` | `user-management-business-hours` |
| S4 | `save vs save & deploy` | `save-vs-save-deploy` |
| S5 | `Where do I add a webhook callback URL?` | `integrations/webhooks` |
| S6 | `sticky assignment` | `chat-management-assignment-rules` |

## Negative queries (should return empty results due to guardrail)

| # | Query | Expected |
|---|-------|----------|
| N1 | `Tell me a joke` | Empty results |
| N2 | `How do I make pizza?` | Empty results |

## Multi-concept (top 5 results should cover both slugs)

| # | Query | Expected slugs in top 5 |
|---|-------|------------------------|
| M1 | `business hours vs auto replies` | `user-management-business-hours` AND `response-management-auto-replies` |
| M2 | `campaign click metrics vs goal conversions` | `campaign-analytics` AND `goal-analytics` |

## Report format

For each test, report:
```
S1: PASS/FAIL — top source: <source path>
S2: PASS/FAIL — top source: <source path>
...
N1: PASS/FAIL — results count: <n>
N2: PASS/FAIL — results count: <n>
M1: PASS/FAIL — sources in top 5: <list>
M2: PASS/FAIL — sources in top 5: <list>
```
