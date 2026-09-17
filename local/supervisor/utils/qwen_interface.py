"""Qwen LLM interface via company proxy (Bearer auth, OpenAI-compatible)."""

import json
import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


class QwenInterface:
    """HTTP client for Qwen LLM via company proxy."""

    def __init__(
        self,
        base_url: str,
        auth_token: str,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 1500,
        timeout_seconds: int = 60,
    ):
        """Initialize Qwen interface.

        Args:
            base_url: Proxy base URL (e.g., https://llmproxy.gupshup.io/)
            auth_token: Bearer token for authentication
            model: Model name (e.g., Qwen3-Coder-480B)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            timeout_seconds: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds

    def call(self, prompt: str, system_message: Optional[str] = None) -> Optional[str]:
        """Call Qwen LLM and return response text.

        Args:
            prompt: User prompt/query
            system_message: Optional system message for context

        Returns:
            Response text from LLM, or None on failure.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json",
            }

            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }

            url = f"{self.base_url}/v1/chat/completions"
            logger.debug(f"Calling Qwen at {url}")

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()

            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not content:
                logger.warning("Empty response from Qwen")
                return None

            # Strip markdown code fences if present
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            content = content.strip()

            return content

        except requests.exceptions.Timeout:
            logger.error(f"Qwen call timed out after {self.timeout_seconds}s")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Qwen API request failed: {e}")
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse Qwen response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling Qwen: {e}")
            return None
