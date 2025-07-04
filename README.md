# Gün 2: Fine-tuning için Sentetik Veri Yapısı Tasarımı

Bu proje, Llama-3.1-8B-Instruct modelinin fine-tuning'i için sentetik veri yapısını tasarlar ve oluşturur.

## Proje Yapısı

```
├── data_structure.py              # Temel veri yapısı ve örnekler
├── extended_data_generator.py     # Genişletilmiş veri üreticisi (Telekom odaklı)
├── combine_datasets.py            # Veri setlerini birleştirme scripti
├── synthetic_training_data.json   # Temel sentetik veri seti (10 veri noktası)
├── extended_synthetic_data.json   # Genişletilmiş sentetik veri seti (37 veri noktası)
├── complete_training_dataset.json # Birleştirilmiş tam veri seti (47 veri noktası)
└── README.md                      # Bu dosya
```

## Veri Yapısı

Her veri noktası şu JSON formatında olacak:

```json
{
    "instruction": "Yapılacak işlemin açıklaması",
    "input": "Kullanıcı girdisi veya bağlam",
    "output": "<tool_code>print(backend_api.some_function(...))</tool_code>"
}
```

### Alan Açıklamaları

- **instruction**: Modelin ne yapması gerektiğini belirten talimat
- **input**: İşlem için gerekli girdi bilgileri
- **output**: Backend API çağrısını içeren kod bloğu (tool_code etiketleri içinde)

## Kullanım

### 1. Temel Veri Yapısı Oluşturma

```bash
python data_structure.py
```

Bu komut:
- 10 temel veri noktası oluşturur
- Veri yapısını doğrular
- `synthetic_training_data.json` dosyasına kaydeder

### 2. Genişletilmiş Veri Seti Oluşturma

```bash
python extended_data_generator.py
```

Bu komut:
- 37 genişletilmiş veri noktası oluşturur (16 Telekom odaklı dahil)
- 12 farklı kategoriyi kapsar
- `extended_synthetic_data.json` dosyasına kaydeder

### 3. Veri Setlerini Birleştirme

```bash
python combine_datasets.py
```

Bu komut:
- Tüm veri setlerini birleştirir
- Veri doğrulaması yapar
- `complete_training_dataset.json` dosyasına kaydeder (47 veri noktası)

## Veri Kategorileri

### **Genel E-Ticaret Kategorileri**

#### 1. Kullanıcı Yönetimi
- Kullanıcı arama ve filtreleme
- Kullanıcı istatistikleri
- Profil güncelleme

#### 2. Ürün Yönetimi
- Ürün arama ve filtreleme
- Ürün varyantları
- Ürün değerlendirmeleri

#### 3. Sipariş Yönetimi
- Sipariş geçmişi
- Sipariş iptal işlemleri
- Kargo takibi

#### 4. Analitik ve Raporlama
- Günlük satış raporları
- Kategori performans analizi
- Müşteri segmentasyonu

#### 5. Stok Yönetimi
- Düşük stok uyarıları
- Stok hareketleri
- Stok giriş işlemleri

#### 6. Promosyon Yönetimi
- Aktif kampanyalar
- Kupon kullanım istatistikleri
- Yeni kampanya oluşturma

#### 7. Müşteri Hizmetleri
- Destek talepleri
- Müşteri şikayetleri
- Ticket güncelleme

### **🚀 YENİ: Telekom Odaklı Kategoriler**

#### 8. Paket ve Tarife Yönetimi
- Mevcut paket sorgulama
- Paket değiştirme işlemleri
- Uygun paket önerileri
- Kota sorgulama

#### 9. Fatura Yönetimi
- Fatura detay sorgulama
- Ödeme durumu kontrolü
- Otomatik ödeme talimatları

#### 10. Teknik Destek ve Arıza
- Ağ durumu kontrolü
- Arıza kaydı oluşturma
- Sinyal gücü testleri

#### 11. Hat ve Numara Yönetimi
- Yeni hat açma başvuruları
- Hat dondurma işlemleri
- Numara taşıma durumu

#### 12. İnternet ve TV Hizmetleri
- Fiber alt yapı kontrolü
- TV kanal paketi yönetimi
- Modem ayar güncelleme

## Örnek Telekom Veri Noktası

```json
{
    "instruction": "Mevcut paketi kontrol et",
    "input": "Müşteri numarası 5551234567 olan abonenin mevcut paket bilgilerini getir",
    "output": "<tool_code>print(backend_api.get_customer_package('5551234567'))</tool_code>"
}
```

## Veri Doğrulama

Oluşturulan veri setleri otomatik olarak doğrulanır:

- Tüm gerekli alanların varlığı
- Veri tiplerinin doğruluğu
- tool_code etiketlerinin varlığı
- JSON formatının geçerliliği
- Benzersiz instruction türlerinin sayısı

## Veri Dağılımı İstatistikleri

📊 **Toplam: 47 veri noktası**
- Kullanıcı Yönetimi: 5 veri noktası (10.6%)
- Ürün Yönetimi: 6 veri noktası (12.8%)
- Sipariş Yönetimi: 5 veri noktası (10.6%)
- Analitik/Raporlama: 7 veri noktası (14.9%)
- Stok Yönetimi: 3 veri noktası (6.4%)
- Promosyon Yönetimi: 2 veri noktası (4.3%)
- Müşteri Hizmetleri: 3 veri noktası (6.4%)
- **🚀 Telekom Kategorileri: 16 veri noktası (34.0%)**

## Sonraki Adımlar

Bu veri yapısı, Gün 3'te fine-tuning işlemi için kullanılacaktır. Veri seti:

- Modelin backend API çağrıları yapmayı öğrenmesini sağlar
- Gerçekçi telekom müşteri hizmetleri senaryolarını kapsar
- Çeşitli işlem türlerini içerir
- Türkçe dil desteği sunar
- E-ticaret ve telekom domainlerini birleştirir

## Gereksinimler

- Python 3.7+
- json (standart kütüphane)
- typing (standart kütüphane)
- datetime (standart kütüphane)

## Çıktı Dosyaları

- `synthetic_training_data.json`: 10 temel veri noktası
- `extended_synthetic_data.json`: 37 genişletilmiş veri noktası (16 Telekom odaklı dahil)
- `complete_training_dataset.json`: 47 birleştirilmiş veri noktası

**🎯 Toplam: 47 fine-tuning veri noktası (16 tanesi Telekom odaklı)** 