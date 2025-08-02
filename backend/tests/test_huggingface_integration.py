#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugging Face Model Entegrasyonu Test Scripti
"""

import asyncio
import logging
import sys
from pathlib import Path

# Project root'u ekle
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from app.services.ai_orchestrator import ai_orchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_model_loading():
    """Model yükleme testini yap"""
    print("🔄 Model yükleme testi başlatılıyor...")
    
    try:
        # Sistem durumunu kontrol et
        durum = await ai_orchestrator.sistem_durumu_getir()
        print(f"📊 Sistem Durumu:")
        print(f"   Model: {durum['model_hizmeti']['model_adi']}")
        print(f"   Model Yüklü: {durum['model_hizmeti']['model_loaded']}")
        print(f"   Araç Sayısı: {durum['arac_kaydi']['toplam_arac']}")
        
        return durum['model_hizmeti']['model_loaded']
        
    except Exception as e:
        logger.error(f"Model yükleme testi hatası: {e}")
        return False

async def test_simple_chat():
    """Basit chat testi yap"""
    print("\n💬 Basit chat testi başlatılıyor...")
    
    test_mesajlari = [
        "Merhaba, nasılsın?",
        "Faturamı görmek istiyorum. Müşteri ID: 1234",
        "Paket bilgilerimi öğrenebilir miyim?",
        "Arıza kaydı oluşturmak istiyorum"
    ]
    
    for mesaj in test_mesajlari:
        try:
            print(f"\n📤 Kullanıcı: {mesaj}")
            
            # Mesajı gönder
            sonuc = await ai_orchestrator.kullanici_mesaj_isle(
                mesaj=mesaj,
                kullanici_id="TEST_USER",
                oturum_id="TEST_SESSION"
            )
            
            print(f"🤖 AI: {sonuc['yanit']}")
            print(f"📊 Güven: {sonuc['guven_puani']:.2%}")
            print(f"🔧 Araç Sayısı: {len(sonuc['arac_cagrilari'])}")
            
            if sonuc['arac_cagrilari']:
                for arac in sonuc['arac_cagrilari']:
                    print(f"   📦 {arac['arac_adi']}: {arac['durum']}")
            
        except Exception as e:
            logger.error(f"Chat testi hatası: {e}")
            print(f"❌ Hata: {e}")

async def test_tool_calling():
    """Araç çağırma testini yap"""
    print("\n🔧 Araç çağırma testi başlatılıyor...")
    
    tool_test_messages = [
        "1234 numaralı müşterinin faturasını getir",
        "5678 ID'li kullanıcının paket bilgilerini göster",
        "9999 müşteri numarası için kota bilgilerini kontrol et"
    ]
    
    for mesaj in tool_test_messages:
        try:
            print(f"\n📤 Tool Test: {mesaj}")
            
            sonuc = await ai_orchestrator.kullanici_mesaj_isle(
                mesaj=mesaj,
                kullanici_id="TOOL_TEST_USER",
                oturum_id="TOOL_TEST_SESSION"
            )
            
            print(f"🤖 Yanıt: {sonuc['yanit'][:100]}...")
            print(f"🔧 Kullanılan Araçlar: {len(sonuc['arac_cagrilari'])}")
            
            for arac in sonuc['arac_cagrilari']:
                print(f"   📦 {arac['arac_adi']}: {arac['durum']}")
                if arac.get('sonuc'):
                    print(f"      ✅ Sonuç: {str(arac['sonuc'])[:50]}...")
            
        except Exception as e:
            logger.error(f"Tool calling testi hatası: {e}")
            print(f"❌ Hata: {e}")

async def main():
    """Ana test fonksiyonu"""
    print("🚀 Hugging Face Entegrasyon Testi Başlatılıyor\n")
    print("="*60)
    
    # 1. Model yükleme testi
    model_loaded = await test_model_loading()
    
    if not model_loaded:
        print("❌ Model yüklenemedi, testler devam edecek ancak simüle edilmiş yanıtlar alabilirsiniz.")
    else:
        print("✅ Model başarıyla yüklendi!")
    
    # 2. Basit chat testi
    await test_simple_chat()
    
    # 3. Tool calling testi
    await test_tool_calling()
    
    print("\n" + "="*60)
    print("🎉 Test tamamlandı!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        logger.error(f"Test sırasında beklenmeyen hata: {e}")
        sys.exit(1) 