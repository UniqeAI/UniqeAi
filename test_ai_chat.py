#!/usr/bin/env python3
import urllib.request
import json
import time

def test_ai_chat():
    """AI chat endpoint'ini test et"""
    
    # Test mesajı
    test_data = {
        "message": "geçmiş faturalarım",
        "user_id": 1
    }
    
    try:
        # Request hazırla
        data = json.dumps(test_data).encode('utf-8')
        req = urllib.request.Request(
            'http://localhost:8000/api/v1/chat/',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print("🤖 AI Chat Testi Başlıyor...")
        print(f"📤 Gönderilen mesaj: {test_data['message']}")
        
        # Request gönder
        start_time = time.time()
        response = urllib.request.urlopen(req, timeout=30)
        end_time = time.time()
        
        # Response oku
        response_data = json.loads(response.read().decode())
        
        print(f"⏱️  Yanıt süresi: {end_time - start_time:.2f} saniye")
        print(f"📥 Yanıt: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_health():
    """Health endpoint'ini test et"""
    try:
        response = urllib.request.urlopen('http://localhost:8000/api/v1/health')
        health_data = json.loads(response.read().decode())
        print(f"🏥 Backend Durumu: {json.dumps(health_data, indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"❌ Health check hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Test Başlıyor...")
    print("=" * 50)
    
    # Health check
    test_health()
    print()
    
    # AI chat test
    test_ai_chat() 