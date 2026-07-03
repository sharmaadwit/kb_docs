import base64
from urllib.parse import quote

import requests


def _get_secret(context, name: str):
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


def _normalize_host(host: str) -> str:
    if not host:
        return ""
    host = host.strip()
    if not host.startswith(("http://", "https://")):
        host = f"https://{host}"
    return host.rstrip("/")


def _resolve_config(context):
    provider = (_get_secret(context, "KB_GIT_PROVIDER") or "gitlab").strip().lower()
    if provider != "gitlab":
        raise RuntimeError("Configured git provider is not GitLab")

    host = _get_secret(context, "KB_GITLAB_HOST") or "https://gitlab.com"
    repo = _get_secret(context, "KB_REPO") or _get_secret(context, "DEFAULT_GITLAB_PROJECT")
    branch = _get_secret(context, "KB_BRANCH") or "main"
    token = _get_secret(context, "KB_TOKEN")
    return {
        "host": _normalize_host(host),
        "repo": repo,
        "branch": branch,
        "token": token,
    }


def _headers(token: str) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["PRIVATE-TOKEN"] = token
    return headers


def _project_id(repo: str) -> str:
    if not repo:
        return ""
    repo = repo.strip()
    if repo.isdigit():
        return repo
    return quote(repo, safe="")


def gitlab_fetch(project: str = None, path: str = "", file_path: str = None, ref: str = None, recursive: bool = True, per_page: int = 100, context=None) -> dict:
    """Fetch files from a GitLab repository by listing tree entries or reading one file."""
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    cfg = _resolve_config(context)
    project_value = (project or cfg["repo"] or "").strip()
    if not project_value:
        raise ValueError("Provide 'project' or set KB_REPO in skill settings")

    ref_value = (ref or cfg["branch"] or "main").strip() or "main"
    project_encoded = _project_id(project_value)
    host = cfg["host"]
    token = cfg["token"]

    if file_path:
        encoded_path = quote(file_path.strip().lstrip("/"), safe="")
        url = f"{host}/api/v4/projects/{project_encoded}/repository/files/{encoded_path}/raw"
        response = requests.get(url, headers=_headers(token), params={"ref": ref_value}, timeout=30)
        if response.status_code == 401:
            raise RuntimeError("GitLab authentication failed. Check the token in skill settings")
        if response.status_code == 404:
            raise RuntimeError("GitLab file was not found")
        response.raise_for_status()
        content = response.text
        try:
            content_bytes = content.encode("utf-8")
            is_binary = False
            decoded = content
        except Exception:
            content_bytes = response.content
            is_binary = True
            decoded = base64.b64encode(content_bytes).decode("ascii")
        return {
            "mode": "file",
            "project": project_value,
            "ref": ref_value,
            "file_path": file_path,
            "is_binary": is_binary,
            "content": decoded,
            "content_length": len(content_bytes),
        }

    if not isinstance(per_page, int):
        raise ValueError("'per_page' must be an integer")
    if per_page < 1 or per_page > 100:
        raise ValueError("'per_page' must be between 1 and 100")

    url = f"{host}/api/v4/projects/{project_encoded}/repository/tree"
    params = {"ref": ref_value, "recursive": str(bool(recursive)).lower(), "per_page": per_page}
    if path:
        params["path"] = path

    response = requests.get(url, headers=_headers(token), params=params, timeout=30)
    if response.status_code == 401:
        raise RuntimeError("GitLab authentication failed. Check the token in skill settings")
    if response.status_code == 404:
        raise RuntimeError("GitLab project or path was not found")
    response.raise_for_status()

    items = response.json() or []
    return {
        "mode": "tree",
        "project": project_value,
        "ref": ref_value,
        "path": path,
        "recursive": bool(recursive),
        "count": len(items),
        "items": [
            {
                "name": item.get("name"),
                "path": item.get("path"),
                "type": item.get("type"),
                "mode": item.get("mode"),
                "id": item.get("id"),
            }
            for item in items
        ],
    }


def _fetch_remote_file(host: str, project_id: str, token: str, file_path: str, ref: str):
    """Fetch a single file's JSON metadata payload from GitLab (read-only).

    Returns (payload, exists). payload has 'raw' (the GitLab file object) and
    'content' (the decoded UTF-8 text). A 404 yields (None, False).
    """
    url = (
        f"{_normalize_host(host)}/api/v4/projects/{project_id}/repository/files/"
        f"{quote(file_path.strip().lstrip('/'), safe='')}"
    )
    resp = requests.get(url, headers=_headers(token), params={"ref": ref}, timeout=30)
    if resp.status_code == 404:
        return None, False
    if resp.status_code == 401:
        raise RuntimeError("GitLab authentication failed. Check the token in skill settings")
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return {"raw": data, "content": content}, True


def gitlab_pull_files(file_paths: list, branch: str = None, context=None) -> dict:
    """Fetch remote file contents from GitLab in read-only mode.

    SuperAgent-safe: performs no local filesystem access and returns the fetched
    file contents to the caller. Uses the clean error-handling pattern with
    consistent return shapes.

    Returns a dict with: ok, project_id, branch, read_only, pulled_count,
    missing_count, files[], missing_files[] (and error when ok is False).
    """
    if context is None or not callable(getattr(context, "get_secret", None)):
        raise RuntimeError("Skill execution context is missing or does not support get_secret()")

    if not isinstance(file_paths, list) or not file_paths:
        return {"ok": False, "error": "file_paths must be a non-empty list of strings"}

    for file_path in file_paths:
        if not isinstance(file_path, str) or not file_path.strip():
            return {"ok": False, "error": "each file path must be a non-empty string"}

    try:
        cfg = _resolve_config(context)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"GitLab configuration error: {exc}"}

    host = cfg["host"]
    token = cfg["token"]
    project_id = _project_id(cfg["repo"] or "")
    target_branch = (branch or cfg["branch"] or "main").strip() or "main"

    missing_secrets = [
        name
        for name, value in (("KB_GITLAB_HOST", host), ("KB_REPO", project_id), ("KB_TOKEN", token))
        if not value
    ]
    if missing_secrets:
        return {"ok": False, "error": f"Missing required GitLab secrets: {', '.join(missing_secrets)}"}

    try:
        pulled = []
        missing_files = []

        for file_path in file_paths:
            remote_payload, exists = _fetch_remote_file(host, project_id, token, file_path, target_branch)
            if not exists:
                missing_files.append(file_path)
                continue

            raw = remote_payload["raw"]
            pulled.append(
                {
                    "file": file_path,
                    "content": remote_payload["content"],
                    "blob_id": raw.get("blob_id"),
                    "commit_id": raw.get("commit_id"),
                    "last_commit_id": raw.get("last_commit_id"),
                }
            )

        return {
            "ok": True,
            "project_id": project_id,
            "branch": target_branch,
            "read_only": True,
            "pulled_count": len(pulled),
            "missing_count": len(missing_files),
            "files": pulled,
            "missing_files": missing_files,
        }
    except requests.HTTPError as exc:
        return {"ok": False, "error": f"GitLab API error: {exc}"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"GitLab pull failed: {exc}"}


def sync_skill_files_from_gitlab(context=None) -> dict:
    """Fetch all .py files from GitLab's skill/ folder on the configured branch and
    return their contents and metadata in a structured response.

    This is a valid SuperAgent skill action: it performs no local filesystem access
    (no os / open) and instead returns the fetched file contents to the caller.

    Lists the skill/ tree with gitlab_fetch, then delegates the per-file reads to
    gitlab_pull_files for a consistent, read-only fetch. Individual file failures
    are captured and do not abort the sync.

    Returns a summary dict with the fetched files, count, and any per-file errors.
    """
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    cfg = _resolve_config(context)
    branch = (cfg.get("branch") or "main").strip() or "main"

    # Step 1: list the skill/ folder tree on the configured branch.
    try:
        listing = gitlab_fetch(path="skill", recursive=False, ref=branch, context=context)
    except Exception as exc:
        return {
            "mode": "sync",
            "ref": branch,
            "files_found": 0,
            "files": [],
            "errors": [{"file": "skill/", "error": f"Failed to list skill folder: {exc}"}],
            "ok": False,
        }

    # Step 2: filter for blob entries that are .py files.
    py_paths = [
        item.get("path")
        for item in (listing.get("items") or [])
        if item.get("type") == "blob"
        and (item.get("name") or "").endswith(".py")
        and item.get("path")
    ]

    # Step 3: pull each file's content in one read-only batch.
    pull = gitlab_pull_files(py_paths, branch=branch, context=context)
    if not pull.get("ok"):
        return {
            "mode": "sync",
            "ref": branch,
            "files_found": 0,
            "files": [],
            "errors": [{"file": "skill/", "error": pull.get("error", "GitLab pull failed")}],
            "ok": False,
        }

    files = [
        {
            "name": entry["file"].rsplit("/", 1)[-1],
            "remote_path": entry["file"],
            "content": entry["content"],
            "encoding": "utf-8",
            "blob_id": entry.get("blob_id"),
            "commit_id": entry.get("commit_id"),
            "last_commit_id": entry.get("last_commit_id"),
        }
        for entry in pull.get("files", [])
    ]
    errors = [
        {"file": path, "error": "GitLab file was not found"}
        for path in pull.get("missing_files", [])
    ]

    return {
        "mode": "sync",
        "ref": branch,
        "files_found": len(files),
        "files": files,
        "errors": errors,
        "ok": len(errors) == 0,
    }
