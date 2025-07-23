---
name: API Senkronizasyon Görevi
about: Backend API değişiklikleri sonrası sentetik veri seti güncelleme görevi
title: "[API-SYNC] AI/ML veri setini Backend API v{VERSION} ile senkronize et"
labels: ai-model, enhancement, blocked
assignees: ''

---

## 📋 Görev Tanımı

Bu issue, Backend ekibinin API tasarımını kesinleştirmesi sonrası AI/ML sentetik veri setinin güncellenmesi için açılmıştır.

## 🎯 Hedef

Sentetik veri setini Backend API v{VERSION} ile uyumlu hale getirmek.

## ✅ Kontrol Listesi

### Backend API Analizi
- [ ] Yeni API dokümantasyonunu incele
- [ ] Fonksiyon adı değişikliklerini tespit et
- [ ] Parametre yapısı değişikliklerini tespit et
- [ ] Yeni eklenen fonksiyonları belirle
- [ ] Kaldırılan fonksiyonları belirle

### Veri Seti Güncelleme
- [ ] `ai_model/scripts/api_mapping.py` dosyasındaki API_MAP'i güncelle
- [ ] Yeni fonksiyonlar için sentetik veri örnekleri oluştur
- [ ] Kaldırılan fonksiyonlara ait veri noktalarını temizle
- [ ] Veri doğrulama testlerini çalıştır

### Versiyonlama
- [ ] README.md'de sürüm numarasını v{VERSION}'a güncelle
- [ ] Değişiklik logunu güncelle
- [ ] Önceki sürümü yedekle

### Test ve Doğrulama
- [ ] Güncellenmiş veri seti ile fine-tuning testi yap
- [ ] Backend mock API ile entegrasyon testi yap
- [ ] Veri kalitesini doğrula

## 🔗 Bağımlılıklar

- **Beklenilen Issue:** Backend API v{VERSION} tasarımının tamamlanması
- **Engellenen İssue:** Fine-tuning pipeline'ının güncellenmesi

## 📅 Tahmini Süre

- **Analiz:** 2 saat
- **Güncelleme:** 4 saat  
- **Test:** 2 saat
- **Toplam:** 1 gün

## 🎯 Başarı Kriterleri

- [ ] Tüm sentetik veri noktaları yeni API ile uyumlu
- [ ] Veri doğrulama testleri geçiyor
- [ ] Backend ekibi API uyumluluğunu onayladı
- [ ] Dokümantasyon güncel

## 📝 Notlar

Bu görev, backend API kesinleştikten sonra otomatik olarak başlatılacaktır. API değişiklikleri minimum olduğu durumda, sadece `api_mapping.py` dosyasının güncellenmesi yeterli olabilir. 