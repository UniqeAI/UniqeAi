#!/usr/bin/env python3
"""
Chat API Test Scripti (Port 8001)
Backend chat endpoint'ini test eder
"""

import requests
import json

def test_chat_api():
    """Chat API'yi test eder"""
    
    print("🤖 CHAT API TEST EDİLİYOR (Port 8001)...")
    print("=" * 50)
    
    # Test mesajı
    test_data = {
        "message": "geçmiş faturalarımı göster",
        "user_id": 1
    }
    
    try:
        # Chat endpoint'ine istek gönder
        response = requests.post(
            "http://127.0.0.1:8001/api/v1/chat/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Başarılı yanıt:")
            print(f"   Yanıt: {result.get('response', 'N/A')}")
            
            # Araç çağrılarını kontrol et
            tool_calls = result.get('tool_calls', [])
            if tool_calls:
                print(f"🔧 Araç çağrıları: {len(tool_calls)} adet")
                for i, tool in enumerate(tool_calls):
                    print(f"   {i+1}. Araç: {tool.get('arac_adi', 'N/A')}")
                    print(f"      Parametreler: {tool.get('parametreler', {})}")
            else:
                print("⚠️ Araç çağrısı yapılmadı")
        else:
            print(f"❌ Hata: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend bağlantısı kurulamadı. Backend çalışıyor mu?")
    except Exception as e:
        print(f"❌ Genel hata: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 CHAT API TEST EDİLDİ!")

if __name__ == "__main__":
    test_chat_api() 