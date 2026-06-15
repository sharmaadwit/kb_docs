source_url: https://docs.gupshup.io/docs/waba-setup-console

<!-- kb-golden:v10 -->
# WABA Setup - Detailed Gupshup Console Flow

**Module**: Channels

## Definition

Step-by-step guide for connecting WABA within Gupshup Console specifically.

## Prerequisites Checklist

✓ WABA created in Meta Business Manager  
✓ Phone Number Code from Meta  
✓ Admin access to Gupshup Console  
✓ Gupshup project created  

## Step 1: Navigate to WABA Setup

1. Go to **Console → Channels → WhatsApp → WABA Management**
2. Click **Add WABA** button

**You'll see fields:**
- WABA ID (from Meta)
- Phone Number Code
- Display Name (how it shows in your Console)

## Step 2: Enter WABA Details

**WABA ID:** Find in Meta Business Manager → WhatsApp → Settings → Account Info

**Phone Number Code:** Generated in Meta when you added phone number

**Display Name:** Suggested format: "WhatsApp - [Business Name]"

**Associated Phone Numbers:** Shows numbers added in Meta

**Support Phone:** Phone number customers can call

## Step 3: Authorize WABA Connection

1. Click **Authorize WABA**
2. Permission prompt appears
3. Gupshup requests:
   - Permission to send messages
   - Permission to manage templates
   - Permission to view analytics
4. Click **Approve** or customize permissions
5. Click **Confirm Authorization**

**Status changes:** "Pending" → "Connected"

## Step 4: Configure Templates

1. Go to **Templates** in sidebar
2. Click **Create New Template**
3. Choose type: Text, Media, Interactive
4. Fill in template content
5. **Fallback text:** Required (shown on non-WhatsApp devices)
6. Click **Submit for Approval**

**Meta approves in:** 2-4 hours usually

## Step 5: Monitor WABA Status

**In Console → WABA Management:**
- **Green indicator:** Healthy connection
- **Yellow indicator:** Issue detected, review status
- **Red indicator:** Connection failed, reconnect

**What to check:**
- WABA connection status
- Webhook endpoint status
- Phone number approval status

## Step 6: Setup Webhooks (Optional)

1. Go to **Settings → Webhooks**
2. Click **Add Webhook**
3. Enter webhook URL (HTTPS required)
4. Select events:
   - message_received
   - message_delivered
   - message_read
   - template_status
5. Click **Save Webhook**
6. Verify with test event

## Step 7: Configure Analytics

1. Go to **Analytics → Messages**
2. View metrics:
   - Sent count
   - Delivered count
   - Failed count
   - Delivery rate %
3. Create custom dashboard (optional)

## WABA Quotas & Limits

| Resource | Limit |
|----------|-------|
| Phone numbers per WABA | 5 included, +$5/month |
| Message rate | 100/second |
| Templates | 1000 max |
| Webhooks | 20 endpoints |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection failed | Verify WABA ID, phone code correct |
| Phone stuck pending | Verify ownership in Meta, wait 24h |
| Can't add phone | Check WABA limit, request more numbers |
| Webhooks not firing | Verify URL is HTTPS, public, add logging |
| Template stuck review | Check for prohibited content |

## Quick Checks

- ✓ WABA status: Green indicator?
- ✓ Phone number: Approved?
- ✓ Templates: At least 1 approved?
- ✓ Webhooks: (Optional) Added and tested?
- ✓ Analytics: Tracking messages?

## Reference (from source)

<!-- procedural:v2 -->
# WABA Setup - Detailed Console Flow

Step-by-step guide for connecting WhatsApp Business Account in Gupshup Console.
