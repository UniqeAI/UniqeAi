# 🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3 - MODULAR EDITION

Bu proje, orijinal `ULTIMATE_HUMAN_LEVEL_DATASET_GENERATOR_V3.py` dosyasının profesyonel modüler yapıya dönüştürülmüş halidir.

## 📁 Modüler Yapı

```
modular_generator/
├── __init__.py                 # Ana modül girişi
├── main.py                     # Çalıştırma dosyası
├── core_generator.py           # Ana generator sınıfı
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
│   ├── basic_scenarios.py     # Temel senaryolar
│   └── advanced_scenarios.py  # Gelişmiş senaryolar
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
cd ai_model/scripts
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
- **basic_scenarios.py**: Temel senaryolar (standard, tool_chaining, proactive, vb.)
- **advanced_scenarios.py**: Gelişmiş senaryolar (negotiation, teaching, innovation, vb.)

### `utils/`
- **helpers.py**: Yardımcı fonksiyonlar (mock data generation, user ID generation, vb.)

### `config/`
- **settings.py**: Konfigürasyon ayarları, API mapping, senaryo ağırlıkları

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

**Orijinal işlevsellik %100 korundu!** 🚀 