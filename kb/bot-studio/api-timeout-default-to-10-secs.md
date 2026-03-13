source_url: https://console-docs.gupshup.io/docs/api-timeout-default-to-10-secs

<!-- kb-golden:v9 -->
# API Timeout Default to 10 Secs

**Module**: Bot Studio

## Definition
Timeout Default Value

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → API Timeout Default to 10 Secs

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **API Timeout Default to 10 Secs**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- When closing the API settings modal, the system will validate all API timeout values.

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Error Validation: Any timeout set below 1 second or above 60 seconds will trigger an error notification, ensuring all timeout values remain within the valid range.
- Invalid timeouts (e.g., 0 or outside the 1-60 second range) will prompt an error, requiring correction before proceeding.

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **API Timeout Default to 10 Secs**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# API Timeout Default to 10 Secs

**Module**: Bot Studio

## Overview
Timeout Default Value

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Timeout Default Value

# Introduction

This enhancement standardizes the API Timeout settings in Journey Builder, setting a default timeout of 10 seconds for new API calls. The update ensures improved performance consistency by establishing minimum and maximum limits for API response times. The feature also includes error handling to prevent invalid timeout values and backward compatibility to preserve the settings of existing APIs.

# Key Aspects of the Feature

- Default Timeout: Newly created API calls will automatically have a timeout of 10 seconds.
- Time Constraints: Minimum Timeout: 1 second. Maximum Timeout: 60 seconds. Invalid values (e.g., 0 or empty) will be disallowed.
- Minimum Timeout: 1 second.
- Maximum Timeout: 60 seconds.
- Invalid values (e.g., 0 or empty) will be disallowed.
- Backward Compatibility: Timeout changes will not affect pre-existing APIs unless edited.
- Error Validation: Any timeout set below 1 second or above 60 seconds will trigger an error notification, ensuring all timeout values remain within the valid range.
# How to Use

- Setting Timeout for New APIs: When creating a new API node in Journey Builder, the timeout field will default to 10 seconds. Adjust the timeout value if necessary, keeping it between 1 and 60 seconds.
- When creating a new API node in Journey Builder, the timeout field will default to 10 seconds.
- Adjust the timeout value if necessary, keeping it between 1 and 60 seconds.
- Editing Existing APIs: Existing APIs with a timeout of 0 or invalid entries will not be affected until edited. If editing the timeout setting on an older API, update the timeout to a valid range (1-60 seconds) before saving.
- Existing APIs with a timeout of 0 or invalid entries will not be affected until edited.
- If editing the timeout setting on an older API, update the timeout to a valid range (1-60 seconds) before saving.
- Validation on Modal Close: When closing the API settings modal, the system will validate all API timeout values. Invalid timeouts (e.g., 0 or outside the 1-60 second range) will prompt an error, requiring correction before proceeding.
- When closing the API settings modal, the system will validate all API timeout values.
- Invalid timeouts (e.g., 0 or outside the 1-60 second range) will prompt an error, requiring correction before proceeding.
# Use Cases

- Standardized API Call Durations Scenario: A business requires a consistent response time across multiple APIs for user-facing processes. Benefit: Defaulting to 10 seconds ensures predictable response handling while allowing customization within a set range, improving user experience.
- Scenario: A business requires a consistent response time across multiple APIs for user-facing processes.
- Benefit: Defaulting to 10 seconds ensures predictable response handling while allowing customization within a set range, improving user experience.
- Performance Optimization Scenario: An e-commerce platform wants to minimize delays in order processing by setting clear limits on API response times. Benefit: The 1-60 second range prevents excessively long waits or timeouts, enhancing platform performance and reliability.
- Scenario: An e-commerce platform wants to minimize delays in order processing by setting clear limits on API response times.
- Benefit: The 1-60 second range prevents excessively long waits or timeouts, enhancing platform performance and reliability.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
