# AI Model Sentetik Veri Seti

Bu klasör, Llama-3.1-8B-Instruct modelinin fine-tuning'i için oluşturulan sentetik veri setlerini içermektedir.

## Dosya Açıklamaları

### 📊 Veri Setleri

- **`complete_training_dataset.json`** - **ANA VERİ SETİ** (47 veri noktası)
  - Temel ve genişletilmiş veri setlerinin birleştirilmiş hali
  - Fine-tuning için hazır format
  - E-ticaret ve Telekom senaryolarını içerir

- **`synthetic_training_data.json`** - Temel veri seti (10 veri noktası)
  - İlk oluşturulan temel örnekler
  - Genel e-ticaret senaryoları

- **`extended_synthetic_data.json`** - Genişletilmiş veri seti (37 veri noktası)
  - 16 Telekom odaklı veri noktası dahil
  - 12 farklı kategoriyi kapsar

### 🗂️ Veri Kategorileri

#### **E-Ticaret Kategorileri**
- Kullanıcı Yönetimi
- Ürün Yönetimi  
- Sipariş Yönetimi
- Analitik ve Raporlama
- Stok Yönetimi
- Promosyon Yönetimi
- Müşteri Hizmetleri

#### **🚀 Telekom Kategorileri**
- Paket ve Tarife Yönetimi
- Fatura Yönetimi
- Teknik Destek ve Arıza
- Hat ve Numara Yönetimi
- İnternet ve TV Hizmetleri

## Veri Formatı

Her veri noktası şu formatı takip eder:

```json
{
    "instruction": "Yapılacak işlemin açıklaması",
    "input": "Kullanıcı girdisi veya bağlam", 
    "output": "<tool_code>print(backend_api.function_name(parameters))</tool_code>"
}
```

## Kullanım

Fine-tuning için `complete_training_dataset.json` dosyasını kullanın. Bu dosya:

- ✅ 47 çeşitli veri noktası
- ✅ Doğrulanmış format
- ✅ Backend API uyumlu
- ✅ Türkçe dil desteği
- ✅ Telekom domain odaklı

## İstatistikler

📈 **Toplam Veri Dağılımı:**
- Kullanıcı Yönetimi: 5 veri noktası (10.6%)
- Ürün Yönetimi: 6 veri noktası (12.8%) 
- Sipariş Yönetimi: 5 veri noktası (10.6%)
- Analitik/Raporlama: 7 veri noktası (14.9%)
- Stok Yönetimi: 3 veri noktası (6.4%)
- Promosyon Yönetimi: 2 veri noktası (4.3%)
- Müşteri Hizmetleri: 3 veri noktası (6.4%)
- **🎯 Telekom Kategorileri: 16 veri noktası (34.0%)**

Bu veri seti, AI/ML ekibinin Gün 2 görevinin başarılı şekilde tamamlanması sonucu oluşturulmuştur. 