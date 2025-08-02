#!/usr/bin/env python3
"""
Fatura Gösterme Test Scripti
"""

import requests
import json

def test_fatura_goster():
    """Fatura gösterme testi"""
    
    print("🧪 Fatura Gösterme Testi")
    print("=" * 40)
    
    # Test mesajları
    test_messages = [
        "Geçmiş faturalarımı göster",
        "Mevcut faturası göster",
        "Paket bilgilerimi göster",
        "Kalan kotamı göster"
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
                print(f"✅ Başarılı (Status: {response.status_code})")
                print(f"🤖 AI Yanıtı:")
                print(result.get('response', 'Yanıt yok'))
                
                # Araç çağrılarını kontrol et
                tool_calls = result.get('tool_calls', [])
                if tool_calls:
                    print(f"\n🔧 Çalıştırılan Araçlar:")
                    for tool in tool_calls:
                        arac_adi = tool.get('arac_adi', 'Bilinmiyor')
                        durum = tool.get('durum', 'Bilinmiyor')
                        print(f"   - {arac_adi}: {durum}")
                        
                        # Sonuç kontrolü
                        sonuc = tool.get('sonuc', {})
                        if sonuc and isinstance(sonuc, dict):
                            if 'data' in sonuc:
                                print(f"     📊 Veri bulundu: {len(sonuc['data'])} kayıt")
                            else:
                                print(f"     ⚠️ Veri yok")
                else:
                    print("   ⚠️ Hiç araç çağrılmadı")
                
            else:
                print(f"❌ Hata (Status: {response.status_code})")
                print(f"Hata Detayı: {response.text}")
                
        except Exception as e:
            print(f"❌ Hata: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_fatura_goster() 