from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import requests

from .types import InferenceResult


class GenericHTTPAdapter:
    def __init__(self, endpoint: str, params: Dict[str, Any]):
        self.endpoint = endpoint
        self.params = {"temperature": 0, **(params or {})}

    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 3) -> InferenceResult:
        payload = {"prompt": prompt, **self.params}
        last_error: Optional[str] = None
        for attempt in range(max_retries):
            try:
                def _post():
                    return requests.post(self.endpoint, json=payload, timeout=timeout)

                resp = await asyncio.to_thread(_post)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data.get("output") or data.get("text") or str(data)
                    return InferenceResult(raw_output=text, success=True, error=None)
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
            except Exception as e:
                last_error = str(e)
            await asyncio.sleep(min(2 ** attempt, 8))
        return InferenceResult(raw_output="", success=False, error=last_error)


