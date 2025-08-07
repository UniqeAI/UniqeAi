# 🤖 ChoyrensAI Telekom Agent - Model Test Suite

Bu test suite, eğitilmiş Meta Llama 3 Instruct modelinizi kapsamlı ve profesyonel bir şekilde test etmenizi sağlar.

## 📋 Özellikler

- **Çoklu Test Senaryoları**: Temel konuşma, tool kullanımı, çoklu amaç, hata yönetimi ve karmaşık senaryolar
- **Otomatik Değerlendirme**: Yanıt kalitesi, tool kullanımı, anahtar kelime kontrolü
- **Detaylı Raporlama**: JSON formatında sonuçlar ve görsel tablolar
- **Performans Metrikleri**: Yanıt süresi, başarı oranı, kalite skorları
- **Hata Analizi**: Başarısız testlerin detaylı analizi

## 🚀 Kurulum

### Gereksinimler

```bash
pip install torch transformers rich bitsandbytes accelerate
```

### Model Yolu Ayarlama

`model_test_suite.py` dosyasında model yolunu güncelleyin:

```python
# Model yolu - eğitilmiş modelinizin yolunu buraya yazın
model_path = "UniqeAi/ai_model/final-model_v5_bf16"
```

## 🧪 Test Senaryoları

### 1. Temel Konuşma Testleri (BASIC)
- Selamlama ve genel bilgi sorguları
- Modelin temel konuşma yeteneğini test eder

### 2. Tool Kullanım Testleri (TOOL_USAGE)
- Fatura sorgulama, paket değiştirme, internet hız testi
- Modelin doğru tool'ları çağırma yeteneğini test eder

### 3. Çoklu Amaç Testleri (MULTI_INTENT)
- Birden fazla işlemi aynı anda yapma
- Modelin karmaşık istekleri anlama yeteneğini test eder

### 4. Hata Yönetimi Testleri (ERROR_HANDLING)
- Yanlış numara, teknik sorunlar
- Modelin hata durumlarını yönetme yeteneğini test eder

### 5. Karmaşık Senaryolar (COMPLEX)
- Karmaşık müşteri sorguları
- Modelin ileri seviye problem çözme yeteneğini test eder

## 📊 Çalıştırma

```bash
cd ai_model/scripts
python model_test_suite.py
```

## 📈 Sonuçlar

### Ekran Çıktısı
- Genel test özeti
- Test tipi bazlı sonuçlar
- Örnek başarılı ve başarısız testler

### JSON Dosyası
`test_results/` klasöründe timestamp ile kaydedilir:
- Detaylı test sonuçları
- Performans metrikleri
- Hata analizleri

### Metrikler
- **Toplam Test**: Çalıştırılan test sayısı
- **Başarılı Test**: Başarılı olan test sayısı
- **Başarı Oranı**: Başarılı testlerin yüzdesi
- **Ortalama Yanıt Süresi**: Model yanıt süreleri
- **Ortalama Kalite Skoru**: 0-100 arası kalite puanı

## 🎯 Kalite Değerlendirmesi

### Puanlama Sistemi (100 puan üzerinden)
- **Tool Kullanımı**: 40 puan
- **Anahtar Kelime Kontrolü**: 30 puan
- **Yanıt Uzunluğu**: 20 puan
- **Türkçe Karakter Kullanımı**: 10 puan

## 🔧 Özelleştirme

### Yeni Test Senaryoları Ekleme

```python
TestCase(
    type=TestType.COMPLEX,
    input_text="Yeni test senaryosu",
    expected_tools=["tool_name"],
    expected_keywords=["anahtar", "kelimeler"],
    description="Test açıklaması"
)
```

### Test Parametreleri

```python
# Model parametreleri
max_new_tokens=1024
temperature=0.7
top_p=0.9

# Test konfigürasyonu
enable_tool_testing=True
enable_metrics=True
save_results=True
```

## 📝 Örnek Çıktı

```
🤖 ChoyrensAI Telekom Agent - Model Test Suite
================================================================================

📊 TEST SONUÇLARI
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                              Genel Test Özeti                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Metrik                    │ Değer                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Toplam Test               │ 12                                              │
│ Başarılı Test             │ 10                                              │
│ Başarı Oranı              │ 83.3%                                           │
│ Ortalama Yanıt Süresi     │ 2.45s                                           │
│ Ortalama Kalite Skoru     │ 78.5/100                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🐛 Sorun Giderme

### Model Yükleme Hatası
- Model yolunun doğru olduğundan emin olun
- Gerekli bağımlılıkların yüklü olduğunu kontrol edin

### Tool Parse Hatası
- Tool çağrı formatının doğru olduğunu kontrol edin
- `tool_definitions.py` dosyasının mevcut olduğundan emin olun

### Bellek Hatası
- Model boyutunu küçültün (4-bit kuantizasyon kullanılıyor)
- Batch size'ı azaltın

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Log dosyalarını kontrol edin
2. Model yolunu doğrulayın
3. Bağımlılıkları güncelleyin

---

**Not**: Bu test suite, modelinizin performansını değerlendirmek için tasarlanmıştır. Sonuçlar modelinizin eğitim kalitesini ve veri setinin etkinliğini yansıtır. 