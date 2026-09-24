"""
Isolation guard — run once at supervisor startup before any other logic.

Enforces two hard invariants:
  1. No Langfuse write instrumentation: the supervisor READS Langfuse traces
     from a local cache file. It must NEVER write traces back (that would
     corrupt the production telemetry that the supervisor analyses).
  2. No SuperAgent endpoint calls: the supervisor is a read-only analysis loop
     over cached telemetry. Calling the live skill endpoint would (a) add cost,
     (b) pollute Langfuse with supervisor-generated traces, and (c) introduce
     current-code bias into the historical-gap analysis.

How it works
------------
* Langfuse: the Python SDK auto-activates when LANGFUSE_PUBLIC_KEY and
  LANGFUSE_SECRET_KEY are both present in the environment. We strip those vars
  so even a transitive import of `langfuse` cannot phone home.  We also patch
  `socket.getaddrinfo` and `urllib.request.urlopen` as a belt-and-suspenders
  block against any direct calls to *.langfuse.com.
* SuperAgent / skill: we block known SuperAgent hostnames the same way.
  Any attempt to resolve or open those hosts raises IsolationViolation.

The guard is intentionally loud — it raises on violation rather than silently
swallowing errors, so a misconfigured run fails fast instead of silently
polluting production data.
"""

from __future__ import annotations

import logging
import os
import socket
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Blocked host patterns
# ---------------------------------------------------------------------------

# Langfuse write hosts — the supervisor reads a local JSON cache, never the
# live API directly, and must never write traces back.
_BLOCKED_LANGFUSE_HOSTS: frozenset[str] = frozenset({
    "cloud.langfuse.com",
    "us.cloud.langfuse.com",
    "eu.cloud.langfuse.com",
    "langfuse.com",
})

# SuperAgent / skill endpoint hosts.
# llmproxy.gupshup.io is intentionally NOT blocked — that is the internal
# Qwen LLM proxy used by the hermes judge (pure text generation, no tracing).
_BLOCKED_SKILL_HOSTS: frozenset[str] = frozenset({
    "api.gupshup.io",
    "superagent.gupshup.io",
    "superagentapi.gupshup.io",
    "agentai.gupshup.io",
    "agent.gupshup.io",
    "partner.gupshup.io",  # SuperAgent partner API
})

_ALL_BLOCKED: frozenset[str] = _BLOCKED_LANGFUSE_HOSTS | _BLOCKED_SKILL_HOSTS

# ---------------------------------------------------------------------------
# Langfuse SDK env vars that trigger auto-instrumentation
# ---------------------------------------------------------------------------
_LANGFUSE_SDK_VARS: tuple[str, ...] = (
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    # LANGFUSE_HOST is kept so config.py can read it for the cache path, but
    # without the key pair the SDK cannot activate — still cleared for safety.
    "LANGFUSE_HOST",
)


class IsolationViolation(RuntimeError):
    """Raised when the supervisor attempts a blocked network call."""


# ---------------------------------------------------------------------------
# Internal: save original socket functions before patching
# ---------------------------------------------------------------------------
_orig_getaddrinfo = socket.getaddrinfo
_orig_urlopen = urllib.request.urlopen


def _blocking_getaddrinfo(host: str, *args: Any, **kwargs: Any) -> Any:
    """Drop-in for socket.getaddrinfo that blocks forbidden hosts."""
    if isinstance(host, str):
        for blocked in _ALL_BLOCKED:
            if host == blocked or host.endswith("." + blocked):
                raise IsolationViolation(
                    f"ISOLATION VIOLATION: supervisor attempted DNS lookup of blocked host "
                    f"'{host}'. This would call {'Langfuse' if blocked in _BLOCKED_LANGFUSE_HOSTS else 'SuperAgent/skill'}. "
                    f"The supervisor is read-only over the local trace cache — no live calls allowed."
                )
    return _orig_getaddrinfo(host, *args, **kwargs)


def _blocking_urlopen(url: Any, *args: Any, **kwargs: Any) -> Any:
    """Drop-in for urllib.request.urlopen that blocks forbidden hosts."""
    url_str = str(getattr(url, "full_url", url))
    for blocked in _ALL_BLOCKED:
        if blocked in url_str:
            raise IsolationViolation(
                f"ISOLATION VIOLATION: supervisor attempted HTTP call to blocked URL "
                f"'{url_str}'. This would call {'Langfuse' if blocked in _BLOCKED_LANGFUSE_HOSTS else 'SuperAgent/skill'}. "
                f"The supervisor is read-only over the local trace cache — no live calls allowed."
            )
    return _orig_urlopen(url, *args, **kwargs)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def enforce() -> None:
    """Call once at the top of supervisor_agent.main() before anything else.

    Actions taken:
      1. Strips Langfuse SDK env vars so the SDK cannot auto-activate.
      2. Patches socket.getaddrinfo to block forbidden host resolutions.
      3. Patches urllib.request.urlopen to block forbidden HTTP calls.
      4. Logs a clear confirmation that isolation is active.

    Raises IsolationViolation on any subsequent blocked call.
    """
    stripped: list[str] = []
    for var in _LANGFUSE_SDK_VARS:
        if var in os.environ:
            del os.environ[var]
            stripped.append(var)

    if stripped:
        logger.warning(
            "isolation_guard: stripped Langfuse SDK env vars to prevent "
            "auto-instrumentation: %s", stripped
        )

    # Patch network layer
    socket.getaddrinfo = _blocking_getaddrinfo  # type: ignore[assignment]
    urllib.request.urlopen = _blocking_urlopen  # type: ignore[assignment]

    blocked_hosts = sorted(_ALL_BLOCKED)
    logger.info(
        "isolation_guard: ACTIVE — supervisor run is fully isolated. "
        "Blocked hosts (%d): %s", len(blocked_hosts), ", ".join(blocked_hosts)
    )
    logger.info(
        "isolation_guard: Qwen LLM proxy (llmproxy.gupshup.io) remains ALLOWED "
        "for hermes judge turns (text generation only, no tracing)."
    )


def check_sys_modules() -> None:
    """Assert the Langfuse SDK write client and skill/kb_answer are not loaded.

    Call after imports settle (e.g. after load_config()) to catch any
    transitive import that snuck in a Langfuse client.
    """
    import sys

    langfuse_write_mods = [
        m for m in sys.modules
        if "langfuse" in m.lower() and "langfuse_traces" not in m.lower()
    ]
    if langfuse_write_mods:
        raise IsolationViolation(
            f"ISOLATION VIOLATION: Langfuse SDK modules loaded in supervisor process: "
            f"{langfuse_write_mods}. These could write traces back to Langfuse. "
            f"Remove the import that pulls them in."
        )

    skill_mods = [
        m for m in sys.modules
        if "kb_answer" in m.lower() or ("skill" in m.lower() and "kb" in m.lower())
    ]
    if skill_mods:
        raise IsolationViolation(
            f"ISOLATION VIOLATION: skill/kb_answer loaded in supervisor process: "
            f"{skill_mods}. The supervisor must not execute live skill code."
        )

    logger.info(
        "isolation_guard: sys.modules check passed — "
        "no Langfuse SDK write clients, no skill/kb_answer loaded."
    )
