# 🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3 - MODULAR EDITION

Bu proje, orijinal `ULTIMATE_HUMAN_LEVEL_DATASET_GENERATOR_V3.py` dosyasının profesyonel modüler yapıya dönüştürülmüş halidir.

## 📁 Modüler Yapı

```
modular_generator/
├── __init__.py                 # Ana modül girişi
├── main.py                     # Çalıştırma dosyası
├── core_generator.py           # Ana generator sınıfı
├── lazy_loading.py             # Lazy loading property fonksiyonları
├── initializers.py             # Initialize metodları
├── README.md                   # Bu dosya
├── models/                     # Veri modelleri
│   ├── __init__.py
│   ├── enums.py               # Enum tanımları
│   └── dataclasses.py         # Dataclass tanımları
├── exceptions/                 # Özel hata sınıfları
│   ├── __init__.py
│   └── custom_exceptions.py
├── validators/                 # Doğrulama fonksiyonları
│   ├── __init__.py
│   └── api_validators.py
├── generators/                 # Senaryo üreticileri
│   ├── __init__.py
│   ├── advanced_scenarios/    # Gelişmiş senaryolar (her biri ayrı dosya)
│   │   ├── __init__.py
│   │   ├── negotiation_skills.py
│   │   ├── teaching_mentoring.py
│   │   ├── innovation_thinking.py
│   │   ├── temporal_reasoning.py
│   │   ├── cross_cultural_communication.py
│   │   ├── advanced_error_recovery.py
│   │   ├── social_dynamics.py
│   │   ├── conflicting_information.py
│   │   ├── strategic_planning.py
│   │   ├── empathetic_reasoning.py
│   │   ├── adaptive_communication.py
│   │   ├── predictive_analytics.py
│   │   ├── resource_optimization.py
│   │   └── collaborative_filtering.py
│   └── basic_scenarios/       # Temel senaryolar (her biri ayrı dosya)
│       ├── __init__.py
│       ├── standard.py
│       ├── tool_chaining.py
│       ├── proactive.py
│       ├── disambiguation.py
│       ├── multi_intent.py
│       ├── ethical_dilemma.py
│       ├── payment_history.py
│       ├── setup_autopay.py
│       ├── change_package.py
│       ├── suspend_line.py
│       ├── error_response.py
│       ├── package_details.py
│       ├── enable_roaming.py
│       ├── get_user_tickets.py
│       ├── get_ticket_status.py
│       └── test_internet_speed.py
├── utils/                      # Yardımcı fonksiyonlar
│   ├── __init__.py
│   └── helpers.py
└── config/                     # Konfigürasyon ayarları
    ├── __init__.py
    └── settings.py
```

## 🎯 Özellikler

- ✅ **%100 Modüler Yapı**: Her bileşen ayrı modülde
- ✅ **Kolay Bakım**: Kod organizasyonu ve okunabilirlik
- ✅ **Genişletilebilir**: Yeni senaryolar kolayca eklenebilir
- ✅ **Test Edilebilir**: Her modül bağımsız test edilebilir
- ✅ **Aynı İşlevsellik**: Orijinal script ile %100 uyumlu
- ✅ **Enterprise Grade**: Profesyonel kod yapısı
- ✅ **V3 Enhancement**: Memory optimization ve lazy loading
- ✅ **20+ Kişilik Profili**: Gelişmiş arketip sistemi
- ✅ **7 Bilişsel Kalıp**: İleri düzey düşünme modelleri
- ✅ **3 Kültürel Bağlam**: Çok kültürlü destek
- ✅ **Ayrı Dosya Yapısı**: Lazy loading ve initialize metodları ayrı dosyalarda

## 🚀 Kullanım

### 1. Basit Kullanım

```python
from modular_generator import SupremeHumanLevelDatasetGenerator

# Generator'ı başlat
generator = SupremeHumanLevelDatasetGenerator()

# Dataset üret
dataset = generator.generate_supreme_dataset(num_samples=100)

# Kaydet
generator.save_dataset(dataset, "my_dataset.json")
```

### 2. Komut Satırından Çalıştırma

```bash
cd ai_model
python -m modular_generator.main --num-samples 1000 --output-file my_dataset.json
```

### 3. Modüler Import

```python
# Sadece belirli bileşenleri import et
from modular_generator.models import ScenarioType
from modular_generator.validators import validate_scenario_quality
from modular_generator.generators import generate_standard_scenario
```

## 📊 Modül Açıklamaları

### `models/`
- **enums.py**: Senaryo türleri, bilişsel durumlar, duygusal bağlamlar
- **dataclasses.py**: Kişilik profilleri, konuşma hafızası, kültürel bağlamlar

### `exceptions/`
- **custom_exceptions.py**: Özel hata sınıfları (SchemaValidationError, ParameterMismatchError, vb.)

### `validators/`
- **api_validators.py**: API doğrulama, senaryo kalite kontrolü, Pydantic uyumluluk

### `generators/`
- **advanced_scenarios/**: Gelişmiş senaryolar (her biri ayrı dosya)
  - negotiation_skills.py, teaching_mentoring.py, innovation_thinking.py, vb.
- **basic_scenarios/**: Temel senaryolar (her biri ayrı dosya)
  - standard.py, tool_chaining.py, proactive.py, vb.

### `utils/`
- **helpers.py**: Yardımcı fonksiyonlar (mock data generation, user ID generation, vb.)

### `config/`
- **settings.py**: Konfigürasyon ayarları, API mapping, senaryo ağırlıkları

### `lazy_loading.py`
- **Property fonksiyonları**: Memory optimization için lazy loading

### `initializers.py`
- **Initialize metodları**: V3 Enhancement özelliklerini destekler

## 🔧 Geliştirme

### Yeni Senaryo Ekleme

1. `generators/` klasöründe yeni dosya oluştur
2. Senaryo fonksiyonunu yaz
3. `generators/__init__.py`'ye ekle
4. `core_generator.py`'de `_get_scenario_generators()` metoduna ekle
5. `config/settings.py`'de ağırlık tanımla

### Yeni Validator Ekleme

1. `validators/` klasöründe yeni dosya oluştur
2. Validator fonksiyonunu yaz
3. `validators/__init__.py`'ye ekle
4. `core_generator.py`'de kullan

### Yeni Lazy Loading Property Ekleme

1. `initializers.py`'ye initialize metodunu ekle
2. `lazy_loading.py`'ye property fonksiyonunu ekle
3. `core_generator.py`'de property'yi tanımla

## 🧪 Test

```python
# Modül testi
python -c "from modular_generator import SupremeHumanLevelDatasetGenerator; print('✅ Import başarılı')"

# Generator testi
python -c "from modular_generator import SupremeHumanLevelDatasetGenerator; g = SupremeHumanLevelDatasetGenerator(); print('✅ Generator başarılı')"

# Küçük dataset testi
python -c "from modular_generator import SupremeHumanLevelDatasetGenerator; g = SupremeHumanLevelDatasetGenerator(); dataset = g.generate_supreme_dataset(5); print(f'✅ {len(dataset)} senaryo üretildi')"
```

## 📈 Avantajlar

### Orijinal Dosyaya Göre:
- **Daha İyi Organizasyon**: Kod mantıklı modüllere ayrılmış
- **Kolay Bakım**: Her modül bağımsız olarak güncellenebilir
- **Daha İyi Test Edilebilirlik**: Her modül ayrı test edilebilir
- **Takım Çalışması**: Farklı geliştiriciler farklı modüllerde çalışabilir
- **Kod Tekrarını Azaltma**: Ortak fonksiyonlar utils'de
- **Konfigürasyon Yönetimi**: Ayarlar ayrı dosyada

### V3 Enhancement Özellikleri:
- **Memory Optimization**: Lazy loading ile bellek tasarrufu
- **20+ Kişilik Profili**: Gelişmiş arketip sistemi
- **7 Bilişsel Kalıp**: İleri düzey düşünme modelleri
- **3 Kültürel Bağlam**: Çok kültürlü destek
- **Zamansal Akıl Yürütme**: Geçmiş-şimdi-gelecek analizi
- **İnovasyon Çerçeveleri**: Design thinking, disruptive innovation
- **Ayrı Dosya Yapısı**: Lazy loading ve initialize metodları ayrı dosyalarda

### Performans:
- **Aynı Hız**: Orijinal script ile aynı performans
- **Memory Optimization**: Lazy loading korunmuş
- **Cache Sistemi**: Aynı cache mekanizması

## 🎉 Başarı!

Bu modüler yapı sayesinde:
- ✅ Kod daha okunabilir ve anlaşılır
- ✅ Bakım ve geliştirme kolaylaştı
- ✅ Takım çalışması mümkün hale geldi
- ✅ Test edilebilirlik arttı
- ✅ Genişletilebilirlik sağlandı
- ✅ V3 Enhancement özellikleri eklendi
- ✅ Ayrı dosya yapısı ile daha organize

**Orijinal işlevsellik %100 korundu!** 🚀 