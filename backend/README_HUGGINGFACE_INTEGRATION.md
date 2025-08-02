# 🤖 Hugging Face Model Entegrasyonu

Bu doküman, UniqeAi-develop projesindeki Telekom AI Backend'inin Hugging Face modeli ile entegrasyonunu açıklamaktadır.

## 📋 Yapılan Değişiklikler

### 1. AI Orchestrator Güncellemesi (`backend/app/services/ai_orchestrator.py`)

- **LlamaInferenceService** simüle edilmiş servisi **HuggingFaceInferenceService** gerçek model servisi ile değiştirildi
- Model yükleme: `Choyrens/ChoyrensAI-Telekom-Agent-v1-merged`
- Quantization desteği: 4-bit BitsAndBytesConfig
- Tool calling parsing: advanced_playground.py'den uyarlandı
- Hata yönetimi ve fallback mekanizması eklendi

### 2. Yeni Özellikler

#### Model Yükleme
```python
# Quantization ayarları
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
```

#### System Prompt  
- Dinamik sistem promptu oluşturma
- Araç listesi otomatik entegrasyonu843905

- Türkçe dil desteği

#### Tool Calling Parsing
- `<|begin_of_tool_code|>` ... `<|end_of_tool_code|>` format desteği
- Parametre ayrıştırma ve tip dönüşümü
- JSON encoding/decoding

## 🚀 Kullanım

### Backend Başlatma

```bash
# Method 1: Start script ile
python backend/start_backend.py

# Method 2: Doğrudan uvicorn ile  
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test Etme

```bash
# Model entegrasyonu testi
python backend/test_huggingface_integration.py
```

### API Endpoints

- **Chat**: `POST /api/v1/chat/`
- **Health Check**: `GET /api/v1/chat/system/status`
- **Swagger UI**: `http://localhost:8000/docs`

## 📊 Sistem Durumu Kontrolü

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/chat/system/status")
print(response.json())
```

Örnek yanıt:
```json
{
    "success": true,
    "data": {
        "model_hizmeti": {
            "model_adi": "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged",
            "model_loaded": true
        },
        "arac_sayisi": 19
    }
}
```

## 💬 Chat API Kullanımı

```python
import requests

# Chat mesajı gönder
response = requests.post("http://localhost:8000/api/v1/chat/", json={
    "message": "Faturamı görmek istiyorum, müşteri ID: 1234",
    "user_id": "test_user"
})

print(response.json())
```

Örnek yanıt:
```json
{
    "success": true,
    "data": {
        "response": "Faturanızı kontrol ediyorum...",
        "confidence": 0.90,
        "tool_calls": [
            {
                "arac_adi": "get_current_bill",
                "durum": "tamamlandi"
            }
        ]
    }
}
```

## 🔧 Sorun Giderme

### Model Yüklenemezse

1. **CUDA Kontrolü**:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```

2. **Memory Kontrolü**:
   ```bash
   nvidia-smi
   ```

3. **Token Kontrolü**:
   ```bash
   huggingface-cli login
   ```

### Hata Logları

```bash
# Backend logları
tail -f backend/logs/app.log

# Systemd servisi olarak çalıştırıyorsanız
journalctl -u telekom-ai-backend -f
```

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **GPU**: RTX 4060 veya üzeri (8GB+ VRAM)
- **RAM**: 16GB+ sistem belleği
- **Python**: 3.8+
- **CUDA**: 12.1+

### Python Paketleri
```bash
pip install -r requirements.txt
```

Kritik paketler:
- `torch>=2.1.0`
- `transformers>=4.35.0`
- `bitsandbytes>=0.41.0`
- `accelerate>=0.25.0`

## 🎯 Performans Ayarları

### GPU Memory Optimization
```python
# Model yükleme sırasında
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

### Batch Size Ayarları
- **Development**: 1 (tek mesaj)
- **Production**: 2-4 (concurrent users)

## 🔮 Gelecek Geliştirmeler

- [ ] Model caching mekanizması
- [ ] Multi-GPU desteği
- [ ] Streaming response desteği
- [ ] Model swap (runtime'da model değiştirme)
- [ ] Metrics ve monitoring

## 📞 Destek

Entegrasyon sorunları için:
1. GitHub Issues oluşturun
2. Log dosyalarını paylaşın
3. System specs belirtin

---

**Not**: Bu entegrasyon, telekom-ai-integration-guide.md dosyasındaki gereksinimlere göre yapılmıştır. 