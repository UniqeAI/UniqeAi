# Telekom AI Asistanı

Bu uygulama, Telekom müşteri hizmetleri için geliştirilmiş AI destekli bir portal uygulamasıdır.

## Özellikler

- **Kullanıcı Kimlik Doğrulama**: Güvenli giriş sistemi
- **AI Sohbet Arayüzü**: Müşteri sorularına otomatik yanıt
- **Fatura Yönetimi**: Fatura görüntüleme ve ödeme
- **Kullanım İstatistikleri**: Veri ve konuşma kullanım raporları
- **Tarife Yönetimi**: Tarife görüntüleme ve değiştirme
- **Teknik Destek**: Bilet oluşturma ve takip
- **Destek Personeli Paneli**: Bilet yönetimi ve müşteri arama

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## Test Kullanıcıları

### Müşteri Hesabı:
- **Telefon**: 05321234567
- **Şifre**: Telekom123

### Destek Personeli:
- **E-posta**: support@telekom.com
- **Şifre**: Support123

## Kullanım

1. Tarayıcınızda `http://localhost:8501` adresine gidin
2. Test hesabı bilgileri ile giriş yapın
3. AI asistan ile sohbet edin veya hızlı aksiyonları kullanın

## Teknolojiler

- **Frontend**: Streamlit
- **Grafikler**: Plotly
- **Veri İşleme**: Pandas
- **Güvenlik**: SHA256 şifreleme 