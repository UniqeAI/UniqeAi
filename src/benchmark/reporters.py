from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def plot_model_bars(aggregate_map: Dict[str, pd.DataFrame], out_dir: str | Path):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    for model_id, df in aggregate_map.items():
        rows.append(
            {
                "model": model_id,
                "bleu": float(df["bleu"].mean()) if not df.empty else 0.0,
                "rouge": float(df["rouge"].mean()) if not df.empty else 0.0,
                "bertscore": float(df["bertscore"].mean()) if not df.empty else 0.0,
                "llm_score": float(df["llm_score"].mean()) if not df.empty else 0.0,
                "schema_valid_rate": float(df["schema_valid"].mean()) if not df.empty else 0.0,
            }
        )

    agg = pd.DataFrame(rows)
    if agg.empty:
        return
    ax = agg.set_index("model")[
        ["bleu", "rouge", "bertscore", "llm_score", "schema_valid_rate"]
    ].plot(kind="bar", figsize=(12, 5), ylim=(0, 1))
    ax.set_title("Model Karşılaştırma (0-1)")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out / "models_bar.png")


