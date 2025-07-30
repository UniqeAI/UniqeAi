#!/usr/bin/env python3
"""
Geçmiş Fatura Test Scripti
"""

import requests
import json

def test_gecmis_fatura():
    """Geçmiş fatura testi"""
    
    print("🧪 Geçmiş Fatura Testi")
    print("=" * 40)
    
    # Test mesajları
    test_messages = [
        "Geçmiş faturalarımı göster",
        "Geçmiş fatura bilgilerimi göster",
        "Önceki faturalarımı göster",
        "Fatura geçmişimi göster"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test #{i}: {message}")
        
        try:
            # Chat isteği gönder
            response = requests.post(
                "http://localhost:8000/api/v1/chat/",
                json={
                    "message": message,
                    "user_id": 1,
                    "session_id": f"test_session_{i}"
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Başarılı")
                print(f"🤖 AI Yanıtı: {result.get('yanit', 'Yanıt yok')}")
                
                # Araç çağrılarını kontrol et
                arac_cagrilari = result.get('arac_cagrilari', [])
                if arac_cagrilari:
                    print(f"🔧 Çalıştırılan Araçlar:")
                    for arac in arac_cagrilari:
                        arac_adi = arac.get('arac_adi', 'Bilinmiyor')
                        durum = arac.get('durum', 'Bilinmiyor')
                        print(f"   - {arac_adi}: {durum}")
                        
                        # Doğru araç çağrıldı mı kontrol et
                        if "get_past_bills" in arac_adi or "get_bill_history" in arac_adi:
                            print("   ✅ DOĞRU ARAÇ: Geçmiş faturalar için doğru araç çağrıldı!")
                        else:
                            print("   ❌ YANLIŞ ARAÇ: Geçmiş faturalar için yanlış araç çağrıldı!")
                else:
                    print("   ⚠️ Hiç araç çağrılmadı")
                
            else:
                print(f"❌ Hata (Status: {response.status_code})")
                print(f"Hata Detayı: {response.text}")
                
        except Exception as e:
            print(f"❌ Hata: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_gecmis_fatura() 