FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app
ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "-m", "benchmark.run", "--models", "models.yaml", "--dataset", "data/telekom_test_set.sample.jsonl", "--out", "reports/"]


