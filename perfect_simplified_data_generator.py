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
            output_code="print(backend_api.get_customer_profile('gmail.com'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kullanıcı istatistiklerini getir",
            input_text="Son 6 ayda kayıt olan kullanıcı sayısını ve aktif kullanıcı oranını göster",
            output_code="print(backend_api.analyze_customer_behavior(6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kullanıcı profilini güncelle",
            input_text="ID'si 12345 olan kullanıcının telefon numarasını '0555-123-4567' olarak değiştir",
            output_code="print(backend_api.update_customer_preferences(12345, '0555-123-4567'))"
        ))
        
        return data
    
    def generate_product_management_data(self) -> List[Dict[str, str]]:
        """Ürün yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Ürün ara",
            input_text="iPhone 15 Pro modellerini bul ve fiyatlarını listele",
            output_code="print(backend_api.search_products('iPhone 15 Pro'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün detayları",
            input_text="ID 12345 olan ürünün detaylı bilgilerini getir",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kategori listele",
            input_text="Elektronik kategorisindeki tüm alt kategorileri göster",
            output_code="print(backend_api.get_product_details('electronics'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok durumu kontrol et",
            input_text="ID 12345 olan ürünün stok durumunu ve mevcut adedini kontrol et",
            output_code="print(backend_api.check_stock_status(12345))"
        ))
        
        # YENİ VERİ NOKTALARI (+8)
        data.append(self.create_data_point(
            instruction="Yeni ürün ekle",
            input_text="Samsung Galaxy S24 modelini sisteme yeni ürün olarak ekle",
            output_code="print(backend_api.get_product_details('Samsung Galaxy S24', category='phones'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün fiyatı güncelle",
            input_text="ID 12345 olan ürünün fiyatını 15000 TL olarak güncelle",
            output_code="print(backend_api.update_product_price(12345, price=15000))"
        ))
        
        data.append(self.create_data_point(
            instruction="Benzer ürünler",
            input_text="ID 12345 olan ürüne benzer ürünleri fiyat aralığı ile birlikte öner",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün yorumları",
            input_text="ID 12345 olan ürünün müşteri yorumlarını ve puanlarını getir",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fiyat geçmişi",
            input_text="ID 12345 olan ürünün son 6 aydaki fiyat değişim geçmişini göster",
            output_code="print(backend_api.get_product_details(12345, months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün görüntüleme sayısı",
            input_text="ID 12345 olan ürünün bu ayki görüntüleme istatistiklerini analiz et",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu ürün güncelleme",
            input_text="Elektronik kategorisindeki tüm ürünlerde %5 indirim uygula",
            output_code="print(backend_api.update_product_price('electronics', discount_percent=5))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün karşılaştırma",
            input_text="iPhone 15 ve Samsung S24 modellerinin özelliklerini karşılaştır",
            output_code="print(backend_api.get_product_details(['iPhone 15', 'Samsung S24']))"
        ))
        
        # YENİ PROFESYONEL ÜRÜN YÖNETİMİ (+13)
        data.append(self.create_data_point(
            instruction="AI destekli ürün kategorilendirme",
            input_text="Yeni eklenen ürünleri yapay zeka ile otomatik kategorilere ayır",
            output_code="print(backend_api.get_product_details())"
        ))
        
        data.append(self.create_data_point(
            instruction="Dinamik fiyatlandırma algoritması",
            input_text="Piyasa verilerine göre ID 12345 ürününün optimal fiyatını hesapla",
            output_code="print(backend_api.update_product_price(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün yaşam döngüsü analizi",
            input_text="ID 12345 ürününün pazardaki yaşam döngüsü evresini analiz et",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çapraz satış önerisi motoru",
            input_text="ID 12345 ürünü için en uygun çapraz satış ürünlerini öner",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün sosyal medya etkisi",
            input_text="ID 12345 ürününün sosyal medya mention'larını ve sentiment analizini yap",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Tedarikçi performans değerlendirmesi",
            input_text="SUPP001 tedarikçisinin ürün kalitesi ve teslimat performansını değerlendir",
            output_code="print(backend_api.get_product_details('SUPP001'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün sürdürülebilirlik skoru",
            input_text="ID 12345 ürününün çevre dostu özelliklerini ve sürdürülebilirlik skorunu hesapla",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Personalizasyon motoru",
            input_text="Müşteri ID 789'un geçmiş davranışlarına göre ürün önerilerini kişiselleştir",
            output_code="print(backend_api.get_product_details(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain ürün doğrulaması",
            input_text="ID 12345 ürününün orijinallik ve tedarik zinciri bilgilerini blockchain'de doğrula",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="AR ürün deneyimi",
            input_text="ID 12345 ürünü için artırılmış gerçeklik deneme deneyimini aktif et",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün trend tahmini",
            input_text="Elektronik kategorisindeki gelecek 6 aylık trend tahminlerini yap",
            output_code="print(backend_api.get_product_performance_report('electronics', months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çoklu dil ürün açıklaması",
            input_text="ID 12345 ürününün açıklamasını İngilizce, Almanca ve Fransızca'ya çevir",
            output_code="print(backend_api.get_product_details(12345, languages=['en', 'de', 'fr']))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün iade analizi",
            input_text="ID 12345 ürününün iade nedenlerini analiz et ve kalite iyileştirme önerileri ver",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        return data
    
    def generate_order_management_data(self) -> List[Dict[str, str]]:
        """Sipariş yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Sipariş durumu sorgula",
            input_text="Sipariş numarası SIP123456'nın mevcut durumunu ve kargo takip bilgilerini göster",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Yeni sipariş oluştur",
            input_text="Müşteri ID 789 için ürün ID 123'ü 2 adet olarak sipariş oluştur",
            output_code="print(backend_api.create_order(customer_id=789, product_id=123, quantity=2))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş iptali",
            input_text="Sipariş numarası SIP123456'yı iptal et ve iade işlemini başlat",
            output_code="print(backend_api.cancel_order('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş geçmişi",
            input_text="Müşteri ID 789'un son 12 aydaki tüm sipariş geçmişini listele",
            output_code="print(backend_api.get_order_history(customer_id=789, months=12))"
        ))
        
        # YENİ VERİ NOKTALARI (+8)
        data.append(self.create_data_point(
            instruction="Hızlı sipariş",
            input_text="Müşteri ID 789'un daha önce aldığı ürünlerden hızlı sipariş seçeneklerini göster",
            output_code="print(backend_api.get_order_history(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş değiştir",
            input_text="Sipariş SIP123456'da ürün miktarını 3'e çıkar ve teslimat adresini güncelle",
            output_code="print(backend_api.get_order_status('SIP123456', quantity=3, update_address=True))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu sipariş",
            input_text="Müşteri ID 789 için sepetteki 5 farklı ürünü tek seferde sipariş et",
            output_code="print(backend_api.create_order(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş faturası",
            input_text="Sipariş SIP123456'nın detaylı fatura bilgilerini ve vergi hesaplamasını getir",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Teslimat takibi",
            input_text="Sipariş SIP123456'nın kargo şirketinden anlık teslimat konumunu getir",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş iade",
            input_text="Sipariş SIP123456'dan ürün ID 123'ü iade et ve iade nedenini kaydet",
            output_code="print(backend_api.get_order_status('SIP123456', product_id=123, reason='defective'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Teslimat zamanı güncelle",
            input_text="Sipariş SIP123456'nın teslimat tarihini yarın saat 15:00 olarak planla",
            output_code="print(backend_api.get_order_status('SIP123456', datetime='2024-01-15 15:00'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş analizi",
            input_text="Müşteri ID 789'un sipariş verme alışkanlıklarını ve tercih ettiği ürün kategorilerini analiz et",
            output_code="print(backend_api.analyze_customer_behavior(customer_id=789))"
        ))
        
        # YENİ PROFESYONEL SİPARİŞ YÖNETİMİ (+13)
        data.append(self.create_data_point(
            instruction="AI destekli sipariş tahmini",
            input_text="Müşteri ID 789'un gelecek siparişlerini yapay zeka ile tahmin et",
            output_code="print(backend_api.get_order_history(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain sipariş takibi",
            input_text="Sipariş SIP123456'nın tüm aşamalarını blockchain üzerinde şeffaf olarak kaydet",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Dinamik teslimat optimizasyonu",
            input_text="Trafik ve hava durumu verilerine göre sipariş SIP123456'nın teslimat rotasını optimize et",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sosyal sipariş özelliği",
            input_text="Müşteri ID 789'un arkadaşlarıyla grup sipariş vermesini aktif et",
            output_code="print(backend_api.create_order(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sürdürülebilir teslimat",
            input_text="Sipariş SIP123456 için karbon ayak izi düşük teslimat seçeneklerini öner",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ses tabanlı sipariş",
            input_text="Müşteri ID 789 için sesli asistan ile sipariş verme özelliğini aktif et",
            output_code="print(backend_api.create_order(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Subscription sipariş yönetimi",
            input_text="Müşteri ID 789'un aylık kahve abonelik siparişini ayarla",
            output_code="print(backend_api.create_order(customer_id=789, product='coffee', frequency='monthly'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Drone teslimatı",
            input_text="Uygun koşullarda sipariş SIP123456'yı drone ile teslimat için planla",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Emotional AI sipariş deneyimi",
            input_text="Müşteri ID 789'un ruh haline göre sipariş önerilerini kişiselleştir",
            output_code="print(backend_api.get_order_history(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çoklu kanal sipariş entegrasyonu",
            input_text="Sipariş SIP123456'yı mobil, web ve mağaza kanallarında senkronize et",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Quantum güvenlik sipariş",
            input_text="Yüksek değerli sipariş SIP123456 için quantum şifreleme güvenliği uygula",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sipariş carbon offset",
            input_text="Sipariş SIP123456'nın karbondioksit salınımını hesapla ve karbon kredisi öner",
            output_code="print(backend_api.get_order_status('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Neural sipariş optimizasyonu",
            input_text="Sinir ağları ile sipariş işlem sürecini optimize et ve darboğazları tespit et",
            output_code="print(backend_api.get_order_status())"
        ))
        
        return data
    
    def generate_analytics_data(self) -> List[Dict[str, str]]:
        """Analitik ve raporlama ile ilgili veri örnekleri"""
        data = []
        
        # Satış analizleri
        data.append(self.create_data_point(
            instruction="Günlük satış raporu oluştur",
            input_text="Bugünün satış verilerini, en çok satan ürünleri ve toplam geliri göster",
            output_code="print(backend_api.generate_sales_report(datetime.now().strftime('%Y-%m-%d')))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kategori performans analizi",
            input_text="Her kategorinin aylık satış performansını ve büyüme oranını karşılaştır",
            output_code="print(backend_api.get_product_performance_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri segmentasyonu yap",
            input_text="Müşterileri alışveriş tutarına göre segmentlere ayır ve her segmentin özelliklerini analiz et",
            output_code="print(backend_api.analyze_customer_behavior())"
        ))
        
        return data
    
    def generate_analytics_reporting_data(self) -> List[Dict[str, str]]:
        """Analiz ve raporlama veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Satış raporu oluştur",
            input_text="Son 30 günün günlük satış verilerini ve trend analizini oluştur",
            output_code="print(backend_api.generate_sales_report(days=30))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri analizi",
            input_text="En değerli müşterileri ve satın alma davranışlarını analiz et",
            output_code="print(backend_api.analyze_customer_behavior())"
        ))
        
        data.append(self.create_data_point(
            instruction="Ürün performansı",
            input_text="Bu ayki en çok satan ürünleri ve kategori bazında performansı raporla",
            output_code="print(backend_api.get_product_performance_report(month='current'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Gelir analizi",
            input_text="Aylık gelir trendlerini ve yıllık büyüme oranını hesapla",
            output_code="print(backend_api.generate_sales_report(period='yearly'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri segmentasyon raporu",
            input_text="Müşteri segmentlerini harcama davranışlarına göre analiz et",
            output_code="print(backend_api.generate_sales_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Kampanya etkinlik analizi",
            input_text="Son 3 aydaki pazarlama kampanyalarının ROI analizini yap",
            output_code="print(backend_api.generate_sales_report(months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Web sitesi trafiği",
            input_text="Site ziyaretçilerinin davranış analizi ve dönüşüm oranlarını raporla",
            output_code="print(backend_api.generate_sales_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Envanter devir hızı",
            input_text="Ürün kategorilerine göre stok devir hızını ve verimliliği analiz et",
            output_code="print(backend_api.generate_sales_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri memnuniyet raporu",
            input_text="Müşteri yorumları ve derecelendirmelerine dayalı memnuniyet analizi oluştur",
            output_code="print(backend_api.generate_sales_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Coğrafi satış analizi",
            input_text="Şehir ve bölge bazında satış dağılımını ve potansiyel pazarları analiz et",
            output_code="print(backend_api.generate_sales_report())"
        ))
        
        data.append(self.create_data_point(
            instruction="Tahminleme modeli",
            input_text="Gelecek 6 ay için satış tahminlemesi ve talep analizi yap",
            output_code="print(backend_api.generate_sales_report(months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fiyat optimizasyon analizi",
            input_text="Ürün fiyatlarının satış üzerindeki etkisini analiz et ve optimal fiyat öner",
            output_code="print(backend_api.get_product_performance_report())"
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
            output_code="print(backend_api.get_low_stock_products(days=30, limit=20))"
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
            output_code="print(backend_api.send_email())"
        ))
        
        data.append(self.create_data_point(
            instruction="Kupon kullanım istatistikleri",
            input_text="'YILBASI2024' kupon kodunun kullanım sayısını ve toplam indirim tutarını hesapla",
            output_code="print(backend_api.generate_sales_report('YILBASI2024'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Yeni kampanya oluştur",
            input_text="Elektronik kategorisinde %20 indirim kampanyası oluştur, 15 gün geçerli olsun",
            output_code="print(backend_api.send_email('elektronik', 20, days=15))"
        ))
        
        return data
    
    def generate_customer_management_data(self) -> List[Dict[str, str]]:
        """Müşteri yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Müşteri bilgilerini getir",
            input_text="Müşteri ID 12345'in detaylı profil bilgilerini ve iletişim bilgilerini göster",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Yeni müşteri kaydı",
            input_text="Email adresi 'ali@example.com' olan yeni müşteriyi sisteme kaydet",
            output_code="print(backend_api.register_customer('ali@example.com'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri tercihlerini güncelle",
            input_text="Müşteri ID 12345'in bildirim tercihlerini güncelle ve email'i aktif et",
            output_code="print(backend_api.update_customer_preferences(12345, email_notifications=True))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Müşteri segmentasyonu",
            input_text="Müşteri ID 12345'in hangi müşteri segmentine ait olduğunu analiz et",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sadakat puanı",
            input_text="Müşteri ID 12345'in mevcut sadakat puanını ve kazanabileceği avantajları göster",
            output_code="print(backend_api.get_loyalty_points(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri adres güncelleme",
            input_text="Müşteri ID 12345'in teslimat adresini yeni adres bilgileri ile güncelle",
            output_code="print(backend_api.update_customer_address(12345, new_address='Yeni Mahalle, Sokak No:5'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri aktivite geçmişi",
            input_text="Müşteri ID 12345'in son 6 aydaki tüm aktivitelerini ve etkileşimlerini listele",
            output_code="print(backend_api.get_customer_activity(12345, months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri şikayet kaydı",
            input_text="Müşteri ID 12345'in teslimat gecikmesi konusundaki şikayetini kaydet",
            output_code="print(backend_api.get_customer_activity(12345, type='delivery_delay'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri iletişim geçmişi",
            input_text="Müşteri ID 12345 ile yapılan tüm iletişim kayıtlarını ve notlarını göster",
            output_code="print(backend_api.get_customer_activity(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri doğum günü",
            input_text="Bu ay doğum günü olan tüm müşterileri listele ve özel teklifler hazırla",
            output_code="print(backend_api.get_customer_profile())"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri hesap silme",
            input_text="Müşteri ID 12345'in hesap silme talebini işle ve veri koruma sürecini başlat",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri referans sistemi",
            input_text="Müşteri ID 12345'in referans ettiği müşterileri ve kazandığı bonusları göster",
            output_code="print(backend_api.get_customer_activity(12345))"
        ))
        
        # YENİ PROFESYONEL MÜŞTERİ YÖNETİMİ (+13)
        data.append(self.create_data_point(
            instruction="AI destekli müşteri davranış analizi",
            input_text="Müşteri ID 12345'in alışveriş davranışlarını yapay zeka ile derinlemesine analiz et",
            output_code="print(backend_api.analyze_customer_behavior(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri yaşam boyu değeri",
            input_text="Müşteri ID 12345'in CLV (Customer Lifetime Value) hesaplaması yap",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain müşteri kimlik doğrulama",
            input_text="Müşteri ID 12345'in kimlik bilgilerini blockchain üzerinde güvenli doğrula",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sentiment analizi müşteri geri bildirimi",
            input_text="Müşteri ID 12345'in tüm geri bildirimlerinin sentiment analizini yap",
            output_code="print(backend_api.analyze_customer_behavior(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri journey mapping",
            input_text="Müşteri ID 12345'in satın alma yolculuğunu ve touchpoint'lerini haritalandır",
            output_code="print(backend_api.get_customer_activity(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Predictive churn analizi",
            input_text="Müşteri ID 12345'in churn risk skorunu makine öğrenmesi ile hesapla",
            output_code="print(backend_api.get_customer_activity(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hyper-personalization motoru",
            input_text="Müşteri ID 12345 için mikro-segment bazında ultra kişisel deneyim oluştur",
            output_code="print(backend_api.update_customer_preferences(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Voice of Customer analizi",
            input_text="Müşteri ID 12345'in ses kayıtlarından duygusal analiz ve ihtiyaç tespiti yap",
            output_code="print(backend_api.analyze_customer_behavior(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri avatar oluşturma",
            input_text="Müşteri ID 12345'in davranışlarından dijital avatar ve persona oluştur",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Real-time engagement skoru",
            input_text="Müşteri ID 12345'in anlık engagement seviyesini izle ve aksiyonlar öner",
            output_code="print(backend_api.get_customer_activity(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri DNA profili",
            input_text="Müşteri ID 12345'in tercih genlerini ve davranış DNA'sını çıkar",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Quantum müşteri eşleştirme",
            input_text="Müşteri ID 12345 ile benzer quantum durumdaki müşterileri bul",
            output_code="print(backend_api.get_customer_profile(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Neuro-marketing müşteri analizi",
            input_text="Müşteri ID 12345'in nöro-pazarlama verilerini analiz et",
            output_code="print(backend_api.analyze_customer_behavior(12345))"
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
        
        # YENİ VERİ NOKTALARI (+8)
        data.append(self.create_data_point(
            instruction="Paket geçmişini sorgula",
            input_text="5551234567 numaralı hattın son 12 aydaki paket değişiklik geçmişini göster",
            output_code="print(backend_api.get_customer_package('5551234567', months=12))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket yükseltme önerisi",
            input_text="Aylık 40GB kullanımı olan müşteri için en uygun paket yükseltmesini öner",
            output_code="print(backend_api.get_suitable_packages(current_usage=40))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket fiyat karşılaştırması",
            input_text="Mevcut pazardaki tüm 30GB internet paketlerinin fiyat karşılaştırmasını yap",
            output_code="print(backend_api.get_suitable_packages(data_amount='30GB'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket kullanım analizi",
            input_text="5551234567 numaralı hattın son 3 aydaki ortalama kullanım verilerini analiz et",
            output_code="print(backend_api.get_usage_statistics('5551234567', months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu paket değişikliği",
            input_text="Şirket numarası CORP123 altındaki tüm hatları 'Kurumsal 100GB' paketine geçir",
            output_code="print(backend_api.change_package('CORP123', 'corporate_100gb'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket kullanım uyarısı",
            input_text="5551234567 numaralı hat kotasının %80'ini kullandığında SMS uyarısı ayarla",
            output_code="print(backend_api.get_remaining_quotas('5551234567', threshold=80))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket otomatik yenileme",
            input_text="5551234567 numaralı hat için aylık otomatik paket yenileme özelliğini aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket iptal etme",
            input_text="5551234567 numaralı hattın mevcut ek paketlerini iptal et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        # YENİ PROFESYONELPAKETLER (+13)
        data.append(self.create_data_point(
            instruction="Kurumsal paket yönetimi",
            input_text="Şirket CORP123'ün 50 hatlık kurumsal paket planını optimize et",
            output_code="print(backend_api.change_package('CORP123', line_count=50))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket limiti aşım kontrolü",
            input_text="5551234567 numaralı hattın paket limitlerini aştığı durumları analiz et",
            output_code="print(backend_api.get_remaining_quotas('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Dinamik paket önerisi",
            input_text="Kullanım verilerine göre 5551234567 için en optimal paket kombinasyonunu öner",
            output_code="print(backend_api.get_suitable_packages('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Aile paketi yönetimi",
            input_text="Aile grubu FAM001'in tüm hatları için ortak paket planı oluştur",
            output_code="print(backend_api.change_package('FAM001'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sezonsal paket kampanyası",
            input_text="Yaz dönemine özel internet paketlerini aktif et ve fiyatlandırmayı güncelle",
            output_code="print(backend_api.change_package(season='summer'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket kullanım tahmini",
            input_text="5551234567 numaralı hattın gelecek 3 aylık kullanım tahminini hesapla",
            output_code="print(backend_api.get_remaining_quotas('5551234567', months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Konuşma paket analizi",
            input_text="5551234567 numaralı hattın konuşma alışkanlıklarını analiz et ve paket öner",
            output_code="print(backend_api.get_usage_statistics('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Uluslararası paket aktivasyonu",
            input_text="5551234567 numaralı hat için Avrupa roaming paketini aktif et",
            output_code="print(backend_api.change_package('5551234567', region='europe'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket geçiş uyarı sistemi",
            input_text="Kota %90 dolduğunda otomatik paket yükseltme uyarısı sistemini aktif et",
            output_code="print(backend_api.get_suitable_packages(threshold=90))"
        ))
        
        data.append(self.create_data_point(
            instruction="Özel gün paket indirimi",
            input_text="Müşteri doğum günü için 5551234567 hattına özel paket indirimi uygula",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket sadakat programı",
            input_text="2 yıldır aynı paketi kullanan müşterilere sadakat bonusu ver",
            output_code="print(backend_api.get_bill_details(years=2))"
        ))
        
        data.append(self.create_data_point(
            instruction="Esnek paket yapılandırması",
            input_text="5551234567 için özelleştirilebilir paket oluştur: 20GB internet, 1000 dakika, 500 SMS",
            output_code="print(backend_api.change_package('5551234567', data_gb=20, minutes=1000, sms=500))"
        ))
        
        data.append(self.create_data_point(
            instruction="Paket performans karşılaştırması",
            input_text="Mevcut piyasadaki benzer paketlerle karşılaştırmalı analiz yap",
            output_code="print(backend_api.get_suitable_packages())"
        ))
        
        return data

    def generate_telekom_billing_data(self) -> List[Dict[str, str]]:
        """Telekom faturalama yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Mevcut faturayı görüntüle",
            input_text="5551234567 numaralı hattın bu ayki fatura detaylarını göster",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura geçmişi",
            input_text="5551234567 numaralı hattın son 6 aylık fatura geçmişini listele",
            output_code="print(backend_api.get_bill_details('5551234567', months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura ödeme",
            input_text="5551234567 numaralı hattın 150 TL tutarındaki faturasını kredi kartı ile öde",
            output_code="print(backend_api.pay_bill('5551234567', amount=150, method='credit_card'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Fatura özeti",
            input_text="5551234567 numaralı hattın yıllık fatura özetini ve toplam tutarını göster",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Otomatik ödeme ayarla",
            input_text="5551234567 numaralı hat için aylık otomatik fatura ödeme ayarını aktif et",
            output_code="print(backend_api.setup_auto_payment('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura ödeme geçmişi",
            input_text="5551234567 numaralı hattın son 12 aydaki tüm ödeme işlemlerini listele",
            output_code="print(backend_api.get_payment_history('5551234567', months=12))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ödenmemiş faturalar",
            input_text="5551234567 numaralı hattın ödenmemiş faturalarını ve toplam borcunu göster",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura taksitlendirme",
            input_text="5551234567 numaralı hattın 300 TL tutarındaki faturasını 3 taksitte öde",
            output_code="print(backend_api.process_payment('5551234567', amount=300, installments=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura detay analizi",
            input_text="5551234567 numaralı hattın bu ayki fatura kalemi detaylarını kategori bazında analiz et",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu fatura ödeme",
            input_text="Şirket numarası CORP123 altındaki tüm hatların faturalarını toplu olarak öde",
            output_code="print(backend_api.pay_bill('CORP123'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura uyarı ayarları",
            input_text="5551234567 numaralı hat için fatura son ödeme tarihinden 3 gün önce SMS uyarısı ayarla",
            output_code="print(backend_api.get_bill_details('5551234567', days_before=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="E-fatura ayarları",
            input_text="5551234567 numaralı hat için e-fatura gönderimini aktif et",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        # YENİ PROFESYONEL FATURALAMA (+13)
        data.append(self.create_data_point(
            instruction="Kurumsal faturalama sistemi",
            input_text="Şirket CORP123'ün merkezi faturalama sistemini aktif et ve department bazında ayır",
            output_code="print(backend_api.get_bill_details('CORP123', department_split=True))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura tahsilatı takibi",
            input_text="Vadesi geçmiş faturaları olan müşterileri listele ve tahsilat sürecini başlat",
            output_code="print(backend_api.get_bill_details())"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura düzeltme işlemi",
            input_text="Fatura INV-2024-001'de hatalı tarife yansıyan tutarı düzelt",
            output_code="print(backend_api.get_bill_details('INV-2024-001', error_type='tariff_miscalculation'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Peşin ödeme indirimi",
            input_text="Yıllık peşin ödeme yapan müşterilere %15 indirim uygula",
            output_code="print(backend_api.get_bill_details(discount_rate=15))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura döviz kuru güncellemesi",
            input_text="Uluslararası aramalar için USD bazlı tarifeleri güncel kurla hesapla",
            output_code="print(backend_api.change_package('USD'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura borç yapılandırması",
            input_text="5551234567 numaralı hattın birikmiş borcunu 12 aya yay",
            output_code="print(backend_api.get_bill_details('5551234567', months=12))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura vergi hesaplaması",
            input_text="KDV oranı değişikliği sonrası tüm fatura kategorilerini yeniden hesapla",
            output_code="print(backend_api.get_bill_details(tax_type='VAT'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu fatura düzenleme",
            input_text="İnsan kaynakları departmanı için çalışan hatlarının toplu faturalamasını ayarla",
            output_code="print(backend_api.get_bill_details('HR_DEPT'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura yasal raporlama",
            input_text="Mali müşavir için yasal gerekliliklere uygun fatura raporları oluştur",
            output_code="print(backend_api.get_bill_details())"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura limiti belirleme",
            input_text="5551234567 numaralı hat için aylık fatura limitini 500 TL olarak ayarla",
            output_code="print(backend_api.get_bill_details('5551234567', limit=500))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura kampanya hesaplaması",
            input_text="Ekim ayı kampanyası indirimlerini faturalara uygula ve hesapla",
            output_code="print(backend_api.get_bill_details(campaign='october_2024'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura blockchain kayıt",
            input_text="Güvenlik için kritik fatura kayıtlarını blockchain'e kaydet",
            output_code="print(backend_api.get_bill_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura AI anomali tespiti",
            input_text="Olağandışı fatura artışlarını yapay zeka ile tespit et ve uyar",
            output_code="print(backend_api.get_bill_details())"
        ))
        
        return data

    def generate_telekom_technical_data(self) -> List[Dict[str, str]]:
        """Telekom teknik destek ve arıza yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Arıza bildir",
            input_text="5551234567 numaralı hatta internet bağlantı sorunu var, arıza kaydı oluştur",
            output_code="print(backend_api.create_fault_ticket('5551234567', issue='internet_connection'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Arıza durumu sorgula",
            input_text="Arıza kaydı TK123456'nın mevcut durumunu ve çözüm sürecini göster",
            output_code="print(backend_api.create_fault_ticket('TK123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Teknik test yap",
            input_text="5551234567 numaralı hattın bağlantı kalitesini ve hız testini gerçekleştir",
            output_code="print(backend_api.create_fault_ticket('5551234567'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Arıza geçmişi",
            input_text="5551234567 numaralı hattın son 12 aydaki tüm arıza kayıtlarını listele",
            output_code="print(backend_api.create_fault_ticket('5551234567', months=12))"
        ))
        
        data.append(self.create_data_point(
            instruction="Teknik ekip görevlendir",
            input_text="Arıza kaydı TK123456 için saha teknik ekibi görevlendir",
            output_code="print(backend_api.create_fault_ticket('TK123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Modem ayarları sıfırla",
            input_text="5551234567 numaralı hattın modem ayarlarını fabrika varsayılanına sıfırla",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sinyal kalitesi analizi",
            input_text="5551234567 numaralı hattın son 7 günlük sinyal kalitesi verilerini analiz et",
            output_code="print(backend_api.check_network_status('5551234567', days=7))"
        ))
        
        data.append(self.create_data_point(
            instruction="Bölgesel arıza kontrolü",
            input_text="İstanbul Kadıköy bölgesindeki aktif arıza raporlarını ve etkilenen hat sayısını göster",
            output_code="print(backend_api.check_network_status('istanbul_kadikoy'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Uzaktan müdahale",
            input_text="5551234567 numaralı hattın modemini uzaktan yeniden başlat",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Arıza öncelik seviyesi",
            input_text="Arıza kaydı TK123456'nın öncelik seviyesini 'Yüksek' olarak güncelle",
            output_code="print(backend_api.create_fault_ticket('TK123456', priority='high'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Teknisyen randevu",
            input_text="5551234567 numaralı hat için yarın saat 14:00'da teknisyen randevusu ayarla",
            output_code="print(backend_api.create_fault_ticket('5551234567', datetime='2024-01-15 14:00'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Arıza çözüm raporu",
            input_text="Arıza kaydı TK123456 için detaylı çözüm raporunu oluştur",
            output_code="print(backend_api.get_ticket_status('TK123456'))"
        ))
        
        # YENİ PROFESYONEL TEKNİK DESTEK (+13)
        data.append(self.create_data_point(
            instruction="Öngörülü bakım sistemi",
            input_text="AI ile ağ altyapısındaki potansiyel arızaları önceden tespit et",
            output_code="print(backend_api.check_network_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Fiber altyapı tarama",
            input_text="İstanbul Beşiktaş bölgesindeki fiber altyapının sağlık taramasını gerçekleştir",
            output_code="print(backend_api.check_network_status('istanbul_besiktas'))"
        ))
        
        data.append(self.create_data_point(
            instruction="5G sinyal optimizasyonu",
            input_text="Yoğun kullanım alanlarında 5G baz istasyonlarının performansını optimize et",
            output_code="print(backend_api.check_network_status(area_type='high_traffic'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Uzaktan yazılım güncellemesi",
            input_text="5551234567 numaralı hattın modem firmware'ini otomatik güncelle",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ağ trafiği dengeleme",
            input_text="Yoğun saatlerde ağ trafiğini otomatik olarak dengeleyici sistemlere yönlendir",
            output_code="print(backend_api.check_network_status(peak_hours=True))"
        ))
        
        data.append(self.create_data_point(
            instruction="IoT cihaz arıza tespiti",
            input_text="Akıllı ev cihazlarındaki bağlantı sorunlarını toplu analiz et",
            output_code="print(backend_api.create_fault_ticket())"
        ))
        
        data.append(self.create_data_point(
            instruction="Kablosuz ağ güvenlik taraması",
            input_text="5551234567 numaralı hattın WiFi ağında güvenlik açıklarını tara",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Veri merkezi izleme",
            input_text="İstanbul veri merkezindeki sunucu performansını ve sıcaklık değerlerini izle",
            output_code="print(backend_api.check_network_status('istanbul_dc'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain tabanlı arıza kaydı",
            input_text="Kritik altyapı arızalarını blockchain üzerinde immutable kayıt tut",
            output_code="print(backend_api.create_support_ticket())"
        ))
        
        data.append(self.create_data_point(
            instruction="AR destekli teknik müdahale",
            input_text="Saha teknisyeni için artırılmış gerçeklik destekli arıza çözüm rehberi başlat",
            output_code="print(backend_api.create_support_ticket('TECH001'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri internet hızı garantisi",
            input_text="5551234567 numaralı hatta garanti edilen hızın %80'inin altına düşme durumunu analiz et",
            output_code="print(backend_api.check_network_status('5551234567', threshold=80))"
        ))
        
        data.append(self.create_data_point(
            instruction="Küresel ağ bağlantı testi",
            input_text="Türkiye'den global ağlara erişim kalitesini ve gecikme sürelerini test et",
            output_code="print(backend_api.check_network_status('turkey'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Siber güvenlik olay müdahalesi",
            input_text="Tespit edilen DDoS saldırısına karşı otomatik güvenlik tedbirlerini aktif et",
            output_code="print(backend_api.get_customer_package())"
        ))
        
        return data

    def generate_telekom_line_data(self) -> List[Dict[str, str]]:
        """Telekom hat ve numara yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Yeni hat aktivasyonu",
            input_text="TC kimlik numarası 12345678901 olan müşteri için yeni mobil hat açılışı yap",
            output_code="print(backend_api.get_customer_package('12345678901'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat kapama işlemi",
            input_text="5551234567 numaralı hattı kalıcı olarak kapat",
            output_code="print(backend_api.suspend_line('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Numara taşıma",
            input_text="5551234567 numarasını başka operatörden Telekom'a taşı",
            output_code="print(backend_api.get_customer_package('5551234567', from_operator='other'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Hat bilgileri sorgula",
            input_text="5551234567 numaralı hattın detaylı bilgilerini ve aktivasyon tarihini göster",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Geçici hat dondurma",
            input_text="5551234567 numaralı hattı 30 gün süreyle geçici olarak dondur",
            output_code="print(backend_api.suspend_line('5551234567', days=30))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat yeniden aktivasyon",
            input_text="Dondurulmuş olan 5551234567 numaralı hattı tekrar aktif et",
            output_code="print(backend_api.reactivate_line('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Numara değişikliği",
            input_text="5551234567 numaralı hat için yeni bir numara rezerve et",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat sahiplik devri",
            input_text="5551234567 numaralı hattın sahipliğini TC 12345678901'den TC 98765432109'a devret",
            output_code="print(backend_api.get_customer_package('5551234567', old_tc='12345678901', new_tc='98765432109'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çoklu hat sorgulama",
            input_text="TC kimlik numarası 12345678901 olan müşterinin tüm aktif hatlarını listele",
            output_code="print(backend_api.get_customer_package('12345678901'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat güvenlik ayarları",
            input_text="5551234567 numaralı hat için SIM kart değişim korumasını aktif et",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Roaming ayarları",
            input_text="5551234567 numaralı hat için uluslararası roaming hizmetini aktif et",
            output_code="print(backend_api.enable_roaming('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat kullanım istatistikleri",
            input_text="5551234567 numaralı hattın son 6 aydaki kullanım istatistiklerini analiz et",
            output_code="print(backend_api.get_usage_statistics('5551234567', months=6))"
        ))
        
        # YENİ PROFESYONEL HAT YÖNETİMİ (+13)
        data.append(self.create_data_point(
            instruction="eSIM aktivasyonu",
            input_text="5551234567 numaralı hat için dijital eSIM profili oluştur ve aktif et",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kurumsal hat toplu yönetimi",
            input_text="Şirket CORP123'ün 200 hatlık portföyünü merkezi sistemde yönet",
            output_code="print(backend_api.get_customer_package('CORP123', line_count=200))"
        ))
        
        data.append(self.create_data_point(
            instruction="Numara rezervasyon sistemi",
            input_text="VIP müşteri için özel numara 5550000001'i rezerve et",
            output_code="print(backend_api.get_customer_package('5550000001', customer_type='vip'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Aile hesabı birleştirme",
            input_text="Aile üyeleri 5551234567, 5551234568, 5551234569'u tek hesapta birleştir",
            output_code="print(backend_api.get_customer_profile(['5551234567', '5551234568', '5551234569']))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çoklu SIM kartı yönetimi",
            input_text="5551234567 numarası için tablet ve telefon olmak üzere 2 SIM kart aktif et",
            output_code="print(backend_api.get_customer_package('5551234567', device_types=['phone', 'tablet']))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat güvenlik profili",
            input_text="5551234567 numaralı hat için biyometrik güvenlik ve 2FA koruması aktif et",
            output_code="print(backend_api.get_customer_package('5551234567', biometric=True, two_factor=True))"
        ))
        
        data.append(self.create_data_point(
            instruction="Yurtdışı hat kullanım izni",
            input_text="5551234567 numaralı hattın AB ülkelerinde kullanım iznini geçici olarak aktif et",
            output_code="print(backend_api.enable_roaming('5551234567', duration_days=30))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain tabanlı numara sahipliği",
            input_text="5551234567 numarasının sahiplik geçmişini blockchain üzerinde kaydet",
            output_code="print(backend_api.get_customer_profile('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="AI destekli kullanım analizi",
            input_text="Yapay zeka ile 5551234567 hattının anormal kullanım paternlerini tespit et",
            output_code="print(backend_api.get_usage_statistics('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat kredibilite skoru",
            input_text="5551234567 numaralı hattın ödeme geçmişine göre kredibilite skorunu hesapla",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Dinamik numara maskeleme",
            input_text="Güvenlik için 5551234567 numarasına geçici maskeleme numarası ata",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Hat performans optimizasyonu",
            input_text="5551234567 hattının ağ performansını coğrafi konum bazında optimize et",
            output_code="print(backend_api.get_usage_statistics('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kurumsal hiyerarşi yönetimi",
            input_text="Şirket CORP123'te departman bazında hat yetkilerini ve limitlerini ayarla",
            output_code="print(backend_api.get_bill_details('CORP123'))"
        ))
        
        return data

    def generate_telekom_internet_tv_data(self) -> List[Dict[str, str]]:
        """Telekom internet ve TV hizmetleri veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Internet hızı testi",
            input_text="5551234567 numaralı hattın mevcut internet hızını test et",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV kanal paketi değiştir",
            input_text="5551234567 numaralı aboneliğin TV paketini 'Süper TV Paketi'ne yükselt",
            output_code="print(backend_api.change_package('5551234567', 'super_tv_package'))"
        ))
        
        data.append(self.create_data_point(
            instruction="İnternet kullanım raporu",
            input_text="5551234567 numaralı hattın bu ayki internet kullanım raporunu göster",
            output_code="print(backend_api.get_usage_statistics('5551234567'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Fiber internet kurulum",
            input_text="5551234567 numaralı müşteri için fiber internet kurulum randevusu ayarla",
            output_code="print(backend_api.create_fault_ticket('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV kanal listesi",
            input_text="5551234567 numaralı aboneliğin izleyebileceği tüm TV kanallarını listele",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="İnternet kotası artırma",
            input_text="5551234567 numaralı hattın aylık internet kotasını 100GB artır",
            output_code="print(backend_api.change_package('5551234567', additional_gb=100))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV kaydedici hizmeti",
            input_text="5551234567 numaralı abonelik için TV kaydedici hizmetini aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="WiFi şifre değiştirme",
            input_text="5551234567 numaralı hattın WiFi şifresini 'YeniSifre123' olarak değiştir",
            output_code="print(backend_api.check_network_status('5551234567', new_password='YeniSifre123'))"
        ))
        
        data.append(self.create_data_point(
            instruction="İnternet hız yükseltme",
            input_text="5551234567 numaralı hattın internet hızını 100 Mbps'e yükselt",
            output_code="print(backend_api.change_package('5551234567', speed='100mbps'))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV stream kalitesi",
            input_text="5551234567 numaralı abonelik için 4K TV yayın kalitesini aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="İnternet paylaşım limiti",
            input_text="5551234567 numaralı hat için mobil hotspot özelliğini 50GB limit ile aktif et",
            output_code="print(backend_api.get_customer_package('5551234567', limit_gb=50))"
        ))
        
        data.append(self.create_data_point(
            instruction="TV çocuk koruma",
            input_text="5551234567 numaralı abonelik için çocuk koruma ayarlarını aktif et",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        # YENİ PROFESYONEL İNTERNET & TV (+13)
        data.append(self.create_data_point(
            instruction="8K TV yayın teknolojisi",
            input_text="5551234567 aboneliği için 8K çözünürlük destekli premium TV hizmetini aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="AI destekli içerik önerisi",
            input_text="5551234567 kullanıcısının izleme alışkanlıklarına göre kişiselleştirilmiş içerik öner",
            output_code="print(backend_api.get_product_performance_report('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fiber gigabit hızı aktifleştir",
            input_text="5551234567 aboneliği için 1000 Mbps fiber internet hizmetini aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çoklu ekran yayın senkronizasyonu",
            input_text="5551234567 aboneliği için TV, tablet ve telefon ekranlarında senkronize yayın başlat",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Bulut oyun servisi",
            input_text="5551234567 aboneliği için cloud gaming platformunu aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="IoT ev otomasyonu entegrasyonu",
            input_text="5551234567 aboneliğini akıllı ev cihazları ile entegre et",
            output_code="print(backend_api.get_customer_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="VR/AR içerik platformu",
            input_text="5551234567 aboneliği için sanal ve artırılmış gerçeklik içerik paketini aktif et",
            output_code="print(backend_api.get_product_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Adaptif kalite kontrolü",
            input_text="Ağ yoğunluğuna göre 5551234567 aboneliğinin video kalitesini dinamik olarak ayarla",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain tabanlı telif hakkı",
            input_text="Premium içeriklerin telif haklarını blockchain üzerinde doğrula",
            output_code="print(backend_api.get_product_details('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Edge computing optimizasyonu",
            input_text="5551234567 aboneliği için en yakın edge sunucudan içerik akışını optimize et",
            output_code="print(backend_api.check_network_status('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sesli asistan TV kontrolü",
            input_text="5551234567 aboneliği için sesli komutlarla TV kontrolünü aktif et",
            output_code="print(backend_api.get_customer_profile('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Sosyal izleme deneyimi",
            input_text="5551234567 aboneliği için arkadaşlarla birlikte sanal izleme odasını aktif et",
            output_code="print(backend_api.change_package('5551234567'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Quantum şifreli bağlantı",
            input_text="Premium müşteri 5551234567 için quantum şifreleme destekli güvenli bağlantı sağla",
            output_code="print(backend_api.get_customer_profile('5551234567'))"
        ))
        
        return data

    def generate_payment_billing_data(self) -> List[Dict[str, str]]:
        """Ödeme ve faturalama veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Ödeme işlemi yap",
            input_text="Sipariş SIP123456 için 450 TL tutarında kredi kartı ile ödeme al",
            output_code="print(backend_api.process_payment('SIP123456', amount=450, method='credit_card'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ödeme geçmişi",
            input_text="Müşteri ID 789'un son 6 aydaki tüm ödeme işlemlerini listele",
            output_code="print(backend_api.get_payment_history(customer_id=789, months=6))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura oluştur",
            input_text="Sipariş SIP123456 için detaylı fatura oluştur ve müşteriye email gönder",
            output_code="print(backend_api.get_bill_details('SIP123456', send_email=True))"
        ))
        
        data.append(self.create_data_point(
            instruction="İade işlemi",
            input_text="Sipariş SIP123456 için 150 TL tutarında iade işlemini başlat",
            output_code="print(backend_api.process_refund('SIP123456', amount=150))"
        ))
        
        # YENİ VERİ NOKTALARI (+8)
        data.append(self.create_data_point(
            instruction="Ödeme yöntemleri",
            input_text="Müşteri ID 789 için kaydedilmiş tüm ödeme yöntemlerini ve son kullanım tarihlerini göster",
            output_code="print(backend_api.get_payment_history(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Taksitli ödeme",
            input_text="750 TL tutarındaki siparişi 3 taksit olarak böl ve ödeme planını oluştur",
            output_code="print(backend_api.setup_auto_payment(amount=750, installments=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ödeme durumu sorgula",
            input_text="Sipariş SIP123456'nın ödeme durumunu ve bekleyen tutarları kontrol et",
            output_code="print(backend_api.get_payment_history('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Fatura iptal etme",
            input_text="Fatura no INV-2024-001'i iptal et ve muhasebe kaydını düzelt",
            output_code="print(backend_api.get_customer_profile('INV-2024-001'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ödeme hatası çözümle",
            input_text="Başarısız ödeme işlemi PAY123456'yı yeniden dene ve hata kaydını güncelle",
            output_code="print(backend_api.process_payment('PAY123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu faturalama",
            input_text="Bu ayın tüm tamamlanan siparişleri için toplu faturalama işlemini çalıştır",
            output_code="print(backend_api.get_bill_details(month='current'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Ödeme raporu",
            input_text="Son 30 günün günlük ödeme istatistiklerini ve gelir analizini oluştur",
            output_code="print(backend_api.get_payment_history(days=30))"
        ))
        
        data.append(self.create_data_point(
            instruction="Para iadesi takibi",
            input_text="Müşteri ID 789'un bekleyen para iadelerini ve işlem durumlarını göster",
            output_code="print(backend_api.process_refund(customer_id=789))"
        ))
        
        # YENİ PROFESYONEL ÖDEME & FATURALAMA (+13)
        data.append(self.create_data_point(
            instruction="Blockchain ödeme doğrulaması",
            input_text="Yüksek tutarlı ödeme PAY123456'yı blockchain üzerinde immutable kaydet",
            output_code="print(backend_api.process_payment('PAY123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="AI fraud detection",
            input_text="Yapay zeka ile şüpheli ödeme işlemlerini gerçek zamanlı tespit et",
            output_code="print(backend_api.process_payment())"
        ))
        
        data.append(self.create_data_point(
            instruction="Quantum güvenlik ödeme",
            input_text="Kredi kartı bilgilerini quantum şifreleme ile güvenli işle",
            output_code="print(backend_api.process_payment('PAY123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Buy Now Pay Later entegrasyonu",
            input_text="750 TL tutarındaki sipariş için BNPL seçeneklerini aktif et",
            output_code="print(backend_api.setup_auto_payment(amount=750))"
        ))
        
        data.append(self.create_data_point(
            instruction="Kripto para ödeme sistemi",
            input_text="Bitcoin ve Ethereum ile ödeme almayı sipariş SIP123456 için aktif et",
            output_code="print(backend_api.process_payment('SIP123456', currencies=['BTC', 'ETH']))"
        ))
        
        data.append(self.create_data_point(
            instruction="Biometric ödeme doğrulaması",
            input_text="Müşteri ID 789 için parmak izi ve yüz tanıma ile ödeme güvenliği aktif et",
            output_code="print(backend_api.setup_auto_payment(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Smart contract otomatik ödeme",
            input_text="Teslimat tamamlandığında otomatik ödeme için smart contract oluştur",
            output_code="print(backend_api.process_payment('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Cross-border ödeme optimizasyonu",
            input_text="Uluslararası ödeme PAY123456 için en düşük komisyon oranını hesapla",
            output_code="print(backend_api.process_payment('PAY123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Voice commerce ödeme",
            input_text="Sesli komutla ödeme işlemini tamamla ve güvenlik doğrulaması yap",
            output_code="print(backend_api.process_payment(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Neural network fatura analizi",
            input_text="Sinir ağları ile fatura kalıplarını analiz et ve anomalileri tespit et",
            output_code="print(backend_api.get_bill_details(customer_id=789))"
        ))
        
        data.append(self.create_data_point(
            instruction="Micro-payment işleme",
            input_text="1 TL altındaki küçük tutarlı ödemeleri toplu işle",
            output_code="print(backend_api.process_payment())"
        ))
        
        data.append(self.create_data_point(
            instruction="Central Bank Digital Currency",
            input_text="Merkez bankası dijital para birimi ile ödeme seçeneğini aktif et",
            output_code="print(backend_api.process_payment('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="ESG uyumlu ödeme raporlaması",
            input_text="Sürdürülebilirlik kriterlerine uygun ödeme ve fatura raporları oluştur",
            output_code="print(backend_api.get_payment_history())"
        ))
        
        return data

    def generate_inventory_stock_data(self) -> List[Dict[str, str]]:
        """Envanter ve stok yönetimi veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Stok seviyesi kontrol et",
            input_text="Ürün ID 12345'in mevcut stok miktarını ve minimum stok seviyesini kontrol et",
            output_code="print(backend_api.check_stock_status(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Düşük stok uyarısı",
            input_text="Minimum stok seviyesinin altında olan tüm ürünleri listele",
            output_code="print(backend_api.get_low_stock_products())"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok hareketi kaydet",
            input_text="Ürün ID 12345'e 100 adet stok ekle ve hareket kaydını oluştur",
            output_code="print(backend_api.add_stock(12345, quantity=100, reason='purchase'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Stok değer hesaplama",
            input_text="Tüm kategorilerdeki toplam stok değerini ve maliyet analizini hesapla",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok hareketi geçmişi",
            input_text="Ürün ID 12345'in son 3 aydaki stok giriş-çıkış hareketlerini listele",
            output_code="print(backend_api.check_stock_status(12345, months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Depo lokasyon sorgula",
            input_text="Ürün ID 12345'in hangi depolarda ve hangi raflarda bulunduğunu göster",
            output_code="print(backend_api.get_product_details(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok rezervasyonu",
            input_text="Sipariş SIP123456 için gerekli ürünleri stoktan rezerve et",
            output_code="print(backend_api.add_stock('SIP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok sayım başlat",
            input_text="Elektronik kategorisindeki tüm ürünler için stok sayım işlemini başlat",
            output_code="print(backend_api.check_stock_status('electronics'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok transfer işlemi",
            input_text="Ürün ID 12345'den İstanbul deposundan Ankara deposuna 50 adet transfer et",
            output_code="print(backend_api.add_stock(12345, from_warehouse='istanbul', to_warehouse='ankara', quantity=50))"
        ))
        
        data.append(self.create_data_point(
            instruction="Tedarikçi stok durumu",
            input_text="Tedarikçi SUPP001'in teslim edebileceği ürünleri ve stok miktarlarını sorgula",
            output_code="print(backend_api.check_stock_status('SUPP001'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Stok optimizasyonu",
            input_text="Satış verilerine göre optimal stok seviyelerini öner ve yeniden sipariş noktalarını hesapla",
            output_code="print(backend_api.get_low_stock_products())"
        ))
        
        data.append(self.create_data_point(
            instruction="Eskiyen stok analizi",
            input_text="90 gün boyunca hareket görmeyen ürünleri listele ve tasfiye önerisi hazırla",
            output_code="print(backend_api.get_low_stock_products(days=90))"
        ))
        
        # YENİ PROFESYONEL ENVANTER & STOK (+13)
        data.append(self.create_data_point(
            instruction="AI destekli talep tahmini",
            input_text="Yapay zeka ile gelecek 3 aylık ürün talebini tahmin et ve stok planla",
            output_code="print(backend_api.generate_sales_report(months=3))"
        ))
        
        data.append(self.create_data_point(
            instruction="Blockchain stok doğrulama",
            input_text="Ürün ID 12345'in tüm stok hareketlerini blockchain üzerinde şeffaf kaydet",
            output_code="print(backend_api.check_stock_status(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="IoT sensörlü stok takibi",
            input_text="Akıllı sensörlerle gerçek zamanlı stok seviyelerini izle",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Drone destekli stok sayımı",
            input_text="Yüksek raflar için drone ile otomatik stok sayım gerçekleştir",
            output_code="print(backend_api.check_stock_status('high_shelves'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Quantum stok optimizasyonu",
            input_text="Quantum algoritmaları ile optimal stok dağılımını hesapla",
            output_code="print(backend_api.get_low_stock_products())"
        ))
        
        data.append(self.create_data_point(
            instruction="RFID otomatik stok takibi",
            input_text="RFID teknolojisi ile ürünlerin gerçek zamanlı konumunu takip et",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Machine learning iade tahmini",
            input_text="Makine öğrenmesi ile iade olasılığı yüksek ürünleri önceden tespit et",
            output_code="print(backend_api.get_product_details())"
        ))
        
        data.append(self.create_data_point(
            instruction="Robotik depo otomasyonu",
            input_text="Otonom robotlarla stok toplama ve yerleştirme işlemlerini optimize et",
            output_code="print(backend_api.get_low_stock_products())"
        ))
        
        data.append(self.create_data_point(
            instruction="Climate control stok yönetimi",
            input_text="Sıcaklık hassas ürünler için iklim kontrollü stok takibi yap",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Predictive maintenance envanter",
            input_text="Depo ekipmanlarının bakım ihtiyaçlarını önceden tahmin et",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Holographic stok görselleştirme",
            input_text="3D hologram ile depo haritası ve stok durumunu görselleştir",
            output_code="print(backend_api.check_stock_status())"
        ))
        
        data.append(self.create_data_point(
            instruction="Cross-docking optimizasyonu",
            input_text="Gelen ve giden ürünler için cross-docking sürecini optimize et",
            output_code="print(backend_api.add_stock())"
        ))
        
        data.append(self.create_data_point(
            instruction="Neural network stok kategorilendirme",
            input_text="Sinir ağları ile ürünleri ABC analizi kategorilerine otomatik ayır",
            output_code="print(backend_api.get_low_stock_products())"
        ))
        
        return data

    def generate_support_communication_data(self) -> List[Dict[str, str]]:
        """Destek ve iletişim veri örnekleri"""
        data = []
        
        data.append(self.create_data_point(
            instruction="Destek talebi oluştur",
            input_text="Müşteri ID 12345'in ürün iade talebi için yeni destek kaydı oluştur",
            output_code="print(backend_api.create_support_ticket(12345, 'product_return'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Canlı sohbet başlat",
            input_text="Müşteri ID 12345 için canlı sohbet oturumu başlat",
            output_code="print(backend_api.start_live_chat(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Email gönder",
            input_text="Müşteri ID 12345'e sipariş onay emaili gönder",
            output_code="print(backend_api.send_email(12345, template='order_confirmation'))"
        ))
        
        # YENİ VERİ NOKTALARI (+9)
        data.append(self.create_data_point(
            instruction="Destek talep durumu",
            input_text="Ticket SUP123456'nın mevcut durumunu ve atanan temsilciyi göster",
            output_code="print(backend_api.get_ticket_status('SUP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Toplu SMS gönderimi",
            input_text="Tüm aktif müşterilere kampanya duyuru SMS'i gönder",
            output_code="print(backend_api.send_email(message='Yeni kampanya başladı!', segment='active_customers'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Müşteri geri bildirimi",
            input_text="Müşteri ID 12345'e çözümlenen destek talebi için memnuniyet anketi gönder",
            output_code="print(backend_api.send_email(12345, ticket_id='SUP123456'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çağrı merkezi yönlendirme",
            input_text="Müşteri ID 12345'i VIP müşteri hattına yönlendir",
            output_code="print(backend_api.create_support_ticket(12345))"
        ))
        
        data.append(self.create_data_point(
            instruction="Otomatik yanıt ayarla",
            input_text="Sık sorulan sorular için otomatik yanıt sistemi ayarla",
            output_code="print(backend_api.send_email('faq'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Destek ekibi istatistikleri",
            input_text="Bu ayki destek ekibinin performans istatistiklerini ve çözüm sürelerini analiz et",
            output_code="print(backend_api.get_ticket_status(month='current'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Push bildirim gönder",
            input_text="Müşteri ID 12345'e sipariş hazırlandı push bildirimi gönder",
            output_code="print(backend_api.send_email(12345, 'Siparişiniz hazırlandı!'))"
        ))
        
        data.append(self.create_data_point(
            instruction="Çok kanallı iletişim",
            input_text="Müşteri ID 12345 ile WhatsApp, email ve SMS üzerinden koordineli iletişim planı oluştur",
            output_code="print(backend_api.send_email(12345, channels=['whatsapp', 'email', 'sms']))"
        ))
        
        data.append(self.create_data_point(
            instruction="Destek kalite kontrol",
            input_text="Çözümlenen ticket SUP123456'nın kalite skorunu değerlendir",
            output_code="print(backend_api.get_ticket_status('SUP123456'))"
        ))
        
        return data






