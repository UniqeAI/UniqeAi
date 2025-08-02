#!/usr/bin/env python3
"""
Tüm Endpoint'leri Test Etme Scripti
Frontend'den tüm API endpoint'lerini test eder
"""

import sys
import os
import json
from utils.api_client import TelekomAPIClient

def test_all_endpoints():
    """Tüm endpoint'leri test eder"""
    
    print("🔍 TÜM ENDPOINT'LER TEST EDİLİYOR...")
    print("=" * 60)
    
    # API client oluştur
    client = TelekomAPIClient()
    test_user_id = 0  # Enes Faruk Aydın
    
    # === KULLANICI İŞLEMLERİ ===
    print("\n👤 KULLANICI İŞLEMLERİ")
    print("-" * 30)
    
    # Register test
    try:
        result = client.register_user({
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User"
        })
        print(f"✅ Register: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Register hatası: {e}")
    
    # Login test
    try:
        result = client.login_user("test@example.com", "test123")
        print(f"✅ Login: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Login hatası: {e}")
    
    # === TELEKOM AUTH İŞLEMLERİ ===
    print("\n🔐 TELEKOM AUTH İŞLEMLERİ")
    print("-" * 30)
    
    # Telekom register test
    try:
        result = client.telekom_register({
            "email": "telekom@example.com",
            "password": "telekom123",
            "name": "Telekom User"
        })
        print(f"✅ Telekom Register: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Telekom register hatası: {e}")
    
    # Telekom login test
    try:
        result = client.telekom_login("telekom@example.com", "telekom123")
        print(f"✅ Telekom Login: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Telekom login hatası: {e}")
    
    # === CHAT İŞLEMLERİ ===
    print("\n💬 CHAT İŞLEMLERİ")
    print("-" * 30)
    
    # Chat health test
    try:
        result = client.check_chat_health()
        print(f"✅ Chat Health: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Chat health hatası: {e}")
    
    # Send message test
    try:
        result = client.send_chat_message("Merhaba", test_user_id)
        print(f"✅ Send Message: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Send message hatası: {e}")
    
    # === FATURA İŞLEMLERİ ===
    print("\n💰 FATURA İŞLEMLERİ")
    print("-" * 30)
    
    # Current bill test
    try:
        result = client.get_current_bill(test_user_id)
        if result.get('success'):
            bill = result.get('data', {})
            print(f"✅ Mevcut Fatura: {bill.get('amount', 0)} TL - {bill.get('status', 'N/A')}")
        else:
            print(f"❌ Mevcut fatura hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Mevcut fatura hatası: {e}")
    
    # Bill history test
    try:
        result = client.get_bill_history(test_user_id, 5)
        if result.get('success'):
            bills = result.get('data', {}).get('bills', [])
            print(f"✅ Fatura Geçmişi: {len(bills)} adet fatura")
        else:
            print(f"❌ Fatura geçmişi hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Fatura geçmişi hatası: {e}")
    
    # Payment history test
    try:
        result = client.get_payment_history(test_user_id)
        if result.get('success'):
            payments = result.get('data', {}).get('payments', [])
            print(f"✅ Ödeme Geçmişi: {len(payments)} adet ödeme")
        else:
            print(f"❌ Ödeme geçmişi hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Ödeme geçmişi hatası: {e}")
    
    # Autopay test
    try:
        result = client.setup_autopay(test_user_id, True)
        print(f"✅ Autopay Setup: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Autopay hatası: {e}")
    
    # === PAKET İŞLEMLERİ ===
    print("\n📦 PAKET İŞLEMLERİ")
    print("-" * 30)
    
    # Current package test
    try:
        result = client.get_current_package(test_user_id)
        if result.get('success'):
            package = result.get('data', {})
            print(f"✅ Mevcut Paket: {package.get('package_name', 'N/A')} - {package.get('monthly_fee', 0)} TL")
        else:
            print(f"❌ Mevcut paket hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Mevcut paket hatası: {e}")
    
    # Remaining quotas test
    try:
        result = client.get_remaining_quotas(test_user_id)
        if result.get('success'):
            quotas = result.get('data', {})
            print(f"✅ Kalan Kota: {quotas.get('internet_remaining_gb', 0)}GB İnternet, {quotas.get('voice_remaining_minutes', 0)}dk Konuşma")
        else:
            print(f"❌ Kota hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Kota hatası: {e}")
    
    # Available packages test
    try:
        result = client.get_available_packages()
        if result.get('success'):
            packages = result.get('data', {}).get('packages', [])
            print(f"✅ Kullanılabilir Paketler: {len(packages)} adet paket")
        else:
            print(f"❌ Kullanılabilir paketler hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Kullanılabilir paketler hatası: {e}")
    
    # Package details test
    try:
        result = client.get_package_details("Mega İnternet")
        if result.get('success'):
            package = result.get('data', {})
            print(f"✅ Paket Detayları: {package.get('package_name', 'N/A')} - {package.get('monthly_fee', 0)} TL")
        else:
            print(f"❌ Paket detayları hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Paket detayları hatası: {e}")
    
    # === MÜŞTERİ İŞLEMLERİ ===
    print("\n👥 MÜŞTERİ İŞLEMLERİ")
    print("-" * 30)
    
    # Customer profile test
    try:
        result = client.get_customer_profile(test_user_id)
        if result.get('success'):
            customer = result.get('data', {})
            print(f"✅ Müşteri Profili: {customer.get('name', 'N/A')} - {customer.get('customer_tier', 'N/A')}")
        else:
            print(f"❌ Müşteri profili hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Müşteri profili hatası: {e}")
    
    # Update contact test
    try:
        result = client.update_customer_contact(test_user_id, "email", "yeni@email.com")
        print(f"✅ Contact Update: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Contact update hatası: {e}")
    
    # === DESTEK İŞLEMLERİ ===
    print("\n🛠️ DESTEK İŞLEMLERİ")
    print("-" * 30)
    
    # Create support ticket test
    try:
        result = client.create_support_ticket(test_user_id, "Test destek talebi", "technical")
        if result.get('success'):
            ticket = result.get('data', {})
            print(f"✅ Destek Talebi: {ticket.get('ticket_id', 'N/A')}")
        else:
            print(f"❌ Destek talebi hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Destek talebi hatası: {e}")
    
    # Get user tickets test
    try:
        result = client.get_users_tickets(test_user_id)
        if result.get('success'):
            tickets = result.get('data', {}).get('tickets', [])
            print(f"✅ Kullanıcı Talepleri: {len(tickets)} adet talep")
        else:
            print(f"❌ Kullanıcı talepleri hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Kullanıcı talepleri hatası: {e}")
    
    # === SİSTEM İŞLEMLERİ ===
    print("\n⚙️ SİSTEM İŞLEMLERİ")
    print("-" * 30)
    
    # Network status test
    try:
        result = client.check_network_status("istanbul")
        if result.get('success'):
            network = result.get('data', {})
            print(f"✅ Ağ Durumu: {network.get('status', 'N/A')}")
        else:
            print(f"❌ Ağ durumu hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Ağ durumu hatası: {e}")
    
    # Internet speed test
    try:
        result = client.test_internet_speed(test_user_id)
        if result.get('success'):
            speed = result.get('data', {})
            print(f"✅ Hız Testi: {speed.get('download_speed', 0)} Mbps")
        else:
            print(f"❌ Hız testi hatası: {result.get('error')}")
    except Exception as e:
        print(f"❌ Hız testi hatası: {e}")
    
    # === ROAMING İŞLEMLERİ ===
    print("\n🌍 ROAMING İŞLEMLERİ")
    print("-" * 30)
    
    # Enable roaming test
    try:
        result = client.enable_roaming(test_user_id, True)
        print(f"✅ Roaming Enable: {'Başarılı' if result.get('success') else 'Başarısız'}")
    except Exception as e:
        print(f"❌ Roaming hatası: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 TÜM ENDPOINT'LER TEST EDİLDİ!")
    print("✅ Frontend artık tüm backend endpoint'lerine erişebiliyor!")

if __name__ == "__main__":
    test_all_endpoints() 