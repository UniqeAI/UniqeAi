#!/usr/bin/env python3
"""
Kayıt API'sini test etmek için script
"""

import urllib.request
import json

def test_register_api():
    """Kayıt API'sini test et"""
    
    # Test verileri
    test_user = {
        "username": "Enes Aydın",
        "password": "testpass123",
        "email": "enes@example.com",
        "full_name": "Enes Aydın",
        "phone": "05551234567",
        "birth_date": "1990-01-01",
        "gender": "Erkek",
        "preferences": {
            "notes": "Test kullanıcısı"
        }
    }
    
    try:
        # Register isteği gönder
        data = json.dumps(test_user).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/user/register",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        
        print(f"Status Code: {response.getcode()}")
        print("Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if response.getcode() == 200:
            print("✅ Kayıt başarılı!")
            
            # Login test et
            login_data = {
                "username": "Enes Aydın",
                "password": "testpass123"
            }
            
            login_data_bytes = json.dumps(login_data).encode('utf-8')
            login_req = urllib.request.Request(
                "http://localhost:8000/api/v1/user/login",
                data=login_data_bytes,
                headers={"Content-Type": "application/json"}
            )
            
            login_response = urllib.request.urlopen(login_req)
            login_result = json.loads(login_response.read().decode())
            
            print(f"\nLogin Status Code: {login_response.getcode()}")
            print("Login Response:")
            print(json.dumps(login_result, indent=2, ensure_ascii=False))
            
            if login_response.getcode() == 200:
                print("✅ Login başarılı!")
            else:
                print("❌ Login başarısız!")
        else:
            print("❌ Kayıt başarısız!")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    test_register_api() 