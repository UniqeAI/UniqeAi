#!/usr/bin/env python3
"""
Gelişmiş AI Chat Terminal - Terminal üzerinden AI'ya sorular sormak için
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

class AIChatTerminal:
    def __init__(self):
        self.session_id = f"CHAT_SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_id = "terminal_user"
        self.conversation_count = 0
        
    async def test_all_functions(self):
        """Tüm fonksiyonları test et"""
        print("🧪 Tüm AI Fonksiyonları Test Ediliyor...")
        
        tests = [
            ("Fatura Geçmişi", "telekom_get_bill_history", {"user_id": 1, "limit": 3}),
            ("Mevcut Fatura", "telekom_get_current_bill", {"user_id": 1}),
            ("Mevcut Paket", "telekom_get_current_package", {"user_id": 1}),
            ("Kalan Kotalar", "telekom_get_remaining_quotas", {"user_id": 1}),
            ("Müşteri Profili", "telekom_get_customer_profile", {"user_id": 1}),
            ("Sistem Sağlık", "system_get_health", {}),
            ("Ağ Durumu", "telekom_get_network_status", {"user_id": 1}),
            ("İnternet Hız Testi", "telekom_run_speed_test", {"user_id": 1}),
            ("Arıza Kayıtları", "telekom_get_trouble_tickets", {"user_id": 1}),
            ("Ödeme Geçmişi", "telekom_get_payment_history", {"user_id": 1}),
        ]
        
        success_count = 0
        total_count = len(tests)
        
        for i, (test_name, func_name, params) in enumerate(tests, 1):
            try:
                print(f"\n{i:2d}. {test_name} Testi:")
                
                # Fonksiyonu çağır
                func = getattr(ai_endpoint_functions, func_name)
                result = await func(**params)
                
                if result.get('success'):
                    print(f"   ✅ Başarılı")
                    success_count += 1
                else:
                    print(f"   ❌ Başarısız: {result.get('error', 'Bilinmeyen hata')}")
                    
            except Exception as e:
                print(f"   ❌ Hata: {e}")
        
        print(f"\n🎯 Test Sonucu: {success_count}/{total_count} başarılı")
        return success_count == total_count
    
    async def chat_with_ai(self, message: str):
        """AI ile sohbet et"""
        self.conversation_count += 1
        
        try:
            # Anahtar kelime tabanlı yanıt sistemi
            response = await self.intelligent_response(message)
            
            print(f"\n🤖 AI (Mesaj #{self.conversation_count}):")
            print(f"   {response}")
            
            return response
            
        except Exception as e:
            error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}"
            print(f"\n❌ Hata: {error_msg}")
            return error_msg
    
    async def intelligent_response(self, message: str):
        """Akıllı yanıt sistemi"""
        message_lower = message.lower()
        
        # Fatura ile ilgili sorular
        if any(word in message_lower for word in ["fatura", "bill"]):
            if any(word in message_lower for word in ["geçmiş", "history", "önceki", "eski"]):
                result = await ai_endpoint_functions.telekom_get_bill_history(user_id=1, limit=5)
                bills = result.get('data', {}).get('bills', [])
                if bills:
                    response = f"Geçmiş faturalarınızı kontrol ettim. {len(bills)} adet fatura bulundu:\n"
                    for i, bill in enumerate(bills[:3], 1):
                        amount = bill.get('amount', 0)
                        date = bill.get('date', 'Bilinmiyor')
                        response += f"   {i}. {date}: {amount} TL\n"
                    return response
                else:
                    return "Geçmiş faturalarınızı kontrol ettim ancak fatura bulunamadı."
            else:
                result = await ai_endpoint_functions.telekom_get_current_bill(user_id=1)
                bill_data = result.get('data', {})
                amount = bill_data.get('amount', 0)
                due_date = bill_data.get('due_date', 'Bilinmiyor')
                return f"Mevcut faturanızı kontrol ettim:\n   Tutar: {amount} TL\n   Son Ödeme: {due_date}"
        
        # Paket ile ilgili sorular
        elif any(word in message_lower for word in ["paket", "tarife", "package"]):
            result = await ai_endpoint_functions.telekom_get_current_package(user_id=1)
            package_data = result.get('data', {})
            package_name = package_data.get('package_name', 'Bilinmiyor')
            price = package_data.get('price', 0)
            return f"Paket bilgilerinizi kontrol ettim:\n   Paket: {package_name}\n   Fiyat: {price} TL/ay"
        
        # Kota ile ilgili sorular
        elif any(word in message_lower for word in ["kota", "kalan", "quota", "remaining"]):
            result = await ai_endpoint_functions.telekom_get_remaining_quotas(user_id=1)
            quota_data = result.get('data', {})
            internet_gb = quota_data.get('internet_remaining_gb', 0)
            sms_count = quota_data.get('sms_remaining', 0)
            call_minutes = quota_data.get('call_remaining_minutes', 0)
            return f"Kalan kotanızı kontrol ettim:\n   İnternet: {internet_gb} GB\n   SMS: {sms_count} adet\n   Konuşma: {call_minutes} dakika"
        
        # Müşteri profili
        elif any(word in message_lower for word in ["müşteri", "profil", "customer", "profile"]):
            result = await ai_endpoint_functions.telekom_get_customer_profile(user_id=1)
            profile_data = result.get('data', {})
            name = profile_data.get('name', 'Bilinmiyor')
            phone = profile_data.get('phone', 'Bilinmiyor')
            email = profile_data.get('email', 'Bilinmiyor')
            return f"Müşteri profilinizi kontrol ettim:\n   Ad: {name}\n   Telefon: {phone}\n   E-posta: {email}"
        
        # Sistem durumu
        elif any(word in message_lower for word in ["sistem", "sağlık", "durum", "health", "status"]):
            result = await ai_endpoint_functions.system_get_health()
            health_data = result.get('data', {})
            status = health_data.get('status', 'unknown')
            uptime = health_data.get('uptime', 'Bilinmiyor')
            return f"Sistem durumunu kontrol ettim:\n   Durum: {status}\n   Çalışma Süresi: {uptime}"
        
        # Ağ durumu
        elif any(word in message_lower for word in ["ağ", "network", "bağlantı", "connection"]):
            result = await ai_endpoint_functions.telekom_get_network_status(user_id=1)
            network_data = result.get('data', {})
            status = network_data.get('status', 'Bilinmiyor')
            speed = network_data.get('speed_mbps', 0)
            return f"Ağ durumunuzu kontrol ettim:\n   Durum: {status}\n   Hız: {speed} Mbps"
        
        # İnternet hız testi
        elif any(word in message_lower for word in ["hız", "speed", "test"]):
            result = await ai_endpoint_functions.telekom_run_speed_test(user_id=1)
            speed_data = result.get('data', {})
            download = speed_data.get('download_mbps', 0)
            upload = speed_data.get('upload_mbps', 0)
            return f"İnternet hız testi yaptım:\n   İndirme: {download} Mbps\n   Yükleme: {upload} Mbps"
        
        # Arıza kayıtları
        elif any(word in message_lower for word in ["arıza", "trouble", "sorun", "problem"]):
            result = await ai_endpoint_functions.telekom_get_trouble_tickets(user_id=1)
            tickets = result.get('data', {}).get('tickets', [])
            if tickets:
                response = f"Arıza kayıtlarınızı kontrol ettim. {len(tickets)} adet kayıt bulundu:\n"
                for i, ticket in enumerate(tickets[:3], 1):
                    status = ticket.get('status', 'Bilinmiyor')
                    description = ticket.get('description', 'Açıklama yok')
                    response += f"   {i}. Durum: {status} - {description}\n"
                return response
            else:
                return "Arıza kayıtlarınızı kontrol ettim. Aktif arıza kaydı bulunmuyor."
        
        # Yardım isteği
        elif any(word in message_lower for word in ["yardım", "help", "ne yapabilir", "komut"]):
            return """Size şu konularda yardımcı olabilirim:

📋 Fatura İşlemleri:
   - "Faturamı göster"
   - "Geçmiş faturalarımı göster"

📦 Paket Bilgileri:
   - "Paket bilgilerimi göster"
   - "Tarifemi değiştir"

📊 Kota Durumu:
   - "Kalan kotamı göster"
   - "İnternet kotamı kontrol et"

👤 Müşteri Profili:
   - "Müşteri bilgilerimi göster"
   - "Profilimi güncelle"

🔧 Sistem Durumu:
   - "Sistem durumunu kontrol et"
   - "Ağ durumumu göster"

⚡ Hız Testi:
   - "İnternet hız testi yap"

🔧 Arıza İşlemleri:
   - "Arıza kayıtlarımı göster"
   - "Yeni arıza kaydı oluştur"

Komutlar: 'quit' (çıkış), 'test' (fonksiyon testi), 'help' (bu menü)"""
        
        # Genel yanıt
        else:
            return "Merhaba! Size nasıl yardımcı olabilirim? Fatura, paket, kota, müşteri profili, sistem durumu, ağ durumu, hız testi veya arıza işlemleri hakkında soru sorabilirsiniz. 'help' yazarak tüm seçenekleri görebilirsiniz."
    
    def show_help(self):
        """Yardım menüsü"""
        print(f"""
🤖 AI Chat Terminal - Yardım Menüsü

📊 Sistem Bilgileri:
   Session ID: {self.session_id}
   User ID: {self.user_id}
   Toplam Mesaj: {self.conversation_count}

💬 Kullanım:
   - Herhangi bir soru sorun
   - 'quit' veya 'exit' yazarak çıkın
   - 'test' yazarak fonksiyon testlerini çalıştırın
   - 'help' yazarak bu menüyü gösterin
   - 'clear' yazarak ekranı temizleyin

🎯 Örnek Sorular:
   - "Faturamı göster"
   - "Geçmiş faturalarımı göster"
   - "Paket bilgilerimi göster"
   - "Kalan kotamı göster"
   - "Müşteri profili göster"
   - "Sistem durumunu kontrol et"
   - "Ağ durumumu göster"
   - "İnternet hız testi yap"
   - "Arıza kayıtlarımı göster"

🔧 Komutlar:
   - quit/exit: Çıkış
   - test: Fonksiyon testleri
   - help: Bu menü
   - clear: Ekran temizleme
        """)
    
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🧹 Ekran temizlendi!")
    
    async def run(self):
        """Ana çalışma döngüsü"""
        self.clear_screen()
        print("🚀 AI Chat Terminal Başlatıldı!")
        print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Session ID: {self.session_id}")
        
        # Önce fonksiyon testlerini çalıştır
        print("\n🧪 Sistem testleri yapılıyor...")
        test_success = await self.test_all_functions()
        
        if test_success:
            print("✅ Tüm sistemler çalışıyor!")
        else:
            print("⚠️ Bazı sistemlerde sorun var, ancak devam edebilirsiniz.")
        
        print("\n💬 Sohbete başlayabilirsiniz! 'help' yazarak yardım alabilirsiniz.")
        
        while True:
            try:
                # Kullanıcı girişi
                user_input = input(f"\n💬 Siz (Mesaj #{self.conversation_count + 1}): ").strip()
                
                if not user_input:
                    continue
                
                # Komut kontrolü
                if user_input.lower() in ['quit', 'exit', 'q', 'çıkış', 'çık']:
                    print("👋 Görüşürüz! İyi günler!")
                    break
                
                elif user_input.lower() == 'test':
                    print("\n🧪 Fonksiyon testleri tekrar çalıştırılıyor...")
                    await self.test_all_functions()
                    continue
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    continue
                
                # AI ile sohbet
                await self.chat_with_ai(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Ctrl+C ile çıkılıyor... Görüşürüz!")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")

async def main():
    """Ana fonksiyon"""
    chat = AIChatTerminal()
    await chat.run()

if __name__ == "__main__":
    asyncio.run(main()) 