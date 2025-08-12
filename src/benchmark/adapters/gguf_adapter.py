from __future__ import annotations

import asyncio
from typing import Any, Dict

from .types import InferenceResult


class LocalGGUFAdapter:
    """Yerel gguf çalıştırma için kanca. Burada sadece arayüz sağlıyoruz.

    Not: Kullanıcı kendi sunucusunu/CLI'sini burada entegre edebilir.
    Örn: llama.cpp server'a HTTP ile çağrı veya subprocess ile binary çağrısı.
    """

    def __init__(self, params: Dict[str, Any]):
        self.params = {"temperature": 0, **(params or {})}

    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 3) -> InferenceResult:
        # Placeholder: implementer tarafından doldurulacak
        await asyncio.sleep(0.01)
        return InferenceResult(raw_output="", success=False, error="GGUF adapter is not implemented")


