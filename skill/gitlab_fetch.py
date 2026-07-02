import base64
import os
import requests
from urllib.parse import quote


LOCAL_SKILL_DIR = "/Users/adwit.sharma/kb_docs/skill"


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


def _resolve_config(context):
    provider = (_get_secret(context, "KB_GIT_PROVIDER") or "gitlab").strip().lower()
    if provider != "gitlab":
        raise RuntimeError("Configured git provider is not GitLab")

    host = _get_secret(context, "KB_GITLAB_HOST") or "https://gitlab.com"
    repo = _get_secret(context, "KB_REPO") or _get_secret(context, "DEFAULT_GITLAB_PROJECT")
    branch = _get_secret(context, "KB_BRANCH") or "main"
    token = _get_secret(context, "KB_TOKEN")
    return {
        "host": host.rstrip("/"),
        "repo": repo,
        "branch": branch,
        "token": token,
    }


def _headers(token):
    headers = {"Accept": "application/json"}
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


def _safe_local_path(base_dir: str, filename: str) -> str:
    """Resolve a filename under base_dir, rejecting any path traversal."""
    base_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(os.path.join(base_abs, filename))
    if target_abs != base_abs and not target_abs.startswith(base_abs + os.sep):
        raise ValueError(f"Refusing to write outside skill directory: {filename}")
    return target_abs


def sync_skill_files_from_gitlab(context=None, local_dir: str = LOCAL_SKILL_DIR) -> dict:
    """Fetch all .py files from GitLab's skill/ folder on the main branch and write them
    directly to the local skill/ folder (overwriting existing files).

    Reuses the existing _get_secret / _resolve_config / _headers / gitlab_fetch
    infrastructure. Individual file failures are captured and do not abort the sync.

    Returns a summary dict with the synced files, count, and any per-file errors.
    """
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    cfg = _resolve_config(context)
    branch = (cfg.get("branch") or "main").strip() or "main"

    synced = []
    errors = []

    # Step 1: list the skill/ folder tree on the configured branch.
    try:
        listing = gitlab_fetch(path="skill", recursive=False, ref=branch, context=context)
    except Exception as exc:
        return {
            "mode": "sync",
            "local_dir": local_dir,
            "ref": branch,
            "synced": [],
            "synced_count": 0,
            "errors": [{"file": "skill/", "error": f"Failed to list skill folder: {exc}"}],
            "ok": False,
        }

    # Step 2: filter for blob entries that are .py files.
    py_files = [
        item
        for item in (listing.get("items") or [])
        if item.get("type") == "blob"
        and (item.get("name") or "").endswith(".py")
        and item.get("path")
    ]

    # Ensure the local target directory exists.
    try:
        os.makedirs(local_dir, exist_ok=True)
    except Exception as exc:
        return {
            "mode": "sync",
            "local_dir": local_dir,
            "ref": branch,
            "synced": [],
            "synced_count": 0,
            "errors": [{"file": local_dir, "error": f"Failed to create local dir: {exc}"}],
            "ok": False,
        }

    # Step 3: fetch and write each file, continuing past individual failures.
    for item in py_files:
        name = item.get("name")
        remote_path = item.get("path")
        try:
            result = gitlab_fetch(file_path=remote_path, ref=branch, context=context)
            content = result.get("content", "")
            local_path = _safe_local_path(local_dir, name)
            if result.get("is_binary"):
                data = base64.b64decode(content)
                with open(local_path, "wb") as handle:
                    handle.write(data)
            else:
                with open(local_path, "w", encoding="utf-8") as handle:
                    handle.write(content)
            synced.append(
                {
                    "name": name,
                    "remote_path": remote_path,
                    "local_path": local_path,
                    "bytes": result.get("content_length"),
                }
            )
        except Exception as exc:
            errors.append({"file": remote_path or name, "error": str(exc)})

    return {
        "mode": "sync",
        "local_dir": local_dir,
        "ref": branch,
        "synced": synced,
        "synced_count": len(synced),
        "errors": errors,
        "ok": len(errors) == 0,
    }
