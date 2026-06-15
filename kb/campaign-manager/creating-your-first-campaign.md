source_url: https://docs.gupshup.io/docs/campaign-manager

<!-- kb-golden:v10 -->
# Creating Your First Campaign

**Module**: Campaign Manager

## What Are Campaigns and Why You Need Them

**Definition**: A campaign is a bulk message sent to multiple recipients through a single configured channel (WhatsApp, RCS, or SMS). Unlike one-off messages, campaigns help you reach thousands of people simultaneously with personalized content, while tracking delivery and engagement.

**Why campaigns matter:**
- **Scale**: Send the same message to thousands of recipients at once
- **Personalization**: Use customer data (names, order IDs, voucher codes) to customize messages
- **Timing**: Schedule messages for optimal delivery times or future dates
- **Tracking**: Monitor sent, delivered, failed, and read rates in one dashboard
- **Compliance**: Built-in opt-in verification to stay compliant with regulations

**When to create your first campaign:**
- You've just connected a WhatsApp, RCS, or SMS channel to Gupshup
- You have a message template approved by the messaging platform
- You have a list of phone numbers for your audience
- You want to send a bulk message (promotions, announcements, order updates, etc.)

---

## Prerequisites — 5 minutes

Before you start, make sure you have these in place:

### 1. Channel Configured
- ✓ WhatsApp Business Account set up and connected to Gupshup Console
- ✓ Or RCS channel enabled with approved MCC/MNC codes
- ✓ Or SMS provider (Twilio, Nexmo, etc.) configured
- **Check:** Console → Channels → [Your Channel] → Status shows "Active"

### 2. Template Approved
- ✓ Message template created and submitted to Meta (WhatsApp), RCS, or carrier
- ✓ Template must show "Approved" status (not "Pending" or "Rejected")
- **Check:** Console → Channels → [Your Channel] → Templates → See approved templates listed

### 3. Audience List Ready
- ✓ Phone numbers in a CSV or XLS file (max 50 MB)
- ✓ One phone number per row in column named "phone" or "Phone"
- ✓ Phone numbers in E.164 format: country code + number, no + or spaces (e.g., `918928075130` for India)
- ✓ Optional columns: name, email, customer_id, order_id (whatever data your template needs)
- **Check:** Open your CSV file in Excel to verify format

### 4. Campaign Manager Access
- ✓ Your user account has "Campaign Manager" permission
- ✓ If you see Campaign Manager in left navigation → you have access
- **Check:** Console → Settings → Users → Your User → Verify Campaign Manager is enabled

---

## Step 1: Start Creating Your Campaign — 2 minutes

**Time estimate**: 2 minutes

1. Log into Gupshup Console
2. In left navigation, click **Campaign Manager**
3. Click **+ New Campaign** (blue button, top-right)
4. You'll see **Step 1: Campaign Details**

### In Campaign Details:
- **Campaign Name**: Give it a descriptive name (e.g., "June Promo - WhatsApp", not "Campaign1")
  - Example: "Order Confirmation - Batch 1"
  - Example: "Welcome Offer - New Users"
- **Description** (optional): Add context for your team (e.g., "Sent to users who signed up June 1-10")
- **Select Channel**: Choose from dropdown:
  - WhatsApp Business (if you have WhatsApp connected)
  - RCS (if you have RCS connected)
  - SMS (if you have SMS provider configured)
- **Select Phone Number**: If your channel has multiple sender numbers, pick one
- **Campaign Type**:
  - **One-time**: Send once at a specific date/time or immediately
  - **Scheduled**: Send at a specific date and time
  - **Recurring**: Send every day/week/month at same time (for repeat campaigns)
  - *For your first campaign, select "Scheduled" or "One-time"*

**Screenshot example**: Campaign name: "June 10 Order Confirmation", Channel: "WhatsApp", Campaign Type: "Scheduled"

Click **Next** to proceed to Step 2.

---

## Step 2: Select Your Recipients — 5 minutes

**Time estimate**: 5 minutes

You'll see **Step 2: Audience Selection**. Choose one of three ways to reach people:

### Option A: Upload Phone Number CSV (Most Common for First Campaign)

1. Click **Upload File**
2. Select your CSV or XLS file from your computer
3. **Match columns**: Map your file columns to Gupshup fields:
   - **Phone column**: Required. Select the column containing phone numbers
   - **Name column**: Optional. Select the column with customer names (used in {{name}} variables)
   - **Email column**: Optional. Select the column with emails
   - **Custom columns**: Any other columns (order_id, promo_code, etc.)
4. Declare consent: Check **"I confirm that the audience has explicitly opted-in to receive messages"**
   - This is mandatory for compliance. Don't check it if you're unsure.
5. Click **Upload & Continue**

**Expected output**: You'll see a summary like "2,500 phone numbers loaded, 18 columns matched"

**CSV format example**:
```
phone,name,email,order_id
918928075130,Raj Kumar,raj@example.com,ORD-12345
919876543210,Priya Singh,priya@example.com,ORD-12346
917654321098,Amit Patel,amit@example.com,ORD-12347
```

### Option B: Select User Segment (If You Have Saved Segments)
1. Click **Select User Segment**
2. Choose from your pre-built segments (e.g., "Active Users - Last 30 Days")
3. Segment must have phone numbers associated

### Option C: Use Query Builder (Advanced)
1. Click **Build Query**
2. Filter users by attributes (signup date, purchase history, etc.)
3. Creates a dynamic audience (runs at send time)

**For your first campaign, use Option A** (upload CSV).

Click **Next** to proceed to Step 3.

---

## Step 3: Choose Your Message Template — 3 minutes

**Time estimate**: 3 minutes

You'll see **Step 3: Select Template**. 

1. **Select Template**: From the dropdown, choose your approved template
   - Only "Approved" templates appear (grayed out templates are still pending)
   - Template shows: Name, content preview, and variables
2. **Map Variables**: For each {{variable}} in your template, tell Gupshup where to get the data:
   - **From CSV column**: Click dropdown, select "name" (or other column from your file)
   - **Fallback value**: If a customer has no data for this column, use this default text
   - Example: Template says "Hi {{name}}", select column "name". Fallback = "Friend"
     - If CSV has "Raj" → message becomes "Hi Raj"
     - If CSV is blank → message becomes "Hi Friend"
3. **Media URL** (if template has images/video/document):
   - If sending same media to all: Paste URL in **Fallback** field
   - If different media per person: Create column in CSV with URLs
   - **Valid URLs**: Amazon S3, Cloudinary, Azure Storage (not Google Drive, Dropbox)
   - **Supported formats**:
     - Image: JPEG, PNG (max 5 MB)
     - Video: MP4, 3gp (max 16 MB)
     - Document: PDF (max 100 MB)
4. **CTA Button Links** (if template has buttons):
   - Static: Enter one URL, same for all recipients
   - Dynamic: Use {{order_id}} or {{promo_code}} in URL like `https://mysite.com/redeem?code={{promo_code}}`

**Example mapping**:
```
Template text: "Hi {{name}}, your order {{order_id}} is ready"
CSV columns: name="Raj", order_id="ORD-123"
Result: "Hi Raj, your order ORD-123 is ready"
```

Click **Next** to proceed to Step 4.

---

## Step 4: Schedule Delivery — 3 minutes

**Time estimate**: 3 minutes

You'll see **Step 4: Schedule & Preview**.

### Delivery Options:

**Send Now**
- Message goes out immediately
- Use for urgent announcements or testing
- Click **Send Campaign**

**Schedule for Specific Date/Time**
1. Click **Schedule**
2. Pick date from calendar
3. Pick time (hours and minutes)
4. Select **Timezone** (important! use your business timezone, not recipient timezone)
5. Click **Schedule Campaign**

**Schedule for Optimal Time (WhatsApp only)**
- Gupshup sends each message when that recipient is most active
- Click **Optimal Time** checkbox
- Gupshup analyzes past recipient behavior and sends during their peak hours
- Requires historical data (may not be available on first campaign)

### Preview Your Message:
Before you send, **verify**:
- ✓ Message preview shows correctly with sample data
- ✓ All {{variables}} are replaced with real values (not blank)
- ✓ Media displays correctly (if applicable)
- ✓ Recipient count matches expected audience size
- ✓ Date/time/timezone are correct

---

## Step 5: Review and Send — 2 minutes

**Time estimate**: 2 minutes

**Final checklist before sending:**

| Check | Status |
|-------|--------|
| Campaign name is descriptive | ✓ |
| Channel is correct | ✓ |
| Recipient count > 0 | ✓ |
| Phone numbers format is correct (E.164) | ✓ |
| Audience has opted-in (declared) | ✓ |
| Template is approved (not pending) | ✓ |
| All variables are mapped | ✓ |
| Message preview shows correct data | ✓ |
| Date/time/timezone is correct | ✓ |
| No test/dummy data in recipient list | ✓ |

**When ready:**
- Click **Send Campaign** (for immediate send) or
- Click **Schedule Campaign** (for scheduled send)

**You'll see**: Campaign moves to "Queued" or "Scheduled" status. Page refreshes.

---

## Step 6: Monitor Your Campaign — Ongoing

**Time estimate**: 1 minute to check initial status, then monitor over 24 hours

After sending, your campaign appears in Campaign Manager with real-time metrics.

### Track Campaign Status:
1. Click **Campaign Manager** in left navigation
2. Find your campaign in the list
3. Click on campaign name to see dashboard

### Key Metrics to Monitor:

| Metric | What It Means |
|--------|--------------|
| **Sent** | Number of messages delivered to WhatsApp/carrier servers |
| **Delivered** | Number successfully delivered to recipient's phone |
| **Failed** | Messages that couldn't be sent (bad number, carrier issue, etc.) |
| **Read** | Recipient opened the message (WhatsApp only) |
| **Delivery Rate %** | (Delivered / Sent) × 100 = success percentage |
| **Clicked** | Recipients clicked a CTA button or link |

### Check Status Timeline:
- **Immediately after send**: Most will show "Sent"
- **5-10 minutes**: Many will show "Delivered"
- **1-2 hours**: Most should show "Delivered" or "Read"
- **24 hours**: Final metrics stable, can calculate ROI

### Example Healthy First Campaign:
- Sent: 2,500
- Delivered: 2,435 (97.4% delivery rate) ✓
- Failed: 65 (2.6%, usually bad numbers)
- Read: 1,210 (49.6% of delivered)
- Clicked: 180 (7.2% of delivered)

---

## First Campaign Checklist

Use this before you hit "Send":

- [ ] I have Campaign Manager access
- [ ] My channel is connected and active
- [ ] My message template is approved
- [ ] My CSV has 10+ phone numbers (test with small list first)
- [ ] Phone numbers are in E.164 format (e.g., 918928075130)
- [ ] I declared that my audience opted-in
- [ ] I mapped all {{variables}} to CSV columns
- [ ] Fallback values are set for missing data
- [ ] Message preview looks correct with real data
- [ ] Date/time/timezone match my intent
- [ ] I'm not sending to myself or a test number (unless intentional)
- [ ] I have a backup of my CSV file

---

## Common Mistakes on Your First Campaign

Avoid these pitfalls:

### Mistake 1: Sending Without Opt-In Consent
**What happens**: Campaign fails compliance checks, platform suspends channel.
**Fix**: Only send to phone numbers that have explicitly opted-in (subscribed).
**Check before sending**: Checkbox says "I confirm opted-in" before you click Send.

### Mistake 2: Template Still "Pending" Approval
**What happens**: Campaign gets stuck in "Pending" status forever.
**Fix**: Wait for platform (Meta, RCS carrier, SMS provider) to approve template first.
**Check before sending**: Template shows "Approved" badge, not "Pending" or "Rejected".

### Mistake 3: Wrong Variable Names in CSV
**What happens**: Variables show as blank in message (e.g., "Hi , your order is ready").
**Fix**: Make sure CSV column names exactly match template variables.
**Example**: Template has {{customer_name}}, but CSV column is "Full_Name" → no match.
**Check**: When you map variables, dropdown shows your CSV columns correctly.

### Mistake 4: Phone Numbers in Wrong Format
**What happens**: Most messages fail with error "Invalid format".
**Fix**: Phone numbers must be E.164 format: country code + number, no + or spaces.
- ❌ Wrong: +91 9876543210, 0198765432, 918928075130 (with spaces)
- ✓ Right: 918928075130 (India), 16175551234 (US)
**Check**: Open your CSV in Excel, copy one number, and verify format.

### Mistake 5: Wrong Timezone
**What happens**: Campaign sends at 3 AM when you meant 3 PM.
**Fix**: Select your **business timezone**, not recipient timezone.
**Example**: Your business is in New York, but audience is in India. Select "America/New_York", Gupshup will convert to send at right time.
**Check**: Look at scheduled send time, mentally add/subtract hours to confirm it's correct.

### Mistake 6: Forgetting to Review Before Send
**What happens**: Campaign goes out with typo or wrong data.
**Fix**: Always click on the preview section and verify 3 sample messages before sending.
**Check**: Look for missing values, formatting issues, broken links.

### Mistake 7: Using Special Characters in Phone Numbers
**What happens**: "Invalid phone number" error.
**Fix**: Remove +, -, (, ), spaces from CSV. Only digits and country code.
- ❌ Wrong: +91-98-765-43210
- ✓ Right: 918928075130
**Check**: Use Excel Find & Replace to remove special characters.

---

## Troubleshooting Common Issues

### Campaign Stuck in "Pending" Status

**Symptoms**: Campaign shows "Pending" for hours, no messages sent.

**Root cause**: Template is not approved yet (still "Pending Review" with Meta).

**Fix**:
1. Go to Channels → [Your Channel] → Templates
2. Find your template, check status
3. If "Pending": Wait for Meta/carrier approval (usually 24-48 hours)
4. If "Rejected": Read rejection reason, edit template, resubmit
5. Once "Approved", re-create campaign (can't reuse pending campaign)

---

### High Failure Rate (>10% failures)

**Symptoms**: Dashboard shows "Failed: 500 out of 2500" (20% failure).

**Root causes** (in order of likelihood):
1. **Bad phone numbers** (most common): Numbers don't exist, inactive, or in wrong format
2. **Carrier coverage**: Recipient's carrier doesn't support WhatsApp/RCS/SMS
3. **Opted-out**: Some numbers have already unsubscribed
4. **Rate limit**: Gupshup account hit sending limit (rare on first campaign)

**Fix**:
- **Check format**: Open CSV, verify all numbers are E.164 (country code + digits only)
- **Validate list**: Use a phone validation API to verify numbers are real
- **Check opt-outs**: Cross-reference against your opt-out/unsubscribe list
- **Contact support**: If >15% failures and format looks correct, [submit support ticket](https://console.gupshup.io/support)

---

### Low Delivery Rate (<70%)

**Symptoms**: "Sent: 2500, Delivered: 1500" (60% delivery).

**Root causes**:
1. **Carrier coverage**: Many numbers on carriers with poor WhatsApp/RCS support
2. **Phone number format issues**: Some numbers may be inactive or not in E.164
3. **Message rejected by carrier**: Rare, but possible if content violates carrier rules
4. **Network issues**: Temporary carrier outages (check next day, usually resolves)

**Fix**:
- **Wait 24 hours**: Delivery can improve as carriers process messages
- **Check format**: Verify numbers use E.164 consistently
- **Review message**: Ensure no suspicious links, excessive URLs, or spam triggers
- **Segment audience**: Try sending to smaller, verified segment first
- **Compare with past**: If previous campaigns had higher rate, investigate what changed

---

### Template Not Showing in Template Selection

**Symptoms**: You created a template, but it doesn't appear in the campaign template dropdown.

**Root cause**: Template is not approved yet, or you selected wrong channel.

**Fix**:
1. Go to Channels → [Your Channel] → Templates
2. Verify template shows "Approved" status
3. If "Pending": Wait for platform approval
4. If "Rejected": Check rejection reason and resubmit
5. When creating campaign, make sure you selected **same channel** where template was created
   - Example: If template is in WhatsApp channel, create campaign in WhatsApp channel, not SMS

---

### Message Sending But Looks Blank

**Symptoms**: Recipient receives message but content is blank or variable shows as "{{name}}".

**Root cause**: Variable wasn't mapped correctly, or CSV column name doesn't match.

**Fix**:
1. Go back to **Step 3: Template**
2. Check variable mapping:
   - For {{name}}, dropdown should show your CSV column (e.g., "name" or "customer_name")
   - Not "Select Column" or empty
3. Check fallback value is set:
   - If CSV row is missing data, fallback text will show instead
   - Example: {{name}} fallback = "Friend" → message shows "Hi Friend" if name missing
4. If CSV column name doesn't match template variable:
   - Rename CSV column to match (e.g., rename "Full_Name" to "name")
   - Re-upload CSV
   - Retry mapping

---

## What's Next After Your First Campaign

Congratulations! You've sent your first campaign. Here's what to do next:

### 1. **Analyze Results** (1-2 hours)
- Check delivery rate (target: >90%)
- Check click rate (varies by message type)
- Note what worked, what didn't

### 2. **Send Second Campaign** (Different Segment)
- Try a different audience segment
- Test different template/message
- Compare delivery and engagement rates

### 3. **Set Up Analytics Dashboard**
- Create dashboard with key metrics
- Add automated alerts (e.g., "notify if delivery rate drops below 85%")
- Track performance over time

### 4. **Schedule Recurring Campaigns**
- Set up campaigns that repeat daily/weekly (e.g., "Weekly Digest")
- Use "Recurring" campaign type instead of "One-time"
- Gupshup sends automatically on schedule

### 5. **Integrate with Bot Studio**
- Link campaigns to chatbot conversations
- Use bot to collect data, then trigger campaigns to confirmed audience
- Example: Bot collects customer preferences → Campaign sends personalized offer

### 6. **Enable Campaign Analytics**
- Track conversion rate (who clicked → who bought?)
- Link campaign sends to your order/CRM system
- Measure ROI per campaign

---

## Quick Reference — Time Estimates

| Step | Time | What You Do |
|------|------|------------|
| Prerequisites | 5 min | Verify channel, template, audience list ready |
| Step 1: Campaign Details | 2 min | Name campaign, choose channel, type |
| Step 2: Select Audience | 5 min | Upload CSV, map columns, declare opt-in |
| Step 3: Choose Template | 3 min | Select template, map variables |
| Step 4: Schedule Delivery | 3 min | Pick date/time or send now |
| Step 5: Review & Send | 2 min | Final checks, click Send |
| **Total** | **20 min** | From zero to campaign sent |

**Monitoring**: 1 minute to check status, then ongoing throughout the day.

---

## Summary

Your first campaign follows a simple 6-step process:

1. **Create** → Give your campaign a name and channel
2. **Audience** → Upload phone numbers
3. **Template** → Pick message and map variables
4. **Schedule** → Choose send time
5. **Review** → Check everything looks right
6. **Send** → Click Send Campaign

Within 24 hours, you'll have clear metrics on delivery, engagement, and success. Use that data to improve your next campaign.

The most important things to remember:
- ✓ Template must be approved first
- ✓ Audience must have opted-in
- ✓ Phone numbers must be in E.164 format
- ✓ Always review before sending
- ✓ Monitor metrics for 24 hours
- ✓ Use insights to improve next campaign

**Next:** Read the [Campaign Analytics guide](campaign-analytics.md) to interpret your results, or [Creating an Automated Campaign](automated-campaign.md) to schedule recurring messages.
