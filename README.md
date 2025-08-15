## ChoyrensAi – Telekom Akıllı Asistan 

ChoyrensAi takımı tarafından geliştirilen, uçtan uca veri üretimi → model eğitimi → servis (backend) → arayüz (frontend) → değerlendirme (benchmark) akışını tek depoda sunan referans uygulama.

- BilisimVadisi2025
- Türkiye Açık Kaynak Platformu

### İçindekiler
- Proje Özeti
- Depo Yapısı
- Bağımlılıklar (Eksiksiz Liste)
- Kurulum ve Çalıştırma Adımları
- Veri Seti (Herkese Açık Bağlantı ve Alternatif Üretim)
- Model Eğitimi (QLoRA/BF16)
- Backend (API)
- Frontend (Web Arayüz)
- Benchmark ve Raporlama
- Testler
- Etiketler ve Duyurular
 - Kod Referansı

### Proje Özeti
- Eğitim scripti: `ai_model/scripts/training/expert_trainer-stable.py`
- Veri üretimi: `ai_model/modular_generator/` (modüler veri üretici)
- Ana veri seti dosyası: `ultimate_human_level_dataset_v2_enhanced_20250809_033446.json`
- Testler ve değerlendirme: `src/benchmark/`
- Frontend: `frontend/`
- Backend: `backend/`

## Depo Yapısı
- `ai_model/modular_generator/`: Üst düzey modüler veri üreteci (senaryolar, şema doğrulama, yardımcılar)
- `ai_model/scripts/training/expert_trainer-stable.py`: Llama-3 için QLoRA/BF16 uzman seviye eğitim scripti
- `backend/`: FastAPI tabanlı REST servisleri ve Telekom mock/örnek uçları
- `frontend/`: Vite + Vue tabanlı web arayüzü
- `src/benchmark/`: Model değerlendirme, metrikler, LLM tabanlı otomatik puanlama
- `reports/`: Benchmark çıktı ve özetleri

## Bağımlılıklar (Eksiksiz Liste)

### Sistem Gereksinimleri
- Python 3.10+
- Node.js 18+ (frontend için)
- (İsteğe bağlı) NVIDIA GPU + CUDA 12.x (model eğitimi için önerilir)

### Python (Backend)
- Kurulum: `pip install -r backend/requirements.txt`

Başlıca paketler:
- fastapi, uvicorn, pydantic (v2), httpx, python-dotenv

### Python (Model Eğitimi)
Eğitim ortamı için önerilen paketler:
```
pip install --upgrade torch transformers datasets accelerate peft trl bitsandbytes pydantic python-dotenv
```

### Python (Benchmark)
Benchmark ve metrikler için önerilen paketler:
```
pip install --upgrade click pandas numpy matplotlib httpx pyyaml sacrebleu rouge-score bert-score
```

Not: `bert-score` ilk çalıştırmada model indirebilir; internet erişimi gerektirir.

### Frontend (Web)
- Node paketleri: `npm install` (veya `pnpm install`)
- Vite, Vue 3, Tailwind (stil dosyaları repo içinde)

## Kurulum ve Çalıştırma Adımları

### 1) Depoyu kopyalayın
```
git clone <repo-url> && cd UniqeAi
```

### 2) Ortam değişkenleri
Kök dizinde `.env` oluşturun ve en azından aşağıdaki anahtarları tanımlayın:
```
HUGGINGFACE_HUB_TOKEN=...
WANDB_API_KEY=...          # (opsiyonel) eğitim logları için
```

### 3) Veri seti
- Seçenek A – İndir (herkese açık bağlantı): Aşağıdaki bölümdeki bağlantıyı kullanın ve dosyayı proje köküne kaydedin.
- Seçenek B – Üret (modüler üreteç):
```
cd ai_model
python -m modular_generator.main --num-samples 10000 --output-file ultimate_human_level_dataset_v2_enhanced_20250809_033446.json
cd ..
```

### 4) Backend’i çalıştırın
```
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5) Frontend’i çalıştırın
```
cd frontend
npm install
npm run dev
```

### 6) Benchmark çalıştırın (opsiyonel)
Örnek bir `models.yaml` oluşturun (mock veya gerçek model tanımları ile):
```yaml
models:
  - id: mock
    name: Mock Echo
    backend: mock
    model_name_or_endpoint: mock
```

Ardından değerlendirmeyi çalıştırın:
```
python -m src.benchmark.run --models models.yaml \
  --dataset ultimate_human_level_dataset_v2_enhanced_20250809_033446.json \
  --out reports --llm-eval
```

## Veri Seti (Herkese Açık Bağlantı)

- Dosya adı: `ultimate_human_level_dataset_v2_enhanced_20250809_033446.json`
- Herkese açık indirme bağlantısı (örnek, Release varlıkları üzerinden):

```
https://github.com/UniqeAI/UniqeAi/releases/latest/download/ultimate_human_level_dataset_v2_enhanced_20250809_033446.json
```

Alternatif barındırma seçenekleri:
- GitHub Releases (önerilir)
- Hugging Face Datasets
- Bulut depolama (örn. Google Drive, S3) – paylaşımı “genel/anyone with the link” yapınız

Not: Lütfen yukarıdaki URL’de `REPO_OWNER/REPO_NAME` kısmını kendi deponuza göre güncelleyiniz.

## Model Eğitimi (QLoRA/BF16)

Eğitim scripti: `ai_model/scripts/training/expert_trainer-stable.py`

Temel kullanım:
```
python ai_model/scripts/training/expert_trainer-stable.py \
  --model_name "meta-llama/Meta-Llama-3-8B-Instruct" \
  --data_paths ultimate_human_level_dataset_v2_enhanced_20250809_033446.json \
  --output_dir UniqeAi/ai_model/final-model_v6_bf16 \
  --num_train_epochs 3 --gradient_accumulation_steps 16 --bf16 True
```

Notlar:
- `.env` içindeki `HUGGINGFACE_HUB_TOKEN` otomatik yüklenir.
- `use_bf16_training=True` ise BF16; aksi halde 4-bit QLoRA kullanılır.
- W&B entegrasyonu için `WANDB_API_KEY` sağlayabilirsiniz.

### Eğitilmiş Modeller

Hugging Face'te yayınlanan modellerimiz:

- [ChoyrensAI-Telekom-Agent-v6-gguf](https://huggingface.co/Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf) - En güncel GGUF formatı (5-bit Q5_K_M, 5.73 GB)
- [ChoyrensAI-Telekom-Agent-v5-gguf](https://huggingface.co/Choyrens/ChoyrensAI-Telekom-Agent-v5-gguf) - 8-bit Q8_0 formatı (8.54 GB)
- [ChoyrensAI-Telekom-Agent-v4-gguf](https://huggingface.co/Choyrens/ChoyrensAI-Telekom-Agent-v4-gguf) - Önceki versiyon GGUF
- [ChoyrensAI-Telekom-Agent-v1-merged](https://huggingface.co/Choyrens/ChoyrensAI-Telekom-Agent-v1-merged) - İlk merged model (Safetensors, BF16)

## Backend (API)
Çalıştırma:
```
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Örnek uçlar:
- `GET /api/v1/health`
- `POST /api/v1/telekom/billing/current`
- `POST /api/v1/telekom/packages/quotas`
- `POST /api/v1/telekom/support/tickets`

Detaylar için `backend/app/api/v1/` ve `backend/app/services/` dizinlerine bakınız.

## Frontend (Web Arayüz)
Geliştirme modu:
```
cd frontend
npm install
npm run dev
```

Öntanımlı API adresi `http://localhost:8000` olup, UI bileşenleri `frontend/src/` altındadır.

## Benchmark ve Raporlama
- Çalıştırma: `python -m src.benchmark.run --models models.yaml --dataset <json> --out reports`
- Toplu rapor birleştirme: `python -m src.benchmark.compare --reports reports/aggregate --out reports/combined.csv`
- Metrikler: BLEU, ROUGE, BERTScore + (opsiyonel) LLM tabanlı değerlendirme

## Testler
```
pytest -q
```
Başlıca testler:
- Backend: `backend/tests/test_telekom_api.py`
- Benchmark: `tests/test_runner_with_mock_model.py`, `tests/test_metrics.py`

## Etiketler ve Duyurular
- GitHub konuları (Topics) bölümüne aşağıdaki etiketleri ekleyiniz:
  - `BilisimVadisi2025`
  - `Turkiye-Acik-Kaynak-Platformu`

GitHub CLI ile eklemek için (opsiyonel):
```
gh repo edit --add-topic BilisimVadisi2025 --add-topic Turkiye-Acik-Kaynak-Platformu
```

Paylaşımlarda ve duyurularda “Türkiye Açık Kaynak Platformu”nu etiketlemeyi unutmayınız.

---

ChoyrensAi • 2025

## Kod Referansı

Bu bölüm, repodaki ana bileşenleri ve önemli fonksiyon/sınıfları yüksek seviyede açıklar.

### ai_model

- `ai_model/scripts/training/expert_trainer-stable.py`
  - `ModelAndDataConfig`, `TrainingArguments`: Eğitim ve veri ayarları.
  - `setup_huggingface_token()`: `.env` → HF token yükleme.
  - `ExpertTrainer`
    - `_normalize_dialogue_item()`: Farklı formatlardan standart `donguler` şemasına dönüştürme.
    - `_format_dialogue()`: Llama-3 chat template’iyle %100 uyumlu tool-calling yapı üretimi.
    - `_load_and_prepare_dataset()`: JSON → `datasets.Dataset` dönüşümü, `tokenizer.apply_chat_template` kullanımı.
    - `run()`: BF16/QLoRA seçimi, LoRA kurulumu (`peft`), `trl.SFTTrainer` ile eğitim ve kayıt.

- `ai_model/modular_generator/`
  - `core_generator.py` – `SupremeHumanLevelDatasetGenerator`
    - `_build_api_response_mapping()`, `_create_validated_response()`
    - `generate_supreme_dataset()`, `save_dataset()`
    - Lazy özellikler: `personality_profiles`, `cognitive_patterns`, `meta_templates`, `cultural_contexts`, `temporal_reasoning_patterns`, `innovation_frameworks` (bkz. `lazy_loading.py`, `initializers.py`).
  - `config/settings.py`
    - `SCENARIO_WEIGHTS`: Senaryo ağırlıkları
    - `API_RESPONSE_MAPPING`: Fonksiyon → Pydantic response modeli eşlemesi
    - `telekom_api_schema.py` import ve şema özetleri
  - `generators/`
    - `basic_scenarios/` ve `advanced_scenarios/`: `generate_*_scenario` fonksiyonları (ör. `generate_change_package_scenario`, `generate_adaptive_communication_scenarios`).
  - `validators/api_validators.py`
    - `validate_tool_call`, `validate_scenario_quality`, `verify_pydantic_compliance`.
  - `utils/helpers.py`
    - `generate_user_id`, `generate_mock_data_for_model`, `create_validated_response`.
  - `telekom_api_schema.py`
    - Telekom alanına özel tüm `Request`/`Response` Pydantic modelleri ve yardımcı fonksiyonlar.

### backend

- `backend/app/main.py`: Uygulama ana girişi, `/api/v1/health`.
- `backend/app/api/v1/telekom.py`: Telekom işlemleri
  - Faturalama: `/billing/current`, `/billing/history`, `/billing/pay`, `/billing/payments`, `/billing/autopay`
  - Paketler: `/packages/current`, `/packages/quotas`, `/packages/change`, `/packages/available`, `/packages/details`
  - Servisler/Ağ: `/services/roaming`, `/network/status`
  - Destek: `/support/tickets`, `/support/tickets/close`, `/support/tickets/status`, `/support/tickets/list`
  - Müşteri: `/customers/profile`, `/customers/contact`, `/lines/suspend`, `/lines/reactivate`
  - Kimlik: `/auth/register`, `/auth/login`
- `backend/app/api/v1/chat.py`: Chat endpoint’leri (yeni/legacy), `ChatRequest`/`ChatResponseNew` şemaları.
- `backend/app/services/ai_orchestrator*.py`: Gerçek/sade orkestratör; araç çağrıları ve final yanıt üretimi.
- `backend/app/services/ai_endpoint_functions.py`: Telekom uçları için istemci yardımcıları (facade).
- Testler: `backend/tests/test_telekom_api.py`.

### frontend

- Vite + Vue 3 yapısı (`frontend/src/`).
- API istemcisi: `frontend/src/services/api.js` (telekom uçlarına sarmalayıcı fonksiyonlar).
- Sayfalar/Bileşenler: `frontend/src/pages/*`, `frontend/src/components/*`.

### benchmark

- `src/benchmark/adapters/`: `openai_adapter.py`, `hf_adapter.py`, `http_adapter.py`, `gguf_adapter.py`, `mock_adapter.py` – ortak `InferenceResult` tipi (`adapters/types.py`).
- `src/benchmark/metrics.py`: BLEU, ROUGE, BERTScore ve `compute_all_metrics`.
- `src/benchmark/llm_eval.py`: OpenAI/HF/Mock LLM değerlendirme fonksiyonları.
- `src/benchmark/pydantic_validator.py`: Model çıktısının telekom şemalarına doğrulanması.
- `src/benchmark/runner.py`: Dataset üzerinde model çalıştırma ve sonuçların kaydı.
- `src/benchmark/compare.py`: Aggregate CSV’leri birleştirme.

### raporlar

- `reports/aggregate/*.csv`: Modellerin toplu sonuçları.

## 🎯 Proje Özellikleri

Bu proje, uçtan uca veri üretimi → model eğitimi → servis (backend) → arayüz (frontend) → değerlendirme (benchmark) akışını tek depoda sunan referans uygulamadır.

### Core Features
- 🧠 **Akıllı Sohbet**: Doğal dil işleme ile müşteri sorularını anlama
- 📊 **Modüler Veri Üretimi**: 20+ kişilik profili, 7 bilişsel kalıp, 3 kültürel bağlam
- ⚡ **Real-time İşlemler**: Anlık fatura, paket ve destek işlemleri
- 🔧 **Kapsamlı Test Sistemi**: BLEU, ROUGE, BERTScore + LLM tabanlı değerlendirme

### Telekom İşlemleri
- 📱 Fatura sorgulama ve ödeme
- 📦 Paket değişimi ve yönetimi
- 🔧 Teknik destek ve arıza bildirimi
- 💰 Kampanya ve promosyon yönetimi
- 📞 Hat işlemleri ve numarahanı
- 🌐 İnternet ve Wi-Fi destek

## 🛠 Technology Stack

### AI & ML
- **Llama 3** - Base language model (Meta-Llama-3-8B-Instruct)
- **Transformers** - Hugging Face model library
- **QLoRA/BF16** - Efficient training techniques
- **Peft & TRL** - Parameter-efficient fine-tuning

### Backend
- **Python 3.10+** - Core backend language
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation and schema enforcement
- **Uvicorn** - ASGI server

### Frontend
- **Vue 3** - Progressive framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework

### Evaluation & Benchmarking
- **BLEU, ROUGE, BERTScore** - Automatic metrics
- **LLM-based evaluation** - GPT-4o-mini scoring
- **Pydantic validation** - Schema compliance checking

### DevOps & Deployment
- **GitHub Actions** - CI/CD pipeline
- **Docker** - Containerization support

## 📈 Performance Metrics

- **Model Size**: 8.03B parameters (Llama-3 based)
- **Training**: QLoRA/BF16 optimized for efficiency
- **Validation**: %100 Pydantic compliance
- **Benchmark**: Multi-metric evaluation system
- **Dataset**: 10,000+ high-quality scenarios

## 🔒 Compliance & Standards

- **BilisimVadisi2025** compliance
- **Türkiye Açık Kaynak Platformu** standards
- Data validation with Pydantic v2
- Professional code review standards 
