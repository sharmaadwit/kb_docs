import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

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


def _append_line(path: str, line: str, context) -> None:
    try:
        import kb_storage
    except ImportError:
        import importlib, sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        kb_storage = importlib.import_module("kb_storage")
    try:
        existing = kb_storage.read_text(path, context=context) or ""
    except Exception:
        existing = ""
    new_content = (existing.rstrip("\n") + "\n" + line + "\n") if existing else (line + "\n")
    kb_storage.write_file(
        path, new_content,
        message=f"KB analytics: append usage log to {path}",
        context=context,
    )


def kb_analytics(event: str = "", payload: object = None, context=None) -> dict:
    """Append usage analytics to both rolling and daily NDJSON files via kb_storage."""
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    rolling_path = (context.get_secret("GITHUB_KB_USAGE_LOG_PATH") or "kb/analytics/kb_usage.ndjson")

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
            _append_line(path, line, context)
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
