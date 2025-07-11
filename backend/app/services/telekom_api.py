import asyncio
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MusteriProfil:
    musteri_id: str
    telefon_numarasi: str
    ad_soyad: str
    email: str
    dogum_tarihi: str
    musteri_seviyesi: str  # standart, premium, vip
    kayit_tarihi: str
    son_odeme_tarihi: str
    toplam_borc: float
    aktif_paket: str
    kalan_veri: float  # GB
    kalan_dakika: int
    kalan_sms: int

@dataclass
class PaketDetay:
    paket_id: str
    paket_adi: str
    aylik_ucret: float
    veri_miktari: float  # GB
    dakika_miktari: int
    sms_miktari: int
    ozellikler: List[str]
    uygunluk: str  # standart, premium, vip

@dataclass
class FaturaDetay:
    fatura_id: str
    donem: str
    toplam_tutar: float
    odeme_durumu: str
    son_odeme_tarihi: str
    kalemler: List[Dict[str, Any]]

class TelekomAPIService:
    def __init__(self):
        self.musteri_veritabani = self._musteri_veritabanini_olustur()
        self.paket_veritabani = self._paket_veritabanini_olustur()
        self.fatura_veritabani = self._fatura_veritabanini_olustur()
        self.destek_talepleri = []
        
    def _musteri_veritabanini_olustur(self) -> Dict[str, MusteriProfil]:
        """Gerçekçi müşteri profilleri oluştur"""
        musteriler = {}
        
        # Örnek müşteri verileri
        ornek_musteriler = [
            {
                "telefon": "05321234567",
                "ad": "Ahmet Yılmaz",
                "email": "ahmet.yilmaz@email.com",
                "seviye": "premium"
            },
            {
                "telefon": "05339876543",
                "ad": "Ayşe Demir",
                "email": "ayse.demir@email.com", 
                "seviye": "standart"
            },
            {
                "telefon": "05355556666",
                "ad": "Mehmet Kaya",
                "email": "mehmet.kaya@email.com",
                "seviye": "vip"
            }
        ]
        
        for i, musteri in enumerate(ornek_musteriler):
            musteri_id = f"MUSTERI_{i+1:04d}"
            musteriler[musteri_id] = MusteriProfil(
                musteri_id=musteri_id,
                telefon_numarasi=musteri["telefon"],
                ad_soyad=musteri["ad"],
                email=musteri["email"],
                dogum_tarihi=f"19{random.randint(70, 90)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                musteri_seviyesi=musteri["seviye"],
                kayit_tarihi=f"202{random.randint(0, 3)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                son_odeme_tarihi=(datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                toplam_borc=random.uniform(0, 500),
                aktif_paket=f"Paket_{musteri['seviye'].upper()}",
                kalan_veri=random.uniform(0, 50),
                kalan_dakika=random.randint(0, 1000),
                kalan_sms=random.randint(0, 500)
            )
            
        return musteriler
    
    def _paket_veritabanini_olustur(self) -> Dict[str, PaketDetay]:
        """Kullanılabilir paketleri oluştur"""
        paketler = {
            "Paket_STANDART": PaketDetay(
                paket_id="PAKET_001",
                paket_adi="Standart Paket",
                aylik_ucret=89.90,
                veri_miktari=10.0,
                dakika_miktari=1000,
                sms_miktari=1000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi"],
                uygunluk="standart"
            ),
            "Paket_PREMIUM": PaketDetay(
                paket_id="PAKET_002", 
                paket_adi="Premium Paket",
                aylik_ucret=149.90,
                veri_miktari=25.0,
                dakika_miktari=2000,
                sms_miktari=2000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi", "Netflix Premium"],
                uygunluk="premium"
            ),
            "Paket_VIP": PaketDetay(
                paket_id="PAKET_003",
                paket_adi="VIP Paket", 
                aylik_ucret=299.90,
                veri_miktari=50.0,
                dakika_miktari=5000,
                sms_miktari=5000,
                ozellikler=["Sınırsız WhatsApp", "Sosyal Medya Paketi", "Netflix Premium", "HBO Max"],
                uygunluk="vip"
            )
        }
        return paketler
    
    def _fatura_veritabanini_olustur(self) -> Dict[str, List[FaturaDetay]]:
        """Fatura veritabanını oluştur"""
        fatura_veritabani = {}
        
        for musteri_id in self.musteri_veritabani.keys():
            fatura_listesi = []
            for ay in range(1, 13):
                fatura = FaturaDetay(
                    fatura_id=f"FATURA_{musteri_id}_{ay:02d}",
                    donem=f"2024-{ay:02d}",
                    toplam_tutar=random.uniform(80, 350),
                    odeme_durumu="odendi" if random.random() > 0.2 else "beklemede",
                    son_odeme_tarihi=f"2024-{ay:02d}-15",
                    kalemler=[
                        {"aciklama": "Aylık Paket Ücreti", "tutar": random.uniform(80, 300)},
                        {"aciklama": "Ek Veri Kullanımı", "tutar": random.uniform(0, 50)},
                        {"aciklama": "Ek Hizmetler", "tutar": random.uniform(0, 20)}
                    ]
                )
                fatura_listesi.append(fatura)
            fatura_veritabani[musteri_id] = fatura_listesi
            
        return fatura_veritabani

    async def musteri_profil_getir(self, telefon_numarasi: str) -> Optional[MusteriProfil]:
        """Kapsamlı müşteri profili ve geçmişi"""
        try:
            logger.info(f"Müşteri profili sorgulanıyor: {telefon_numarasi}")
            
            # Telefon numarasına göre müşteri bul
            for musteri in self.musteri_veritabani.values():
                if musteri.telefon_numarasi == telefon_numarasi:
                    logger.info(f"Müşteri bulundu: {musteri.ad_soyad}")
                    return musteri
            
            logger.warning(f"Müşteri bulunamadı: {telefon_numarasi}")
            return None
            
        except Exception as e:
            logger.error(f"Müşteri profili getirme hatası: {e}")
            raise

    async def mevcut_paket_detaylari(self, musteri_id: str) -> Optional[Dict[str, Any]]:
        """Mevcut paket kullanımı, kalan veri, faturalama"""
        try:
            logger.info(f"Paket detayları sorgulanıyor: {musteri_id}")
            
            if musteri_id not in self.musteri_veritabani:
                logger.warning(f"Müşteri bulunamadı: {musteri_id}")
                return None
                
            musteri = self.musteri_veritabani[musteri_id]
            paket = self.paket_veritabani.get(musteri.aktif_paket)
            
            if not paket:
                logger.warning(f"Paket bulunamadı: {musteri.aktif_paket}")
                return None
                
            paket_detaylari = {
                "musteri_bilgileri": {
                    "ad_soyad": musteri.ad_soyad,
                    "telefon": musteri.telefon_numarasi,
                    "musteri_seviyesi": musteri.musteri_seviyesi
                },
                "aktif_paket": {
                    "paket_adi": paket.paket_adi,
                    "aylik_ucret": paket.aylik_ucret,
                    "veri_miktari": paket.veri_miktari,
                    "dakika_miktari": paket.dakika_miktari,
                    "sms_miktari": paket.sms_miktari,
                    "ozellikler": paket.ozellikler
                },
                "kullanim_durumu": {
                    "kalan_veri": musteri.kalan_veri,
                    "kalan_dakika": musteri.kalan_dakika,
                    "kalan_sms": musteri.kalan_sms,
                    "veri_kullanimi_yuzdesi": ((paket.veri_miktari - musteri.kalan_veri) / paket.veri_miktari) * 100
                },
                "fatura_durumu": {
                    "toplam_borc": musteri.toplam_borc,
                    "son_odeme_tarihi": musteri.son_odeme_tarihi
                }
            }
            
            logger.info(f"Paket detayları başarıyla getirildi: {musteri_id}")
            return paket_detaylari
            
        except Exception as e:
            logger.error(f"Paket detayları getirme hatası: {e}")
            raise

    async def kullanilabilir_paketler(self, musteri_seviyesi: str = "standart") -> List[Dict[str, Any]]:
        """Müşteri profiline göre paket önerileri"""
        try:
            logger.info(f"Kullanılabilir paketler sorgulanıyor: {musteri_seviyesi}")
            
            uygun_paketler = []
            
            for paket in self.paket_veritabani.values():
                if paket.uygunluk == musteri_seviyesi or musteri_seviyesi == "vip":
                    paket_bilgisi = {
                        "paket_id": paket.paket_id,
                        "paket_adi": paket.paket_adi,
                        "aylik_ucret": paket.aylik_ucret,
                        "veri_miktari": paket.veri_miktari,
                        "dakika_miktari": paket.dakika_miktari,
                        "sms_miktari": paket.sms_miktari,
                        "ozellikler": paket.ozellikler,
                        "uygunluk": paket.uygunluk,
                        "oneri_puani": random.randint(70, 100)  # Simüle edilmiş öneri puanı
                    }
                    uygun_paketler.append(paket_bilgisi)
            
            # Fiyata göre sırala
            uygun_paketler.sort(key=lambda x: x["aylik_ucret"])
            
            logger.info(f"{len(uygun_paketler)} paket bulundu: {musteri_seviyesi}")
            return uygun_paketler
            
        except Exception as e:
            logger.error(f"Kullanılabilir paketler getirme hatası: {e}")
            raise

    async def paket_degisiklik_baslat(self, musteri_id: str, hedef_paket: str) -> Dict[str, Any]:
        """Çok adımlı paket değişikliği ve doğrulama"""
        try:
            logger.info(f"Paket değişikliği başlatılıyor: {musteri_id} -> {hedef_paket}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            if hedef_paket not in self.paket_veritabani:
                raise ValueError("Hedef paket bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            yeni_paket = self.paket_veritabani[hedef_paket]
            mevcut_paket = self.paket_veritabani[musteri.aktif_paket]
            
            # Paket değişikliği doğrulama
            if yeni_paket.aylik_ucret < mevcut_paket.aylik_ucret:
                # Düşük pakete geçiş için ek doğrulama
                if musteri.toplam_borc > 0:
                    raise ValueError("Borçlu müşteri düşük pakete geçemez")
            
            # Simüle edilmiş işlem süresi
            await asyncio.sleep(0.5)
            
            # Paket değişikliği başarılı
            musteri.aktif_paket = hedef_paket
            musteri.kalan_veri = yeni_paket.veri_miktari
            musteri.kalan_dakika = yeni_paket.dakika_miktari
            musteri.kalan_sms = yeni_paket.sms_miktari
            
            sonuc = {
                "durum": "basarili",
                "mesaj": f"Paket değişikliği başarıyla tamamlandı: {yeni_paket.paket_adi}",
                "eski_paket": mevcut_paket.paket_adi,
                "yeni_paket": yeni_paket.paket_adi,
                "yeni_aylik_ucret": yeni_paket.aylik_ucret,
                "gecerlilik_tarihi": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "islem_id": f"ISLEM_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            logger.info(f"Paket değişikliği başarılı: {sonuc['islem_id']}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Paket değişikliği hatası: {e}")
            raise

    async def fatura_detaylari_getir(self, musteri_id: str, ay: int) -> Optional[Dict[str, Any]]:
        """Detaylı fatura ve döküm"""
        try:
            logger.info(f"Fatura detayları sorgulanıyor: {musteri_id} - {ay}. ay")
            
            if musteri_id not in self.fatura_veritabani:
                logger.warning(f"Müşteri faturaları bulunamadı: {musteri_id}")
                return None
                
            fatura_listesi = self.fatura_veritabani[musteri_id]
            
            if ay < 1 or ay > len(fatura_listesi):
                logger.warning(f"Geçersiz ay: {ay}")
                return None
                
            fatura = fatura_listesi[ay - 1]
            musteri = self.musteri_veritabani[musteri_id]
            
            fatura_detaylari = {
                "fatura_bilgileri": {
                    "fatura_id": fatura.fatura_id,
                    "donem": fatura.donem,
                    "toplam_tutar": fatura.toplam_tutar,
                    "odeme_durumu": fatura.odeme_durumu,
                    "son_odeme_tarihi": fatura.son_odeme_tarihi
                },
                "musteri_bilgileri": {
                    "ad_soyad": musteri.ad_soyad,
                    "telefon": musteri.telefon_numarasi,
                    "email": musteri.email
                },
                "fatura_kalemleri": fatura.kalemler,
                "ozet": {
                    "toplam_kalem": len(fatura.kalemler),
                    "en_yuksek_kalem": max(fatura.kalemler, key=lambda x: x["tutar"]),
                    "odeme_gecmisi": "Düzenli" if fatura.odeme_durumu == "odendi" else "Gecikmeli"
                }
            }
            
            logger.info(f"Fatura detayları başarıyla getirildi: {fatura.fatura_id}")
            return fatura_detaylari
            
        except Exception as e:
            logger.error(f"Fatura detayları getirme hatası: {e}")
            raise

    async def destek_talep_olustur(self, musteri_id: str, sorun_kategorisi: str, aciklama: str) -> Dict[str, Any]:
        """Teknik destek talebi oluşturma"""
        try:
            logger.info(f"Destek talebi oluşturuluyor: {musteri_id} - {sorun_kategorisi}")
            
            if musteri_id not in self.musteri_veritabani:
                raise ValueError("Müşteri bulunamadı")
                
            musteri = self.musteri_veritabani[musteri_id]
            
            # Destek talebi oluştur
            talep_id = f"TALEP_{musteri_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            destek_talebi = {
                "talep_id": talep_id,
                "musteri_id": musteri_id,
                "musteri_adi": musteri.ad_soyad,
                "telefon": musteri.telefon_numarasi,
                "sorun_kategorisi": sorun_kategorisi,
                "aciklama": aciklama,
                "olusturma_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "durum": "beklemede",
                "oncelik": "normal" if musteri.musteri_seviyesi == "standart" else "yuksek",
                "tahmini_cozum_suresi": "24 saat" if musteri.musteri_seviyesi == "standart" else "4 saat"
            }
            
            self.destek_talepleri.append(destek_talebi)
            
            sonuc = {
                "durum": "basarili",
                "mesaj": "Destek talebi başarıyla oluşturuldu",
                "talep_id": talep_id,
                "tahmini_cozum_suresi": destek_talebi["tahmini_cozum_suresi"],
                "oncelik": destek_talebi["oncelik"]
            }
            
            logger.info(f"Destek talebi oluşturuldu: {talep_id}")
            return sonuc
            
        except Exception as e:
            logger.error(f"Destek talebi oluşturma hatası: {e}")
            raise

# Global servis örneği
telekom_api = TelekomAPIService() 