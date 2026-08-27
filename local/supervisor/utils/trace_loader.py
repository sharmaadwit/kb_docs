"""Trace loader - fetch from Langfuse and manage cache."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from langfuse import Langfuse

logger = logging.getLogger(__name__)


class TraceLoader:
    """Load traces from Langfuse and manage local cache."""

    def __init__(
        self,
        cache_path: Path,
        langfuse_public_key: str,
        langfuse_secret_key: str,
        langfuse_host: str = "https://cloud.langfuse.com",
    ):
        """Initialize trace loader.

        Args:
            cache_path: Path to local cache file (JSON)
            langfuse_public_key: Langfuse public API key
            langfuse_secret_key: Langfuse secret API key
            langfuse_host: Langfuse API host
        """
        self.cache_path = cache_path
        self.langfuse = Langfuse(
            public_key=langfuse_public_key,
            secret_key=langfuse_secret_key,
            host=langfuse_host,
        )
        self._cache: Optional[Dict[str, Any]] = None
        self._traces: List[Dict[str, Any]] = []

    def load_cache(self) -> Dict[str, Any]:
        """Load and parse cache file.

        Returns:
            Cache dict with 'traces' list and 'last_updated' timestamp.
            Empty dict if cache doesn't exist.
        """
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r") as f:
                    self._cache = json.load(f)
                logger.info(f"Loaded cache: {len(self._cache.get('traces', []))} traces")
                return self._cache
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cache: {e}. Starting fresh.")
                self._cache = {"traces": [], "last_updated": None}
                return self._cache
        else:
            logger.info("Cache file not found. Starting fresh.")
            self._cache = {"traces": [], "last_updated": None}
            return self._cache

    def get_last_timestamp(self) -> Optional[datetime]:
        """Extract timestamp of last cached trace.

        Returns:
            datetime of last trace, or None if cache is empty.
        """
        if not self._cache:
            self.load_cache()

        traces = self._cache.get("traces", [])
        if not traces:
            return None

        # Get most recent trace's created_at timestamp
        try:
            last_trace = traces[-1]  # Assume traces are sorted chronologically
            timestamp_str = last_trace.get("created_at")
            if timestamp_str:
                return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (IndexError, ValueError, KeyError) as e:
            logger.warning(f"Failed to extract last timestamp: {e}")

        return None

    def fetch_new_traces(self, last_timestamp: Optional[datetime]) -> List[Dict[str, Any]]:
        """Fetch new traces from Langfuse since last timestamp.

        Args:
            last_timestamp: Fetch traces created after this timestamp.
                           If None, fetch all traces (first run).

        Returns:
            List of new trace dictionaries.
        """
        try:
            logger.info(f"Fetching traces from Langfuse (since {last_timestamp})...")

            # Langfuse SDK: fetch traces
            # Note: This is a simplified fetch - actual API may require pagination
            traces_response = self.langfuse.fetch_traces(
                limit=10000,  # Adjust as needed
            )

            new_traces = []
            for trace in traces_response.data:
                # Filter by timestamp if provided
                if last_timestamp:
                    trace_created = datetime.fromisoformat(
                        trace.timestamp.replace("Z", "+00:00")
                    )
                    if trace_created <= last_timestamp:
                        continue

                # Extract relevant fields from trace
                trace_dict = {
                    "trace_id": trace.id,
                    "created_at": trace.timestamp,
                    "session_id": trace.session_id,
                    "user_id": trace.user_id,
                    # Extract input/output from first generation (kb_answer skill)
                    "input": trace.input or {},
                    "output": trace.output or {},
                    "metadata": trace.metadata or {},
                }

                # Parse kb_answer response structure if available
                if trace.output:
                    # Expected structure from kb_answer.py skill
                    output = trace.output
                    trace_dict.update({
                        "answered": output.get("answered", False),
                        "confidence": output.get("confidence", 0.0),
                        "module": output.get("module", "Unknown"),
                        "intent": output.get("intent", "Unknown"),
                    })

                    # Extract query from input
                    if trace.input and "query" in trace.input:
                        trace_dict["query"] = trace.input["query"]
                    elif trace.input and "user_message" in trace.input:
                        trace_dict["query"] = trace.input["user_message"]

                    # Extract response text
                    if "response" in output:
                        trace_dict["response"] = output["response"]
                    elif "answer" in output:
                        trace_dict["response"] = output["answer"]

                new_traces.append(trace_dict)

            logger.info(f"Fetched {len(new_traces)} new traces from Langfuse")
            return new_traces

        except Exception as e:
            logger.error(f"Failed to fetch traces from Langfuse: {e}")
            return []

    def append_to_cache(self, new_traces: List[Dict[str, Any]]) -> None:
        """Append new traces to cache, deduplicate by trace_id.

        Args:
            new_traces: List of new trace dictionaries to append.
        """
        if not self._cache:
            self.load_cache()

        existing_ids = {t["trace_id"] for t in self._cache.get("traces", [])}
        added_count = 0

        for trace in new_traces:
            if trace["trace_id"] not in existing_ids:
                self._cache["traces"].append(trace)
                existing_ids.add(trace["trace_id"])
                added_count += 1

        # Update timestamp
        self._cache["last_updated"] = datetime.now(timezone.utc).isoformat()

        # Write updated cache
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "w") as f:
                json.dump(self._cache, f, indent=2)
            logger.info(f"Cache updated: {added_count} new traces appended ({len(self._cache['traces'])} total)")
        except IOError as e:
            logger.error(f"Failed to write cache: {e}")

    def get_all_traces(self) -> List[Dict[str, Any]]:
        """Get complete dataset of all cached traces.

        Returns:
            List of all trace dictionaries (combined cache + fetched).
        """
        if not self._cache:
            self.load_cache()

        return self._cache.get("traces", [])
