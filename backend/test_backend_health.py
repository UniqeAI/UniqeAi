#!/usr/bin/env python3
"""
Backend Health Check Scripti
Backend'in çalışıp çalışmadığını kontrol eder
"""

import requests

def test_backend_health():
    """Backend sağlık kontrolü"""
    
    print("🏥 BACKEND SAĞLIK KONTROLÜ...")
    print("=" * 40)
    
    try:
        # Health endpoint'ini kontrol et
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend çalışıyor!")
            result = response.json()
            print(f"   Mesaj: {result.get('message', 'N/A')}")
        else:
            print(f"❌ Backend hatası: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend bağlantısı kurulamadı")
    except Exception as e:
        print(f"❌ Genel hata: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 SAĞLIK KONTROLÜ TAMAMLANDI!")

if __name__ == "__main__":
    test_backend_health() 