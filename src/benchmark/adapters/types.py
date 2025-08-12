from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class InferenceResult:
    raw_output: str
    success: bool
    error: Optional[str]


