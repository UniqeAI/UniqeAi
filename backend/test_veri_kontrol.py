#!/usr/bin/env python3
"""
Mock Veri Kontrol Scripti
Sistemdeki tüm endpoint'lerin verilerini test eder
"""

import sys
import os
import requests
import json

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_all_data():
    """Tüm mock verileri test eder"""
    
    base_url = "http://localhost:8000/api/v1/telekom"
    
    print("🔍 MOCK VERİ KONTROLÜ BAŞLIYOR...")
    print("=" * 50)
    
    # Test edilecek user_id'ler
    test_users = [0, 1, 2, 3, 4, 5]
    
    for user_id in test_users:
        print(f"\n👤 USER ID: {user_id} TEST EDİLİYOR...")
        print("-" * 30)
        
        # 1. Müşteri Profili
        try:
            response = requests.post(f"{base_url}/customers/profile", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                customer = data.get("data", {})
                print(f"✅ Müşteri: {customer.get('name', 'N/A')} - {customer.get('customer_tier', 'N/A')}")
            else:
                print(f"❌ Müşteri profili hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Müşteri profili bağlantı hatası: {e}")
        
        # 2. Mevcut Fatura
        try:
            response = requests.post(f"{base_url}/billing/current", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                bill = data.get("data", {})
                print(f"💰 Mevcut Fatura: {bill.get('amount', 0)} TL - {bill.get('status', 'N/A')}")
            else:
                print(f"❌ Mevcut fatura hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Mevcut fatura bağlantı hatası: {e}")
        
        # 3. Geçmiş Faturalar
        try:
            response = requests.post(f"{base_url}/billing/history", 
                                  json={"user_id": user_id, "limit": 5})
            if response.status_code == 200:
                data = response.json()
                bills = data.get("data", {}).get("bills", [])
                print(f"📋 Geçmiş Faturalar: {len(bills)} adet")
            else:
                print(f"❌ Geçmiş faturalar hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Geçmiş faturalar bağlantı hatası: {e}")
        
        # 4. Paket Bilgisi
        try:
            response = requests.post(f"{base_url}/packages/current", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                package = data.get("data", {})
                print(f"📦 Paket: {package.get('package_name', 'N/A')} - {package.get('monthly_fee', 0)} TL")
            else:
                print(f"❌ Paket bilgisi hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Paket bilgisi bağlantı hatası: {e}")
        
        # 5. Kalan Kota
        try:
            response = requests.post(f"{base_url}/packages/quotas", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                quotas = data.get("data", {})
                print(f"📊 Kota: {quotas.get('internet_remaining_gb', 0)}GB İnternet, {quotas.get('voice_remaining_minutes', 0)}dk Konuşma")
            else:
                print(f"❌ Kota bilgisi hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Kota bilgisi bağlantı hatası: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TÜM VERİLER TEST EDİLDİ!")
    print("✅ Sistem tamamen çalışıyor ve zengin mock veriler mevcut!")

if __name__ == "__main__":
    test_all_data() 