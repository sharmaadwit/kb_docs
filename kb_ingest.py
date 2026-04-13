import base64
import json
import re
from datetime import datetime, timezone
from typing import Dict, List

import requests


def _parse_parameters(parameters: object = None, **kwargs) -> Dict:
    if parameters is None:
        parameters = {}
    if isinstance(parameters, str):
        p = parameters.strip()
        if not p:
            parameters = {}
        else:
            try:
                parameters = json.loads(p)
            except Exception as exc:
                raise ValueError("Invalid parameters: expected JSON object") from exc
    if not isinstance(parameters, dict):
        raise ValueError("parameters must be a dict or JSON string")
    return {**parameters, **kwargs}


def _gh_headers(context) -> Dict[str, str]:
    token = context.get_secret("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GitHub configuration secrets")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _gh_get_json(url: str, context, params: Dict = None) -> Dict:
    r = requests.get(url, headers=_gh_headers(context), params=params or {}, timeout=30)
    if r.status_code >= 400:
        raise RuntimeError("GitHub API request failed")
    return r.json()


def _gh_put_json(url: str, context, payload: Dict) -> Dict:
    r = requests.put(url, headers=_gh_headers(context), data=json.dumps(payload), timeout=30)
    if r.status_code >= 400:
        raise RuntimeError("GitHub API request failed")
    return r.json()


def _list_md_files(owner: str, repo: str, branch: str, docs_path: str, context) -> List[str]:
    out = []
    stack = [docs_path.strip("/")]
    while stack:
        p = stack.pop()
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{p}"
        data = _gh_get_json(url, context, params={"ref": branch})
        if isinstance(data, dict) and data.get("type") == "file":
            if p.lower().endswith(".md"):
                out.append(p)
            continue
        if not isinstance(data, list):
            continue
        for item in data:
            t = item.get("type")
            ip = item.get("path")
            if not ip:
                continue
            if t == "dir":
                if ip.startswith("kb/analytics"):
                    continue
                stack.append(ip)
            elif t == "file" and ip.lower().endswith(".md"):
                out.append(ip)
    return sorted(set(out))


_MAX_RAW_FILE_BYTES = 1_500_000
_MAX_MD_FILES = 400
_MAX_CHUNKS_PER_FILE = 400
_MAX_TOTAL_CHUNKS = 80_000


def _get_raw(owner: str, repo: str, branch: str, path_in_repo: str, context) -> str:
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path_in_repo}"
    r = requests.get(url, headers=_gh_headers(context), timeout=60)
    if r.status_code >= 400:
        raise RuntimeError("GitHub content fetch failed")
    data = r.content
    if len(data) > _MAX_RAW_FILE_BYTES:
        raise RuntimeError("Document exceeds maximum size for ingestion")
    return data.decode("utf-8", errors="replace")


def _normalize_whitespace(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _heading_level(line: str) -> int:
    m = re.match(r"^(#{1,6})\s+", (line or "").strip())
    return len(m.group(1)) if m else 0


def _strip_heading_markup(line: str) -> str:
    return re.sub(r"^#{1,6}\s+", "", (line or "").strip()).strip()


def _is_heading(line: str) -> bool:
    return _heading_level(line) > 0


def _classify_section_type(heading_path: List[str], body: str, source: str) -> str:
    joined = " ".join(heading_path).lower()
    first_lines = " ".join([ln.strip() for ln in (body or "").splitlines()[:8]]).lower()
    hay = f"{source.lower()} {joined} {first_lines}"
    if any(t in hay for t in ["reference (from source)", "reference", "important", "overview", "introduction", "getting started", "about"]):
        return "reference"
    if any(t in hay for t in ["where to configure", "setup path", "navigation", "exact path", "path"]):
        return "path"
    if any(t in hay for t in ["steps", "how to configure", "configuration", "procedure", "setup", "create", "how to"]):
        return "steps"
    if any(t in hay for t in ["prerequisites", "before you begin", "requirements", "dependencies"]):
        return "prerequisites"
    if any(t in hay for t in ["validation", "how to validate", "how to verify", "testing", "verify", "confirm it works", "where to view"]):
        return "validation"
    if any(t in hay for t in ["troubleshooting", "common issues", "debug", "fix"]):
        return "troubleshooting"
    if any(t in hay for t in ["available options", "options", "variants", "types", "supported"]):
        return "options"
    if any(t in hay for t in ["field mapping", "schema", "payload", "fields to configure", "key fields"]):
        return "schema"
    if any(t in hay for t in ["definition", "what this does", "what this feature does", "what happens when enabled", "what happens when disabled", "uses", "benefits"]):
        return "concept"
    return "general"


def _is_placeholder_line(line: str) -> bool:
    low = (line or "").strip().lower()
    if not low:
        return True
    if low.startswith("_add ") or low.startswith("_list ") or low.startswith("_not "):
        return True
    if "updated 10 months ago" in low:
        return True
    if low in {"reference (from source)", "when to use", "overview", "module:"}:
        return True
    return False


def _normalize_chunk_text(text: str) -> str:
    out: List[str] = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("```"):
            continue
        if _is_placeholder_line(line):
            continue
        if line.lower().startswith("module:"):
            continue
        out.append(line)
    return "\n".join(out).strip()


def _is_low_value_chunk(text: str, heading_path: List[str], section_type: str) -> bool:
    low = (text or "").lower()
    if not low:
        return True
    if any(p in low for p in ["_add ", "_list ", "_not specified", "_not applicable", "updated 10 months ago"]):
        return True
    if "reference (from source)" in " ".join(heading_path).lower() and len(low.split()) < 40:
        return True
    if section_type == "reference" and len(low.split()) < 30:
        return True
    useful_lines = [ln for ln in low.splitlines() if ln.strip()]
    if len(useful_lines) <= 2 and all(ln.startswith("#") or ln.startswith("module:") for ln in useful_lines):
        return True
    if len(low.split()) < 12:
        return True
    return False


def _split_sections(text: str, source: str) -> List[dict]:
    text = _normalize_whitespace(text)
    if not text:
        return []
    lines = text.split("\n")
    sections: List[dict] = []
    heading_stack: List[str] = []
    current_lines: List[str] = []
    current_heading_path: List[str] = []

    def flush_current():
        nonlocal current_lines, current_heading_path
        body = "\n".join(current_lines).strip()
        if body:
            sections.append({
                "heading": current_heading_path[-1] if current_heading_path else "",
                "heading_path": current_heading_path[:],
                "body": body,
                "section_type": _classify_section_type(current_heading_path, body, source),
            })
        current_lines = []

    for line in lines:
        if _is_heading(line):
            flush_current()
            level = _heading_level(line)
            heading_text = _strip_heading_markup(line)
            if not heading_text:
                continue
            while len(heading_stack) >= level:
                heading_stack.pop()
            heading_stack.append(heading_text)
            current_heading_path = heading_stack[:]
            current_lines = [line.strip()]
        else:
            if not current_heading_path and not current_lines:
                current_heading_path = []
            current_lines.append(line)

    flush_current()
    return sections


def _find_split_point(text: str, start: int, chunk_size: int) -> int:
    end = min(len(text), start + chunk_size)
    if end >= len(text):
        return len(text)
    window = text[start:end]
    candidates = [
        window.rfind("\n## "),
        window.rfind("\n### "),
        window.rfind("\n\n"),
        window.rfind(". "),
        window.rfind("\n"),
        window.rfind("; "),
        window.rfind(", "),
        window.rfind(" "),
    ]
    best = max(candidates)
    if best <= int(chunk_size * 0.45):
        return end
    return start + best + 1


def _advance_to_safe_start(text: str, idx: int) -> int:
    n = len(text)
    if idx <= 0:
        return 0
    if idx >= n:
        return n
    prev_char = text[idx - 1] if idx - 1 >= 0 else "\n"
    curr_char = text[idx] if idx < n else "\n"
    if prev_char in {"\n", " ", "\t"}:
        return idx
    if not prev_char.isalnum() or not curr_char.isalnum():
        return idx
    j = idx
    while j < n and text[j].isalnum():
        j += 1
    while j < n and text[j] in {" ", "\t"}:
        j += 1
    return j if j < n else idx


def _clean_chunk_edges(piece: str) -> str:
    piece = (piece or "").strip()
    if not piece:
        return ""
    lines = [ln.rstrip() for ln in piece.split("\n")]
    while lines:
        first = lines[0].strip()
        if not first or re.match(r"^[,:;.)\\]\\-]+", first) or (len(first) < 12 and not _is_heading(first)):
            lines.pop(0)
            continue
        break
    while lines:
        last = lines[-1].strip()
        if not last or len(last) < 8 or re.search(r"[:,;/\\-]$", last):
            lines.pop()
            continue
        break
    return "\n".join(lines).strip()


def _chunk_section(section: dict, source: str, chunk_size: int = 1200, overlap: int = 120) -> List[dict]:
    body = _normalize_whitespace(section.get("body") or "")
    if not body:
        return []
    heading = section.get("heading") or ""
    heading_path = section.get("heading_path") or []
    prefix_parts = []
    for i, h in enumerate(heading_path):
        prefix_parts.append(f"{'#' * min(i + 1, 6)} {h}")
    prefix = ("\n".join(prefix_parts) + "\n\n") if prefix_parts else ""
    max_body_size = max(500, chunk_size - len(prefix))
    chunks: List[dict] = []
    i = 0
    n = len(body)
    seen = set()
    while i < n:
        i = _advance_to_safe_start(body, i)
        j = _find_split_point(body, i, max_body_size)
        piece = _clean_chunk_edges(body[i:j])
        if piece:
            text = (prefix + piece).strip() if prefix else piece.strip()
            text = _normalize_chunk_text(text)
            if text and text not in seen:
                seen.add(text)
                chunks.append({
                    "heading": heading,
                    "heading_path": heading_path,
                    "section_type": section.get("section_type") or "general",
                    "text": text,
                })
        if j >= n:
            break
        next_i = max(0, j - overlap)
        if next_i <= i:
            next_i = j
        i = next_i
    return chunks


def _chunk_text(text: str, source: str, chunk_size: int = 1200, overlap: int = 120) -> List[dict]:
    sections = _split_sections(text, source)
    out: List[dict] = []
    for section_idx, section in enumerate(sections):
        section_chunks = _chunk_section(section, source, chunk_size=chunk_size, overlap=overlap)
        for local_idx, rec in enumerate(section_chunks):
            text = _normalize_chunk_text(rec.get("text") or "")
            section_type = rec.get("section_type") or "general"
            heading_path = rec.get("heading_path") or []
            if _is_low_value_chunk(text, heading_path, section_type):
                continue
            out.append({
                "section": section_idx,
                "heading": rec.get("heading") or "",
                "heading_path": heading_path,
                "section_type": section_type,
                "local_chunk": local_idx,
                "text": text,
            })
    return out


def _get_file_sha(owner: str, repo: str, branch: str, path_in_repo: str, context) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path_in_repo}"
    r = requests.get(url, headers=_gh_headers(context), params={"ref": branch}, timeout=30)
    if r.status_code == 404:
        return ""
    if r.status_code >= 400:
        raise RuntimeError("GitHub API request failed")
    return (r.json() or {}).get("sha", "")


def _write_file(owner: str, repo: str, branch: str, path_in_repo: str, content: str, message: str, context) -> None:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path_in_repo}"
    sha = _get_file_sha(owner, repo, branch, path_in_repo, context)
    payload = {"message": message, "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"), "branch": branch}
    if sha:
        payload["sha"] = sha
    _gh_put_json(url, context, payload)


def _safe_path_segment(path: str, fallback: str) -> str:
    p = (path or "").strip().strip("/")
    if not p or ".." in p or "\x00" in p:
        return fallback
    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_./-]*$", p):
        return fallback
    return p


def kb_ingest(parameters: object = None, context=None, **kwargs) -> dict:
    """Ingest markdown docs from a GitHub repo path, chunk them, and write index artifacts."""
    if context is None:
        raise RuntimeError("Skill execution context is missing")

    try:
        params = _parse_parameters(parameters, **kwargs)
    except ValueError:
        return {"ok": False, "error": "Invalid parameters"}

    owner = context.get_secret("GITHUB_OWNER")
    repo = context.get_secret("GITHUB_REPO")
    branch = (context.get_secret("GITHUB_BRANCH") or "main").strip()
    docs_path = _safe_path_segment(
        context.get_secret("GITHUB_DOCS_PATH") or "kb",
        "kb",
    )
    chunks_out = context.get_secret("GITHUB_KB_CHUNKS_PATH") or f"{docs_path}/kb_chunks.jsonl"
    index_out = context.get_secret("GITHUB_KB_INDEX_PATH") or f"{docs_path}/kb_index.json"
    if isinstance(params.get("docs_path"), str) and params.get("docs_path").strip():
        docs_path = _safe_path_segment(params["docs_path"], docs_path)
    if isinstance(params.get("branch"), str) and params["branch"].strip():
        branch = params["branch"].strip()[:256]
        if ".." in branch or "\x00" in branch:
            return {"ok": False, "error": "Invalid branch override"}

    if not owner or not repo or not branch:
        raise RuntimeError("Missing GitHub configuration secrets")

    excluded = [f"{docs_path}/analytics"]
    try:
        md_files = _list_md_files(owner, repo, branch, docs_path, context)
    except Exception:
        return {"ok": False, "error": "Could not list documentation files"}

    if len(md_files) > _MAX_MD_FILES:
        md_files = md_files[:_MAX_MD_FILES]

    chunks_lines = []
    doc_entries = []
    total_chunks = 0

    try:
        for fp in md_files:
            raw = _get_raw(owner, repo, branch, fp, context)
            chunk_records = _chunk_text(raw, fp)
            if len(chunk_records) > _MAX_CHUNKS_PER_FILE:
                chunk_records = chunk_records[:_MAX_CHUNKS_PER_FILE]
            doc_entries.append({"path": fp, "chunks": len(chunk_records)})
            for idx, rec in enumerate(chunk_records):
                if total_chunks >= _MAX_TOTAL_CHUNKS:
                    break
                chunks_lines.append(json.dumps({
                    "id": f"{fp}::chunk_{idx}",
                    "source": fp,
                    "chunk": idx,
                    "section": rec.get("section"),
                    "heading": rec.get("heading") or "",
                    "heading_path": rec.get("heading_path") or [],
                    "section_type": rec.get("section_type") or "general",
                    "is_reference": rec.get("section_type") == "reference",
                    "local_chunk": rec.get("local_chunk"),
                    "text": rec.get("text") or "",
                }, ensure_ascii=False))
                total_chunks += 1
            if total_chunks >= _MAX_TOTAL_CHUNKS:
                break

        now = datetime.now(timezone.utc).isoformat()
        index = {
            "ok": True,
            "created_at": now,
            "repo": f"{owner}/{repo}",
            "branch": branch,
            "docs_path": docs_path,
            "excluded": excluded,
            "md_files": len(md_files),
            "chunks": total_chunks,
            "docs": doc_entries,
            "chunking": {
                "strategy": "heading_path_section_blocks",
                "chunk_size": 1200,
                "overlap": 120,
                "metadata": ["heading", "heading_path", "section_type", "is_reference"],
            },
        }

        _write_file(owner, repo, branch, chunks_out, "\n".join(chunks_lines) + "\n", "KB ingest: write chunks", context)
        _write_file(owner, repo, branch, index_out, json.dumps(index, indent=2), "KB ingest: write index", context)
    except Exception:
        return {"ok": False, "error": "Ingest failed"}

    return {
        "ok": True,
        "repo": f"{owner}/{repo}",
        "branch": branch,
        "docs_path": docs_path,
        "excluded": excluded,
        "md_files": len(md_files),
        "chunks": total_chunks,
        "chunks_out": chunks_out,
        "index_out": index_out,
        "chunking": index["chunking"],
    }
