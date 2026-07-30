# DemoForge API Integration Implementation

## Overview

This document provides implementation details for integrating the DemoForge API with the KB answer pipeline. It covers API endpoints, error handling, and integration points in the skill code.

---

## API Credentials

```python
# Load from environment/context
DEMOFORGE_PAT = context.get_secret("DEMOFORGE_PAT")
DEMOFORGE_BASE_URL = context.get_secret("DEMOFORGE_BASE_URL") or "https://demoforge-api.gupshup.io"
DEMOFORGE_FRONTEND_URL = context.get_secret("DEMOFORGE_FRONTEND_URL") or "https://demoforge-ui.gupshup.io"
```

**Current values** (from `.env`):
- `DEMOFORGE_PAT`: `pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI`
- `DEMOFORGE_BASE_URL`: `https://demoforge-api.gupshup.io`
- `DEMOFORGE_FRONTEND_URL`: `https://demoforge-ui.gupshup.io`

---

## API Endpoints

### 1. Create Share Token

Generate a shareable link for a specific demo.

**Endpoint**:
```
POST /api/shares
```

**Request**:
```json
{
  "demo_id": "6a4402a6f14e94517beb8474",
  "expires_in_days": 7,
  "metadata": {
    "source": "kb_answer",
    "query": "How do I create a campaign?",
    "user_query_id": "user_session_123"
  }
}
```

**Response** (200 OK):
```json
{
  "share_token": "share_abc123def456ghi789",
  "share_url": "https://demoforge-ui.gupshup.io/s/share_abc123def456ghi789",
  "demo_id": "6a4402a6f14e94517beb8474",
  "created_at": "2026-07-02T10:30:00Z",
  "expires_at": "2026-07-09T10:30:00Z"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "invalid_demo_id",
  "message": "Demo 6a4402a6f14e94517beb8474 not found",
  "trace_id": "req_12345"
}
```

**Possible Errors**:
- `400` - `invalid_demo_id`: Demo ID doesn't exist or is inactive
- `401` - `unauthorized`: Invalid or expired DEMOFORGE_PAT
- `429` - `rate_limited`: Too many requests (fallback to YouTube)
- `500` - `internal_error`: Server error (fallback to YouTube)
- `503` - `service_unavailable`: API maintenance (fallback to YouTube)

---

### 2. Get Share Info

Retrieve metadata about an existing share (for analytics/validation).

**Endpoint**:
```
GET /api/shares/{share_token}
```

**Response** (200 OK):
```json
{
  "share_token": "share_abc123def456ghi789",
  "demo_id": "6a4402a6f14e94517beb8474",
  "created_at": "2026-07-02T10:30:00Z",
  "expires_at": "2026-07-09T10:30:00Z",
  "clicks": 3,
  "unique_viewers": 2,
  "metadata": {
    "source": "kb_answer",
    "query": "How do I create a campaign?"
  }
}
```

---

### 3. Get Demo Info

Retrieve demo metadata by ID.

**Endpoint**:
```
GET /api/demos/{demo_id}
```

**Response** (200 OK):
```json
{
  "id": "6a4402a6f14e94517beb8474",
  "name": "Campaign Manager Demo",
  "description": "Send bulk campaigns with personalization",
  "project": "GS Demo",
  "industry": "Banking",
  "persona": "Head of Marketing",
  "use_case": "Send the same offer or update to many recipients at once, with personalized content.",
  "status": "complete",
  "duration_minutes": 8,
  "created_at": "2024-01-15T00:00:00Z",
  "updated_at": "2026-06-20T12:00:00Z"
}
```

---

## Python Implementation

### Module: `demoforge_api.py`

Create a new module to handle DemoForge API interactions:

```python
import logging
import requests
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_credentials(context):
    """Extract DemoForge credentials from context."""
    pat = None
    base_url = None
    frontend_url = None
    
    if context:
        try:
            pat = context.get_secret("DEMOFORGE_PAT")
            base_url = context.get_secret("DEMOFORGE_BASE_URL")
            frontend_url = context.get_secret("DEMOFORGE_FRONTEND_URL")
        except Exception:
            pass
    
    base_url = base_url or "https://demoforge-api.gupshup.io"
    frontend_url = frontend_url or "https://demoforge-ui.gupshup.io"
    
    if not pat:
        return None, None, None
    
    return pat, base_url, frontend_url


def create_share_token(
    demo_id: str,
    context,
    query: str = None,
    expires_in_days: int = 7,
    timeout_sec: int = 5
) -> Optional[str]:
    """Create a shareable link for a demo.
    
    Args:
        demo_id: DemoForge demo ID
        context: Agent context (for secrets)
        query: Optional user query (for telemetry)
        expires_in_days: Share expiration (default 7 days)
        timeout_sec: API timeout (default 5 sec)
    
    Returns:
        Share token string, or None if API fails
    
    Example:
        >>> token = create_share_token("6a4402a6f14e94517beb8474", ctx)
        >>> if token:
        ...     url = f"https://demoforge-ui.gupshup.io/s/{token}"
    """
    try:
        pat, base_url, frontend_url = _get_credentials(context)
        if not pat:
            return None
        
        endpoint = f"{base_url}/api/shares"
        headers = {
            "Authorization": f"Bearer {pat}",
            "Content-Type": "application/json",
        }
        payload = {
            "demo_id": demo_id,
            "expires_in_days": expires_in_days,
        }
        if query:
            payload["metadata"] = {
                "source": "kb_answer",
                "query": query[:500],  # Truncate to prevent huge payloads
            }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=timeout_sec,
        )
        response.raise_for_status()
        
        data = response.json()
        share_token = data.get("share_token")
        
        if share_token:
            logger.info(f"DemoForge share token created: {demo_id} → {share_token[:20]}...")
            return share_token
        else:
            logger.warning(f"DemoForge API returned no token: {data}")
            return None
    
    except requests.exceptions.Timeout:
        logger.warning(f"DemoForge API timeout for demo {demo_id}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"DemoForge API connection error for demo {demo_id}")
        return None
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if hasattr(e, 'response') else 'unknown'
        logger.warning(f"DemoForge API error ({status}) for demo {demo_id}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error creating DemoForge share token: {e}")
        return None


def build_share_url(share_token: str, frontend_url: str = None) -> str:
    """Build the full DemoForge share URL.
    
    Args:
        share_token: Token returned by create_share_token()
        frontend_url: DemoForge UI base URL (default from env)
    
    Returns:
        Full shareable URL
    
    Example:
        >>> token = "share_abc123def456"
        >>> url = build_share_url(token)
        >>> print(url)
        https://demoforge-ui.gupshup.io/s/share_abc123def456
    """
    if not share_token:
        return None
    
    frontend_url = frontend_url or "https://demoforge-ui.gupshup.io"
    return f"{frontend_url}/s/{share_token}"


def get_share_info(share_token: str, context, timeout_sec: int = 5) -> Optional[dict]:
    """Retrieve metadata about an existing share (for analytics).
    
    Args:
        share_token: Share token from create_share_token()
        context: Agent context (for secrets)
        timeout_sec: API timeout
    
    Returns:
        Share metadata dict, or None if API fails
    """
    try:
        pat, base_url, _ = _get_credentials(context)
        if not pat:
            return None
        
        endpoint = f"{base_url}/api/shares/{share_token}"
        headers = {"Authorization": f"Bearer {pat}"}
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=timeout_sec,
        )
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        logger.debug(f"Failed to get share info for {share_token}: {e}")
        return None
```

---

## Integration with `kb_video.py`

Update the existing `select_demoforge_demo()` function to also return the share URL:

```python
def select_demoforge_demo_with_url(
    query: str,
    intent: str,
    module: str,
    context
) -> dict:
    """Select a DemoForge demo and create a shareable link.
    
    Returns a demo dict with 'share_url' populated via API.
    Falls back to None if demo not found or API fails.
    """
    import demoforge_api
    
    # Step 1: Select demo by intent+module
    demo = select_demoforge_demo(query, intent, module, context)
    if not demo:
        return None
    
    # Step 2: Get share token from API
    demo_id = demo.get("demo_id")
    share_token = demoforge_api.create_share_token(
        demo_id=demo_id,
        context=context,
        query=query,
        expires_in_days=7,
    )
    
    if not share_token:
        # API failed, fallback to YouTube
        logger.info(f"DemoForge API failed for {demo_id}, falling back to YouTube")
        return None
    
    # Step 3: Build full share URL
    share_url = demoforge_api.build_share_url(share_token)
    
    return {
        "type": "demoforge",
        "demo_id": demo_id,
        "name": demo.get("name"),
        "industry": demo.get("industry"),
        "persona": demo.get("persona"),
        "share_token": share_token,
        "share_url": share_url,
    }
```

---

## Integration with `kb_answer.py`

Update the answer generation to optionally attach a demo:

```python
# In kb_answer() function, after generating the answer:

# Check if this is a how-to query
if selected_answer_mode == "answered":
    # Detect intent and module from ranked results
    intent = _detect_intent(query, intents)  # "how_to", "overview", etc.
    module = explicit_module  # Already detected by search
    
    # Try to select a DemoForge demo
    try:
        demo = kb_video.select_demoforge_demo_with_url(
            query=query,
            intent=intent,
            module=module,
            context=context,
        )
        if demo:
            response["demo"] = demo
            # Add telemetry
            params["demo_selected"] = demo.get("name")
            params["demo_id"] = demo.get("demo_id")
            params["demo_share_url"] = demo.get("share_url")
    except Exception as e:
        # Swallow demo selection errors - they don't affect answer
        logger.debug(f"Demo selection failed (will fallback): {e}")
```

---

## Telemetry & Monitoring

### Langfuse Trace Fields

Add these fields to the telemetry capture:

```json
{
  "demo_selected": "campaign_manager",
  "demo_id": "6a4402a6f14e94517beb8474",
  "demo_share_url": "https://demoforge-ui.gupshup.io/s/share_abc123",
  "demo_fallback": false,
  "demo_api_latency_ms": 145,
  "demo_error": null
}
```

### Analytics Events

Track demo interactions:

```python
# kb_analytics module
kb_analytics(
    event="demo.offered",
    payload={
        "demo_id": "6a4402a6f14e94517beb8474",
        "demo_name": "Campaign Manager Demo",
        "share_token": "share_abc123def456",
        "query_topic": "campaigns",
        "intent": "how_to",
    },
    context=context,
)
```

---

## Error Handling & Fallback

```
Try DemoForge API (5 sec timeout)
    ├─ Success (200) → Return share_url
    ├─ 400 Bad Request → Log warning, fallback to YouTube
    ├─ 401 Unauthorized → Log error, check DEMOFORGE_PAT
    ├─ 429 Rate Limited → Log warning, fallback to YouTube
    ├─ 5xx Server Error → Log warning, fallback to YouTube
    └─ Timeout/Connection Error → Log warning, fallback to YouTube

Fallback: select_video() → YouTube, then return answer
```

---

## Testing Scenarios

### 1. Success Case
```
Query: "How do I create a campaign?"
Intent: how_to
Module: campaigns
Demo Selected: Campaign Manager (6a4402a6f14e94517beb8474)
API Call: POST /api/shares with demo_id
Response: share_token = "share_abc123..."
Share URL: https://demoforge-ui.gupshup.io/s/share_abc123...
Result: ✓ User gets interactive demo link
```

### 2. Demo Not Found
```
Query: "How do I set up webhooks?"
Intent: how_to
Module: webhooks
Demo Selected: None (unmapped)
Fallback: select_video() → YouTube or nothing
Result: ✓ Plain text answer (no error)
```

### 3. API Timeout
```
Query: "How do I create a campaign?"
Demo Selected: Campaign Manager (6a4402a6f14e94517beb8474)
API Call: Timeout after 5 seconds
Fallback: select_video() → YouTube
Result: ✓ User gets YouTube link instead (no crash)
```

### 4. API Returns 401
```
Query: "How do I create a campaign?"
Demo Selected: Campaign Manager
API Call: 401 Unauthorized
Action: Log error "Invalid DEMOFORGE_PAT"
Fallback: select_video() → YouTube
Note: Admin should check .env credentials
```

### 5. Broad Query with Fallback
```
Query: "Show me a demo of Gupshup"
Intent: overview (pitch)
Module: None (broad)
Demo Lookup: Check for broad_fallback in manifest
Selected: General Demo (if marked broad_fallback: true)
API Call: create_share_token for General Demo
Result: ✓ High-value demo for sales/presales
```

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| API latency | <500ms | Per create_share_token() call |
| Timeout | 5 sec max | No hanging requests |
| Fallback success | 100% | Never crash on API failure |
| Cache hit rate | TBD | Consider caching share tokens |
| Availability | 99.5% | Measured by DemoForge team |

---

## Debugging Checklist

If demos are not appearing:

1. **Check manifest**: Does `demoforge_manifest.json` have module_to_demos index?
   ```bash
   grep -c "module_to_demos" kb/demoforge_manifest.json
   ```

2. **Check credentials**: Is `DEMOFORGE_PAT` loaded?
   ```python
   print(context.get_secret("DEMOFORGE_PAT"))  # Should not be None
   ```

3. **Check API**: Can you curl the endpoint?
   ```bash
   curl -H "Authorization: Bearer $DEMOFORGE_PAT" \
     https://demoforge-api.gupshup.io/api/demos/6a4402a6f14e94517beb8474
   ```

4. **Check intent/module detection**: Are they extracted correctly?
   - Log `_detect_intent(query, intents)` output
   - Log `explicit_module` from search results

5. **Check fallback**: Are demos gracefully falling back to YouTube?
   - Search logs for "DemoForge API failed"
   - Check Langfuse for demo_selected field

---

## Reference URLs

- **DemoForge API Docs**: `https://demoforge-api.gupshup.io/docs`
- **DemoForge Frontend**: `https://demoforge-ui.gupshup.io`
- **Gupshup API Docs**: `https://docs.gupshup.io`
