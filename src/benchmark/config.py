from __future__ import annotations

import os
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal


@dataclass
class ModelConfig:
    id: str
    name: str
    backend: str  # openai | hf | http | gguf
    model_name_or_endpoint: str
    api_key_env: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass
class BenchmarkConfig:
    openai_api_key: Optional[str] = None
    hf_api_token: Optional[str] = None
    timeout_seconds: int = 60
    max_retries: int = 3
    concurrency: int = 4
    do_llm_eval: bool = True
    eval_model: str = os.getenv("BENCH_EVAL_MODEL", "Qwen/Qwen2-7B-Instruct")
    eval_backend: Literal["openai", "hf", "mock"] = os.getenv("BENCH_EVAL_BACKEND", "hf")  # hf by default


def load_models_config(path: str) -> List[ModelConfig]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    models: List[ModelConfig] = []
    for m in raw:
        models.append(
            ModelConfig(
                id=m["id"],
                name=m.get("name", m["id"]),
                backend=m["backend"],
                model_name_or_endpoint=m["model_name_or_endpoint"],
                api_key_env=m.get("api_key_env"),
                params=m.get("params", {}),
                notes=m.get("notes", ""),
            )
        )
    return models


def load_benchmark_env() -> BenchmarkConfig:
    return BenchmarkConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        hf_api_token=os.getenv("HF_API_TOKEN"),
        timeout_seconds=int(os.getenv("BENCH_TIMEOUT", "60")),
        max_retries=int(os.getenv("BENCH_MAX_RETRIES", "3")),
        concurrency=int(os.getenv("BENCH_CONCURRENCY", "4")),
        do_llm_eval=os.getenv("BENCH_DO_LLM_EVAL", "true").lower() == "true",
        eval_model=os.getenv("BENCH_EVAL_MODEL", "Qwen/Qwen2-7B-Instruct"),
        eval_backend=os.getenv("BENCH_EVAL_BACKEND", "hf"),
    )


