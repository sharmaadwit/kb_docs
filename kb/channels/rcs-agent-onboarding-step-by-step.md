source_url: https://docs.gupshup.io/docs/rcs-setup

<!-- kb-golden:v10 -->
# RCS Agent Onboarding - Step by Step

**Module**: Channels

## Definition

RCS Agent registration enables your brand to send rich messages at scale via Dotgo RBM Hub.

## Prerequisites

- Gupshup Console access
- Company website URL
- Brand logo (224x224px, < 90KB, PNG/JPG)
- Privacy policy URL
- Terms & conditions URL
- Support email
- Timeline: 24-48 hours for approval

## Step 1: Gather Required Documents

✓ Legal business name  
✓ Website URL  
✓ Brand logo (see size requirements above)  
✓ Privacy policy link  
✓ Terms & conditions link  
✓ Support contact email  
✓ Brief company description  

## Step 2: Register RCS Agent in Console

1. Go to **Gupshup Console → Channels → RCS**
2. Click **Register RCS Agent**
3. Fill in business details
4. Upload brand logo
5. Paste privacy policy and T&C URLs
6. Enter support email
7. Click **Submit for Verification**

## Step 3: Wait for Dotgo Approval

- Dotgo reviews your application (24-48 hours)
- You'll receive approval email
- Check Console for approval status
- Mark status changes from "Pending" to "Approved"

**If rejected:** Email will explain reason (usually logo format, missing docs)

## Step 4: Configure Agent Credentials

1. After approval, Console shows **Bot ID**
2. Go to **Settings → RCS Agent**
3. Click **Generate Credentials**
4. Save **Client ID** and **Client Secret** securely
5. Store in vault (never commit to code)

## Step 5: Test in Sandbox

1. Go to **RCS Agent → Sandbox Mode**
2. Toggle **Enable Sandbox**
3. Send test message to your phone
4. Verify message arrives
5. Check delivery status in Console

## Step 6: Go Live

1. Disable sandbox mode
2. Create first RCS template
3. Submit template for approval (24-48 hours)
4. After approval, start sending campaigns

## Common Errors

| Error | Fix |
|-------|-----|
| Approval pending > 48hrs | Contact support with Bot ID |
| Invalid logo format | Resize to 224x224px, save as PNG |
| Test message not received | Check phone supports RCS, verify number format |
| Client credential generation fails | Re-verify approval status, try again in 1 hour |

## Next Steps

- Create message templates
- Set up webhooks
- Build RCS campaigns
- Monitor delivery metrics

## Reference (from source)

<!-- procedural:v2 -->
# RCS Agent Onboarding

Complete step-by-step guide to register and configure RCS Agent for Dotgo RBM Hub.
