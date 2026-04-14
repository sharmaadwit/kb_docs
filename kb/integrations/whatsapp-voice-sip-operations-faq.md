<!-- kb-golden:v1 -->
# WhatsApp Voice SIP — recordings, DTMF, checklist, and FAQ

**Module**: Integrations

## Call recording

- By default, **recording** is typically performed on the **customer dialer or recorder** infrastructure.
- **Gupshup** can alternatively perform recording and provide a **recording URL** to the customer (additional commercial arrangement).
- Each recording is correlated using the SIP **Call-ID** for that session.

## DTMF

- Gupshup supports **in-band DTMF**.
- DTMF is carried in the **RTP** media stream, **not** via **SIP INFO** messages.
- Example mapping from the integration guide: `rtpmap:101 telephone-event/48000` with `fmtp:101 0-15` (where that SDP is negotiated for the session).

## Integration checklist

Use this checklist to track progress (owners as in the Version 1.0 SIP integration guide).

| Step | Action | Owner |
|------|--------|--------|
| 1 | Provide WABA number for WhatsApp Voice enablement | Customer |
| 2 | Provide SIP endpoint for inbound calls | Customer |
| 3 | Gupshup provides SIP endpoint for outbound calls | Gupshup |
| 4 | Configure customer SIP endpoint for inbound calling | Gupshup |
| 5 | Configure Gupshup SIP endpoint for outbound calling | Customer |
| 6 | Whitelist IPs and domains in firewall | Customer |
| 7 | Open SIP (**5072**) and RTP (**30000–40000**) ports | Customer |
| 8 | Verify codec compatibility (Opus / G.711) | Both |
| 9 | Test inbound calling end-to-end | Both |
| 10 | Test outbound calling end-to-end | Both |
| 11 | Integrate Call Permissions API | Customer |
| 12 | Test outbound calling with permissions flow | Both |
| 13 | Sign off inbound calling | Customer |
| 14 | Sign off outbound calling | Customer |

## Frequently asked questions

### General

**Q: What is WhatsApp Voice calling?**  
A: End-users can place and receive **voice calls over WhatsApp**. Gupshup acts as a **SIP gateway** between WhatsApp infrastructure and your contact-centre dialer.

**Q: Which codecs are supported?**  
A: Primary **Opus/48000**. Fallback **G.711** (**PCMA/8000**, **PCMU/8000**).

**Q: Are WhatsApp Voice calls regulated by TRAI (India)?**  
A: Per the customer guide, WhatsApp calls are **not** under TRAI guidelines as stated there; WhatsApp calls **cannot be intermixed with PSTN** calls.

**Q: What if someone places a PSTN call to the WABA number?**  
A: The telco treats it as a normal PSTN call; it terminates per your PSTN configuration, not as a WhatsApp Voice SIP leg.

**Q: Are there limits on concurrent calls?**  
A: Yes — **CPS** and **concurrent** limits apply. Contact **Gupshup** for limits for your WABA.

### SIP and network

**Q: Which ports must be open?**  
A: SIP signalling **UDP 5072** (TCP 5072 optional); RTP **UDP 30000–40000**.

**Q: Which IPs and domains should be whitelisted (India)?**  
A: **35.154.159.246**, **13.248.195.10**, and **wavoicetls.knowlarity.com** (per the India table in the guide).

**Q: How does DTMF work?**  
A: **In-band** over RTP per **RFC 4733**, not standalone SIP INFO.

**Q: What if RTP ports are blocked?**  
A: Expect **one-way audio** or call termination with **cause=500** after timeout.

### TLS and security

**Q: Is TLS supported for SIP signalling?**  
A: TLS is used on the **upstream** leg; for the **customer-facing** trunk leg, discuss **TLS/SRTP** enablement with Gupshup.

**Q: Can SRTP be used?**  
A: Yes; recording over SRTP is described as supported. Configure with Gupshup.

### Call permissions

**Q: Must I check permission before every outbound call?**  
A: Not necessarily in real time; you may check in advance and cache in your CRM. Only call users who have granted permission.

**Q: What if I call without permission?**  
A: Expect **403 Forbidden** — **non-retryable** until permission is obtained.

**Q: Is there a batch permissions API?**  
A: **No** in the documented guide; checks are **per user**.

### Call transfer and routing

**Q: Can calls be transferred to external PSTN numbers?**  
A: WhatsApp calls **cannot** be intermixed with PSTN; external PSTN transfer is **not** supported in the standard documented flow.

**Q: Who handles routing?**  
A: Your **dialer**; use SIP headers from Gupshup for routing and desktop metadata.

### Recordings

**Q: Who records by default?**  
A: Typically the **customer** recorder; Gupshup recording with URL is optional/add-on.

**Q: How are recordings identified?**  
A: By the SIP **Call-ID**.
