#!/usr/bin/env python3
"""
POST Endpoint'lerini Test Etme Script'i
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000/api/v1/telekom"

def test_endpoint(endpoint: str, data: Dict[str, Any], description: str):
    """Endpoint'i test et ve sonucu göster"""
    print(f"\n{'='*60}")
    print(f"🔍 TEST: {description}")
    print(f"📡 Endpoint: {endpoint}")
    print(f"📤 Request: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print("✅ BAŞARILI!")
        else:
            print("❌ HATA!")
            
    except Exception as e:
        print(f"❌ HATA: {e}")
    
    print(f"{'='*60}")

def main():
    """Ana test fonksiyonu"""
    print("🚀 TELEKOM API POST ENDPOINT TESTLERİ")
    print("=" * 60)
    
    # Test verileri
    test_cases = [
        {
            "endpoint": "/customers/profile",
            "data": {"user_id": 0},
            "description": "Müşteri Profili (User 0 - Mehmet Demir)"
        },
        {
            "endpoint": "/customers/profile", 
            "data": {"user_id": 1},
            "description": "Müşteri Profili (User 1 - Ayşe Kaya)"
        },
        {
            "endpoint": "/billing/current",
            "data": {"user_id": 2},
            "description": "Fatura Bilgisi (User 2 - Ali Özkan)"
        },
        {
            "endpoint": "/billing/history",
            "data": {"user_id": 3, "limit": 6},
            "description": "Geçmiş Faturalar (User 3 - Fatma Şahin)"
        },
        {
            "endpoint": "/billing/payments",
            "data": {"user_id": 4},
            "description": "Ödeme Geçmişi (User 4 - Mustafa Yılmaz)"
        },
        {
            "endpoint": "/packages/current",
            "data": {"user_id": 0},
            "description": "Mevcut Paket (User 0 - Mehmet Demir)"
        },
        {
            "endpoint": "/packages/quotas",
            "data": {"user_id": 1},
            "description": "Kalan Kotalar (User 1 - Ayşe Kaya)"
        },
        {
            "endpoint": "/diagnostics/speed-test",
            "data": {"user_id": 2},
            "description": "Hız Testi (User 2 - Ali Özkan)"
        },
        {
            "endpoint": "/support/tickets",
            "data": {"user_id": 3, "issue_description": "İnternet hızı çok yavaş, yardım edin!"},
            "description": "Arıza Talebi (User 3 - Fatma Şahin)"
        },
        {
            "endpoint": "/packages/change",
            "data": {"user_id": 4, "new_package_name": "Öğrenci Dostu Tarife"},
            "description": "Paket Değişikliği (User 4 - Mustafa Yılmaz)"
        }
    ]
    
    # Her test case'i çalıştır
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔄 Test {i}/{len(test_cases)}")
        test_endpoint(
            test_case["endpoint"],
            test_case["data"], 
            test_case["description"]
        )
    
    print(f"\n🎉 TÜM TESTLER TAMAMLANDI!")
    print(f"📊 Toplam Test: {len(test_cases)}")

if __name__ == "__main__":
    main() 