"""
Gün 2: Fine-tuning için sentetik veri yapısı tasarımı
Her veri noktası şu formatta olacak:
{
    "instruction": "...",
    "input": "...", 
    "output": "<tool_code>print(backend_api.some_function(...))</tool_code>"
}
"""

import json
from typing import Dict, List, Any

class SyntheticDataGenerator:
    def __init__(self):
        self.data_structure = {
            "instruction": str,
            "input": str,
            "output": str
        }
    
    def create_data_point(self, instruction: str, input_text: str, output_code: str) -> Dict[str, str]:
        """
        Tek bir veri noktası oluşturur
        """
        return {
            "instruction": instruction,
            "input": input_text,
            "output": f"<tool_code>{output_code}</tool_code>"
        }
    
    def generate_sample_data(self) -> List[Dict[str, str]]:
        """
        Fine-tuning için örnek sentetik veri oluşturur
        """
        sample_data = [
            # Kullanıcı yönetimi örnekleri
            self.create_data_point(
                instruction="Kullanıcı bilgilerini getir",
                input_text="ID'si 12345 olan kullanıcının bilgilerini al",
                output_code="print(backend_api.get_user_info(12345))"
            ),
            
            self.create_data_point(
                instruction="Yeni kullanıcı oluştur",
                input_text="Adı 'Ahmet Yılmaz', email'i 'ahmet@example.com' olan yeni kullanıcı ekle",
                output_code="print(backend_api.create_user('Ahmet Yılmaz', 'ahmet@example.com'))"
            ),
            
            # Ürün yönetimi örnekleri
            self.create_data_point(
                instruction="Ürün listesini getir",
                input_text="Kategori 'elektronik' olan tüm ürünleri listele",
                output_code="print(backend_api.get_products_by_category('elektronik'))"
            ),
            
            self.create_data_point(
                instruction="Ürün fiyatını güncelle",
                input_text="ID'si 789 olan ürünün fiyatını 299.99 TL yap",
                output_code="print(backend_api.update_product_price(789, 299.99))"
            ),
            
            # Sipariş yönetimi örnekleri
            self.create_data_point(
                instruction="Sipariş durumunu kontrol et",
                input_text="Sipariş numarası 'ORD-2024-001' olan siparişin durumunu öğren",
                output_code="print(backend_api.get_order_status('ORD-2024-001'))"
            ),
            
            self.create_data_point(
                instruction="Yeni sipariş oluştur",
                input_text="Kullanıcı ID'si 12345, ürün ID'si 789, miktar 2 adet sipariş oluştur",
                output_code="print(backend_api.create_order(12345, 789, 2))"
            ),
            
            # Raporlama örnekleri
            self.create_data_point(
                instruction="Satış raporu oluştur",
                input_text="2024 yılı Ocak ayı satış raporunu hazırla",
                output_code="print(backend_api.generate_sales_report('2024-01'))"
            ),
            
            self.create_data_point(
                instruction="Stok durumunu kontrol et",
                input_text="Tüm ürünlerin stok durumunu listele",
                output_code="print(backend_api.get_inventory_status())"
            ),
            
            # Analitik örnekleri
            self.create_data_point(
                instruction="En çok satan ürünleri bul",
                input_text="Son 30 günde en çok satan 10 ürünü listele",
                output_code="print(backend_api.get_top_selling_products(30, 10))"
            ),
            
            self.create_data_point(
                instruction="Müşteri analizi yap",
                input_text="En aktif 5 müşteriyi ve toplam alışveriş tutarlarını göster",
                output_code="print(backend_api.get_top_customers(5))"
            )
        ]
        
        return sample_data
    
    def save_to_json(self, data: List[Dict[str, str]], filename: str = "synthetic_training_data.json"):
        """
        Veriyi JSON dosyasına kaydeder
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Veri {filename} dosyasına kaydedildi. Toplam {len(data)} veri noktası.")
    
    def load_from_json(self, filename: str = "synthetic_training_data.json") -> List[Dict[str, str]]:
        """
        JSON dosyasından veriyi yükler
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def validate_data_structure(self, data: List[Dict[str, str]]) -> bool:
        """
        Veri yapısının doğruluğunu kontrol eder
        """
        required_fields = ["instruction", "input", "output"]
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                print(f"Hata: {i}. öğe dictionary değil")
                return False
            
            for field in required_fields:
                if field not in item:
                    print(f"Hata: {i}. öğede '{field}' alanı eksik")
                    return False
                
                if not isinstance(item[field], str):
                    print(f"Hata: {i}. öğede '{field}' alanı string değil")
                    return False
            
            # Output alanının tool_code etiketleri içerdiğini kontrol et
            if "<tool_code>" not in item["output"] or "</tool_code>" not in item["output"]:
                print(f"Hata: {i}. öğede output alanı tool_code etiketleri içermiyor")
                return False
        
        print("Veri yapısı doğrulaması başarılı!")
        return True

def main():
    """
    Ana fonksiyon - sentetik veri oluşturma ve test etme
    """
    print("=== Gün 2: Sentetik Veri Yapısı Oluşturma ===\n")
    
    # Veri üreticisini oluştur
    generator = SyntheticDataGenerator()
    
    # Örnek veri oluştur
    print("1. Sentetik veri oluşturuluyor...")
    sample_data = generator.generate_sample_data()
    
    # Veri yapısını doğrula
    print("\n2. Veri yapısı doğrulanıyor...")
    generator.validate_data_structure(sample_data)
    
    # JSON dosyasına kaydet
    print("\n3. Veri JSON dosyasına kaydediliyor...")
    generator.save_to_json(sample_data)
    
    # Örnek veriyi göster
    print("\n4. İlk 3 veri noktası örneği:")
    for i, item in enumerate(sample_data[:3]):
        print(f"\n--- Veri Noktası {i+1} ---")
        print(f"Instruction: {item['instruction']}")
        print(f"Input: {item['input']}")
        print(f"Output: {item['output']}")
    
    print(f"\n=== Tamamlandı! Toplam {len(sample_data)} veri noktası oluşturuldu ===")

if __name__ == "__main__":
    main() 