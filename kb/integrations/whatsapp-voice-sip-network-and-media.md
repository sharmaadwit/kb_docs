<!-- kb-golden:v1 -->
# WhatsApp Voice SIP — network, firewall, and media

**Module**: Integrations

## Network and firewall configuration

Whitelist the following ports and addresses so SIP signalling and RTP media can flow between Gupshup and your dialer infrastructure.

### Ports

| Protocol | Port(s) | Transport | Purpose |
|----------|---------|-----------|---------|
| SIP signalling | **5072** | UDP (primary), TCP (optional) | Call setup and teardown |
| RTP media | **30000–40000** | UDP | Audio streams |

### IP and domain whitelist (India)

The integration guide documents the following for the **India** region:

| Type | Value |
|------|--------|
| IP address | `35.154.159.246` |
| IP address | `13.248.195.10` |
| Domain | `wavoicetls.knowlarity.com` |

### Important note

Allow **both outbound and inbound** traffic to and from these addresses. Blocking SIP or RTP traffic typically causes call failures or **one-way audio**.

If your deployment uses other regions, confirm the current IP and domain list with Gupshup support; this KB reflects the values published in the Version 1.0 customer SIP guide.

## Media and RTP requirements

### Codec and timing parameters

| Parameter | Value |
|-----------|--------|
| Primary codec | Opus/48000 (`rtpmap:102 opus/48000/2`) |
| Fallback codec | PCMA/8000 (G.711) |
| Packetization time | 20 ms |
| DTMF | `rtpmap:126 telephone-event/8000` (RFC 4733) |
| Opus `fmtp` | `maxaveragebitrate=20000; maxplaybackrate=16000; minptime=20; sprop-maxcapturerate=16000; useinbandfec=1` |

### Sample SDP (Opus)

The following example illustrates Opus and telephone-event lines as shown in the SIP integration guide:

```
m=audio 34804 RTP/AVP 102 101
a=rtpmap:102 opus/48000/2
a=fmtp:102 useinbandfec=1; maxaveragebitrate=20000;
maxplaybackrate=16000; sprop-maxcapturerate=16000;
ptime=20; minptime=10; maxptime=40
a=rtpmap:101 telephone-event/48000
a=fmtp:101 0-15
a=ptime:20
```

## Validation and troubleshooting (network and media)

- If callers report **one-way audio** or calls drop after connect, verify RTP **UDP 30000–40000** is open in both directions and that NAT or firewall rules are not rewriting ports incorrectly.
- For **no audio** or immediate teardown with media-related cause codes, confirm **Opus** (or agreed fallback **G.711**) matches on both legs and that SDP matches the documented parameters where applicable.
