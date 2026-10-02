"""SuperAgent live probe — empirical hypothesis testing, hard-capped at 5 calls per run.

Both the supervisor (Hermes judge verification) and interactive sessions use this
to fire a real query at the live SuperAgent endpoint and see what comes back: the
LLM-rewritten/translated query that reaches kb_answer, and the final answer shown
to the user. This lets a verdict ("this is a language gap", "this doc now answers
the query") be checked against reality instead of trusted on reasoning alone.

The 5-call cap is a hard ceiling, not a suggestion — each supervisor run (or each
interactive session that imports this module fresh) gets its own budget starting
at 5. Probing is for confirming/refuting a specific hypothesis on a specific gap,
not for bulk-testing every query.
"""

import json
import logging
import os
import ssl
import threading
import urllib.request
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MAX_PROBES_PER_RUN = 5


def _load_env() -> None:
    dotenv = _REPO_ROOT / ".env"
    if not dotenv.exists():
        return
    for line in dotenv.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and not os.environ.get(k):
            os.environ[k] = v


_load_env()

_SA_URL = os.environ.get("SUPERAGENT_API_URL", "https://superagent.smsgupshup.com/api/agents/chat/stream")
_SA_KEY = os.environ.get("SUPERAGENT_API_KEY", "")
_USER_EMAIL = os.environ.get("SUPERAGENT_PROBE_EMAIL", "kb-supervisor-probe@gupshup.io")


class _ProbeBudget:
    """Process-wide call counter — thread-safe, hard cap, no reset mid-run."""

    def __init__(self, max_calls: int = _MAX_PROBES_PER_RUN):
        self._max = max_calls
        self._used = 0
        self._lock = threading.Lock()
        self._log: list = []

    def remaining(self) -> int:
        with self._lock:
            return self._max - self._used

    def try_consume(self, reason: str) -> bool:
        """Atomically claim one probe call. Returns False if budget exhausted."""
        with self._lock:
            if self._used >= self._max:
                return False
            self._used += 1
            self._log.append(reason)
            return True

    def summary(self) -> str:
        with self._lock:
            if not self._log:
                return "SuperAgent probe budget: 0/%d used" % self._max
            lines = [f"SuperAgent probe budget: {self._used}/{self._max} used"]
            for i, reason in enumerate(self._log, 1):
                lines.append(f"  {i}. {reason}")
            return "\n".join(lines)


# Module-level singleton — one budget per process. The supervisor runs as a fresh
# `python3 -m local.supervisor.supervisor_agent` process each invocation, so this
# naturally resets to 5 per run without any explicit reset call needed.
BUDGET = _ProbeBudget()


def probe_superagent(query: str, reason: str, timeout: int = 60) -> Optional[dict]:
    """Fire one query at the live SuperAgent endpoint, consuming one unit of budget.

    Returns None if budget is exhausted, credentials are missing, or the call fails.
    Returns {"answer": str, "raw_events": list} on success — "answer" is the
    assembled text SuperAgent streamed back (post-rewrite, what a user would see).

    `reason` is a short string describing WHY this probe is being made (which
    hypothesis it's testing) — recorded for the audit trail in BUDGET.summary().
    """
    if not _SA_KEY:
        logger.warning("SuperAgent probe skipped: SUPERAGENT_API_KEY not set")
        return None

    if not BUDGET.try_consume(reason):
        logger.warning(
            "SuperAgent probe DENIED (budget exhausted, %d/%d used) — hypothesis '%s' not verified empirically",
            _MAX_PROBES_PER_RUN, _MAX_PROBES_PER_RUN, reason,
        )
        return None

    logger.info("SuperAgent probe %d/%d: %s — query: %r",
                _MAX_PROBES_PER_RUN - BUDGET.remaining(), _MAX_PROBES_PER_RUN, reason, query[:80])

    headers = {"Content-Type": "application/json", "X-API-Key": _SA_KEY}
    payload = {
        "message": query,
        "session_id": f"supervisor-probe-{abs(hash(query)) % 100000}",
        "user_email_id": _USER_EMAIL,
    }

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    answer_parts: list = []
    raw_events: list = []
    try:
        req = urllib.request.Request(
            _SA_URL, data=json.dumps(payload).encode(), headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            raw = resp.read().decode()
            for line in raw.strip().split("\n"):
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    ev = json.loads(data)
                    raw_events.append(ev)
                    if ev.get("type") == "text_delta":
                        answer_parts.append(ev.get("text", ""))
                    elif "content" in ev:
                        answer_parts.append(ev["content"])
                except Exception:
                    pass
    except Exception as exc:
        logger.warning("SuperAgent probe failed for '%s': %s", reason, exc)
        return None

    return {"answer": "".join(answer_parts), "raw_events": raw_events}
