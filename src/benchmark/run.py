from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

import click
import pandas as pd

from .config import load_models_config, load_benchmark_env
from .runner import run_model_on_dataset, save_jsonl, save_aggregate_csv
from .reporters import plot_model_bars


def _load_dataset(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset bulunamadı: {p}")
    if p.suffix.lower() == ".jsonl":
        rows = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
        return rows
    elif p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ValueError("Dataset uzantısı .jsonl veya .json olmalı")


@click.command()
@click.option("--models", "models_path", required=True, help="models.yaml yolu")
@click.option("--dataset", "dataset_path", required=True, help="telekom_test_set.jsonl/.json yolu")
@click.option("--out", "out_dir", default="reports", help="Çıktı klasörü")
@click.option("--llm-eval/--no-llm-eval", default=True, help="LLM tabanlı değerlendirme")
def main(models_path: str, dataset_path: str, out_dir: str, llm_eval: bool):
    models = load_models_config(models_path)
    bench_cfg = load_benchmark_env()
    bench_cfg.do_llm_eval = llm_eval

    dataset = _load_dataset(dataset_path)
    out = Path(out_dir)
    per_example_dir = out / "per_example"
    aggregate_dir = out / "aggregate"
    per_example_dir.mkdir(parents=True, exist_ok=True)
    aggregate_dir.mkdir(parents=True, exist_ok=True)

    aggregate_map: Dict[str, pd.DataFrame] = {}

    for m in models:
        click.echo(f"\n▶️ Model çalıştırılıyor: {m.id} ({m.backend})")
        results = asyncio.run(run_model_on_dataset(m, bench_cfg, dataset))
        save_jsonl(per_example_dir / f"{m.id}.jsonl", results)
        save_aggregate_csv(aggregate_dir / f"{m.id}.csv", results)
        aggregate_map[m.id] = pd.DataFrame(
            [
                {
                    "id": r.get("id"),
                    "schema_valid": r.get("schema_valid"),
                    "bleu": r.get("metrics", {}).get("bleu", 0.0),
                    "rouge": r.get("metrics", {}).get("rouge", 0.0),
                    "bertscore": r.get("metrics", {}).get("bertscore", 0.0),
                    "llm_score": r.get("llm_score", 0.0),
                }
                for r in results
            ]
        )

    # Basit görselleştirme
    plot_model_bars(aggregate_map, out)

    click.echo(f"\n✅ Tamamlandı. Raporlar: {out.resolve()}")


if __name__ == "__main__":
    main()


