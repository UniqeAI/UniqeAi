#!/usr/bin/env python3
"""
Basit AI test scripti - Terminal üzerinden AI'ya sorular sormak için
"""

import asyncio
import sys
import os
from datetime import datetime

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Sadece ai_endpoint_functions'ı import et
from app.services.ai_endpoint_functions import ai_endpoint_functions

class SimpleAITest:
    def __init__(self):
        self.session_id = f"TEST_SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_id = "test_user"
        
    async def test_functions(self):
        """Temel fonksiyonları test et"""
        print("🧪 AI Fonksiyon Testleri Başlatılıyor...")
        
        try:
            # 1. Fatura geçmişi testi
            print("\n1️⃣ Fatura Geçmişi Testi:")
            result = await ai_endpoint_functions.telekom_get_bill_history(user_id=1, limit=3)
            print(f"   ✅ Başarılı: {len(result.get('data', {}).get('bills', []))} fatura bulundu")
            
            # 2. Mevcut paket testi
            print("\n2️⃣ Mevcut Paket Testi:")
            result = await ai_endpoint_functions.telekom_get_current_package(user_id=1)
            package_name = result.get('data', {}).get('package_name', 'Bilinmiyor')
            print(f"   ✅ Başarılı: Aktif paket: {package_name}")
            
            # 3. Kalan kotalar testi
            print("\n3️⃣ Kalan Kotalar Testi:")
            result = await ai_endpoint_functions.telekom_get_remaining_quotas(user_id=1)
            internet_gb = result.get('data', {}).get('internet_remaining_gb', 0)
            print(f"   ✅ Başarılı: Kalan internet: {internet_gb} GB")
            
            # 4. Müşteri profili testi
            print("\n4️⃣ Müşteri Profili Testi:")
            result = await ai_endpoint_functions.telekom_get_customer_profile(user_id=1)
            customer_name = result.get('data', {}).get('name', 'Bilinmiyor')
            print(f"   ✅ Başarılı: Müşteri adı: {customer_name}")
            
            # 5. Sistem sağlık testi
            print("\n5️⃣ Sistem Sağlık Testi:")
            result = await ai_endpoint_functions.system_get_health()
            status = result.get('data', {}).get('status', 'unknown')
            print(f"   ✅ Başarılı: Sistem durumu: {status}")
            
            print("\n🎉 Tüm testler başarıyla tamamlandı!")
            
        except Exception as e:
            print(f"❌ Test hatası: {e}")
    
    async def interactive_chat(self):
        """İnteraktif sohbet modu"""
        print("\n💬 İnteraktif Sohbet Modu")
        print("Komutlar: 'quit' (çıkış), 'test' (fonksiyon testi), 'help' (yardım)")
        
        while True:
            try:
                user_input = input("\n💬 Siz: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Görüşürüz!")
                    break
                
                elif user_input.lower() == 'test':
                    await self.test_functions()
                    continue
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                # Basit anahtar kelime tabanlı yanıt
                response = await self.simple_response(user_input)
                print(f"🤖 AI: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Ctrl+C ile çıkılıyor...")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    async def simple_response(self, message: str):
        """Basit anahtar kelime tabanlı yanıt"""
        message_lower = message.lower()
        
        try:
            if "fatura" in message_lower:
                if "geçmiş" in message_lower:
                    result = await ai_endpoint_functions.telekom_get_bill_history(user_id=1, limit=3)
                    bills = result.get('data', {}).get('bills', [])
                    return f"Geçmiş faturalarınızı kontrol ettim. {len(bills)} adet fatura bulundu."
                else:
                    result = await ai_endpoint_functions.telekom_get_current_bill(user_id=1)
                    amount = result.get('data', {}).get('amount', 0)
                    return f"Mevcut faturanızı kontrol ettim. Tutar: {amount} TL"
            
            elif "paket" in message_lower:
                result = await ai_endpoint_functions.telekom_get_current_package(user_id=1)
                package_name = result.get('data', {}).get('package_name', 'Bilinmiyor')
                return f"Paket bilgilerinizi kontrol ettim. Aktif paketiniz: {package_name}"
            
            elif "kota" in message_lower or "kalan" in message_lower:
                result = await ai_endpoint_functions.telekom_get_remaining_quotas(user_id=1)
                internet_gb = result.get('data', {}).get('internet_remaining_gb', 0)
                return f"Kalan kotanızı kontrol ettim. İnternet: {internet_gb} GB kaldı."
            
            elif "müşteri" in message_lower or "profil" in message_lower:
                result = await ai_endpoint_functions.telekom_get_customer_profile(user_id=1)
                customer_name = result.get('data', {}).get('name', 'Bilinmiyor')
                return f"Müşteri profilinizi kontrol ettim. Adınız: {customer_name}"
            
            elif "sağlık" in message_lower or "durum" in message_lower:
                result = await ai_endpoint_functions.system_get_health()
                status = result.get('data', {}).get('status', 'unknown')
                return f"Sistem durumunu kontrol ettim. Durum: {status}"
            
            else:
                return "Merhaba! Size nasıl yardımcı olabilirim? Fatura, paket, kota, müşteri profili veya sistem durumu hakkında soru sorabilirsiniz."
                
        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {str(e)}"
    
    def show_help(self):
        """Yardım menüsü"""
        print(f"""
🤖 AI Test Terminal - Yardım

Komutlar:
- 'quit' veya 'exit': Çıkış
- 'test': Fonksiyon testleri
- 'help': Bu menü

Örnek Sorular:
- "Faturamı göster"
- "Geçmiş faturalarımı göster"
- "Paket bilgilerimi göster"
- "Kalan kotamı göster"
- "Müşteri profili göster"
- "Sistem durumunu kontrol et"

Sistem Bilgileri:
- Session ID: {self.session_id}
- User ID: {self.user_id}
        """)

async def main():
    """Ana fonksiyon"""
    test = SimpleAITest()
    
    print("🚀 AI Test Terminal Başlatıldı!")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Önce fonksiyon testlerini çalıştır
    await test.test_functions()
    
    # Sonra interaktif moda geç
    await test.interactive_chat()

if __name__ == "__main__":
    asyncio.run(main()) 