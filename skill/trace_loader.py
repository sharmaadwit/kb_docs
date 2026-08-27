#!/usr/bin/env python3
"""Trace loader for supervisor agent — fetch & cache Langfuse traces incrementally.

This module manages a local JSON cache of Langfuse traces, enabling the supervisor
agent to fetch only new traces since the last load, deduplicate by trace_id, and
maintain a complete in-memory dataset for analysis.

Cache file format (local/cache/langfuse_traces_cache.json):
  {
    "last_fetch_max_timestamp": "2026-08-27T00:26:32.847000Z",
    "traces": {
      "trace_id_1": {trace_object},
      "trace_id_2": {trace_object},
      ...
    }
  }

Trace structure (from Langfuse API):
  {
    "id": "kb-kb_answer-...",
    "name": "kb_answer",
    "timestamp": "2026-08-27T00:26:32.847000Z",
    "input": {...},
    "output": {...},
    "userId": "...",
    "metadata": {...},
    ...
  }

Usage:
  loader = TraceLoader(cache_path="/path/to/cache.json")
  all_traces = loader.load_and_fetch_new()  # Sync cache with Langfuse
  print(f"Total traces: {len(all_traces)}")
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Langfuse SDK import (v4+)
try:
    from langfuse import Langfuse
except ImportError as e:
    raise SystemExit(
        "langfuse SDK not installed. Run: pip3 install --upgrade langfuse"
    ) from e


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Default cache location
DEFAULT_CACHE_PATH = "local/cache/langfuse_traces_cache.json"


class TraceLoader:
    """Load and cache Langfuse traces with incremental fetch support.

    Attributes:
        cache_path: Path to the JSON cache file
        timeout: Langfuse API request timeout in seconds
        langfuse_client: Langfuse v4 SDK client (lazy-loaded)
    """

    def __init__(
        self,
        cache_path: str = DEFAULT_CACHE_PATH,
        timeout: int = 60,
        langfuse_public_key: Optional[str] = None,
        langfuse_secret_key: Optional[str] = None,
        langfuse_host: Optional[str] = None,
    ):
        """Initialize trace loader.

        Args:
            cache_path: Path to cache JSON file (created if missing)
            timeout: Langfuse API timeout in seconds (default: 60)
            langfuse_public_key: Langfuse public key (env fallback: LANGFUSE_PUBLIC_KEY)
            langfuse_secret_key: Langfuse secret key (env fallback: LANGFUSE_SECRET_KEY)
            langfuse_host: Langfuse host (env fallback: LANGFUSE_HOST, default: cloud.langfuse.com)
        """
        self.cache_path = cache_path
        self.timeout = timeout
        self._langfuse_client: Optional[Langfuse] = None

        # Store credentials for lazy initialization
        self._public_key = langfuse_public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self._secret_key = langfuse_secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self._host = langfuse_host or os.getenv(
            "LANGFUSE_HOST", "https://cloud.langfuse.com"
        )

    def _get_langfuse_client(self) -> Langfuse:
        """Lazy-load and return Langfuse client.

        Returns:
            Langfuse v4 client instance

        Raises:
            RuntimeError: If Langfuse credentials are missing
        """
        if self._langfuse_client is not None:
            return self._langfuse_client

        if not self._public_key or not self._secret_key:
            raise RuntimeError(
                "Langfuse credentials missing. Set LANGFUSE_PUBLIC_KEY and "
                "LANGFUSE_SECRET_KEY environment variables or pass as constructor args."
            )

        self._langfuse_client = Langfuse(
            public_key=self._public_key,
            secret_key=self._secret_key,
            host=self._host,
            timeout=self.timeout,
        )
        return self._langfuse_client

    def load_cache(self) -> Dict[str, Any]:
        """Read and parse cache file.

        Returns:
            Dict with keys:
              - "last_fetch_max_timestamp": ISO8601 timestamp string or None
              - "traces": Dict[trace_id, trace_object]

        Note:
            Returns empty cache structure if file doesn't exist.
        """
        if not os.path.exists(self.cache_path):
            logger.info(f"Cache file not found: {self.cache_path} (new cache)")
            return {"last_fetch_max_timestamp": None, "traces": {}}

        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(
                f"Loaded cache: {len(data.get('traces', {}))} traces, "
                f"last_fetch: {data.get('last_fetch_max_timestamp')}"
            )
            return data
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load cache: {e}")
            return {"last_fetch_max_timestamp": None, "traces": {}}

    def get_last_timestamp(self) -> Optional[datetime]:
        """Extract timestamp of last cached trace.

        Returns:
            datetime object (UTC) or None if cache is empty
        """
        cache = self.load_cache()
        timestamp_str = cache.get("last_fetch_max_timestamp")

        if not timestamp_str:
            logger.debug("No previous fetch timestamp in cache")
            return None

        try:
            # Parse ISO8601 timestamp (e.g., "2026-08-27T00:26:32.847000Z")
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            logger.debug(f"Last timestamp: {dt}")
            return dt
        except ValueError as e:
            logger.error(f"Failed to parse last_fetch_max_timestamp: {e}")
            return None

    def fetch_new_traces(self, after_timestamp: Optional[datetime] = None) -> List[Dict]:
        """Query Langfuse SDK for traces created after timestamp.

        Args:
            after_timestamp: Only fetch traces with created_at > this timestamp.
                           If None, fetches all traces (paginated).

        Returns:
            List of trace objects from Langfuse API

        Note:
            - Handles pagination internally (requests up to 1000 per page)
            - Logs fetch progress and any API errors
            - Returns empty list if fetch fails (continues gracefully)
        """
        client = self._get_langfuse_client()

        try:
            traces: List[Dict] = []
            page = 1
            has_more = True

            while has_more:
                logger.debug(f"Fetching page {page} from Langfuse (timeout={self.timeout}s)")

                # Use Langfuse v4 API: client.api.trace.list()
                response = client.api.trace.list(
                    limit=1000,
                    page=page,
                    request_options={"timeout_in_seconds": self.timeout},
                )

                page_traces = response.data if response.data else []
                logger.debug(f"Page {page}: {len(page_traces)} traces")

                # Filter by timestamp if provided
                if after_timestamp:
                    filtered = []
                    for t in page_traces:
                        try:
                            t_timestamp = datetime.fromisoformat(
                                t.get("timestamp", "").replace("Z", "+00:00")
                            )
                            if t_timestamp > after_timestamp:
                                filtered.append(t)
                        except (ValueError, AttributeError):
                            # Skip traces with invalid/missing timestamps
                            pass
                    traces.extend(filtered)
                else:
                    traces.extend(page_traces)

                # Check if more pages exist
                has_more = bool(page_traces) and len(page_traces) == 1000
                page += 1

            logger.info(f"Fetched {len(traces)} traces (after {after_timestamp})")
            return traces

        except Exception as e:
            logger.error(f"Langfuse fetch failed: {e} (continuing with empty batch)")
            return []

    def append_to_cache(self, new_traces: List[Dict]) -> None:
        """Write updated cache with new traces deduplicated by trace_id.

        Args:
            new_traces: List of trace objects to add to cache

        Algorithm:
          1. Load existing cache
          2. Add new traces, overwriting by trace_id (deduplication)
          3. Track max timestamp across all traces
          4. Write atomically with .tmp file
        """
        if not new_traces:
            logger.debug("No new traces to cache")
            return

        # Load existing cache
        cache = self.load_cache()
        traces_dict = cache.get("traces", {})

        # Add new traces, deduplicating by ID
        max_timestamp = cache.get("last_fetch_max_timestamp")
        for trace in new_traces:
            trace_id = trace.get("id")
            if not trace_id:
                logger.warning("Trace missing id field, skipping")
                continue

            traces_dict[trace_id] = trace

            # Track max timestamp
            timestamp_str = trace.get("timestamp")
            if timestamp_str:
                try:
                    if not max_timestamp or timestamp_str > max_timestamp:
                        max_timestamp = timestamp_str
                except Exception:
                    pass

        # Prepare updated cache
        updated_cache = {
            "last_fetch_max_timestamp": max_timestamp,
            "traces": traces_dict,
        }

        # Write atomically with temporary file
        cache_dir = os.path.dirname(self.cache_path) or "."
        os.makedirs(cache_dir, exist_ok=True)

        temp_path = f"{self.cache_path}.tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(updated_cache, f, indent=2, default=str)
            os.replace(temp_path, self.cache_path)
            logger.info(
                f"Cache updated: {len(new_traces)} new traces, "
                f"total: {len(traces_dict)} traces"
            )
        except Exception as e:
            logger.error(f"Failed to write cache: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    def get_all_traces(self) -> List[Dict]:
        """Return complete dataset (all cached traces).

        Returns:
            List of all trace objects in cache (order not guaranteed)
        """
        cache = self.load_cache()
        traces_dict = cache.get("traces", {})
        traces_list = list(traces_dict.values())
        logger.info(f"Returning {len(traces_list)} cached traces")
        return traces_list

    def load_and_fetch_new(self) -> List[Dict]:
        """Orchestrate full sync: load cache, fetch new, update cache, return all.

        Returns:
            List of all traces (cached + newly fetched)

        Workflow:
          1. Load existing cache
          2. Extract last fetch timestamp
          3. Query Langfuse for traces after that timestamp
          4. Append new traces to cache (deduplicate)
          5. Return complete dataset
        """
        logger.info("Starting trace sync workflow")

        # Get last fetch timestamp
        last_timestamp = self.get_last_timestamp()
        logger.info(f"Last fetch: {last_timestamp}")

        # Fetch new traces from Langfuse
        new_traces = self.fetch_new_traces(after_timestamp=last_timestamp)

        # Update cache
        if new_traces:
            self.append_to_cache(new_traces)
        else:
            logger.info("No new traces to cache")

        # Return complete dataset
        return self.get_all_traces()


if __name__ == "__main__":
    # Smoke test: load cache and fetch new traces
    loader = TraceLoader()
    all_traces = loader.load_and_fetch_new()
    print(f"\nSync complete: {len(all_traces)} total traces")
    if all_traces:
        print(f"  First: {all_traces[0].get('id')} at {all_traces[0].get('timestamp')}")
        print(f"  Last: {all_traces[-1].get('id')} at {all_traces[-1].get('timestamp')}")
