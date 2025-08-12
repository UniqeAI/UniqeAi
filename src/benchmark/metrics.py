from __future__ import annotations

from typing import Dict

import evaluate


_bleu = None
_rouge = None
_bertscore = None


def _lazy_bleu():
    global _bleu
    if _bleu is None:
        _bleu = evaluate.load("bleu")
    return _bleu


def _lazy_rouge():
    global _rouge
    if _rouge is None:
        _rouge = evaluate.load("rouge")
    return _rouge


def _lazy_bertscore():
    global _bertscore
    if _bertscore is None:
        _bertscore = evaluate.load("bertscore")
    return _bertscore


def compute_bleu(prediction: str, reference: str) -> float:
    pred = (prediction or "").strip()
    ref = (reference or "").strip()
    if not pred or not ref:
        return 0.0
    try:
        # evaluate BLEU is 0..1
        result = _lazy_bleu().compute(predictions=[pred], references=[[ref]])
        return float(result.get("bleu", 0.0))
    except Exception:
        return 0.0


def compute_rouge(prediction: str, reference: str) -> float:
    pred = (prediction or "").strip()
    ref = (reference or "").strip()
    if not pred or not ref:
        return 0.0
    try:
        # Use ROUGE-Lsum if available; fallback to rougeL
        result = _lazy_rouge().compute(predictions=[pred], references=[ref])
        rouge_l = (
            float(result.get("rougeLsum", 0.0))
            if "rougeLsum" in result
            else float(result.get("rougeL", 0.0))
        )
        return rouge_l
    except Exception:
        return 0.0


def compute_bertscore(prediction: str, reference: str) -> float:
    pred = (prediction or "").strip()
    ref = (reference or "").strip()
    if not pred or not ref:
        return 0.0
    try:
        # BERTScore returns precision/recall/f1 lists in 0..1
        result = _lazy_bertscore().compute(
            predictions=[pred], references=[ref], lang="tr"
        )
        f1 = result.get("f1", [0.0])[0]
        return float(f1)
    except Exception:
        return 0.0


def compute_all_metrics(prediction: str, reference: str) -> Dict[str, float]:
    return {
        "bleu": compute_bleu(prediction, reference),
        "rouge": compute_rouge(prediction, reference),
        "bertscore": compute_bertscore(prediction, reference),
    }


