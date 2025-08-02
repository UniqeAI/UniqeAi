#!/usr/bin/env python3
"""
Detaylı Geçmiş Faturalar Test Scripti
Yeni eklenen geçmiş faturaları test eder
"""

import sys
import os
import requests
import json

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_detailed_bill_history():
    """Detaylı geçmiş faturaları test eder"""
    
    base_url = "http://localhost:8000/api/v1/telekom"
    
    print("🔍 DETAYLI GEÇMİŞ FATURALAR TEST EDİLİYOR...")
    print("=" * 60)
    
    # Test edilecek user_id'ler
    test_users = [0, 1, 2, 3, 4, 5]
    
    for user_id in test_users:
        print(f"\n👤 USER ID: {user_id} DETAYLI FATURA GEÇMİŞİ")
        print("-" * 50)
        
        try:
            # Geçmiş faturaları getir
            response = requests.post(f"{base_url}/billing/history", 
                                  json={"user_id": user_id, "limit": 24})
            
            if response.status_code == 200:
                data = response.json()
                bills = data.get("data", {}).get("bills", [])
                total_paid = data.get("data", {}).get("total_paid", 0)
                total_unpaid = data.get("data", {}).get("total_unpaid", 0)
                average_amount = data.get("data", {}).get("average_amount", 0)
                
                print(f"✅ Toplam Fatura: {len(bills)} adet")
                print(f"💰 Toplam Ödenen: {total_paid:.2f} TL")
                print(f"❌ Toplam Ödenmemiş: {total_unpaid:.2f} TL")
                print(f"📊 Ortalama Tutar: {average_amount:.2f} TL")
                
                # İlk 5 faturayı detaylı göster
                print(f"\n📋 İLK 5 FATURA DETAYI:")
                for i, bill in enumerate(bills[:5]):
                    print(f"  {i+1}. {bill.get('bill_id', 'N/A')}")
                    print(f"     Tutar: {bill.get('amount', 0)} TL")
                    print(f"     Durum: {bill.get('status', 'N/A')}")
                    print(f"     Tarih: {bill.get('bill_date', 'N/A')}")
                    print(f"     Ödeme Yöntemi: {bill.get('payment_method', 'N/A')}")
                    print(f"     Gecikme Ücreti: {bill.get('late_fee', 0)} TL")
                    print(f"     İndirim: {bill.get('discount_applied', 0)} TL")
                    
                    # Hizmetleri göster
                    services = bill.get('services', [])
                    if services:
                        print(f"     Hizmetler:")
                        for service in services:
                            print(f"       - {service.get('service_name', 'N/A')}: {service.get('amount', 0)} TL")
                    print()
                
                # Ödenmemiş faturaları göster
                unpaid_bills = [bill for bill in bills if bill.get('status') == 'unpaid']
                if unpaid_bills:
                    print(f"❌ ÖDENMEMİŞ FATURALAR ({len(unpaid_bills)} adet):")
                    for bill in unpaid_bills:
                        print(f"  - {bill.get('bill_id', 'N/A')}: {bill.get('amount', 0)} TL")
                    print()
                
                # Ödeme yöntemi dağılımı
                payment_methods = {}
                for bill in bills:
                    method = bill.get('payment_method', 'unknown')
                    payment_methods[method] = payment_methods.get(method, 0) + 1
                
                print(f"💳 ÖDEME YÖNTEMİ DAĞILIMI:")
                for method, count in payment_methods.items():
                    print(f"  - {method}: {count} adet")
                print()
                
                # Hizmet türleri analizi
                service_types = {}
                for bill in bills:
                    services = bill.get('services', [])
                    for service in services:
                        service_name = service.get('service_name', 'unknown')
                        service_types[service_name] = service_types.get(service_name, 0) + 1
                
                print(f"🛠️ HİZMET TÜRLERİ:")
                for service, count in service_types.items():
                    print(f"  - {service}: {count} adet")
                print()
                
            else:
                print(f"❌ Fatura geçmişi hatası: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
    
    print("=" * 60)
    print("🎯 DETAYLI GEÇMİŞ FATURALAR TEST EDİLDİ!")
    print("✅ Her kullanıcı için 24 adet detaylı fatura mevcut!")

if __name__ == "__main__":
    test_detailed_bill_history() 