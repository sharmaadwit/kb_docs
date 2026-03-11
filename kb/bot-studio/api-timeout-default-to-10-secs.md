source_url: https://console-docs.gupshup.io/docs/api-timeout-default-to-10-secs
# BOT STUDIO

## API Timeout Default to 10 Secs

# API Timeout Default to 10 Secs

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
Updated 10 months ago
