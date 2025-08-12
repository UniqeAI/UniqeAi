from __future__ import annotations

import asyncio
from typing import Any, Dict

from .types import InferenceResult


class MockEchoAdapter:
    """Ağ erişimi olmadan hızlı smoke test için eko adapteri."""

    def __init__(self, params: Dict[str, Any] | None = None):
        self.params = params or {}

    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 1) -> InferenceResult:
        await asyncio.sleep(0)  # context switch
        return InferenceResult(raw_output=prompt, success=True, error=None)


