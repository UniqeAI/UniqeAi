#!/usr/bin/env python3
"""
Chat API Test Scripti
"""

import requests
import json
import time

def test_chat_api():
    """Chat API'sini test et"""
    
    base_url = "http://localhost:8000"
    
    # Test mesajları
    test_messages = [
        "Geçmiş faturalarımı göster",
        "Paket bilgilerimi göster", 
        "Kalan kotamı göster",
        "Müşteri profili göster",
        "Sistem durumunu kontrol et"
    ]
    
    print("🤖 AI Chat API Testi Başlatılıyor...")
    print(f"📍 Backend URL: {base_url}")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test #{i}: {message}")
        
        try:
            # Chat isteği gönder
            response = requests.post(
                f"{base_url}/api/v1/chat/",
                json={
                    "message": message,
                    "user_id": 1,
                    "session_id": f"test_session_{int(time.time())}"
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Başarılı (Status: {response.status_code})")
                print(f"🤖 AI Yanıtı: {result.get('yanit', 'Yanıt yok')}")
                
                # Araç çağrılarını göster
                arac_cagrilari = result.get('arac_cagrilari', [])
                if arac_cagrilari:
                    print(f"🔧 Çalıştırılan Araçlar:")
                    for arac in arac_cagrilari:
                        print(f"   - {arac.get('arac_adi', 'Bilinmiyor')}: {arac.get('durum', 'Bilinmiyor')}")
                
                # Güven puanını göster
                guven_puani = result.get('guven_puani', 0)
                print(f"🎯 Güven Puanı: {guven_puani:.2f}")
                
            else:
                print(f"❌ Hata (Status: {response.status_code})")
                print(f"Hata Detayı: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Bağlantı Hatası: {e}")
        except Exception as e:
            print(f"❌ Beklenmeyen Hata: {e}")
        
        print("-" * 30)
        time.sleep(1)  # Kısa bekleme
    
    print("\n🎉 Test tamamlandı!")

def test_health_check():
    """Sistem sağlık kontrolü"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        if response.status_code == 200:
            print("✅ Sistem sağlık kontrolü başarılı")
            return True
        else:
            print(f"❌ Sistem sağlık kontrolü başarısız: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Sistem sağlık kontrolü hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Chat API Test Scripti")
    print("=" * 50)
    
    # Önce sağlık kontrolü
    if test_health_check():
        test_chat_api()
    else:
        print("❌ Backend çalışmıyor. Lütfen backend'i başlatın.") 