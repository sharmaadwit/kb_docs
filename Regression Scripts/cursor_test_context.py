"""Execution context for KB skills when running tests locally (e.g. in Cursor).

- ``KB_ENV`` defaults to ``local`` when unset so Langfuse metadata is not ``unknown``.
- ``KB_DEPLOYMENT_LABEL`` defaults to ``cursor`` when unset.
- Langfuse credentials are read from the environment only (never committed):

  - ``LANGFUSE_HOST``
  - ``LANGFUSE_PUBLIC_KEY``
  - ``LANGFUSE_SECRET_KEY``

  If these are set, ``kb_answer`` will attempt ingestion like in deployed runtimes.
"""
from __future__ import annotations

import os

_LOCAL_TEST_USER_EMAIL = "adwit@cursor"

_DEFAULT_KB_ENV = "local"
_DEFAULT_DEPLOYMENT_LABEL = "cursor"

_LANGFUSE_KEYS = frozenset({
    "LANGFUSE_HOST",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
})


def cursor_kb_test_get_secret(key: str) -> str:
    raw = os.environ.get(key)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if key in _LANGFUSE_KEYS:
        return ""
    if key == "KB_ENV":
        return _DEFAULT_KB_ENV
    if key == "KB_DEPLOYMENT_LABEL":
        return _DEFAULT_DEPLOYMENT_LABEL
    return ""


class CursorKBTestContext:
    """Minimal skill ``context``: env-backed secrets + stable local telemetry defaults.

    ``user_email`` is always set so Langfuse gets a stable ``metadata.user_email``,
    ``body.userId`` (via trace user id), and matches the local test partition."""
    __slots__ = ()

    user_email = _LOCAL_TEST_USER_EMAIL

    def get_secret(self, key: str) -> str:
        return cursor_kb_test_get_secret(key)
