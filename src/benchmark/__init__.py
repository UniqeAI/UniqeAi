"""
Telekom benchmark paketi: birden fazla modeli aynı test setinde çalıştırıp
- Pydantic şema doğrulaması (telekom_api_schema) yapar,
- BLEU/ROUGE/BERTScore ölçer,
- LLM tabanlı değerlendirme (GPT-4 yapılandırılabilir) uygular,
- Per-örnek ve toplu raporlar üretir.

CLI:
  python -m benchmark.run --models models.yaml --dataset data/telekom_test_set.jsonl --out reports/
"""


