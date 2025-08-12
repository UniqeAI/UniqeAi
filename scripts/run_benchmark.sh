#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1

MODELS_FILE=${1:-models.yaml}
DATASET_FILE=${2:-data/telekom_test_set.sample.jsonl}
OUT_DIR=${3:-reports}

PYTHONPATH=src:$PYTHONPATH python -m benchmark.run --models "$MODELS_FILE" --dataset "$DATASET_FILE" --out "$OUT_DIR"


