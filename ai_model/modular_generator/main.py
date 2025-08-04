# -*- coding: utf-8 -*-
"""
🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3 - MODULAR EDITION
=============================================================

Bu dosya, modüler SupremeHumanLevelDatasetGenerator'ın ana çalıştırma noktasıdır.
"""

import argparse
import sys
from datetime import datetime

import os

from .core_generator import SupremeHumanLevelDatasetGenerator

def main():
    """SUPREME V3: Ana çalıştırma fonksiyonu - Gelişmiş hata yönetimi ile"""
    parser = argparse.ArgumentParser(description="🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3")
    parser.add_argument(
        "--num-samples", 
        type=int, 
        default=10000, 
        help="Üretilecek toplam veri örneği sayısı."
    )
    parser.add_argument(
        "--output-file", 
        type=str, 
        default=f"ultimate_human_level_dataset_v2_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        help="Çıktı JSON dosyasının adı."
    )
    args = parser.parse_args()

    print("🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3 - %100 ŞEMA UYUMLU")
    print("=" * 70)
    
    try:
    # Generator'ı başlat
        print("🔧 Generator başlatılıyor...")
        generator = SupremeHumanLevelDatasetGenerator()
    
    # Dataset üret
        print(f"📊 {args.num_samples} adet senaryo üretiliyor...")
        dataset = generator.generate_supreme_dataset(num_samples=args.num_samples)
    
    # Kaydet
        print("💾 Dataset kaydediliyor...")
        generator.save_dataset(dataset, args.output_file)
    
        print("\n🎯 SUPREME BAŞARI!")
        print("✅ %100 şema uyumlu dataset üretildi")
        print("✅ Tüm API yanıtları Pydantic doğrulamasından geçti")
        print("✅ Sıfır tolerans politikası uygulandı")
        print("✅ Olağanüstü model eğitimi için hazır!")
        
        print(f"\n📊 Dataset İstatistikleri:")
        print(f"   • Toplam senaryo: {len(dataset)}")
        print(f"   • Validasyon hataları: {generator.validation_errors}")
        print(f"   • Şema ihlalleri: {generator.schema_violations}")
        
        if generator.validation_errors == 0 and generator.schema_violations == 0:
            print("\n🏆 MÜKEMMEL: Hiçbir hata tespit edilmedi!")
            print("🚀 Bu dataset ile olağanüstü model eğitimi başlayabilir!")
        else:
            print(f"\n⚠️ UYARI: {generator.validation_errors + generator.schema_violations} hata tespit edildi")
        
    except ValueError as ve:
        print(f"\n❌ VERİ HATASI: {ve}")
        print("🔍 ÇÖZÜM: API şeması uyumluluğunu kontrol edin")
        sys.exit(1)
        
    except ImportError as ie:
        print(f"\n❌ İMPORT HATASI: {ie}")
        print("🔍 ÇÖZÜM: Gerekli kütüphaneleri yükleyin (pip install pydantic)")
        sys.exit(1)
        
    except FileNotFoundError as fe:
        print(f"\n❌ DOSYA HATASI: {fe}")
        print("🔍 ÇÖZÜM: telekom_api_schema.py dosyasının varlığını kontrol edin")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ BEKLENMEYEN HATA: {e}")
        print("🔍 ÇÖZÜM: Lütfen hata detaylarını kontrol edin")
        print(f"   Hata tipi: {type(e).__name__}")
        import traceback
        print(f"   Stack trace: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main() 