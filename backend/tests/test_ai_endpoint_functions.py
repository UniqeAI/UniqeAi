"""
AI Endpoint Fonksiyonları Test Dosyası
"""

import asyncio
import sys
import os

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.services.ai_endpoint_functions import ai_endpoint_functions

async def test_chat_functions():
    """Chat API fonksiyonlarını test et"""
    print("=== CHAT API FONKSİYONLARI TEST ===")
    
    # Chat mesajı gönder
    print("\n1. Chat mesajı gönder:")
    result = await ai_endpoint_functions.ai_chat_send_message(
        message="Merhaba, fatura bilgilerimi öğrenmek istiyorum",
        user_id="test_user_123",
        session_id="test_session_456"
    )
    print(f"Sonuç: {result}")
    
    # Sistem durumu getir
    print("\n2. Sistem durumu getir:")
    result = await ai_endpoint_functions.ai_chat_get_system_status()
    print(f"Sonuç: {result}")
    
    # Oturum temizle
    print("\n3. Oturum temizle:")
    result = await ai_endpoint_functions.ai_chat_clear_session("test_session_456")
    print(f"Sonuç: {result}")

async def test_telekom_functions():
    """Telekom API fonksiyonlarını test et"""
    print("\n=== TELEKOM API FONKSİYONLARI TEST ===")
    
    # Müşteri profili getir
    print("\n1. Müşteri profili getir:")
    result = await ai_endpoint_functions.telekom_get_customer_profile(user_id=1)
    print(f"Sonuç: {result}")
    
    # Mevcut fatura getir
    print("\n2. Mevcut fatura getir:")
    result = await ai_endpoint_functions.telekom_get_current_bill(user_id=1)
    print(f"Sonuç: {result}")
    
    # Fatura geçmişi getir
    print("\n3. Fatura geçmişi getir:")
    result = await ai_endpoint_functions.telekom_get_bill_history(user_id=1, limit=5)
    print(f"Sonuç: {result}")
    
    # Fatura öde
    print("\n4. Fatura öde:")
    result = await ai_endpoint_functions.telekom_pay_bill(bill_id="F-2024-0001", method="credit_card")
    print(f"Sonuç: {result}")
    
    # Ödeme geçmişi getir
    print("\n5. Ödeme geçmişi getir:")
    result = await ai_endpoint_functions.telekom_get_payment_history(user_id=1)
    print(f"Sonuç: {result}")
    
    # Otomatik ödeme ayarla
    print("\n6. Otomatik ödeme ayarla:")
    result = await ai_endpoint_functions.telekom_setup_autopay(user_id=1, status=True)
    print(f"Sonuç: {result}")
    
    # Mevcut paket getir
    print("\n7. Mevcut paket getir:")
    result = await ai_endpoint_functions.telekom_get_current_package(user_id=1)
    print(f"Sonuç: {result}")
    
    # Kalan kotalar getir
    print("\n8. Kalan kotalar getir:")
    result = await ai_endpoint_functions.telekom_get_remaining_quotas(user_id=1)
    print(f"Sonuç: {result}")
    
    # Paket değiştir
    print("\n9. Paket değiştir:")
    result = await ai_endpoint_functions.telekom_change_package(user_id=1, new_package_name="Premium Paket")
    print(f"Sonuç: {result}")
    
    # Kullanılabilir paketler getir
    print("\n10. Kullanılabilir paketler getir:")
    result = await ai_endpoint_functions.telekom_get_available_packages()
    print(f"Sonuç: {result}")
    
    # Paket detayları getir
    print("\n11. Paket detayları getir:")
    result = await ai_endpoint_functions.telekom_get_package_details(package_name="Mega İnternet")
    print(f"Sonuç: {result}")
    
    # Roaming etkinleştir
    print("\n12. Roaming etkinleştir:")
    result = await ai_endpoint_functions.telekom_enable_roaming(user_id=1, status=True)
    print(f"Sonuç: {result}")
    
    # Ağ durumu kontrol et
    print("\n13. Ağ durumu kontrol et:")
    result = await ai_endpoint_functions.telekom_check_network_status(region="Istanbul")
    print(f"Sonuç: {result}")
    
    # Arıza talebi oluştur
    print("\n14. Arıza talebi oluştur:")
    result = await ai_endpoint_functions.telekom_create_support_ticket(
        user_id=1,
        issue_description="İnternet bağlantım yavaş",
        category="internet",
        priority="medium"
    )
    print(f"Sonuç: {result}")
    
    # Arıza talebi durumu getir
    print("\n15. Arıza talebi durumu getir:")
    result = await ai_endpoint_functions.telekom_get_support_ticket_status(ticket_id="T-2024-1")
    print(f"Sonuç: {result}")
    
    # İnternet hız testi
    print("\n16. İnternet hız testi:")
    result = await ai_endpoint_functions.telekom_test_internet_speed(user_id=1)
    print(f"Sonuç: {result}")
    
    # Müşteri iletişim bilgisi güncelle
    print("\n17. Müşteri iletişim bilgisi güncelle:")
    result = await ai_endpoint_functions.telekom_update_customer_contact(
        user_id=1,
        contact_type="email",
        new_value="yeni@email.com"
    )
    print(f"Sonuç: {result}")
    
    # Hat askıya al
    print("\n18. Hat askıya al:")
    result = await ai_endpoint_functions.telekom_suspend_line(user_id=1, reason="Geçici askıya alma")
    print(f"Sonuç: {result}")
    
    # Hat yeniden aktifleştir
    print("\n19. Hat yeniden aktifleştir:")
    result = await ai_endpoint_functions.telekom_reactivate_line(user_id=1)
    print(f"Sonuç: {result}")

async def test_mock_functions():
    """Mock test fonksiyonlarını test et"""
    print("\n=== MOCK TEST FONKSİYONLARI TEST ===")
    
    # Kullanıcı bilgileri getir
    print("\n1. Kullanıcı bilgileri getir:")
    result = await ai_endpoint_functions.mock_get_user_info(user_id=1)
    print(f"Sonuç: {result}")
    
    # Mevcut paketler getir
    print("\n2. Mevcut paketler getir:")
    result = await ai_endpoint_functions.mock_get_available_packages()
    print(f"Sonuç: {result}")
    
    # Fatura bilgileri getir
    print("\n3. Fatura bilgileri getir:")
    result = await ai_endpoint_functions.mock_get_invoice(user_id=1)
    print(f"Sonuç: {result}")
    
    # Müşteri bilgileri getir
    print("\n4. Müşteri bilgileri getir:")
    result = await ai_endpoint_functions.mock_get_customer_info(user_id=1)
    print(f"Sonuç: {result}")
    
    # Ödeme geçmişi getir
    print("\n5. Ödeme geçmişi getir:")
    result = await ai_endpoint_functions.mock_get_payment_history(user_id=1)
    print(f"Sonuç: {result}")
    
    # Abonelik durumu getir
    print("\n6. Abonelik durumu getir:")
    result = await ai_endpoint_functions.mock_get_subscription_status(user_id=1)
    print(f"Sonuç: {result}")
    
    # Destek talepleri getir
    print("\n7. Destek talepleri getir:")
    result = await ai_endpoint_functions.mock_get_support_tickets(user_id=1)
    print(f"Sonuç: {result}")
    
    # Adres bilgileri getir
    print("\n8. Adres bilgileri getir:")
    result = await ai_endpoint_functions.mock_get_address(user_id=1)
    print(f"Sonuç: {result}")
    
    # Kampanyalar getir
    print("\n9. Kampanyalar getir:")
    result = await ai_endpoint_functions.mock_get_campaigns()
    print(f"Sonuç: {result}")

async def main():
    """Ana test fonksiyonu"""
    print("🤖 AI ENDPOINT FONKSİYONLARI TEST BAŞLIYOR...")
    print("=" * 60)
    
    try:
        # Chat fonksiyonlarını test et
        await test_chat_functions()
        
        # Telekom fonksiyonlarını test et
        await test_telekom_functions()
        
        # Mock fonksiyonlarını test et
        await test_mock_functions()
        
        print("\n" + "=" * 60)
        print("✅ TÜM TESTLER BAŞARIYLA TAMAMLANDI!")
        print("🎉 AI endpoint fonksiyonları çalışıyor!")
        
    except Exception as e:
        print(f"\n❌ TEST HATASI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 