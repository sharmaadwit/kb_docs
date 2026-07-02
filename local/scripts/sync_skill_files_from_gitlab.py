#!/usr/bin/env python3
"""
Local script to sync skill files from GitLab.

This script calls the SuperAgent skill action sync_skill_files_from_gitlab()
(which fetches file contents), then writes them to the local skill/ folder.

Usage:
  python local/scripts/sync_skill_files_from_gitlab.py

Environment:
  - Set KB_GIT_PROVIDER, KB_GITLAB_HOST, KB_REPO, KB_BRANCH, KB_TOKEN in .env
  - Or set them as environment variables

Exit codes:
  0 = success
  1 = fetch failed
  2 = write errors (partial success)
  3 = all writes failed
"""

import base64
import json
import os
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).parent.parent.parent / "skill"


def load_env():
    """Load .env file if present."""
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = value
    return {
        "KB_GIT_PROVIDER": os.getenv("KB_GIT_PROVIDER", "gitlab"),
        "KB_GITLAB_HOST": os.getenv("KB_GITLAB_HOST", "https://gitlab.gupshup.io"),
        "KB_REPO": os.getenv("KB_REPO"),
        "KB_BRANCH": os.getenv("KB_BRANCH", "main"),
        "KB_TOKEN": os.getenv("KB_TOKEN"),
    }


def sync_files_from_gitlab():
    """
    Sync skill files from GitLab by calling the skill action and writing locally.

    This mimics what SuperAgent would return from sync_skill_files_from_gitlab().
    """
    import requests
    from urllib.parse import quote

    config = load_env()

    # Validate config
    if not config["KB_REPO"] or not config["KB_TOKEN"]:
        print("ERROR: KB_REPO and KB_TOKEN required. Set in .env or environment.", file=sys.stderr)
        return 1

    def _get_secret(name):
        return config.get(name)

    def _project_id(repo):
        repo = str(repo).strip()
        return repo if repo.isdigit() else quote(repo, safe="")

    def _headers(token):
        headers = {"Accept": "application/json"}
        if token:
            headers["PRIVATE-TOKEN"] = token
        return headers

    def gitlab_fetch_file(file_path, branch):
        """Fetch a single file from GitLab."""
        host = config["KB_GITLAB_HOST"].rstrip("/")
        repo = config["KB_REPO"]
        token = config["KB_TOKEN"]

        project_encoded = _project_id(repo)
        encoded_path = quote(file_path.strip().lstrip("/"), safe="")
        url = f"{host}/api/v4/projects/{project_encoded}/repository/files/{encoded_path}/raw"

        response = requests.get(
            url,
            headers=_headers(token),
            params={"ref": branch},
            timeout=30
        )

        if response.status_code == 401:
            raise RuntimeError("GitLab authentication failed")
        if response.status_code == 404:
            raise RuntimeError(f"File not found: {file_path}")

        response.raise_for_status()

        try:
            content = response.text
            content_bytes = content.encode("utf-8")
            is_binary = False
            decoded = content
        except Exception:
            content_bytes = response.content
            is_binary = True
            decoded = base64.b64encode(content_bytes).decode("ascii")

        return {
            "is_binary": is_binary,
            "content": decoded,
            "content_length": len(content_bytes),
        }

    def gitlab_fetch_tree(path, branch):
        """Fetch tree listing from GitLab."""
        host = config["KB_GITLAB_HOST"].rstrip("/")
        repo = config["KB_REPO"]
        token = config["KB_TOKEN"]

        project_encoded = _project_id(repo)
        url = f"{host}/api/v4/projects/{project_encoded}/repository/tree"

        response = requests.get(
            url,
            headers=_headers(token),
            params={"ref": branch, "recursive": "false", "per_page": "100", "path": path},
            timeout=30
        )

        if response.status_code == 401:
            raise RuntimeError("GitLab authentication failed")
        if response.status_code == 404:
            raise RuntimeError("GitLab project or path not found")

        response.raise_for_status()

        items = response.json() or []
        return items

    # Sync logic (mirrors SuperAgent skill)
    branch = config["KB_BRANCH"] or "main"
    files = []
    errors = []

    print(f"Listing skill/ folder from GitLab on {branch}...")
    try:
        items = gitlab_fetch_tree("skill", branch)
    except Exception as exc:
        print(f"ERROR: Failed to list skill folder: {exc}", file=sys.stderr)
        return 1

    py_files = [
        item
        for item in items
        if item.get("type") == "blob"
        and (item.get("name") or "").endswith(".py")
        and item.get("path")
    ]

    print(f"Found {len(py_files)} .py files")

    # Fetch each file
    for item in py_files:
        name = item.get("name")
        remote_path = item.get("path")
        print(f"  Fetching {name}...", end=" ")
        try:
            result = gitlab_fetch_file(remote_path, branch)
            content = result.get("content", "")
            is_binary = bool(result.get("is_binary"))

            files.append({
                "name": name,
                "remote_path": remote_path,
                "content": content,
                "bytes": result.get("content_length"),
                "encoding": "base64" if is_binary else "utf-8",
            })
            print("✓")
        except Exception as exc:
            errors.append({"file": remote_path or name, "error": str(exc)})
            print(f"✗ ({exc})")

    # Write files locally
    if not files:
        print("No files to write.")
        return 1 if errors else 0

    print(f"\nWriting {len(files)} files to {SKILL_DIR}...")
    write_errors = []

    for file_meta in files:
        name = file_meta["name"]
        content = file_meta["content"]
        encoding = file_meta["encoding"]
        local_path = SKILL_DIR / name

        print(f"  Writing {name}...", end=" ")
        try:
            if encoding == "base64":
                data = base64.b64decode(content)
                local_path.write_bytes(data)
            else:
                local_path.write_text(content, encoding="utf-8")
            print("✓")
        except Exception as exc:
            write_errors.append({"file": name, "error": str(exc)})
            print(f"✗ ({exc})")

    # Summary
    print(f"\nSummary:")
    print(f"  Files synced: {len(files)}")
    print(f"  Fetch errors: {len(errors)}")
    print(f"  Write errors: {len(write_errors)}")

    if write_errors:
        print("\nWrite failures:")
        for err in write_errors:
            print(f"  {err['file']}: {err['error']}")

    if errors:
        print("\nFetch failures:")
        for err in errors:
            print(f"  {err['file']}: {err['error']}")

    # Exit code
    if write_errors:
        return 3 if len(write_errors) == len(files) else 2
    if errors:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(sync_files_from_gitlab())
