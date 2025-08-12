from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Optional

import requests

from .types import InferenceResult


class HFInferenceAdapter:
    def __init__(self, model: str, api_key_env: Optional[str], params: Dict[str, Any]):
        self.model = model
        self.api_key_env = api_key_env or "HF_API_TOKEN"
        self.params = {"temperature": 0, **(params or {})}

    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 3) -> InferenceResult:
        token = os.getenv(self.api_key_env)
        if not token:
            return InferenceResult(raw_output="", success=False, error=f"Missing API key env: {self.api_key_env}")

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "inputs": prompt,
            "parameters": {"temperature": self.params.get("temperature", 0), "max_new_tokens": self.params.get("max_tokens", 512)},
            "options": {"wait_for_model": True},
        }

        last_error: Optional[str] = None
        for attempt in range(max_retries):
            try:
                # requests is blocking; run in thread to keep async contract
                def _post():
                    return requests.post(url, headers=headers, json=payload, timeout=timeout)

                resp = await asyncio.to_thread(_post)
                if resp.status_code == 200:
                    data = resp.json()
                    # Model outputs vary; try to normalize to string
                    if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
                        text = data[0]["generated_text"]
                    else:
                        text = str(data)
                    return InferenceResult(raw_output=text, success=True, error=None)
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
            except Exception as e:
                last_error = str(e)
            await asyncio.sleep(min(2 ** attempt, 8))
        return InferenceResult(raw_output="", success=False, error=last_error)


