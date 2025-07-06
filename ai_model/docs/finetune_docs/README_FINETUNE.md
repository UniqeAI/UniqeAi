# 🔥 Llama-3.1-8B Fine-tuning Rehberi

Bu klasörde bulunan scriptler ile Llama-3.1-8B-Instruct modelini Türkçe çağrı merkezi senaryoları için fine-tune edebilirsiniz.

## 📁 Dosya Yapısı

```
scripts/
├── run_finetune.py          # Ana fine-tuning scripti (tam özellikli)
├── quick_finetune.py        # Hızlı başlangıç scripti (basitleştirilmiş)
├── data_structure.py        # Veri yapısı oluşturma (Gün 2)
├── extended_data_generator.py # Genişletilmiş veri üretimi (Gün 2)  
├── combine_datasets.py      # Veri setlerini birleştirme (Gün 2)
├── turkish_preprocessing.py # Türkçe ön işleme (Gün 4)
└── README_FINETUNE.md       # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Sistem Gereksinimleri

**Minimum:**
- Python 3.8+
- 8GB RAM
- 10GB disk alanı

**Önerilen:**
- Python 3.10+
- NVIDIA GPU (8GB+ VRAM)
- 16GB RAM
- 50GB disk alanı

### 2. Paket Kurulumu

```bash
# Ana dizinden çalıştırın
pip install -r requirements.txt

# Opsiyonel: Flash Attention 2 (performans için)
pip install flash-attn --no-build-isolation
```

### 3. Veri Hazırlığı (Zaten Yapılmış)

Eğer daha önce yapılmamışsa:

```bash
cd ai_model/scripts
python data_structure.py
python extended_data_generator.py  
python combine_datasets.py
```

### 4. Fine-tuning Başlatma

**Seçenek A: Quick Start (Yeni Başlayanlar İçin)**
```bash
cd ai_model/scripts
python quick_finetune.py
```

**Seçenek B: Tam Kontrol**
```bash
cd ai_model/scripts
python run_finetune.py
```

## ⚙️ Konfigürasyon Seçenekleri

### GPU Bellek Ayarları

| GPU VRAM | Önerilen Ayar | Batch Size | Quantization |
|----------|---------------|------------|--------------|
| 4-6 GB   | 4-bit + LoRA  | 1          | Zorunlu      |
| 8-12 GB  | 4-bit + LoRA  | 1-2        | Önerilen     |
| 16+ GB   | 8-bit + LoRA  | 2-4        | Opsiyonel    |

### LoRA Parametreleri

```python
# Hafif fine-tuning (hızlı, az değişiklik)
lora_config = LoraConfig(r=8, lora_alpha=16)

# Orta fine-tuning (varsayılan)
lora_config = LoraConfig(r=16, lora_alpha=32)

# Ağır fine-tuning (yavaş, çok değişiklik)
lora_config = LoraConfig(r=32, lora_alpha=64)
```

### Eğitim Parametreleri

```python
# Hızlı test (1 epoch)
num_train_epochs=1, learning_rate=2e-4

# Standart (3 epoch) - Önerilen
num_train_epochs=3, learning_rate=1e-4

# Kapsamlı (5 epoch)
num_train_epochs=5, learning_rate=5e-5
```

## 📊 Veri Seti Bilgileri

### Mevcut Veri Seti
- **Dosya:** `../data/complete_training_dataset.json`
- **Boyut:** 47 veri noktası
- **Format:** Instruction-Input-Output
- **Dil:** Türkçe
- **Domain:** Çağrı merkezi + E-ticaret

### Veri Kategorileri
- 🏢 **Telekom (34.0%):** 16 veri noktası
- 🛒 **E-ticaret (66.0%):** 31 veri noktası
  - Kullanıcı yönetimi
  - Ürün yönetimi  
  - Sipariş yönetimi
  - Analitik/Raporlama
  - Stok yönetimi
  - Promosyon yönetimi
  - Müşteri hizmetleri

## 🔧 Sorun Giderme

### Yaygın Hatalar

**1. CUDA Out of Memory**
```
Çözüm: 
- Batch size'ı azaltın (per_device_train_batch_size=1)
- 4-bit quantization kullanın
- Gradient checkpointing aktif edin
```

**2. Import Errors**
```
Çözüm:
- pip install -r requirements.txt
- Python sürümünü kontrol edin (3.8+)
- Virtual environment kullanın
```

**3. Veri Dosyası Bulunamadı**
```
Çözüm:
- data_structure.py çalıştırın
- combine_datasets.py çalıştırın  
- Dosya yolunu kontrol edin
```

**4. Flash Attention Hatası**
```
Çözüm:
- flash-attn kaldırın: pip uninstall flash-attn
- Script'te attn_implementation="flash_attention_2" satırını kaldırın
```

### Log Dosyaları

Fine-tuning sırasında oluşturulan loglar:

```
scripts/
├── training_logs/
│   └── training_20240622_143022.log
├── fine_tuned_model/
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   ├── tokenizer.json
│   └── training_log.json
```

## 📈 Performans İpuçları

### 1. GPU Optimizasyonu
```python
# Flash Attention 2 kullanın (varsa)
attn_implementation="flash_attention_2"

# Gradient checkpointing
gradient_checkpointing=True

# BF16 precision
bf16=True
```

### 2. Veri Optimizasyonu
```python
# Packing kapatın (küçük veri seti için)
packing=False

# Max sequence length ayarlayın
max_seq_length=1024  # Veriye göre ayarlayın
```

### 3. Memory Management
```python
# Gradient accumulation kullanın
gradient_accumulation_steps=8

# Batch size küçük tutun
per_device_train_batch_size=1
```

## 🎯 Sonraki Adımlar

Fine-tuning tamamlandıktan sonra:

1. **Model Test Etme**
   ```bash
   python test_model.py
   ```

2. **Backend Entegrasyonu**
   - Model'i backend/app/ klasörüne kopyala
   - API endpoint'leri oluştur

3. **Frontend Entegrasyonu**
   - Streamlit arayüzü güncelle
   - Chat interface implement et

4. **Performans Değerlendirme**
   - BLEU score hesapla
   - Manuel değerlendirme yap
   - A/B test düzenle

## 🔗 İlgili Dosyalar

- `../data/README.md` - Veri seti detayları
- `../../backend/README.md` - Backend entegrasyon
- `../../docs/CALISTIRMA_VE_TEST_REHBERI.md` - Genel kullanım rehberi

## 📞 Destek

Sorularınız için:
- GitHub Issues
- Proje dokümantasyonu
- Team Slack kanalı 