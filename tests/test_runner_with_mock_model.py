import asyncio
from benchmark.config import ModelConfig, load_benchmark_env
from benchmark.runner import run_model_on_dataset


class DummyAdapter:
    async def infer(self, prompt: str, timeout: int = 60, max_retries: int = 3):
        from benchmark.adapters.types import InferenceResult

        return InferenceResult(raw_output=prompt, success=True, error=None)


def test_runner_with_dummy(monkeypatch):
    # Monkeypatch _build_adapter to return DummyAdapter
    from benchmark import runner as runner_mod

    monkeypatch.setattr(runner_mod, "_build_adapter", lambda cfg: DummyAdapter())

    model = ModelConfig(
        id="dummy", name="dummy", backend="http", model_name_or_endpoint="", api_key_env=None, params={}
    )
    bench = load_benchmark_env()
    dataset = [
        {"id": "1", "input": "selam", "expected_output": "selam", "metadata": {}},
        {"id": "2", "input": "merhaba", "expected_output": "merhaba", "metadata": {}},
    ]

    results = asyncio.run(run_model_on_dataset(model, bench, dataset))
    assert len(results) == 2
    assert all(r.get("success") for r in results)


