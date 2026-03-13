source_url: https://console-docs.gupshup.io/docs/regex-validation-in-prompt-nodes

<!-- kb-golden:v7 -->
# RegEx Validation in Prompt Nodes

**Module**: Bot Studio

## Definition
As part of our platform hardening and bot reliability initiatives, Gupshup Console validates all regular expressions in Prompt Nodes using the Re2 regex engine, developed by Google. This ensures that patterns used for validating user input are safe, efficient, and non-blocking at runtime.

## Procedure
### Exact path
Gupshup Console → Bot Studio → RegEx Validation in Prompt Nodes

### Where to configure it
Gupshup Console → Bot Studio → RegEx Validation in Prompt Nodes

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **RegEx Validation in Prompt Nodes**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **RegEx Validation in Prompt Nodes**.
4. Test your regex in a Re2-compatible environment before using it in Console.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- Test your regex in a Re2-compatible environment before using it in Console

## Available options
- 1. Compliance with Re2 Syntax
- 2. Runtime Safety (Catastrophic Backtracking Prevention)
- 3. Invalid or Malformed Patterns

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Regex entered during node configuration is validated on click of Tick icon on the regex field. If the expression does not conform to Re2 standards, an error is shown and the journey cannot be saved until it is corrected.
- You will see an error: Invalid regex expression. learn more.
- An error toast appears below the regex field: Invalid regex expression. learn more
- The journey cannot be saved until the regex is correctly saved

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# RegEx Validation in Prompt Nodes

**Module**: Bot Studio

## Overview
As part of our platform hardening and bot reliability initiatives, Gupshup Console validates all regular expressions in Prompt Nodes using the Re2 regex engine, developed by Google. This ensures that patterns used for validating user input are safe, efficient, and non-blocking at runtime.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Overview

As part of our platform hardening and bot reliability initiatives, Gupshup Console validates all regular expressions in Prompt Nodes using the Re2 regex engine, developed by Google. This ensures that patterns used for validating user input are safe, efficient, and non-blocking at runtime.

Regex entered during node configuration is validated on click of Tick icon on the regex field. If the expression does not conform to Re2 standards, an error is shown and the journey cannot be saved until it is corrected.

## What Validations Are Performed?

The regex string entered is validated on the following grounds:

### 1. Compliance with Re2 Syntax

Re2 has a strict subset of regular expression features, and the Console validation checks whether:

- The syntax is compatible with Re2 grammar
- The expression does not contain disallowed constructs
Unsupported features include:

- Lookbehind assertions: (?<=...), (?<!...)
- Backreferences: \1, \2, etc.
- Possessive quantifiers: ++, *+, ?+
- Atomic groups: (?>...)
- Conditional expressions: (?(1)A|B)
- Certain complex nested quantifiers or poorly structured groupings
### 2. Runtime Safety (Catastrophic Backtracking Prevention)

Even if a pattern is syntactically correct, Re2 rejects it if:

- It contains ambiguous quantifiers (e.g., .*.*, (.+)+) that can lead to exponential backtracking
- It could result in unbounded execution time under certain user inputs
### 3. Invalid or Malformed Patterns

Console will also flag patterns that:

- Contain unmatched parentheses or brackets
- End abruptly (e.g., *, +, or ? without a preceding token)
- Use invalid escape sequences (e.g., \Q, \C)
## Example: Why is My Regex Showing “Invalid”?

If you try saving a node with the regex:

```
^(?<=Order\s)\d+$
```

You will see an error: Invalid regex expression. learn more.

Reason: This pattern uses a lookbehind assertion (?<=...), which is not supported by Re2. Even though it may work in other engines like JavaScript or Python, it will be rejected by the Console to ensure runtime safety.

## UI Behavior on Invalid Regex

If an invalid regex is detected :

- An error toast appears below the regex field: Invalid regex expression. learn more
- The regex input field in the Prompt Node is highlighted in red
- The journey cannot be saved until the regex is correctly saved
## What You Should Do

- Use simpler, linear-safe regex patterns such as: ^[a-zA-Z\s]+$ (for names) ^\d{6}$ (for PIN codes) ^[A-Za-z0-9_]+$ (for usernames)
- ^[a-zA-Z\s]+$ (for names)
- ^\d{6}$ (for PIN codes)
- ^[A-Za-z0-9_]+$ (for usernames)
- Avoid unsupported features like lookbehind and backreferences
- Test your regex in a Re2-compatible environment before using it in Console

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
