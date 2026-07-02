import base64
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.parse import quote as _kb_quote

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


# --- Inline provider-agnostic git storage (GitHub/GitLab) ---
# Self-contained: the skill sandbox forbids importing sibling modules.
def _kb_secret(context, name):
    if context is None:
        return None
    try:
        v = context.get_secret(name)
    except Exception:
        return None
    if v is None:
        return None
    t = str(v).strip()
    return t or None


def _kb_cfg(context):
    provider = (_kb_secret(context, "KB_GIT_PROVIDER") or "github").strip().lower()
    if provider not in ("github", "gitlab"):
        provider = "github"
    kb_repo = _kb_secret(context, "KB_REPO")
    owner = repo = project = ""
    if provider == "github":
        if kb_repo and "/" in kb_repo:
            owner, repo = kb_repo.split("/", 1)
        else:
            owner = _kb_secret(context, "GITHUB_OWNER") or ""
            repo = _kb_secret(context, "GITHUB_REPO") or ""
        project = ("%s/%s" % (owner, repo)) if owner and repo else ""
    else:
        project = kb_repo or ""
    branch = _kb_secret(context, "KB_BRANCH") or _kb_secret(context, "GITHUB_BRANCH") or "main"
    token = _kb_secret(context, "KB_TOKEN") or _kb_secret(context, "GITHUB_TOKEN") or ""
    host = (_kb_secret(context, "KB_GITLAB_HOST") or "https://gitlab.com").rstrip("/")
    return {"provider": provider, "owner": owner, "repo": repo,
            "project": project, "branch": branch, "token": token, "host": host}


def _kb_gl_proj(project):
    return project if project.isdigit() else _kb_quote(project, safe="")


def _kb_read_text(path, context):
    cfg = _kb_cfg(context)
    if cfg["provider"] == "github":
        url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (
            cfg["owner"], cfg["repo"], cfg["branch"], path)
        headers = {"Accept": "application/vnd.github+json"}
        if cfg["token"]:
            headers["Authorization"] = "Bearer " + cfg["token"]
    else:
        url = "%s/api/v4/projects/%s/repository/files/%s/raw?ref=%s" % (
            cfg["host"], _kb_gl_proj(cfg["project"]), _kb_quote(path, safe=""), cfg["branch"])
        headers = {"Accept": "application/json"}
        if cfg["token"]:
            headers["PRIVATE-TOKEN"] = cfg["token"]
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def _kb_write_file(path, content, message, context):
    cfg = _kb_cfg(context)
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    if cfg["provider"] == "github":
        base = "https://api.github.com/repos/%s/%s/contents/%s" % (
            cfg["owner"], cfg["repo"], path)
        h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if cfg["token"]:
            h["Authorization"] = "Bearer " + cfg["token"]
        sha = ""
        rg = requests.get(base, headers=h, params={"ref": cfg["branch"]}, timeout=30)
        if rg.status_code == 200:
            sha = (rg.json() or {}).get("sha", "")
        payload = {"message": message, "content": encoded, "branch": cfg["branch"]}
        if sha:
            payload["sha"] = sha
        r = requests.put(base, headers=h, data=json.dumps(payload), timeout=30)
        r.raise_for_status()
        return
    enc = _kb_gl_proj(cfg["project"])
    url = "%s/api/v4/projects/%s/repository/files/%s" % (
        cfg["host"], enc, _kb_quote(path, safe=""))
    h = {"Accept": "application/json"}
    if cfg["token"]:
        h["PRIVATE-TOKEN"] = cfg["token"]
    body = {"branch": cfg["branch"], "content": encoded,
            "encoding": "base64", "commit_message": message}
    r = requests.post(url, headers=h, json=body, timeout=30)
    if r.status_code == 400 and "already exists" in r.text.lower():
        r = requests.put(url, headers=h, json=body, timeout=30)
    r.raise_for_status()


def _append_line(path: str, line: str, context) -> None:
    try:
        existing = _kb_read_text(path, context) or ""
    except Exception:
        existing = ""
    new_content = (existing.rstrip("\n") + "\n" + line + "\n") if existing else (line + "\n")
    _kb_write_file(path, new_content, f"KB analytics: append usage log to {path}", context)


def kb_analytics(event: str = "", payload: object = None, context=None) -> dict:
    """Append usage analytics to both rolling and daily NDJSON files in the git repo."""
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
