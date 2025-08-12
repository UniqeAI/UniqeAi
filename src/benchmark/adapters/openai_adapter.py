from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Optional

from .types import InferenceResult


class OpenAIAdapter:
    def __init__(self, model: str, api_key_env: Optional[str], params: Dict[str, Any]):
        self.model = model
        self.api_key_env = api_key_env or "OPENAI_API_KEY"
        self.params = {"temperature": 0, **(params or {})}

    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 3) -> InferenceResult:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return InferenceResult(raw_output="", success=False, error=f"Missing API key env: {self.api_key_env}")

        # Import here to avoid global dependency if not used
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=api_key)
        last_error: Optional[str] = None

        for attempt in range(max_retries):
            try:
                resp = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=self.params.get("temperature", 0),
                        max_tokens=self.params.get("max_tokens", 512),
                        seed=self.params.get("seed"),
                    ),
                    timeout=timeout,
                )
                text = resp.choices[0].message.content or ""
                return InferenceResult(raw_output=text, success=True, error=None)
            except Exception as e:
                last_error = str(e)
                # exponential backoff
                await asyncio.sleep(min(2 ** attempt, 8))
        return InferenceResult(raw_output="", success=False, error=last_error)


