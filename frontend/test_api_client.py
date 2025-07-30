#!/usr/bin/env python3
"""
API client'ı test etmek için script
"""

import sys
import os

# Utils klasörünü path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from utils.api_client import get_api_client, TelekomAPIClient
    print("✅ API client başarıyla import edildi")
    
    # API client instance'ı oluştur
    api_client = get_api_client()
    print("✅ API client instance oluşturuldu")
    
    # Metodları kontrol et
    methods = dir(api_client)
    print(f"✅ API client metodları: {methods}")
    
    # register_user metodunu kontrol et
    if hasattr(api_client, 'register_user'):
        print("✅ register_user metodu mevcut")
    else:
        print("❌ register_user metodu bulunamadı")
    
    # login_user metodunu kontrol et
    if hasattr(api_client, 'login_user'):
        print("✅ login_user metodu mevcut")
    else:
        print("❌ login_user metodu bulunamadı")
    
    # Test verisi
    test_data = {
        "username": "Test User",
        "password": "testpass123",
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "05551234567"
    }
    
    print(f"✅ Test verisi hazırlandı: {test_data}")
    
except ImportError as e:
    print(f"❌ Import hatası: {e}")
except Exception as e:
    print(f"❌ Hata: {e}") 