"""
Gün 2: Veri Setlerini Birleştirme
Temel ve genişletilmiş veri setlerini birleştirerek tam fine-tuning veri setini oluşturur
"""

import json
from typing import List, Dict

def load_json_data(filename: str) -> List[Dict[str, str]]:
    """JSON dosyasından veri yükler"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_data(data: List[Dict[str, str]], filename: str):
    """Veriyi JSON dosyasına kaydeder"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Veri {filename} dosyasına kaydedildi. Toplam {len(data)} veri noktası.")

def validate_combined_data(data: List[Dict[str, str]]) -> bool:
    """Birleştirilmiş veriyi doğrular"""
    print("\n=== BİRLEŞTİRİLMİŞ VERİ DOĞRULAMASI ===")
    
    # Temel doğrulama
    required_fields = ["instruction", "input", "output"]
    unique_instructions = set()
    
    for i, item in enumerate(data):
        # Gerekli alanları kontrol et
        for field in required_fields:
            if field not in item:
                print(f"Hata: {i}. öğede '{field}' alanı eksik")
                return False
            
            if not isinstance(item[field], str):
                print(f"Hata: {i}. öğede '{field}' alanı string değil")
                return False
        
        # tool_code etiketlerini kontrol et
        if "<tool_code>" not in item["output"] or "</tool_code>" not in item["output"]:
            print(f"Hata: {i}. öğede output alanı tool_code etiketleri içermiyor")
            return False
        
        # Benzersiz instruction'ları topla
        unique_instructions.add(item["instruction"])
    
    print(f"✓ Toplam veri noktası: {len(data)}")
    print(f"✓ Benzersiz instruction türü: {len(unique_instructions)}")
    print(f"✓ Tüm alanlar mevcut ve doğru tipte")
    print(f"✓ Tüm output'lar tool_code etiketleri içeriyor")
    print("✓ Veri doğrulaması başarılı!")
    
    return True

def analyze_data_distribution(data: List[Dict[str, str]]):
    """Veri dağılımını analiz eder"""
    print("\n=== VERİ DAĞILIMI ANALİZİ ===")
    
    # Instruction türlerini kategorilere ayır
    categories = {
        "Kullanıcı Yönetimi": 0,
        "Ürün Yönetimi": 0,
        "Sipariş Yönetimi": 0,
        "Analitik/Raporlama": 0,
        "Stok Yönetimi": 0,
        "Promosyon Yönetimi": 0,
        "Müşteri Hizmetleri": 0
    }
    
    for item in data:
        instruction = item["instruction"].lower()
        
        if any(word in instruction for word in ["kullanıcı", "user", "profil"]):
            categories["Kullanıcı Yönetimi"] += 1
        elif any(word in instruction for word in ["ürün", "product", "varyant", "değerlendirme"]):
            categories["Ürün Yönetimi"] += 1
        elif any(word in instruction for word in ["sipariş", "order", "kargo", "shipping"]):
            categories["Sipariş Yönetimi"] += 1
        elif any(word in instruction for word in ["rapor", "analiz", "istatistik", "segment"]):
            categories["Analitik/Raporlama"] += 1
        elif any(word in instruction for word in ["stok", "inventory", "hareket"]):
            categories["Stok Yönetimi"] += 1
        elif any(word in instruction for word in ["kampanya", "promotion", "kupon", "coupon"]):
            categories["Promosyon Yönetimi"] += 1
        elif any(word in instruction for word in ["destek", "support", "şikayet", "ticket"]):
            categories["Müşteri Hizmetleri"] += 1
    
    # Sonuçları yazdır
    total = len(data)
    for category, count in categories.items():
        percentage = (count / total) * 100
        print(f"{category}: {count} veri noktası ({percentage:.1f}%)")

def main():
    """Ana fonksiyon"""
    print("=== Gün 2: Veri Setlerini Birleştirme ===\n")
    
    try:
        # Veri setlerini yükle
        print("1. Veri setleri yükleniyor...")
        basic_data = load_json_data("synthetic_training_data.json")
        extended_data = load_json_data("extended_synthetic_data.json")
        
        print(f"   - Temel veri seti: {len(basic_data)} veri noktası")
        print(f"   - Genişletilmiş veri seti: {len(extended_data)} veri noktası")
        
        # Veri setlerini birleştir
        print("\n2. Veri setleri birleştiriliyor...")
        combined_data = basic_data + extended_data
        
        print(f"   - Birleştirilmiş toplam: {len(combined_data)} veri noktası")
        
        # Veriyi doğrula
        print("\n3. Birleştirilmiş veri doğrulanıyor...")
        if not validate_combined_data(combined_data):
            print("Hata: Veri doğrulaması başarısız!")
            return
        
        # Veri dağılımını analiz et
        analyze_data_distribution(combined_data)
        
        # Birleştirilmiş veriyi kaydet
        print("\n4. Birleştirilmiş veri kaydediliyor...")
        save_json_data(combined_data, "complete_training_dataset.json")
        
        # Örnek veri noktalarını göster
        print("\n5. Örnek veri noktaları:")
        for i, item in enumerate(combined_data[:3]):
            print(f"\n--- Veri Noktası {i+1} ---")
            print(f"Instruction: {item['instruction']}")
            print(f"Input: {item['input']}")
            print(f"Output: {item['output']}")
        
        print(f"\n=== TAMAMLANDI! ===")
        print(f"Toplam {len(combined_data)} veri noktası ile tam fine-tuning veri seti oluşturuldu.")
        print(f"Dosya: complete_training_dataset.json")
        
    except FileNotFoundError as e:
        print(f"Hata: {e}")
        print("Lütfen önce data_structure.py ve extended_data_generator.py scriptlerini çalıştırın.")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main() 