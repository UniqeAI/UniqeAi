.PHONY: install test run-sample docker-build format

install:
	python -m pip install -r requirements.txt

test:
	pytest -q

run-sample:
	bash scripts/run_benchmark.sh models.yaml data/telekom_test_set.sample.jsonl reports/

docker-build:
	docker build -t telekom-benchmark:latest .

format:
	black src tests


