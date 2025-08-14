from __future__ import annotations

from pathlib import Path
from typing import Dict

import click
import pandas as pd


@click.command()
@click.option("--reports", "reports_dir", required=True, help="aggregate CSV klasörü (reports/aggregate)")
@click.option("--out", "out_path", default="reports/combined.csv", help="birleşik CSV çıkışı")
def main(reports_dir: str, out_path: str):
    agg_dir = Path(reports_dir)
    if not agg_dir.exists():
        raise FileNotFoundError(f"Aggregate dizini bulunamadı: {agg_dir}")

    frames = []
    for csv_file in agg_dir.glob("*.csv"):
        df = pd.read_csv(csv_file)
        df.insert(0, "model_id", csv_file.stem)
        frames.append(df)

    if not frames:
        click.echo("Hiç CSV bulunamadı.")
        return

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(out_path, index=False)
    click.echo(f"Birleşik çıktı: {Path(out_path).resolve()}")


if __name__ == "__main__":
    main()



