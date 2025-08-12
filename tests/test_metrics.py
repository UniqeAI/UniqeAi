from benchmark.metrics import compute_all_metrics


def test_metrics_compute():
    m = compute_all_metrics("merhaba dünya", "merhaba dunya")
    assert set(m.keys()) == {"bleu", "rouge", "bertscore"}


