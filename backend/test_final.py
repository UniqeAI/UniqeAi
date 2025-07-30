#!/usr/bin/env python3
"""
Final Test Scripti
"""

import requests
import json

def test_final():
    """Final test"""
    
    print("🧪 Final Test - Geçmiş Faturalar")
    print("=" * 40)
    
    # Test mesajı
    message = "Geçmiş faturalarımı göster"
    
    print(f"📝 Test Mesajı: {message}")
    
    try:
        # Chat isteği gönder
        response = requests.post(
            "http://localhost:8000/api/v1/chat/",
            json={
                "message": message,
                "user_id": 1,
                "session_id": "final_test"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Başarılı (Status: {response.status_code})")
            print(f"🤖 AI Yanıtı: {result.get('response', 'Yanıt yok')}")
            
            # Araç çağrılarını kontrol et
            tool_calls = result.get('tool_calls', [])
            if tool_calls:
                print(f"🔧 Çalıştırılan Araçlar:")
                for tool in tool_calls:
                    arac_adi = tool.get('arac_adi', 'Bilinmiyor')
                    durum = tool.get('durum', 'Bilinmiyor')
                    print(f"   - {arac_adi}: {durum}")
                    
                    # Doğru araç çağrıldı mı kontrol et
                    if "get_past_bills" in arac_adi or "get_bill_history" in arac_adi:
                        print("   ✅ DOĞRU ARAÇ: Geçmiş faturalar için doğru araç çağrıldı!")
                    elif "get_current_bill" in arac_adi:
                        print("   ❌ YANLIŞ ARAÇ: Geçmiş faturalar için yanlış araç çağrıldı!")
                    else:
                        print(f"   ⚠️ BİLİNMEYEN ARAÇ: {arac_adi}")
            else:
                print("   ⚠️ Hiç araç çağrılmadı")
            
            # Güven puanı
            confidence = result.get('confidence', 0)
            print(f"🎯 Güven Puanı: {confidence}")
            
        else:
            print(f"❌ Hata (Status: {response.status_code})")
            print(f"Hata Detayı: {response.text}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_final() 