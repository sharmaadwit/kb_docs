source_url: https://console-docs.gupshup.io/docs/regex-validation-in-prompt-nodes
# BOT STUDIO

## RegEx Validation in Prompt Nodes

# RegEx Validation in Prompt Nodes

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
Updated 10 months ago
