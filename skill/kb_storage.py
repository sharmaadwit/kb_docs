"""
Provider-agnostic KB content storage helpers.

Secrets used:
- KB_GIT_PROVIDER: "github" (default) or "gitlab"
- KB_REPO: repository identity
  - GitHub: "owner/repo"
  - GitLab: "group/project" or numeric project id
- KB_BRANCH: branch name (default: "main")
- KB_TOKEN: API token
- KB_GITLAB_HOST: GitLab host URL (default: "https://gitlab.com")

Legacy fallbacks:
- GITHUB_OWNER + GITHUB_REPO (used when KB_REPO is unset for GitHub)
- GITHUB_BRANCH
- GITHUB_TOKEN
"""

import base64
import json
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests


def _get_secret(context: Any, name: str) -> Optional[str]:
    if context is None:
        return None
    try:
        value = context.get_secret(name)
    except Exception:
        return None
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _resolve_config(context=None) -> Dict[str, str]:
    provider = (_get_secret(context, "KB_GIT_PROVIDER") or "github").strip().lower()
    if provider not in {"github", "gitlab"}:
        provider = "github"

    kb_repo = _get_secret(context, "KB_REPO")
    gh_owner = _get_secret(context, "GITHUB_OWNER")
    gh_repo = _get_secret(context, "GITHUB_REPO")

    owner = ""
    repo = ""
    project = ""
    if provider == "github":
        repo_spec = kb_repo or ""
        if repo_spec and "/" in repo_spec:
            owner, repo = repo_spec.split("/", 1)
        else:
            owner = gh_owner or ""
            repo = gh_repo or ""
        project = f"{owner}/{repo}" if owner and repo else ""
    else:
        project = kb_repo or ""

    branch = _get_secret(context, "KB_BRANCH") or _get_secret(context, "GITHUB_BRANCH") or "main"
    token = _get_secret(context, "KB_TOKEN") or _get_secret(context, "GITHUB_TOKEN") or ""
    gitlab_host = (_get_secret(context, "KB_GITLAB_HOST") or "https://gitlab.com").rstrip("/")

    return {
        "provider": provider,
        "branch": branch,
        "token": token,
        "owner": owner,
        "repo": repo,
        "project": project,
        "gitlab_host": gitlab_host,
    }


def _encode_gitlab_project(project: str) -> str:
    if project.isdigit():
        return project
    return quote(project, safe="")


def _github_raw_url(cfg: Dict[str, str], path: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{cfg['owner']}/{cfg['repo']}"
        f"/{cfg['branch']}/{path}"
    )


def _gitlab_raw_url(cfg: Dict[str, str], path: str) -> str:
    enc_project = _encode_gitlab_project(cfg["project"])
    enc_path = quote(path, safe="")
    return (
        f"{cfg['gitlab_host']}/api/v4/projects/{enc_project}/repository/files/{enc_path}"
        f"/raw?ref={cfg['branch']}"
    )


def _github_contents_api_url(cfg: Dict[str, str], path: str) -> str:
    return f"https://api.github.com/repos/{cfg['owner']}/{cfg['repo']}/contents/{path}"


def _gitlab_file_api_url(cfg: Dict[str, str], path: str) -> str:
    enc_project = _encode_gitlab_project(cfg["project"])
    enc_path = quote(path, safe="")
    return f"{cfg['gitlab_host']}/api/v4/projects/{enc_project}/repository/files/{enc_path}"


def _github_headers(token: str = "") -> Dict[str, str]:
    headers: Dict[str, str] = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _github_write_headers(token: str = "") -> Dict[str, str]:
    headers = _github_headers(token)
    headers["X-GitHub-Api-Version"] = "2022-11-28"
    return headers


def _gitlab_headers(token: str = "") -> Dict[str, str]:
    headers: Dict[str, str] = {"Accept": "application/json"}
    if token:
        headers["PRIVATE-TOKEN"] = token
    return headers


def _parse_json_response(resp: requests.Response) -> Dict[str, Any]:
    try:
        data = resp.json()
    except Exception:
        data = None
    if isinstance(data, dict):
        return data
    return {"ok": True}


def read_text(path: str, context=None) -> str:
    cfg = _resolve_config(context)
    provider = cfg["provider"]
    if provider == "github":
        url = _github_raw_url(cfg, path)
        headers = _github_headers(cfg["token"])
    elif provider == "gitlab":
        url = _gitlab_raw_url(cfg, path)
        headers = _gitlab_headers(cfg["token"])
    else:
        raise RuntimeError(f"Unsupported git provider: {provider}")

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        raise RuntimeError(f"Could not read file from {provider}: {path}") from exc

    if not resp.text:
        raise RuntimeError(f"Empty response while reading file from {provider}: {path}")
    return resp.text


def read_json(path: str, context=None) -> Any:
    try:
        return json.loads(read_text(path, context=context))
    except Exception as exc:
        raise RuntimeError(f"Could not parse JSON file: {path}") from exc


def read_jsonl(path: str, context=None) -> List[Dict]:
    raw = read_text(path, context=context)
    rows: List[Dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:
            raise RuntimeError(f"Could not parse JSONL file: {path}") from exc
        if not isinstance(obj, dict):
            raise RuntimeError(f"JSONL line is not an object in file: {path}")
        rows.append(obj)
    return rows


def _github_get_sha(cfg: Dict[str, str], path: str) -> str:
    url = _github_contents_api_url(cfg, path)
    resp = requests.get(
        url,
        headers=_github_headers(cfg["token"]),
        params={"ref": cfg["branch"]},
        timeout=30,
    )
    if resp.status_code == 404:
        return ""
    resp.raise_for_status()
    data = _parse_json_response(resp)
    sha = data.get("sha")
    return sha if isinstance(sha, str) else ""


def _gitlab_file_exists_error(resp: requests.Response) -> bool:
    if resp.status_code != 400:
        return False
    text_parts: List[str] = [resp.text.lower()]
    try:
        body = resp.json()
    except Exception:
        body = None
    if isinstance(body, dict):
        for value in body.values():
            text_parts.append(str(value).lower())
    joined = " ".join(text_parts)
    return "already exists" in joined


def write_file(path: str, content: str, message: str, context=None) -> Dict:
    cfg = _resolve_config(context)
    provider = cfg["provider"]
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    if provider == "github":
        try:
            sha = _github_get_sha(cfg, path)
            payload: Dict[str, Any] = {
                "message": message,
                "content": encoded,
                "branch": cfg["branch"],
            }
            if sha:
                payload["sha"] = sha
            resp = requests.put(
                _github_contents_api_url(cfg, path),
                headers=_github_write_headers(cfg["token"]),
                data=json.dumps(payload),
                timeout=30,
            )
            resp.raise_for_status()
        except Exception as exc:
            raise RuntimeError(f"Could not write file to github: {path}") from exc
        data = _parse_json_response(resp)
        return data if data else {"ok": True, "provider": provider, "path": path}

    if provider == "gitlab":
        body = {
            "branch": cfg["branch"],
            "content": encoded,
            "encoding": "base64",
            "commit_message": message,
        }
        url = _gitlab_file_api_url(cfg, path)
        headers = _gitlab_headers(cfg["token"])
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=30)
            if _gitlab_file_exists_error(resp):
                resp = requests.put(url, headers=headers, json=body, timeout=30)
            resp.raise_for_status()
        except Exception as exc:
            raise RuntimeError(f"Could not write file to gitlab: {path}") from exc
        data = _parse_json_response(resp)
        return data if data else {"ok": True, "provider": provider, "path": path}

    raise RuntimeError(f"Unsupported git provider: {provider}")



def list_directory(path: str, context=None) -> List[Dict]:
    """List files and subdirectories at path. Returns list of {type, path, name} dicts."""
    cfg = _resolve_config(context)
    provider = cfg["provider"]

    if provider == "github":
        url = _github_contents_api_url(cfg, path)
        try:
            resp = requests.get(
                url,
                headers=_github_headers(cfg["token"]),
                params={"ref": cfg["branch"]},
                timeout=30,
            )
            resp.raise_for_status()
        except Exception as exc:
            raise RuntimeError(f"Could not list directory from github: {path}") from exc
        items = resp.json()
        if not isinstance(items, list):
            return []
        return [
            {"type": item.get("type"), "path": item.get("path"), "name": item.get("name")}
            for item in items
        ]

    if provider == "gitlab":
        enc_project = _encode_gitlab_project(cfg["project"])
        try:
            resp = requests.get(
                f"{cfg['gitlab_host']}/api/v4/projects/{enc_project}/repository/tree",
                headers=_gitlab_headers(cfg["token"]),
                params={"path": path, "ref": cfg["branch"], "per_page": 100},
                timeout=30,
            )
            resp.raise_for_status()
        except Exception as exc:
            raise RuntimeError(f"Could not list directory from gitlab: {path}") from exc
        items = resp.json()
        if not isinstance(items, list):
            return []
        return [
            {
                "type": "dir" if item.get("type") == "tree" else "file",
                "path": f"{path}/{item['name']}" if path else item["name"],
                "name": item.get("name"),
            }
            for item in items
        ]

    raise RuntimeError(f"Unsupported git provider: {provider}")
