#!/usr/bin/env python3
"""
AI Chat Session Token Test Scripti
AI'nin session token ile doğru çalışıp çalışmadığını test eder
"""

import sys
import os
import asyncio

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

async def test_ai_chat_session():
    """AI chat'i session token ile test eder"""
    
    try:
        from app.services.ai_orchestrator_real import ai_orchestrator
        
        print("🤖 AI CHAT SESSION TOKEN TEST EDİLİYOR...")
        print("=" * 60)
        
        # Test mesajları
        test_messages = [
            "geçmiş faturalarımı göster",
            "mevcut faturası",
            "paketlerim",
            "kalan kotam"
        ]
        
        for message in test_messages:
            print(f"\n📝 Test mesajı: {message}")
            print("-" * 40)
            
            try:
                # AI orkestratör ile mesajı işle
                result = await ai_orchestrator.kullanici_mesaj_isle(
                    mesaj=message,
                    kullanici_id="test_user",
                    oturum_id="test_session"
                )
                
                print(f"✅ AI Yanıtı: {result.get('yanit', 'N/A')}")
                
                # Araç çağrılarını kontrol et
                arac_cagrilari = result.get('arac_cagrilari', [])
                if arac_cagrilari:
                    print(f"🔧 Araç çağrıları: {len(arac_cagrilari)} adet")
                    for i, arac in enumerate(arac_cagrilari):
                        print(f"   {i+1}. Araç: {arac.arac_adi}")
                        print(f"      Parametreler: {arac.parametreler}")
                        print(f"      Durum: {arac.durum}")
                        if arac.sonuc:
                            print(f"      Sonuç: {arac.sonuc}")
                else:
                    print("⚠️ Araç çağrısı yapılmadı")
                    
            except Exception as e:
                print(f"❌ Hata: {e}")
        
        print("\n" + "=" * 60)
        print("🎯 AI CHAT SESSION TOKEN TEST EDİLDİ!")
        
    except ImportError as e:
        print(f"❌ Import hatası: {e}")
    except Exception as e:
        print(f"❌ Genel hata: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_chat_session()) 