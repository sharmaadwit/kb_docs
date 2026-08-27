"""Trace loader - fetch from Langfuse and manage cache."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TraceLoader:
    """Load traces from Langfuse and manage local cache."""

    def __init__(
        self,
        cache_path: Path,
        langfuse_public_key: Optional[str] = None,
        langfuse_secret_key: Optional[str] = None,
        langfuse_host: str = "https://cloud.langfuse.com",
    ):
        """Initialize trace loader.

        Args:
            cache_path: Path to local cache file (JSON)
            langfuse_public_key: Langfuse public API key (optional)
            langfuse_secret_key: Langfuse secret API key (optional)
            langfuse_host: Langfuse API host
        """
        self.cache_path = cache_path
        self.langfuse_public_key = langfuse_public_key
        self.langfuse_secret_key = langfuse_secret_key
        self.langfuse_host = langfuse_host
        self._cache: Optional[Dict[str, Any]] = None

    def load_cache(self) -> Dict[str, Any]:
        """Load and parse cache file.

        Returns:
            Cache dict. Format: {last_fetch_max_timestamp, traces: {trace_id -> trace_data}}.
        """
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r") as f:
                    self._cache = json.load(f)
                traces_count = len(self._cache.get("traces", {}))
                logger.info(f"Loaded cache: {traces_count} traces")
                return self._cache
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cache: {e}. Starting fresh.")
                self._cache = {"last_fetch_max_timestamp": None, "traces": {}}
                return self._cache
        else:
            logger.info("Cache file not found. Starting fresh.")
            self._cache = {"last_fetch_max_timestamp": None, "traces": {}}
            return self._cache

    def get_last_timestamp(self) -> Optional[str]:
        """Extract timestamp of last cached trace fetch.

        Returns:
            ISO datetime string of last fetch, or None if cache is empty.
        """
        if not self._cache:
            self.load_cache()

        return self._cache.get("last_fetch_max_timestamp")

    def fetch_new_traces(self, last_timestamp: Optional[str]) -> List[Dict[str, Any]]:
        """Fetch new traces from Langfuse since last timestamp.

        For now, returns empty list (API integration deferred).
        Supervisor can be enhanced later with Langfuse SDK integration.

        Args:
            last_timestamp: Fetch traces created after this timestamp.

        Returns:
            List of new trace dictionaries.
        """
        logger.info(f"Fetching new traces from Langfuse (since {last_timestamp})...")
        logger.warning("Langfuse API integration not yet implemented. Using existing cache only.")
        return []

    def append_to_cache(self, new_traces: List[Dict[str, Any]]) -> None:
        """Append new traces to cache, deduplicate by trace_id.

        Args:
            new_traces: List of new trace dictionaries to append.
        """
        if not self._cache:
            self.load_cache()

        traces_dict = self._cache.get("traces", {})
        added_count = 0

        for trace in new_traces:
            trace_id = trace.get("id")
            if trace_id and trace_id not in traces_dict:
                traces_dict[trace_id] = trace
                added_count += 1

        self._cache["traces"] = traces_dict

        # Update timestamp
        self._cache["last_fetch_max_timestamp"] = datetime.now(timezone.utc).isoformat()

        # Write updated cache
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "w") as f:
                json.dump(self._cache, f, indent=2)
            logger.info(f"Cache updated: {added_count} new traces appended ({len(traces_dict)} total)")
        except IOError as e:
            logger.error(f"Failed to write cache: {e}")

    def get_all_traces(self) -> List[Dict[str, Any]]:
        """Get complete dataset of all cached traces as list.

        Returns:
            List of all trace dictionaries (converted from dict cache format).
        """
        if not self._cache:
            self.load_cache()

        traces_dict = self._cache.get("traces", {})
        return list(traces_dict.values())
