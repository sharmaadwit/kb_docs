# Integrations

Connect your apps and services so your AI can work with your real data
Integrations are connections to external services your AI assistant can use. When you connect an integration, you give SuperAgent permission to read from and act on your behalf in that service—so you can ask things like "Show my unread emails" or "Create a Jira ticket for this bug" and the AI will do it.
What are integrations?
Integrations let your AI work with the tools you already use every day. Instead of copying data manually or switching between apps, you can stay in the chat and ask the AI to handle it. The AI uses secure, authorized connections to access your accounts—you control which services are connected and can disconnect them anytime.
Available integrations
SuperAgent supports connections to these popular services. Each card shows what the AI can do once connected:
Gupshup MCP
Run campaigns, get templates approved, read analytics across WhatsApp, SMS and RCS
Gmail
Read emails, send replies, search your inbox, draft messages
Google Sheets
Add rows, update cells, read data, create charts
Google Calendar
Check your schedule, create events, find free slots
Google Drive
List files, read documents, organize folders
Google Docs
Search documents, read content, create docs, edit text
Jira
Create tickets, update status, search issues, add comments
Salesforce
Look up contacts, create leads, update records
Gupshup MCP
Gupshup MCP is the connector for your own Gupshup account, and it sits at the top of the Connectors catalog. One connection covers all three of your messaging channels, so you can draft a template, get it approved, launch a campaign, and read the results without leaving the chat.
Templates — Draft and preview messages, build multi-step flows, create A/B variants, rewrite copy, localize into another language, then submit for approval, track what is pending, and fix anything that gets rejected.
Campaigns — Send on WhatsApp, SMS or RCS, schedule for later, add timed follow-ups, build and size your audience from your CDP or CRM, then review results and tune what is already running.
Analytics — Compare channels like for like, find where delivery is failing and why, see which templates perform best, break spend down by channel, and check your quality rating, tier and sending limits.
There are 40 ready-made commands in total. Type / in the chat box to browse them, or just say what you want in your own words. Nothing needs to be filled in up front: pick a command and answer as the conversation goes.
Info
Nothing sends until you confirm
Any command that would actually send messages opens a review first, showing the audience size, the channel and fallback, and the estimated spend. No messages go out until you approve that review.
Connecting takes about two minutes. Add Gupshup MCP from the Connectors catalog, sign in once with your Gupshup account, then enter your credentials for each channel you want to switch on. WhatsApp uses your account ID and password; SMS and RCS each use their own enterprise account ID and password. Turn on only the channels you need now and add the rest later without reconnecting.
How connecting works
Connecting an integration is simple. Go to the Integrations area, find the service you want, and click Connect. A popup will open asking you to sign in and authorize SuperAgent to access your account. Once you approve, the connection is established—no technical setup required.
Info
Authorization
You'll sign in through the service's own login page (e.g., Google or Atlassian). SuperAgent never sees your password; it only receives a secure token that allows it to act on your behalf within the permissions you grant.
Enabling and disabling integrations
After you connect an integration, you can turn it on or off without disconnecting. When disabled, the AI won't use that service—useful if you want to keep the connection for later but don't need it for current tasks. Re-enable it anytime with a single toggle.
Just describe what you need in plain language—the AI figures out which integration to use and how to do it.
What can you ask?
Here are example prompts you can try once an integration is connected:
Gupshup MCP — "Draft a WhatsApp template for our monsoon sale with a discount code and a CTA button" · "Where am I losing delivery, and why?"
Gmail — "Show my unread emails from today" · "Draft a reply to Sarah's last message"
Google Sheets — "Add a new row to my expenses sheet" · "Create a chart from column B"
Google Calendar — "What meetings do I have tomorrow?" · "Schedule a 30-min call with Alex on Friday"
Google Drive — "Find the Q4 report in my Drive" · "List files shared with me this week"
Google Docs — "Find my meeting notes doc and summarize it" · "Create a new doc titled Weekly update with a short intro"
Jira — "Create a bug ticket for the login issue" · "Show my open tickets"
Salesforce — "Look up the contact info for Acme Corp" · "Create a new lead"
Tip
Combine integrations
You can use multiple integrations in a single prompt. For example: "Check my calendar for tomorrow and draft a prep email for each meeting using Gmail."
What's next?
Connect an Integration — Step-by-step setup guide
Agents — Build agents that use your integrations
Scheduled Tasks — Automate integration-powered workflows
## Previous
Recipes: Overview
Connect an Integration
