"""Trace loader - reads from the shared dashboard cache (dict-of-dicts format)."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TraceLoader:
    """Load traces from the shared langfuse_traces_cache.json."""

    def __init__(
        self,
        cache_path: Path,
        langfuse_public_key: str = "",
        langfuse_secret_key: str = "",
        langfuse_host: str = "https://cloud.langfuse.com",
    ):
        self.cache_path = cache_path
        self._cache: Optional[Dict[str, Any]] = None

    def load_cache(self) -> Dict[str, Any]:
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r") as f:
                    self._cache = json.load(f)
                traces_dict = self._cache.get("traces", {})
                n = len(traces_dict) if isinstance(traces_dict, dict) else len(traces_dict)
                logger.info("Loaded cache: %d traces", n)
                return self._cache
            except (json.JSONDecodeError, IOError) as e:
                logger.warning("Failed to load cache: %s. Starting fresh.", e)
        self._cache = {"last_fetch_max_timestamp": None, "traces": {}}
        return self._cache

    def get_last_timestamp(self) -> Optional[datetime]:
        if not self._cache:
            self.load_cache()
        ts = self._cache.get("last_fetch_max_timestamp")
        if not ts:
            return None
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except ValueError as e:
            logger.warning("Failed to extract last timestamp: %s", e)
            return None

    def fetch_new_traces(self, last_timestamp: Optional[datetime]) -> List[Dict[str, Any]]:
        # Cache is maintained by the dashboard refresh script; supervisor reads it.
        logger.info("Supervisor reads dashboard cache only — no direct Langfuse fetch.")
        return []

    def append_to_cache(self, new_traces: List[Dict[str, Any]]) -> None:
        # Nothing to append — dashboard refresh owns the cache file.
        pass

    def get_all_traces(self) -> List[Dict[str, Any]]:
        if not self._cache:
            self.load_cache()
        traces = self._cache.get("traces", {})
        if isinstance(traces, dict):
            return list(traces.values())
        return list(traces)
