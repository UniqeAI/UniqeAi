# 🚀 UniqueAI Kurulum Rehberi

## 📋 Sistem Gereksinimleri

- **OS**: Windows 10/11
- **Python**: 3.8+
- **GPU**: NVIDIA RTX 4060 (8GB VRAM)
- **RAM**: 32GB (önerilen)
- **Disk**: 15GB boş alan

## 🔧 Kurulum Adımları

### 1. PyTorch + CUDA Kurulumu (RTX 4060 için)

```powershell
# PyTorch with CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. Diğer Kütüphaneleri Kurma

```powershell
# Requirements dosyasından kurulum
pip install -r requirements.txt
```

### 3. CUDA Kontrolü

```powershell
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

**Beklenen çıktı:**
```
PyTorch: 2.1.x+cu121
CUDA: True
```

## 🔑 Hugging Face Token Ayarları

### 1. Token Alma
- [Hugging Face Settings](https://huggingface.co/settings/tokens) adresine gidin
- "New token" oluşturun
- **Write** yetkisi verin

### 2. Token Ayarlama

**PowerShell:**
```powershell
$env:HUGGINGFACE_HUB_TOKEN = "hf_your_token_here"
```

**CMD:**
```cmd
set HUGGINGFACE_HUB_TOKEN=hf_your_token_here
```

## 🚀 Fine-tuning Başlatma

```powershell
# Klasöre git
cd "ai_model/scripts"

# Fine-tuning başlat
python QLORA_RTXU4060_FINAL.py
```

## 📊 Veri Setleri

- **Enhanced Dataset**: `data/telekom_training_dataset_enhanced.json` (1699 samples)
- **Original Dataset**: `data/telekom_training_dataset.json` (500 samples)

## 🔍 Test Etme

```powershell
# Mock backend ile test
python test_model_with_mock.py
```

## ⚠️ Sorun Giderme

### CUDA Bulunamıyor
```powershell
# NVIDIA sürücülerini güncelleyin
# PyTorch'u yeniden kurun
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Memory Hatası
- Batch size'ı azaltın (config'de)
- Diğer programları kapatın
- Gradient accumulation artırın

### Token Hatası
- Token'ın doğru ayarlandığından emin olun
- Write yetkisi olduğunu kontrol edin

## 📈 Beklenen Performans

- **Eğitim Süresi**: ~2-3 saat (1699 samples, 3 epochs)
- **VRAM Kullanımı**: ~6-7GB
- **Çıktı**: `./qlora_fine_tuned_model/` klasörü

## 🎯 Sonraki Adımlar

1. Fine-tuning tamamlandıktan sonra model test edin
2. Backend API'yi çalıştırın
3. Frontend'i başlatın
4. Entegrasyon testleri yapın 