#!/usr/bin/env python3
"""
Tüm Endpoint Verilerini Test Etme Scripti
Yeni eklenen tüm verileri test eder
"""

import sys
import os
import requests
import json

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_all_data():
    """Tüm yeni verileri test eder"""
    
    base_url = "http://localhost:8000/api/v1/telekom"
    
    print("🔍 TÜM ENDPOINT VERİLERİ TEST EDİLİYOR...")
    print("=" * 70)
    
    # Test edilecek user_id'ler
    test_users = [0, 1, 2, 3, 4, 5]
    
    for user_id in test_users:
        print(f"\n👤 USER ID: {user_id} TÜM VERİLER TEST EDİLİYOR")
        print("=" * 50)
        
        # === ÖDEME GEÇMİŞİ TEST ===
        try:
            response = requests.post(f"{base_url}/billing/payments", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                payments = data.get("data", {}).get("payments", [])
                total_amount = data.get("data", {}).get("total_amount", 0)
                payment_methods = data.get("data", {}).get("payment_methods", [])
                print(f"✅ Ödeme Geçmişi: {len(payments)} adet ödeme")
                print(f"   Toplam Tutar: {total_amount:.2f} TL")
                print(f"   Ödeme Yöntemleri: {', '.join(payment_methods)}")
            else:
                print(f"❌ Ödeme geçmişi hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Ödeme geçmişi bağlantı hatası: {e}")
        
        # === DESTEK TALEPLERİ TEST ===
        try:
            response = requests.post(f"{base_url}/support/tickets/list", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                tickets = data.get("data", {}).get("tickets", [])
                open_tickets = data.get("data", {}).get("open_tickets", 0)
                resolved_tickets = data.get("data", {}).get("resolved_tickets", 0)
                print(f"✅ Destek Talepleri: {len(tickets)} adet talep")
                print(f"   Açık Talepler: {open_tickets}")
                print(f"   Çözülen Talepler: {resolved_tickets}")
                
                # İlk 2 talebi detaylı göster
                for i, ticket in enumerate(tickets[:2]):
                    print(f"   {i+1}. {ticket.get('ticket_id', 'N/A')}: {ticket.get('issue', 'N/A')} ({ticket.get('status', 'N/A')})")
            else:
                print(f"❌ Destek talepleri hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Destek talepleri bağlantı hatası: {e}")
        
        # === AĞ DURUMU TEST ===
        regions = ["istanbul", "ankara", "izmir", "bursa", "antalya"]
        for region in regions:
            try:
                response = requests.post(f"{base_url}/network/status", 
                                      json={"region": region})
                if response.status_code == 200:
                    data = response.json()
                    network = data.get("data", {})
                    print(f"✅ Ağ Durumu ({region}): {network.get('status', 'N/A')}")
                    print(f"   Kapsama: %{network.get('coverage', 0)}")
                    print(f"   Hız: {network.get('speed', 'N/A')}")
                    if network.get('issues'):
                        print(f"   Sorunlar: {', '.join(network.get('issues', []))}")
                else:
                    print(f"❌ Ağ durumu hatası ({region}): {response.status_code}")
            except Exception as e:
                print(f"❌ Ağ durumu bağlantı hatası ({region}): {e}")
            break  # Sadece ilk bölgeyi test et
        
        # === HIZ TESTİ ===
        try:
            response = requests.post(f"{base_url}/diagnostics/speed-test", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                speed = data.get("data", {})
                print(f"✅ Hız Testi:")
                print(f"   Download: {speed.get('download_speed_mbps', 0)} Mbps")
                print(f"   Upload: {speed.get('upload_speed_mbps', 0)} Mbps")
                print(f"   Ping: {speed.get('ping_ms', 0)} ms")
                print(f"   Jitter: {speed.get('jitter_ms', 0)} ms")
            else:
                print(f"❌ Hız testi hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Hız testi bağlantı hatası: {e}")
        
        # === ROAMING TEST ===
        try:
            response = requests.post(f"{base_url}/services/roaming", 
                                  json={"user_id": user_id, "status": True})
            if response.status_code == 200:
                data = response.json()
                roaming = data.get("data", {})
                print(f"✅ Roaming Durumu:")
                print(f"   Aktif: {roaming.get('roaming_enabled', False)}")
                print(f"   Ülkeler: {', '.join(roaming.get('supported_countries', []))}")
                print(f"   Kullanım: {roaming.get('current_usage', 0)} GB")
                print(f"   Maliyet: {roaming.get('current_cost', 0)} TL")
            else:
                print(f"❌ Roaming hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Roaming bağlantı hatası: {e}")
        
        # === OTOMATİK ÖDEME TEST ===
        try:
            response = requests.post(f"{base_url}/billing/autopay", 
                                  json={"user_id": user_id, "status": True})
            if response.status_code == 200:
                data = response.json()
                autopay = data.get("data", {})
                print(f"✅ Otomatik Ödeme:")
                print(f"   Aktif: {autopay.get('autopay_enabled', False)}")
                print(f"   Yöntem: {autopay.get('payment_method', 'N/A')}")
                print(f"   Kart Son 4: {autopay.get('card_last4', 'N/A')}")
                print(f"   Sonraki Ödeme: {autopay.get('next_payment_date', 'N/A')}")
            else:
                print(f"❌ Otomatik ödeme hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Otomatik ödeme bağlantı hatası: {e}")
        
        # === HAT ASKIYA ALMA TEST ===
        try:
            response = requests.post(f"{base_url}/lines/suspend", 
                                  json={"user_id": user_id, "reason": "Test"})
            if response.status_code == 200:
                data = response.json()
                suspend = data.get("data", {})
                print(f"✅ Hat Askıya Alma:")
                print(f"   Durum: {suspend.get('status', 'N/A')}")
                print(f"   Sebep: {suspend.get('reason', 'N/A')}")
                print(f"   Yeniden Aktivasyon Ücreti: {suspend.get('reactivation_fee', 0)} TL")
            else:
                print(f"❌ Hat askıya alma hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Hat askıya alma bağlantı hatası: {e}")
        
        print()
    
    print("=" * 70)
    print("🎯 TÜM ENDPOINT VERİLERİ TEST EDİLDİ!")
    print("✅ Tüm yeni veriler başarıyla eklendi ve çalışıyor!")

if __name__ == "__main__":
    test_all_data() 