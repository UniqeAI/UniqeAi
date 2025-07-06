"""
Gün 2: Genişletilmiş Sentetik Veri Üreticisi
Daha fazla çeşitlilik ve gerçekçi senaryolar içeren veri örnekleri
"""

import json
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

class ExtendedDataGenerator:
    def __init__(self):
        self.categories = ["elektronik", "giyim", "kitap", "spor", "ev", "kozmetik", "oyuncak", "gıda"]
        self.user_names = ["Ahmet", "Ayşe", "Mehmet", "Fatma", "Ali", "Zeynep", "Mustafa", "Elif", "Hasan", "Selin"]
        self.user_surnames = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Özdemir", "Arslan", "Doğan", "Kılıç"]
        
    def create_data_point(self, instruction: str, input_text: str, output_code: str) -> Dict[str, str]:
        """Tek bir veri noktası oluşturur"""
        return {
            "instruction": instruction,
            "input": input_text,
            "output": f"<tool_code>{output_code}</tool_code>"
        }
    
    def generate_user_management_data(self) -> List[Dict[str, str]]:
        """Kullanıcı yönetimi ile ilgili veri örnekleri"""
        data = []
        
        # Kullanıcı arama ve filtreleme
        data.append(self.create_data_point(
            instruction="Kullanıcıları filtrele",
            input_text="Email adresi 'gmail.com' ile biten tüm kullanıcıları bul",
            output_code="print(backend_api.filter_users_by_email_domain('gmail.com'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kullanıcı istatistiklerini getir",
            input_text="Son 6 ayda kayıt olan kullanıcı sayısını ve aktif kullanıcı oranını göster",
            output_code="print(backend_api.get_user_statistics(6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kullanıcı profilini güncelle",
            input_text="ID'si 12345 olan kullanıcının telefon numarasını '0555-123-4567' olarak değiştir",
            output_code="print(backend_api.update_user_phone(12345, '0555-123-4567'))"
        ))
        
        return data
    
    def generate_product_management_data(self) -> List[Dict[str, str]]:
        """Ürün yönetimi ile ilgili veri örnekleri"""
        data = []
        
        # Ürün arama ve filtreleme
        data.append(self.create_data_point(
            instruction="Ürün arama yap",
            input_text="Fiyatı 100-500 TL arasında olan 'telefon' kelimesi geçen ürünleri bul",
            output_code="print(backend_api.search_products('telefon', min_price=100, max_price=500))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün varyantlarını getir",
            input_text="ID'si 456 olan ürünün tüm renk ve boyut seçeneklerini listele",
            output_code="print(backend_api.get_product_variants(456))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün değerlendirmelerini getir",
            input_text="ID'si 789 olan ürünün son 50 değerlendirmesini ve ortalama puanını göster",
            output_code="print(backend_api.get_product_reviews(789, limit=50))"
        ))
        
        return data
    
    def generate_order_management_data(self) -> List[Dict[str, str]]:
        """Sipariş yönetimi ile ilgili veri örnekleri"""
        data = []
        
        # Sipariş işlemleri
        data.append(self.create_data_point(
            instruction="Sipariş geçmişini getir",
            input_text="Kullanıcı ID'si 12345 olan müşterinin son 12 aydaki tüm siparişlerini listele",
            output_code="print(backend_api.get_user_order_history(12345, months=12))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş iptal et",
            input_text="Sipariş numarası 'ORD-2024-005' olan siparişi iptal et ve iade sürecini başlat",
            output_code="print(backend_api.cancel_order('ORD-2024-005'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kargo takibi yap",
            input_text="Sipariş numarası 'ORD-2024-003' olan siparişin kargo durumunu kontrol et",
            output_code="print(backend_api.track_shipping('ORD-2024-003'))"
        ))
        
        return data
    
    def generate_analytics_data(self) -> List[Dict[str, str]]:
        """Analitik ve raporlama ile ilgili veri örnekleri"""
        data = []
        
        # Satış analizleri
        data.append(self.create_data_point(
            instruction="Günlük satış raporu oluştur",
            input_text="Bugünün satış verilerini, en çok satan ürünleri ve toplam geliri göster",
            output_code="print(backend_api.generate_daily_sales_report(datetime.now().strftime('%Y-%m-%d')))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kategori performans analizi",
            input_text="Her kategorinin aylık satış performansını ve büyüme oranını karşılaştır",
            output_code="print(backend_api.analyze_category_performance())"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri segmentasyonu yap",
            input_text="Müşterileri alışveriş tutarına göre segmentlere ayır ve her segmentin özelliklerini analiz et",
            output_code="print(backend_api.segment_customers_by_spending())"
        ))
        
        return data
    
    def generate_inventory_data(self) -> List[Dict[str, str]]:
        """Stok yönetimi ile ilgili veri örnekleri"""
        data = []
        
        # Stok işlemleri
        data.append(self.create_data_point(
            instruction="Düşük stok uyarısı",
            input_text="Stok miktarı 10'dan az olan tüm ürünleri listele ve tedarikçi bilgilerini göster",
            output_code="print(backend_api.get_low_stock_products(threshold=10))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok hareketleri raporu",
            input_text="Son 30 günde en çok stok hareketi olan 20 ürünü ve hareket detaylarını göster",
            output_code="print(backend_api.get_stock_movements_report(days=30, limit=20))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok girişi yap",
            input_text="Ürün ID'si 456 olan ürüne 50 adet stok girişi yap, lot numarası 'LOT-2024-001'",
            output_code="print(backend_api.add_stock(456, 50, 'LOT-2024-001'))"
        ))
        
        return data
    
    def generate_promotion_data(self) -> List[Dict[str, str]]:
        """Promosyon ve kampanya yönetimi ile ilgili veri örnekleri"""
        data = []
        
        # Kampanya işlemleri
        data.append(self.create_data_point(
            instruction="Aktif kampanyaları listele",
            input_text="Şu anda aktif olan tüm kampanyaları, indirim oranlarını ve geçerlilik tarihlerini göster",
            output_code="print(backend_api.get_active_promotions())"
        ))
        
        data.append(self.create_data_point(
            instruction="Kupon kullanım istatistikleri",
            input_text="'YILBASI2024' kupon kodunun kullanım sayısını ve toplam indirim tutarını hesapla",
            output_code="print(backend_api.get_coupon_usage_stats('YILBASI2024'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Yeni kampanya oluştur",
            input_text="Elektronik kategorisinde %20 indirim kampanyası oluştur, 15 gün geçerli olsun",
            output_code="print(backend_api.create_promotion('elektronik', 20, days=15))"
        ))
        
        return data
    
    def generate_customer_service_data(self) -> List[Dict[str, str]]:
        """Müşteri hizmetleri ile ilgili veri örnekleri"""
        data = []
        
        # Destek talepleri
        data.append(self.create_data_point(
            instruction="Destek taleplerini listele",
            input_text="Bekleyen destek taleplerini öncelik sırasına göre listele",
            output_code="print(backend_api.get_pending_support_tickets())"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri şikayetini kaydet",
            input_text="Kullanıcı ID'si 12345 olan müşterinin 'ürün hasarlı geldi' şikayetini kaydet",
            output_code="print(backend_api.create_support_ticket(12345, 'ürün hasarlı geldi', 'high'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Destek talebini güncelle",
            input_text="Ticket ID'si 789 olan destek talebini 'çözüldü' durumuna güncelle",
            output_code="print(backend_api.update_support_ticket(789, 'resolved'))"
        ))
        
        return data
    
    def generate_telekom_package_data(self) -> List[Dict[str, str]]:
        """Telekom paket ve tarife yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Mevcut paketi kontrol et",
            input_text="Müşteri numarası 5551234567 olan abonenin mevcut paket bilgilerini getir",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket değiştir",
            input_text="Müşteri 5551234567 numaralı hattını 'Süper Internet 50GB' paketine geçir",
            output_code="print(backend_api.change_package('5551234567', 'super_internet_50gb'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Uygun paketleri listele",
            input_text="Aylık kullanımı 25GB olan müşteri için uygun internet paketlerini göster",
            output_code="print(backend_api.get_suitable_packages(usage_gb=25))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket kalan miktarını sorgula",
            input_text="5551234567 numaralı hattın bu ay kalan internet, dakika ve SMS kotasını göster",
            output_code="print(backend_api.get_remaining_quotas('5551234567'))"
        ))
        
        return data
    
    def generate_telekom_billing_data(self) -> List[Dict[str, str]]:
        """Telekom fatura yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Fatura detayını getir",
            input_text="Müşteri 5551234567 numaralı hattının Ocak 2024 fatura detayını göster",
            output_code="print(backend_api.get_bill_details('5551234567', '2024-01'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura ödeme durumunu kontrol et",
            input_text="5551234567 numaralı hattın son 6 aylık fatura ödeme durumunu listele",
            output_code="print(backend_api.get_payment_status('5551234567', months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Otomatik ödeme talimatı oluştur",
            input_text="5551234567 numaralı hat için kredi kartından otomatik fatura ödeme talimatı ver",
            output_code="print(backend_api.setup_autopay('5551234567', 'credit_card'))"
        ))
        
        return data
    
    def generate_telekom_technical_support_data(self) -> List[Dict[str, str]]:
        """Telekom teknik destek veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Ağ durumunu kontrol et",
            input_text="İstanbul Kadıköy bölgesindeki şebeke durumunu ve aktif arızaları kontrol et",
            output_code="print(backend_api.check_network_status('istanbul', 'kadikoy'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Arıza kaydı oluştur",
            input_text="5551234567 numaralı hatta 'internet bağlantısı yok' arıza kaydı oluştur",
            output_code="print(backend_api.create_fault_ticket('5551234567', 'internet_connection_issue'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sinyal gücünü test et",
            input_text="5551234567 numaralı hattın bulunduğu konumdaki sinyal gücünü ve kalitesini ölç",
            output_code="print(backend_api.test_signal_strength('5551234567'))"
        ))
        
        return data
    
    def generate_telekom_line_management_data(self) -> List[Dict[str, str]]:
        """Telekom hat ve numara yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Yeni hat açma başvurusu",
            input_text="Ahmet Yılmaz adına yeni GSM hattı açma başvurusu oluştur",
            output_code="print(backend_api.create_new_line_application('Ahmet Yılmaz', 'gsm'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat dondurma işlemi",
            input_text="5551234567 numaralı hattı 3 ay süreyle dondur",
            output_code="print(backend_api.suspend_line('5551234567', duration_months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Numara taşıma durumu",
            input_text="5551234567 numaralı hattın numara taşıma başvuru durumunu kontrol et",
            output_code="print(backend_api.check_number_portability('5551234567'))"
        ))
        
        return data
    
    def generate_telekom_internet_tv_data(self) -> List[Dict[str, str]]:
        """Telekom internet ve TV hizmetleri veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Fiber alt yapı kontrolü",
            input_text="İstanbul Beşiktaş Levent mahallesi için fiber internet alt yapı durumunu kontrol et",
            output_code="print(backend_api.check_fiber_infrastructure('istanbul', 'besiktas', 'levent'))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV kanal paketi değiştir",
            input_text="Müşteri 5551234567 için mevcut TV paketine spor kanalları paketini ekle",
            output_code="print(backend_api.add_tv_package('5551234567', 'sports_channels'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Modem ayarlarını güncelle",
            input_text="5551234567 numaralı hattın modem wifi şifresini değiştir",
            output_code="print(backend_api.update_modem_wifi_password('5551234567', 'new_password'))"
        ))
        
        return data
    
    def generate_all_data(self) -> List[Dict[str, str]]:
        """Tüm kategorilerden veri örnekleri oluşturur"""
        all_data = []
        
        all_data.extend(self.generate_user_management_data())
        all_data.extend(self.generate_product_management_data())
        all_data.extend(self.generate_order_management_data())
        all_data.extend(self.generate_analytics_data())
        all_data.extend(self.generate_inventory_data())
        all_data.extend(self.generate_promotion_data())
        all_data.extend(self.generate_customer_service_data())
        all_data.extend(self.generate_telekom_package_data())
        all_data.extend(self.generate_telekom_billing_data())
        all_data.extend(self.generate_telekom_technical_support_data())
        all_data.extend(self.generate_telekom_line_management_data())
        all_data.extend(self.generate_telekom_internet_tv_data())
        
        return all_data
    
    def save_to_json(self, data: List[Dict[str, str]], filename: str = "extended_synthetic_data.json"):
        """Veriyi JSON dosyasına kaydeder"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Genişletilmiş veri {filename} dosyasına kaydedildi. Toplam {len(data)} veri noktası.")
    
    def print_data_summary(self, data: List[Dict[str, str]]):
        """Veri özetini yazdırır"""
        print(f"\n=== VERİ ÖZETİ ===")
        print(f"Toplam veri noktası: {len(data)}")
        
        # Instruction türlerini analiz et
        instructions = [item['instruction'] for item in data]
        unique_instructions = set(instructions)
        print(f"Benzersiz instruction türü: {len(unique_instructions)}")
        
        # İlk 5 instruction türünü göster
        print("\nÖrnek instruction türleri:")
        for i, instruction in enumerate(list(unique_instructions)[:5]):
            print(f"  {i+1}. {instruction}")

def main():
    """Ana fonksiyon"""
    print("=== Gün 2: Genişletilmiş Sentetik Veri Oluşturma ===\n")
    
    generator = ExtendedDataGenerator()
    
    print("1. Genişletilmiş sentetik veri oluşturuluyor...")
    all_data = generator.generate_all_data()
    
    print("\n2. Veri özeti:")
    generator.print_data_summary(all_data)
    
    print("\n3. Veri JSON dosyasına kaydediliyor...")
    generator.save_to_json(all_data)
    
    print("\n4. İlk 2 veri noktası örneği:")
    for i, item in enumerate(all_data[:2]):
        print(f"\n--- Veri Noktası {i+1} ---")
        print(f"Instruction: {item['instruction']}")
        print(f"Input: {item['input']}")
        print(f"Output: {item['output']}")
    
    print(f"\n=== Tamamlandı! Genişletilmiş veri seti oluşturuldu ===")

if __name__ == "__main__":
    main() 