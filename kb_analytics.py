import base64
import json
from datetime import datetime, timezone
from typing import Dict, List

import requests


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
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text}")
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
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text}")

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

    line = json.dumps({"ts": now_iso, "event": event, "payload": payload}, ensure_ascii=False)

    written: List[str] = []
    errors: List[str] = []
    for path in [rolling_path, daily_path]:
        try:
            _append_line(owner, repo, branch, path, line, context)
            written.append(path)
        except Exception as e:
            errors.append(f"{path}: {str(e)}")

    return {
        "ok": len(written) > 0,
        "written_paths": written,
        "daily_path": daily_path,
        "rolling_path": rolling_path,
        "errors": errors,
    }
