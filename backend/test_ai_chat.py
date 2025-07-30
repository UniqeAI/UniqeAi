#!/usr/bin/env python3
"""
Terminal üzerinden AI'ya sorular sormak için interaktif test scripti
"""

import asyncio
import sys
import os
from datetime import datetime

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.services.ai_orchestrator import ai_orchestrator
from app.services.ai_endpoint_functions import ai_endpoint_functions

class AIChatTerminal:
    def __init__(self):
        self.session_id = f"TERMINAL_SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_id = "terminal_user"
        self.conversation_history = []
        
    async def send_message(self, message: str):
        """AI'ya mesaj gönder ve yanıt al"""
        try:
            print(f"\n🤖 AI'ya gönderiliyor: {message}")
            print("⏳ İşleniyor...")
            
            # AI orchestrator ile mesajı işle
            result = await ai_orchestrator.kullanici_mesaj_isle(
                mesaj=message,
                kullanici_id=self.user_id,
                oturum_id=self.session_id
            )
            
            # Sonucu göster
            print(f"\n✅ AI Yanıtı:")
            print(f"📝 Mesaj: {result['yanit']}")
            print(f"🎯 Güven Puanı: {result['guven_puani']:.2f}")
            
            if result['arac_cagrilari']:
                print(f"🔧 Çalıştırılan Araçlar:")
                for arac in result['arac_cagrilari']:
                    print(f"   - {arac['arac_adi']}: {arac['durum']}")
                    if arac.get('sonuc'):
                        print(f"     Sonuç: {arac['sonuc']}")
            
            # Konuşma geçmişine ekle
            self.conversation_history.append({
                'user': message,
                'ai': result['yanit'],
                'timestamp': datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    async def test_specific_functions(self):
        """Belirli fonksiyonları test et"""
        print("\n🧪 Belirli Fonksiyon Testleri:")
        
        # Fatura testi
        print("\n1. Fatura Geçmişi Testi:")
        result = await ai_endpoint_functions.telekom_get_bill_history(user_id=1, limit=3)
        print(f"   Sonuç: {result}")
        
        # Paket testi
        print("\n2. Mevcut Paket Testi:")
        result = await ai_endpoint_functions.telekom_get_current_package(user_id=1)
        print(f"   Sonuç: {result}")
        
        # Kota testi
        print("\n3. Kalan Kotalar Testi:")
        result = await ai_endpoint_functions.telekom_get_remaining_quotas(user_id=1)
        print(f"   Sonuç: {result}")
    
    def show_help(self):
        """Yardım menüsünü göster"""
        print(f"""
🤖 AI Chat Terminal - Yardım Menüsü

Kullanım:
- Herhangi bir mesaj yazın ve Enter'a basın
- 'quit' veya 'exit' yazarak çıkın
- 'help' yazarak bu menüyü gösterin
- 'test' yazarak fonksiyon testlerini çalıştırın
- 'history' yazarak konuşma geçmişini gösterin
- 'clear' yazarak konuşma geçmişini temizleyin

Örnek Sorular:
- "Faturamı göster"
- "Geçmiş faturalarımı göster"
- "Paket bilgilerimi göster"
- "Kalan kotamı göster"
- "Arıza kaydı oluştur"
- "Ağ durumunu kontrol et"
- "İnternet hız testi yap"
- "Kullanıcı bilgilerimi göster"

Sistem Bilgileri:
- Session ID: {self.session_id}
- User ID: {self.user_id}
- Toplam Araç Sayısı: {len(ai_orchestrator.telekom_arac_kaydi.mevcut_araclari_getir())}
        """)
    
    def show_history(self):
        """Konuşma geçmişini göster"""
        if not self.conversation_history:
            print("📝 Henüz konuşma geçmişi yok.")
            return
        
        print(f"\n📝 Konuşma Geçmişi ({len(self.conversation_history)} mesaj):")
        for i, conv in enumerate(self.conversation_history, 1):
            print(f"\n{i}. Kullanıcı: {conv['user']}")
            print(f"   AI: {conv['ai']}")
            print(f"   Zaman: {conv['timestamp']}")
    
    def clear_history(self):
        """Konuşma geçmişini temizle"""
        self.conversation_history.clear()
        print("🗑️ Konuşma geçmişi temizlendi.")
    
    async def run(self):
        """Ana çalışma döngüsü"""
        print("🤖 AI Chat Terminal Başlatıldı!")
        print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Session ID: {self.session_id}")
        
        self.show_help()
        
        while True:
            try:
                # Kullanıcı girişi
                user_input = input("\n💬 Siz: ").strip()
                
                if not user_input:
                    continue
                
                # Komut kontrolü
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Görüşürüz!")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'test':
                    await self.test_specific_functions()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                
                # AI'ya mesaj gönder
                await self.send_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Ctrl+C ile çıkılıyor...")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")

async def main():
    """Ana fonksiyon"""
    chat = AIChatTerminal()
    await chat.run()

if __name__ == "__main__":
    print("🚀 AI Chat Terminal Başlatılıyor...")
    asyncio.run(main()) 