# DemoForge API Reference — Integration Guide

**Tested:** 2026-07-01 | **Base URL:** `https://demoforge-api.gupshup.io` | **Auth:** Bearer PAT

---

## Summary

| Endpoint | Method | Latency | Status | Response |
|----------|--------|---------|--------|----------|
| `/projects` | GET | 0.13s | 200 | `list[Project]` |
| `/projects/{project_id}/demos` | GET | 0.15–0.5s | 200 | `list[Demo]` |
| `/demos/{demo_id}/share` | POST | 0.11–0.22s | 200 | `Demo` (full object) |

---

## Error Handling Matrix

All errors return `{"detail": "<message>"}`.

| Scenario | HTTP | Detail | Retry? | Action |
|----------|------|--------|--------|--------|
| Invalid/revoked PAT | 401 | `Invalid or revoked personal access token` | ❌ | Fail fast; alert config |
| Missing auth header | 401 | `Authentication required` | ❌ | Fail fast |
| Project not found | 404 | `Project not found` | ❌ | Return None, fallback to YouTube |
| Demo not found | 404 | `Demo not found` | ❌ | Return None, fallback to YouTube |
| Invalid project ID format | 400 | `Invalid project ID` | ❌ | Validate before calling; don't retry |
| Invalid demo ID format | 400 | `Invalid demo ID` | ❌ | Validate before calling; don't retry |
| GET on /share endpoint | 405 | Method not allowed | ❌ | Use POST only |
| Server error | 5xx | — | ✅ | Retry (max 2, exponential backoff) |
| Rate limit | 429 | — | ✅ | Retry with backoff |
| Network timeout | — | — | ✅ | Retry (max 2, exponential backoff) |

**Retry Strategy:** Only on 429, 5xx, and network timeouts. Max 2 retries with exponential backoff (250ms → 1s).

---

## JSON Schemas

### GET /projects → `list[Project]`

```json
{
  "id": "6a213c233808c27de0c875f1",           // string: 24-hex ObjectId
  "user_id": "...",                           // string: ObjectId
  "name": "GS Demo",                          // string: required
  "description": "Sales demos for Gupshup",   // string: required
  "kind": "standard",                         // enum: "standard" | "video_only"
  "demo_count": 8,                            // integer: >= 0
  "members": [
    {
      "user_id": "...",
      "role": "owner",
      "added_at": "2026-01-15T10:30:00"
    }
  ],
  "created_at": "2026-01-01T00:00:00",        // ISO-8601 (no TZ suffix, µs precision)
  "updated_at": "2026-07-01T12:45:30"
}
```

---

### GET /projects/{project_id}/demos → `list[Demo]`

Each demo is a 34-key object. Critical fields for kb_answer.py:

```json
{
  "id": "6a4402a6f14e94517beb8474",          // string: 24-hex ObjectId; required
  "project_id": "6a213c233808c27de0c875f1",  // string: ObjectId; required
  "user_id": "...",
  "name": "Campaign Manager Demo",            // string; required
  "use_case": "Campaign Creation & Analytics",// string; nullable
  "industry": "Retail",                       // string; nullable
  "persona": "Marketing Manager",             // string; nullable
  "capabilities": "...",                      // string: long text (~400 chars); nullable
  "technical_level": "Non-technical",         // string; nullable
  "mode": "VIDEO",                            // enum: "VIDEO" | "NORMAL" | "DEEP" | "CODE"
  "status": "complete",                       // enum: "complete" | "partial" | "failed"
  "output": {
    // Shape varies by mode. For VIDEO:
    "objective": "...",
    "architecture": "...",         // Mermaid diagram
    "videoScript": "..."
    // For NORMAL:
    // "objective", "architecture", "sampleData", "narration", "demoSteps"
  },
  "raw_partial": null,                        // string (raw LLM JSON); present when partial
  "usage": {
    "input_tokens": 1200,
    "output_tokens": 800,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0
  },
  "cost_usd": 0.045,
  "outcome": null,                            // enum: "won" | "lost" | "in_progress" | null
  "tags": [],
  "starred": false,
  "share_token": "3deb4110-e216-4ef8-9082-d78c765ebc4a",  // UUIDv4; always present (pre-minted)
  "share_status": "active",                   // enum: "active" | null
  "test_share_token": null,
  "created_at": "2026-06-15T09:20:00",
  "updated_at": "2026-07-01T12:45:00",
  
  // Additional fields (less critical):
  "gitlab_url": null,
  "runtime_spec": null,
  "docs_context": null,
  "cloned_from": null,
  "competitor": null,
  "duration_range": "15-30",
  "health_score": null,
  "is_root_demo": false,
  "narration_voice": null,
  "runtime_render_mode": null,
  "ui_config": {
    "show_demo_runtime": true,
    "show_health_score": false,
    "show_present": true,
    "show_sharing": true,
    "show_analytics": true,
    "show_export": false
  }
}
```

**Key behaviors:**
- `share_token` is UUIDv4 and pre-minted (present even before POST /share)
- `share_status` is null until POST /share is called (then becomes "active")
- `status` must be "complete" to be shareable (filter out partial/failed)
- `mode` DEEP/CODE present in schema but not observed in live data — handle defensively
- `output` shape depends on `mode` — parse carefully

---

### POST /demos/{demo_id}/share → `Demo` (full object)

**Request:**
```
POST /demos/6a4402a6f14e94517beb8474/share
Authorization: Bearer pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI
```

**Response:** Returns the entire Demo object (same schema as GET /demos above).

**Key:** POST is **idempotent**. Calling twice on the same demo returns the same `share_token`. The real effect is setting `share_status = "active"`.

**Observed behavior:**
```
POST /demos/.../share (first call)
  → share_token: 3deb4110-e216-4ef8-9082-d78c765ebc4a
  → share_status: active
  → latency: 0.22s

POST /demos/.../share (second call, same demo)
  → share_token: 3deb4110-... (identical)
  → share_status: active
  → latency: 0.11s
```

---

## URL Construction

**⚠️ Placeholder — Confirm with DemoForge team:**

```python
SHARE_VIEWER_BASE = "https://demoforge.gupshup.io/share"  # or /s, or /demo/share — UNCONFIRMED
share_url = f"{SHARE_VIEWER_BASE}/{share_token}"
# Likely: https://demoforge.gupshup.io/share/3deb4110-e216-4ef8-9082-d78c765ebc4a
```

---

## Code Snippets (Production-Ready)

### Authentication

```python
import httpx
from typing import Optional

DEMOFORGE_BASE = "https://demoforge-api.gupshup.io"
DEMOFORGE_TIMEOUT = httpx.Timeout(5.0, connect=3.0)  # generous; observed <0.5s

def _headers(pat: str) -> dict:
    """Return auth headers."""
    return {"Authorization": f"Bearer {pat}"}
```

### List Projects

```python
async def list_projects(
    client: httpx.AsyncClient,
    pat: str
) -> list[dict] | None:
    """
    List all projects accessible to the PAT's user.
    
    Returns:
        list of project dicts, or None on error.
    """
    try:
        r = await client.get(
            f"{DEMOFORGE_BASE}/projects",
            headers=_headers(pat),
            timeout=DEMOFORGE_TIMEOUT
        )
        if r.status_code == 401:
            # PAT invalid/revoked
            return None
        r.raise_for_status()
        return r.json()
    except httpx.TimeoutException:
        return None
    except Exception:
        return None
```

### List Demos in Project

```python
async def list_project_demos(
    client: httpx.AsyncClient,
    pat: str,
    project_id: str
) -> list[dict] | None:
    """
    List all demos in a project. Filter to status='complete' client-side.
    
    Returns:
        list of demo dicts, or None on error.
    """
    try:
        r = await client.get(
            f"{DEMOFORGE_BASE}/projects/{project_id}/demos",
            headers=_headers(pat),
            timeout=DEMOFORGE_TIMEOUT
        )
        if r.status_code == 401:
            return None  # Auth failed
        if r.status_code == 404:
            return []    # Project not found
        r.raise_for_status()
        return r.json()
    except httpx.TimeoutException:
        return None
    except Exception:
        return None
```

### Share a Demo (Mint Share Link)

```python
async def share_demo(
    client: httpx.AsyncClient,
    pat: str,
    demo_id: str,
    max_retries: int = 2
) -> dict | None:
    """
    Mint (or fetch) a share token for a demo. Idempotent.
    
    Returns:
        {
            "share_token": "3deb4110-...",
            "share_status": "active",
            "share_url": "https://demoforge.gupshup.io/share/3deb4110-..."
        }
        or None on error.
    """
    retry_count = 0
    backoff_ms = 250
    
    while retry_count <= max_retries:
        try:
            r = await client.post(
                f"{DEMOFORGE_BASE}/demos/{demo_id}/share",
                headers=_headers(pat),
                timeout=DEMOFORGE_TIMEOUT
            )
            
            if r.status_code == 401:
                # Auth failed — do not retry
                return None
            
            if r.status_code == 404:
                # Demo not found — do not retry
                return None
            
            if r.status_code == 400:
                # Bad ID format — do not retry
                return None
            
            if r.status_code >= 500:
                # Server error — retry
                if retry_count < max_retries:
                    await asyncio.sleep(backoff_ms / 1000)
                    backoff_ms *= 4
                    retry_count += 1
                    continue
                return None
            
            r.raise_for_status()
            demo = r.json()
            
            return {
                "share_token": demo["share_token"],
                "share_status": demo.get("share_status"),
                "share_url": f"https://demoforge.gupshup.io/share/{demo['share_token']}"
            }
        
        except httpx.TimeoutException:
            if retry_count < max_retries:
                await asyncio.sleep(backoff_ms / 1000)
                backoff_ms *= 4
                retry_count += 1
                continue
            return None
        
        except Exception:
            return None
    
    return None
```

### Demo Selection Helper

```python
def select_best_complete_demo(
    demos: list[dict],
    industry_preference: str | None = None
) -> dict | None:
    """
    Filter to complete demos; optionally prefer by industry.
    
    Returns:
        First complete demo, or None.
    """
    complete = [d for d in demos if d.get("status") == "complete"]
    if not complete:
        return None
    
    if industry_preference:
        by_industry = [d for d in complete if d.get("industry") == industry_preference]
        if by_industry:
            return by_industry[0]
    
    return complete[0]
```

---

## Integration Checklist for kb_answer.py

- [ ] Load PAT from env/secrets (never hardcode)
- [ ] Create persistent httpx.AsyncClient (reuse across calls)
- [ ] Set timeout: 5s total, 3s connect (ample headroom)
- [ ] Validate demo_id/project_id as 24-hex before calling (avoid 400s)
- [ ] Filter demos to `status == "complete"` before surfacing
- [ ] Only call POST /share when `share_status != "active"`
- [ ] Handle all 4xx as non-retriable (fail gracefully, fallback to YouTube)
- [ ] Retry only on 429/5xx with exponential backoff (max 2 retries)
- [ ] Parse defensively: nullable fields everywhere, `output` shape varies by mode
- [ ] Log all API calls (success + failure) for monitoring
- [ ] Telemetry: record demo_id, share_token, api_latency, error (if any)
- [ ] **TODO: Confirm share URL path with DemoForge team** (currently `https://demoforge.gupshup.io/share/{token}`)

---

## Deployment Notes

**Environment variable:**
```bash
export DEMOFORGE_PAT="pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI"
```

**Load in kb_answer.py:**
```python
import os

demoforge_pat = os.getenv("DEMOFORGE_PAT")
if not demoforge_pat:
    raise RuntimeError("DEMOFORGE_PAT environment variable not set")
```

**For CI/CD:** Store PAT as a GitHub secret (Gupshup repo settings) and pass during deployment.

---

## Testing with Real API

**Test project:** "GS Demo" (id: `6a213c233808c27de0c875f1`)  
**Test demo:** "Campaign Manager Demo" (id: `6a4402a6f14e94517beb8474`, mode: VIDEO, status: complete)

Quick curl test:
```bash
PAT="pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI"
curl -s https://demoforge-api.gupshup.io/projects \
  -H "Authorization: Bearer $PAT" | jq .
```

---

## Known Unknowns

- [ ] **Share URL path** — assumed `https://demoforge.gupshup.io/share/{token}`, needs confirmation
- [ ] Rate limits — not documented or observed; keep retries conservative
- [ ] Modes DEEP/CODE — present in schema, not observed in live data; handle defensively
- [ ] Demo status "failed" — present in plan, not observed; filter it out with "complete" check

