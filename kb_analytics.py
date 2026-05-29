import base64
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

_MAX_STR = 2000
_MAX_LIST = 50
_MAX_DICT_KEYS = 40
_MAX_DEPTH = 8
_REDACT_KEY_FRAGMENTS = (
    "secret",
    "token",
    "password",
    "authorization",
    "api_key",
    "apikey",
    "cookie",
    "session",
    "langfuse",
    "trace",
    "credential",
    "bearer",
)


def _normalize_event_name(event: str) -> str:
    s = (event or "").strip()[:128]
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", s) or "event"


def _redact_key(key: str) -> bool:
    low = (key or "").lower()
    return any(frag in low for frag in _REDACT_KEY_FRAGMENTS)


def _sanitize_payload(value: Any, depth: int = 0) -> Any:
    if depth > _MAX_DEPTH:
        return "[truncated-depth]"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        s = value.replace("\x00", "")
        if len(s) > _MAX_STR:
            return s[: _MAX_STR] + "…"
        return s
    if isinstance(value, bytes):
        return "[binary-redacted]"
    if isinstance(value, list):
        out: List[Any] = []
        for i, item in enumerate(value[:_MAX_LIST]):
            out.append(_sanitize_payload(item, depth + 1))
        if len(value) > _MAX_LIST:
            out.append(f"[{len(value) - _MAX_LIST} more items omitted]")
        return out
    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        keys = list(value.keys())[:_MAX_DICT_KEYS]
        for k in keys:
            sk = str(k)
            if _redact_key(sk):
                out[sk] = "[REDACTED]"
            else:
                out[sk] = _sanitize_payload(value[k], depth + 1)
        if len(value) > _MAX_DICT_KEYS:
            out["_truncated_keys"] = len(value) - _MAX_DICT_KEYS
        return out
    return str(value)[:_MAX_STR]


def _gh_headers(context) -> Dict[str, str]:
    token = context.get_secret("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GitHub configuration secrets")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _gh_put(url: str, context, payload: Dict):
    r = requests.put(url, headers=_gh_headers(context), data=json.dumps(payload), timeout=30)
    if r.status_code >= 400:
        raise RuntimeError("GitHub storage request failed")
    return r


def _append_line(owner: str, repo: str, branch: str, path: str, line: str, context) -> None:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=_gh_headers(context), params={"ref": branch}, timeout=30)

    sha = ""
    existing = ""
    if r.status_code == 200:
        j = r.json()
        sha = j.get("sha", "")
        if j.get("encoding") == "base64" and j.get("content"):
            existing = base64.b64decode(j["content"]).decode("utf-8", errors="replace")
    elif r.status_code != 404:
        raise RuntimeError("GitHub storage request failed")

    new_content = (existing.rstrip("\n") + "\n" + line + "\n") if existing else (line + "\n")
    payload_put = {
        "message": f"KB analytics: append usage log to {path}",
        "content": base64.b64encode(new_content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload_put["sha"] = sha
    _gh_put(url, context, payload_put)


def kb_analytics(event: str = "", payload: object = None, context=None) -> dict:
    """Append usage analytics to both rolling and daily GitHub NDJSON files."""
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    owner = context.get_secret("GITHUB_OWNER")
    repo = context.get_secret("GITHUB_REPO")
    branch = context.get_secret("GITHUB_BRANCH") or "main"
    rolling_path = context.get_secret("GITHUB_KB_USAGE_LOG_PATH") or "kb/analytics/kb_usage.ndjson"

    if not owner or not repo:
        raise RuntimeError("Missing GitHub configuration secrets")

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    daily_path = f"kb/analytics/{now.strftime('%Y-%m-%d')}.ndjson"

    safe_event = _normalize_event_name(event)
    safe_payload = _sanitize_payload(payload)
    line = json.dumps({"ts": now_iso, "event": safe_event, "payload": safe_payload}, ensure_ascii=False)
    if len(line) > 120_000:
        line = json.dumps(
            {"ts": now_iso, "event": safe_event, "payload": "[record too large]"},
            ensure_ascii=False,
        )

    written: List[str] = []
    errors: List[str] = []
    for path in [rolling_path, daily_path]:
        try:
            _append_line(owner, repo, branch, path, line, context)
            written.append(path)
        except Exception:
            errors.append("append_failed")

    preview = safe_payload if isinstance(safe_payload, dict) else {"value": safe_payload}

    return {
        "ok": len(written) > 0,
        "sanitized": True,
        "redaction_applied": True,
        "stores_written": len(written),
        "sanitized_payload": preview,
        "errors": errors,
    }
