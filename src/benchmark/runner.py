from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import BenchmarkConfig, ModelConfig
from .metrics import compute_all_metrics
from .pydantic_validator import validate_against_schema
from .llm_eval import llm_grade_openai, llm_grade_mock, llm_grade_hf
from .adapters.openai_adapter import OpenAIAdapter
from .adapters.hf_adapter import HFInferenceAdapter
from .adapters.http_adapter import GenericHTTPAdapter
from .adapters.gguf_adapter import LocalGGUFAdapter
from .adapters.mock_adapter import MockEchoAdapter
from .adapters.types import InferenceResult


def _build_adapter(model_cfg: ModelConfig):
    backend = model_cfg.backend.lower()
    if backend == "openai":
        return OpenAIAdapter(model_cfg.model_name_or_endpoint, model_cfg.api_key_env, model_cfg.params)
    if backend == "hf":
        return HFInferenceAdapter(model_cfg.model_name_or_endpoint, model_cfg.api_key_env, model_cfg.params)
    if backend == "http":
        # Özel mock:// protokolü ile ağsız eko adapteri
        if str(model_cfg.model_name_or_endpoint).startswith("mock://echo"):
            return MockEchoAdapter(model_cfg.params)
        return GenericHTTPAdapter(model_cfg.model_name_or_endpoint, model_cfg.params)
    if backend == "gguf":
        return LocalGGUFAdapter(model_cfg.params)
    raise ValueError(f"Unsupported backend: {backend}")


async def _run_one(
    adapter,
    example: Dict[str, Any],
    bench_cfg: BenchmarkConfig,
    eval_model: str,
) -> Dict[str, Any]:
    input_text = example.get("input", "")
    expected = example.get("expected_output", "")
    fn_name = example.get("metadata", {}).get("function_name")

    result: InferenceResult = await adapter.infer(
        input_text, timeout=bench_cfg.timeout_seconds, max_retries=bench_cfg.max_retries
    )

    schema = validate_against_schema(result.raw_output, function_name=fn_name)
    metrics = compute_all_metrics(result.raw_output or "", expected or "")

    if bench_cfg.do_llm_eval:
        if bench_cfg.eval_backend == "hf":
            grading = await llm_grade_hf(input_text, expected, result.raw_output or "", model=eval_model)
        elif bench_cfg.eval_backend == "openai" and bench_cfg.openai_api_key:
            grading = await llm_grade_openai(input_text, expected, result.raw_output or "", model=eval_model)
        else:
            grading = await llm_grade_mock(input_text, expected, result.raw_output or "")
    else:
        grading = await llm_grade_mock(input_text, expected, result.raw_output or "")

    return {
        "id": example.get("id"),
        "input": input_text,
        "expected": expected,
        "output": result.raw_output,
        "success": result.success,
        "error": result.error,
        "schema_valid": schema["valid"],
        "schema_errors": schema["errors"],
        "metrics": metrics,
        "llm_score": grading.get("score", 0.0),
        "llm_reasons": grading.get("reasons", ""),
        "metadata": example.get("metadata", {}),
    }


async def run_model_on_dataset(
    model_cfg: ModelConfig, bench_cfg: BenchmarkConfig, dataset: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    adapter = _build_adapter(model_cfg)
    sem = asyncio.Semaphore(bench_cfg.concurrency)

    async def _sem_task(ex):
        async with sem:
            return await _run_one(adapter, ex, bench_cfg, bench_cfg.eval_model)

    tasks = [_sem_task(ex) for ex in dataset]
    return await asyncio.gather(*tasks)


def save_jsonl(path: str | Path, rows: List[Dict[str, Any]]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_aggregate_csv(path: str | Path, rows: List[Dict[str, Any]]):
    import pandas as pd

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(
        [
            {
                "id": r.get("id"),
                "schema_valid": r.get("schema_valid"),
                "bleu": r.get("metrics", {}).get("bleu", 0.0),
                "rouge": r.get("metrics", {}).get("rouge", 0.0),
                "bertscore": r.get("metrics", {}).get("bertscore", 0.0),
                "llm_score": r.get("llm_score", 0.0),
            }
            for r in rows
        ]
    )
    # Toplu istatistikler ayrıca CSV'nin sonuna ayrı bir bölüm olarak kaydedilebilir
    df.to_csv(p, index=False)


