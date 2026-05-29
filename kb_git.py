"""GitLab repository access for Product KB skills."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests

DEFAULT_GITLAB_BASE_URL = "https://gitlab.gupshup.io"
DEFAULT_GITLAB_PROJECT = "gs/ce/applications/AI/gupshup_guide"
DEFAULT_BRANCH = "main"
DEFAULT_DOCS_PATH = "kb"

_SECRET_ALIASES = {
    "token": ("GITLAB_TOKEN", "GITHUB_TOKEN"),
    "project": ("GITLAB_PROJECT", "GITHUB_PROJECT"),
    "branch": ("GITLAB_BRANCH", "GITHUB_BRANCH"),
    "base_url": ("GITLAB_BASE_URL",),
    "docs_path": ("GITLAB_DOCS_PATH", "GITHUB_DOCS_PATH"),
    "chunks_path": ("GITLAB_KB_CHUNKS_PATH", "GITHUB_KB_CHUNKS_PATH"),
    "index_path": ("GITLAB_KB_INDEX_PATH", "GITHUB_KB_INDEX_PATH"),
    "usage_log_path": ("GITLAB_KB_USAGE_LOG_PATH", "GITHUB_KB_USAGE_LOG_PATH"),
    "owner": ("GITLAB_OWNER", "GITHUB_OWNER"),
    "repo": ("GITLAB_REPO", "GITHUB_REPO"),
}


def _secret(context, key: str, default: Optional[str] = None) -> Optional[str]:
    if not context:
        return default
    for name in _SECRET_ALIASES.get(key, ()):
        val = context.get_secret(name)
        if val:
            return str(val).strip()
    return default


def _project_path(context) -> str:
    project = _secret(context, "project")
    if project:
        return project.strip("/")
    owner = _secret(context, "owner")
    repo = _secret(context, "repo")
    if owner and repo:
        return f"{owner.strip('/')}/{repo.strip('/')}"
    return DEFAULT_GITLAB_PROJECT


def repo_cfg(context, *, include_docs: bool = True) -> Dict[str, str]:
    docs_root = (_secret(context, "docs_path") or DEFAULT_DOCS_PATH).strip("/")
    cfg = {
        "base_url": (_secret(context, "base_url") or DEFAULT_GITLAB_BASE_URL).rstrip("/"),
        "project": _project_path(context),
        "branch": _secret(context, "branch") or DEFAULT_BRANCH,
        "docs_path": docs_root,
        "chunks_path": _secret(context, "chunks_path") or f"{docs_root}/kb_chunks.jsonl",
    }
    if include_docs:
        cfg["index_path"] = _secret(context, "index_path") or f"{docs_root}/kb_index.json"
        cfg["usage_log_path"] = (
            _secret(context, "usage_log_path") or f"{docs_root}/analytics/kb_usage.ndjson"
        )
    return cfg


def _encoded_project(project: str) -> str:
    return quote(project, safe="")


def _api_base(cfg: Dict[str, str]) -> str:
    return f"{cfg['base_url']}/api/v4/projects/{_encoded_project(cfg['project'])}"


def gitlab_headers(context, user_agent: str = "superagent-product-kb") -> Dict[str, str]:
    token = _secret(context, "token")
    if not token:
        raise RuntimeError("KB repo configuration or GitLab token is missing")
    return {
        "PRIVATE-TOKEN": token,
        "Accept": "application/json",
        "User-Agent": user_agent,
    }


def raw_file_url(cfg: Dict[str, str], path_in_repo: str) -> str:
    path = path_in_repo.strip("/")
    return (
        f"{cfg['base_url']}/{cfg['project']}/-/raw/{cfg['branch']}/{path}"
    )


def fetch_raw_text(
    context,
    path_in_repo: str,
    *,
    cfg: Optional[Dict[str, str]] = None,
    timeout: int = 60,
    user_agent: str = "superagent-product-kb",
    max_bytes: Optional[int] = None,
) -> str:
    cfg = cfg or repo_cfg(context)
    url = raw_file_url(cfg, path_in_repo)
    r = requests.get(url, headers=gitlab_headers(context, user_agent), timeout=timeout)
    if r.status_code >= 400:
        raise RuntimeError("Could not load knowledge base content")
    data = r.content
    if max_bytes is not None and len(data) > max_bytes:
        raise RuntimeError("Document exceeds maximum size for ingestion")
    return data.decode("utf-8", errors="replace")


def fetch_raw_jsonl(context, chunks_path: str, *, user_agent: str = "superagent-product-kb") -> List[Dict]:
    text = fetch_raw_text(context, chunks_path, user_agent=user_agent, timeout=30)
    items: List[Dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    return items


def _api_get(context, url: str, *, params: Optional[Dict] = None, user_agent: str = "superagent-product-kb") -> Any:
    r = requests.get(
        url,
        headers=gitlab_headers(context, user_agent),
        params=params or {},
        timeout=30,
    )
    if r.status_code >= 400:
        raise RuntimeError("GitLab API request failed")
    return r.json()


def _api_request(
    context,
    method: str,
    url: str,
    *,
    json_body: Optional[Dict] = None,
    user_agent: str = "superagent-product-kb",
) -> Any:
    r = requests.request(
        method,
        url,
        headers=gitlab_headers(context, user_agent),
        json=json_body,
        timeout=60,
    )
    if r.status_code >= 400:
        raise RuntimeError("GitLab API request failed")
    if r.status_code == 204 or not r.content:
        return {}
    return r.json()


def list_md_files(
    context,
    docs_path: str,
    *,
    cfg: Optional[Dict[str, str]] = None,
    exclude_prefixes: Optional[List[str]] = None,
    user_agent: str = "superagent-product-kb-ingest",
) -> List[str]:
    cfg = cfg or repo_cfg(context)
    exclude_prefixes = exclude_prefixes or []
    api = _api_base(cfg)
    out: List[str] = []
    page = 1
    per_page = 100
    root = docs_path.strip("/")

    while True:
        params = {
            "path": root,
            "ref": cfg["branch"],
            "recursive": "true",
            "per_page": per_page,
            "page": page,
        }
        batch = _api_get(context, f"{api}/repository/tree", params=params, user_agent=user_agent)
        if not isinstance(batch, list) or not batch:
            break
        for item in batch:
            path = str(item.get("path") or "")
            if item.get("type") != "blob" or not path.lower().endswith(".md"):
                continue
            if any(path.startswith(p.rstrip("/")) for p in exclude_prefixes):
                continue
            if path.startswith("kb/analytics"):
                continue
            out.append(path)
        if len(batch) < per_page:
            break
        page += 1

    return sorted(set(out))


def read_file_text(
    context,
    path_in_repo: str,
    *,
    cfg: Optional[Dict[str, str]] = None,
    user_agent: str = "superagent-product-kb",
) -> Optional[str]:
    """Return file text, or None if missing."""
    cfg = cfg or repo_cfg(context)
    api = _api_base(cfg)
    encoded_path = quote(path_in_repo.strip("/"), safe="")
    url = f"{api}/repository/files/{encoded_path}/raw"
    r = requests.get(
        url,
        headers=gitlab_headers(context, user_agent),
        params={"ref": cfg["branch"]},
        timeout=30,
    )
    if r.status_code == 404:
        return None
    if r.status_code >= 400:
        raise RuntimeError("GitLab storage request failed")
    return r.content.decode("utf-8", errors="replace")


def write_file(
    context,
    path_in_repo: str,
    content: str,
    message: str,
    *,
    cfg: Optional[Dict[str, str]] = None,
    user_agent: str = "superagent-product-kb-ingest",
) -> None:
    cfg = cfg or repo_cfg(context)
    api = _api_base(cfg)
    encoded_path = quote(path_in_repo.strip("/"), safe="")
    url = f"{api}/repository/files/{encoded_path}"
    existing = read_file_text(context, path_in_repo, cfg=cfg, user_agent=user_agent)
    body = {
        "branch": cfg["branch"],
        "commit_message": message,
        "content": content,
    }
    method = "PUT" if existing is not None else "POST"
    _api_request(context, method, url, json_body=body, user_agent=user_agent)


def append_ndjson_line(
    context,
    path_in_repo: str,
    line: str,
    message: str,
    *,
    cfg: Optional[Dict[str, str]] = None,
    user_agent: str = "superagent-product-kb-analytics",
) -> None:
    existing = read_file_text(context, path_in_repo, cfg=cfg, user_agent=user_agent)
    if existing:
        new_content = existing.rstrip("\n") + "\n" + line + "\n"
    else:
        new_content = line + "\n"
    write_file(context, path_in_repo, new_content, message, cfg=cfg, user_agent=user_agent)


def require_repo_config(context) -> Dict[str, str]:
    cfg = repo_cfg(context)
    if not cfg.get("project") or not _secret(context, "token"):
        raise RuntimeError("KB repo configuration or GitLab token is missing")
    return cfg
