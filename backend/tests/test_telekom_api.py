import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta

from app.services.telekom_api import (
    TelekomAPIService, 
    MusteriProfil, 
    PaketDetay, 
    FaturaDetay
)

class TestTelekomAPIService:
    @pytest.fixture
    def telekom_service(self):
        """Test için TelekomAPIService örneği"""
        return TelekomAPIService()
    
    @pytest.fixture
    def ornek_musteri_id(self):
        """Test için örnek müşteri ID"""
        return "MUSTERI_0001"
    
    @pytest.fixture
    def ornek_telefon(self):
        """Test için örnek telefon numarası"""
        return "05321234567"

    @pytest.mark.asyncio
    async def test_musteri_profil_getir_basarili(self, telekom_service, ornek_telefon):
        """Müşteri profili başarıyla getirilir"""
        musteri = await telekom_service.musteri_profil_getir(ornek_telefon)
        
        assert musteri is not None
        assert musteri.telefon_numarasi == ornek_telefon
        assert musteri.ad_soyad == "Ahmet Yılmaz"
        assert musteri.musteri_seviyesi == "premium"
        assert hasattr(musteri, 'musteri_id')
        assert hasattr(musteri, 'email')
        assert hasattr(musteri, 'toplam_borc')

    @pytest.mark.asyncio
    async def test_musteri_profil_getir_bulunamadi(self, telekom_service):
        """Var olmayan müşteri için None döner"""
        musteri = await telekom_service.musteri_profil_getir("99999999999")
        assert musteri is None

    @pytest.mark.asyncio
    async def test_mevcut_paket_detaylari_basarili(self, telekom_service, ornek_musteri_id):
        """Paket detayları başarıyla getirilir"""
        paket_detaylari = await telekom_service.mevcut_paket_detaylari(ornek_musteri_id)
        
        assert paket_detaylari is not None
        assert "musteri_bilgileri" in paket_detaylari
        assert "aktif_paket" in paket_detaylari
        assert "kullanim_durumu" in paket_detaylari
        assert "fatura_durumu" in paket_detaylari
        
        # Müşteri bilgileri kontrolü
        musteri_bilgileri = paket_detaylari["musteri_bilgileri"]
        assert "ad_soyad" in musteri_bilgileri
        assert "telefon" in musteri_bilgileri
        assert "musteri_seviyesi" in musteri_bilgileri
        
        # Aktif paket kontrolü
        aktif_paket = paket_detaylari["aktif_paket"]
        assert "paket_adi" in aktif_paket
        assert "aylik_ucret" in aktif_paket
        assert "veri_miktari" in aktif_paket
        assert "dakika_miktari" in aktif_paket
        assert "sms_miktari" in aktif_paket
        assert "ozellikler" in aktif_paket

    @pytest.mark.asyncio
    async def test_mevcut_paket_detaylari_musteri_bulunamadi(self, telekom_service):
        """Var olmayan müşteri için None döner"""
        paket_detaylari = await telekom_service.mevcut_paket_detaylari("VAR_OLMAYAN_MUSTERI")
        assert paket_detaylari is None

    @pytest.mark.asyncio
    async def test_kullanilabilir_paketler_standart(self, telekom_service):
        """Standart müşteri seviyesi için paketler getirilir"""
        paketler = await telekom_service.kullanilabilir_paketler("standart")
        
        assert len(paketler) > 0
        assert all(paket["uygunluk"] == "standart" for paket in paketler)
        
        # Fiyata göre sıralı olduğunu kontrol et
        fiyatlar = [paket["aylik_ucret"] for paket in paketler]
        assert fiyatlar == sorted(fiyatlar)

    @pytest.mark.asyncio
    async def test_kullanilabilir_paketler_premium(self, telekom_service):
        """Premium müşteri seviyesi için paketler getirilir"""
        paketler = await telekom_service.kullanilabilir_paketler("premium")
        
        assert len(paketler) > 0
        assert all(paket["uygunluk"] in ["standart", "premium"] for paket in paketler)

    @pytest.mark.asyncio
    async def test_kullanilabilir_paketler_vip(self, telekom_service):
        """VIP müşteri seviyesi için tüm paketler getirilir"""
        paketler = await telekom_service.kullanilabilir_paketler("vip")
        
        assert len(paketler) > 0
        # VIP müşteriler tüm paketleri görebilir
        assert len(paketler) >= 3  # En az 3 paket olmalı

    @pytest.mark.asyncio
    async def test_paket_degisiklik_baslat_basarili(self, telekom_service, ornek_musteri_id):
        """Paket değişikliği başarıyla başlatılır"""
        hedef_paket = "Paket_VIP"
        
        sonuc = await telekom_service.paket_degisiklik_baslat(ornek_musteri_id, hedef_paket)
        
        assert sonuc["durum"] == "basarili"
        assert "mesaj" in sonuc
        assert "eski_paket" in sonuc
        assert "yeni_paket" in sonuc
        assert "yeni_aylik_ucret" in sonuc
        assert "gecerlilik_tarihi" in sonuc
        assert "islem_id" in sonuc
        
        # Müşterinin paketinin güncellendiğini kontrol et
        musteri = telekom_service.musteri_veritabani[ornek_musteri_id]
        assert musteri.aktif_paket == hedef_paket

    @pytest.mark.asyncio
    async def test_paket_degisiklik_baslat_musteri_bulunamadi(self, telekom_service):
        """Var olmayan müşteri için hata fırlatır"""
        with pytest.raises(ValueError, match="Müşteri bulunamadı"):
            await telekom_service.paket_degisiklik_baslat("VAR_OLMAYAN_MUSTERI", "Paket_STANDART")

    @pytest.mark.asyncio
    async def test_paket_degisiklik_baslat_paket_bulunamadi(self, telekom_service, ornek_musteri_id):
        """Var olmayan paket için hata fırlatır"""
        with pytest.raises(ValueError, match="Hedef paket bulunamadı"):
            await telekom_service.paket_degisiklik_baslat(ornek_musteri_id, "VAR_OLMAYAN_PAKET")

    @pytest.mark.asyncio
    async def test_fatura_detaylari_getir_basarili(self, telekom_service, ornek_musteri_id):
        """Fatura detayları başarıyla getirilir"""
        fatura_detaylari = await telekom_service.fatura_detaylari_getir(ornek_musteri_id, 1)
        
        assert fatura_detaylari is not None
        assert "fatura_bilgileri" in fatura_detaylari
        assert "musteri_bilgileri" in fatura_detaylari
        assert "fatura_kalemleri" in fatura_detaylari
        assert "ozet" in fatura_detaylari
        
        # Fatura bilgileri kontrolü
        fatura_bilgileri = fatura_detaylari["fatura_bilgileri"]
        assert "fatura_id" in fatura_bilgileri
        assert "donem" in fatura_bilgileri
        assert "toplam_tutar" in fatura_bilgileri
        assert "odeme_durumu" in fatura_bilgileri
        assert "son_odeme_tarihi" in fatura_bilgileri
        
        # Fatura kalemleri kontrolü
        fatura_kalemleri = fatura_detaylari["fatura_kalemleri"]
        assert len(fatura_kalemleri) > 0
        assert all("aciklama" in kalem for kalem in fatura_kalemleri)
        assert all("tutar" in kalem for kalem in fatura_kalemleri)

    @pytest.mark.asyncio
    async def test_fatura_detaylari_getir_musteri_bulunamadi(self, telekom_service):
        """Var olmayan müşteri için None döner"""
        fatura_detaylari = await telekom_service.fatura_detaylari_getir("VAR_OLMAYAN_MUSTERI", 1)
        assert fatura_detaylari is None

    @pytest.mark.asyncio
    async def test_fatura_detaylari_getir_gecersiz_ay(self, telekom_service, ornek_musteri_id):
        """Geçersiz ay için None döner"""
        fatura_detaylari = await telekom_service.fatura_detaylari_getir(ornek_musteri_id, 13)
        assert fatura_detaylari is None

    @pytest.mark.asyncio
    async def test_destek_talep_olustur_basarili(self, telekom_service, ornek_musteri_id):
        """Destek talebi başarıyla oluşturulur"""
        sorun_kategorisi = "Teknik Sorun"
        aciklama = "İnternet bağlantısı yavaş"
        
        sonuc = await telekom_service.destek_talep_olustur(ornek_musteri_id, sorun_kategorisi, aciklama)
        
        assert sonuc["durum"] == "basarili"
        assert "mesaj" in sonuc
        assert "talep_id" in sonuc
        assert "tahmini_cozum_suresi" in sonuc
        assert "oncelik" in sonuc
        
        # Destek talebinin listeye eklendiğini kontrol et
        assert len(telekom_service.destek_talepleri) > 0
        son_talep = telekom_service.destek_talepleri[-1]
        assert son_talep["musteri_id"] == ornek_musteri_id
        assert son_talep["sorun_kategorisi"] == sorun_kategorisi
        assert son_talep["aciklama"] == aciklama

    @pytest.mark.asyncio
    async def test_destek_talep_olustur_musteri_bulunamadi(self, telekom_service):
        """Var olmayan müşteri için hata fırlatır"""
        with pytest.raises(ValueError, match="Müşteri bulunamadı"):
            await telekom_service.destek_talep_olustur("VAR_OLMAYAN_MUSTERI", "Test", "Test")

    @pytest.mark.asyncio
    async def test_musteri_veritabani_olusturma(self, telekom_service):
        """Müşteri veritabanı doğru oluşturulur"""
        assert len(telekom_service.musteri_veritabani) > 0
        
        # İlk müşteriyi kontrol et
        ilk_musteri_id = list(telekom_service.musteri_veritabani.keys())[0]
        musteri = telekom_service.musteri_veritabani[ilk_musteri_id]
        
        assert isinstance(musteri, MusteriProfil)
        assert musteri.musteri_id == ilk_musteri_id
        assert hasattr(musteri, 'telefon_numarasi')
        assert hasattr(musteri, 'ad_soyad')
        assert hasattr(musteri, 'email')
        assert hasattr(musteri, 'musteri_seviyesi')

    @pytest.mark.asyncio
    async def test_paket_veritabani_olusturma(self, telekom_service):
        """Paket veritabanı doğru oluşturulur"""
        assert len(telekom_service.paket_veritabani) > 0
        
        # Standart paketi kontrol et
        standart_paket = telekom_service.paket_veritabani.get("Paket_STANDART")
        assert standart_paket is not None
        assert isinstance(standart_paket, PaketDetay)
        assert standart_paket.paket_adi == "Standart Paket"
        assert standart_paket.aylik_ucret > 0
        assert standart_paket.veri_miktari > 0

    @pytest.mark.asyncio
    async def test_fatura_veritabani_olusturma(self, telekom_service):
        """Fatura veritabanı doğru oluşturulur"""
        assert len(telekom_service.fatura_veritabani) > 0
        
        # İlk müşterinin faturalarını kontrol et
        ilk_musteri_id = list(telekom_service.fatura_veritabani.keys())[0]
        faturalar = telekom_service.fatura_veritabani[ilk_musteri_id]
        
        assert len(faturalar) == 12  # 12 ay
        assert all(isinstance(fatura, FaturaDetay) for fatura in faturalar)
        
        # İlk faturayı kontrol et
        ilk_fatura = faturalar[0]
        assert "FATURA_" in ilk_fatura.fatura_id
        assert ilk_fatura.toplam_tutar > 0
        assert len(ilk_fatura.kalemler) > 0

    @pytest.mark.asyncio
    async def test_paket_degisiklik_borc_kontrolu(self, telekom_service):
        """Borçlu müşteri düşük pakete geçemez"""
        # Borçlu bir müşteri oluştur
        borclu_musteri_id = "BORCLU_MUSTERI"
        telekom_service.musteri_veritabani[borclu_musteri_id] = MusteriProfil(
            musteri_id=borclu_musteri_id,
            telefon_numarasi="05320000000",
            ad_soyad="Borçlu Müşteri",
            email="borclu@test.com",
            dogum_tarihi="1990-01-01",
            musteri_seviyesi="premium",
            kayit_tarihi="2020-01-01",
            son_odeme_tarihi="2024-01-15",
            toplam_borc=100.0,  # Borçlu
            aktif_paket="Paket_PREMIUM",
            kalan_veri=10.0,
            kalan_dakika=1000,
            kalan_sms=1000
        )
        
        # Düşük pakete geçmeye çalış
        with pytest.raises(ValueError, match="Borçlu müşteri düşük pakete geçemez"):
            await telekom_service.paket_degisiklik_baslat(borclu_musteri_id, "Paket_STANDART")

    @pytest.mark.asyncio
    async def test_destek_talep_oncelik_kontrolu(self, telekom_service, ornek_musteri_id):
        """Müşteri seviyesine göre öncelik belirlenir"""
        # Premium müşteri için destek talebi
        sonuc = await telekom_service.destek_talep_olustur(ornek_musteri_id, "Test", "Test")
        
        # Premium müşteri yüksek öncelik almalı
        assert sonuc["oncelik"] == "yuksek"
        assert sonuc["tahmini_cozum_suresi"] == "4 saat"

if __name__ == "__main__":
    pytest.main([__file__]) 