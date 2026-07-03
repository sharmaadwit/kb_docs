# WhatsApp Message Pricing

WhatsApp message pricing on Meta's platform is structured around **message categories**. Costs vary significantly by country and market maturity.

## Message Categories

### 1. Template Messages
**Pre-approved, low-cost messages**

- Must use Meta-approved template
- Can only be sent within 24 hours of customer initiation
- Lowest cost per message
- Rates vary by region and message type (text, media, interactive)

**Use cases:**
- Order confirmations
- Delivery notifications
- Appointment reminders
- Account alerts

### 2. Service Messages
**Messages sent outside the 24-hour window**

- Used for account updates, order confirmations, appointment reminders
- Sent by business after 24-hour customer window closes
- Higher cost than template messages
- No frequency limits

**Use cases:**
- Monthly billing notifications
- Password reset confirmations
- Service status updates
- Account change notifications

### 3. Authentication Messages
**One-time password (OTP) for account security**

- Lowest-cost category
- Used for 2FA, account verification, identity confirmation
- Single-use codes with automatic expiration
- Fast delivery guaranteed

**Use cases:**
- Account signup verification
- Login OTP
- Payment confirmation codes
- Sensitive action verification

### 4. Marketing Messages
**Promotional content**

- Can only be sent within 24 hours of customer initiation
- Customer must have opted in
- Highest cost per message
- Strict frequency limits

**Use cases:**
- Promotional offers and discounts
- New product announcements
- Flash sales
- Seasonal campaigns

### 5. Meta Business Agent Messages
**AI agent responses**

- Charged **per token** at **$2.00 USD per 1 million tokens**
- Approximately **4–5 cents per interaction**
- No message template requirement
- Unlimited frequency within service limits

**Typical interaction costs:**
- Short response (100 tokens): $0.0002
- Medium response (300 tokens): $0.0006
- Long response (500 tokens): $0.0010

## Regional Pricing Variations

Pricing varies by country, market maturity, and capacity constraints.

### Developed Markets (Lower Cost)
- United States, Canada, UK
- Australia, Western Europe
- Template messages: $0.01–0.05 per message
- Service messages: $0.02–0.10 per message

### Emerging Markets (Variable Pricing)
- India, Brazil, Mexico
- Southeast Asia, Eastern Europe
- Template messages: $0.005–0.02 per message
- Service messages: $0.01–0.05 per message

### High-Demand Markets (Premium Pricing)
- China, Middle East, Africa
- Capacity constraints and demand
- Template messages: $0.05–0.20+ per message
- Service messages: $0.10–0.50+ per message

## Cost Examples

### E-Commerce Order Notification Flow
```
Customer purchases item
  ↓
Order confirmation template:      $0.015  (sent within 24h)
  ↓
[24+ hours pass]
  ↓
Shipping update service msg:      $0.05   (sent after window)
  ↓
[2FA for return]
  ↓
OTP authentication message:       $0.002  (sent on demand)
  ↓
Total for interaction:            ~$0.07
```

### Customer Support with BizAI Agent
```
Customer inquiry                           $0.00   (incoming, not charged)
  ↓
BizAI response (400 tokens):              $0.008  ($2M/1M tokens)
  ↓
[If escalation needed]
  ↓
Service message to support team:          $0.05
  ↓
Total cost per resolution:                ~$0.058
```

### Monthly Volume Impact

**10,000 messages/month**
- Mostly template messages
- Average cost: $0.02 per message
- Monthly: $200

**100,000 messages/month**
- Mix of template + service + BizAI
- Average cost: $0.015 per message
- Monthly: $1,500

**1,000,000 messages/month**
- High volume (BizAI agent + templates)
- Average cost: $0.008 per message (volume discounts)
- Monthly: $8,000

## Cost Optimization Strategies

1. **Use templates whenever possible** — 5-10x cheaper than service messages
2. **Batch non-urgent updates** — Combine multiple updates into single message
3. **Optimize with BizAI agent** — Self-service reduces escalations and support costs
4. **Target by region** — Higher-value customers in lower-cost markets
5. **Manage marketing wisely** — Strict compliance with opt-in to avoid account penalties

## Quality Rating Impact

Your account's **quality rating** affects throughput and cost:

- **Green (Good)** — Normal rates, unlimited throughput
- **Yellow (Medium)** — Normal rates, throttled throughput (slower delivery)
- **Red (Poor)** — Possible rate increases, significant throttling, risk of ban

Quality is affected by:
- Customer complaint rate
- Message rejection rate
- Spam reports
- Filter violations

---

See also:
- [[meta-business-agent]] — Pricing for agent messages
- [[bizai-pricing]] — Gupshup's BizAI pricing
- [[whatsapp-api]] — How to send different message types
