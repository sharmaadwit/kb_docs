source_url: https://docs.gupshup.io/docs/whatsapp-setup

<!-- kb-golden:v10 -->
# WhatsApp Business Account (WABA) Setup

**Module**: Channels

## Definition

WhatsApp Business Account (WABA) is required to send messages at scale. This guide covers registration through Gupshup Console.

## Prerequisites

- Meta Business Account with admin access
- Gupshup Console project created
- Business phone number (can be landline)
- Timeline: 24-48 hours for approval

## Step 1: Create WABA in Meta Business Manager

1. Go to **Meta Business Manager** (business.facebook.com)
2. Click **Accounts → WhatsApp Accounts**
3. Click **Create Account**
4. Enter business name, phone number, industry, support email
5. Accept terms and click **Create**
6. Meta sends verification email

## Step 2: Generate Phone Number Code

1. In Meta Business Manager, select your WABA
2. Go to **Phone Numbers**
3. Click **Add Phone Number**
4. Verify phone ownership via SMS/call
5. Once verified, click **Generate Code**
6. Save this code (needed in Step 3)

## Step 3: Connect WABA to Gupshup Console

1. Go to **Gupshup Console → Channels → WhatsApp**
2. Click **Connect WABA**
3. Paste the **Phone Number Code** from Meta
4. Click **Authorize**
5. Grant Gupshup permissions to access WABA
6. Click **Confirm**

**Status:** WABA is now connected. Phone number status shows "Approved" or "Pending".

## Step 4: Create & Approve Templates

1. Go to **Templates** in Console
2. Click **Create Template**
3. Choose template type (Text, Media, Interactive)
4. Write template content
5. Provide fallback text
6. Click **Submit for Approval**
7. Meta approves in 2-4 hours (usually)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| WABA connection failed | Check phone code is correct, verify business ownership in Meta |
| Phone number stuck pending | Verify phone number via SMS in Meta, wait 24 hours |
| Template approval delayed | Check for prohibited content, ensure fallback text provided |
| Can't add phone number | Check WABA limits (5 included), request more from support |

## Next Steps

- Create first campaign
- Set up webhooks for incoming messages
- Configure message templates
- Begin sending

## Reference (from source)

<!-- procedural:v2 -->
# WhatsApp WABA Setup

Step-by-step guide to register and connect WhatsApp Business Account in Gupshup.
