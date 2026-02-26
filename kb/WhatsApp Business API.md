# WhatsApp Business API

Gupshup's WhatsApp Business API provides APIs to send free form messages (session messages) and template messages (utility/marketing/authentication) to users on WhatsApp.

### Session Messaging
- Session messages can be sent within a 24-hour window of the last user message.
- These are free-form and don't require prior approval.

### Template Messaging
- Template messages are required to initiate a conversation with a user outside the 24-hour window.
- These must be pre-approved by WhatsApp.
- Supported types: Utility, Marketing, Authentication.

### API Endpoint
The API endpoint is used to send both session and template messages by providing the appropriate request body and authentication.
