#!/usr/bin/env python3
"""
Quick Fine-tuning Script
========================

Minimal konfigürasyon ile hızlı fine-tuning yapma scripti.
Yeni başlayanlar için basitleştirilmiş versiyon.

Kullanım:
    python quick_finetune.py

Bu script:
- Otomatik GPU/CPU detection yapar
- Minimal parametre ile başlar
- Hata durumunda daha açıklayıcı mesajlar verir
"""

import os
import sys

def check_requirements():
    """Gerekli paketlerin kurulu olup olmadığını kontrol et"""
    missing_packages = []
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError:
        missing_packages.append("torch")
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError:
        missing_packages.append("transformers")
    
    try:
        import peft
        print(f"✅ PEFT: {peft.__version__}")
    except ImportError:
        missing_packages.append("peft")
    
    try:
        import trl
        print(f"✅ TRL: {trl.__version__}")
    except ImportError:
        missing_packages.append("trl")
    
    if missing_packages:
        print(f"\n❌ Eksik paketler: {', '.join(missing_packages)}")
        print("Çözüm: pip install -r requirements.txt")
        return False
    
    return True

def check_data_file():
    """Veri dosyasının varlığını kontrol et"""
    data_path = "../data/complete_training_dataset.json"
    
    if os.path.exists(data_path):
        print(f"✅ Veri dosyası bulundu: {data_path}")
        return True
    else:
        print(f"❌ Veri dosyası bulunamadı: {data_path}")
        print("Çözüm: Önce data_structure.py ve combine_datasets.py scriptlerini çalıştırın")
        return False

def check_gpu():
    """GPU durumunu kontrol et"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✅ GPU: {gpu_name} ({gpu_memory:.1f} GB)")
            
            if gpu_memory < 6:
                print("⚠️ Uyarı: 6GB'den az GPU belleği var. Eğitim yavaş olabilir.")
            
            return True
        else:
            print("⚠️ GPU bulunamadı. CPU kullanılacak (çok yavaş).")
            return False
    except:
        print("❌ GPU kontrolü başarısız")
        return False

def main():
    """Ana kontrol ve başlatma fonksiyonu"""
    print("🚀 Quick Fine-tuning Kontrolü")
    print("=" * 40)
    
    # 1. Paket kontrolü
    print("\n1️⃣ Paket Kontrolü:")
    if not check_requirements():
        sys.exit(1)
    
    # 2. Veri dosyası kontrolü
    print("\n2️⃣ Veri Dosyası Kontrolü:")
    if not check_data_file():
        sys.exit(1)
    
    # 3. GPU kontrolü
    print("\n3️⃣ GPU Kontrolü:")
    has_gpu = check_gpu()
    
    # 4. Fine-tuning başlat
    print("\n4️⃣ Fine-tuning Başlatılıyor:")
    
    try:
        from run_finetune import FineTuner
        
        # Basit konfigürasyon
        fine_tuner = FineTuner()
        
        print("⚙️ Konfigürasyon:")
        print(f"  - Model: {fine_tuner.model_name}")
        print(f"  - Veri: {fine_tuner.data_path}")
        print(f"  - Çıktı: {fine_tuner.output_dir}")
        
        # Kullanıcı onayı
        response = input("\nFine-tuning'i başlatmak istiyor musunuz? (y/n): ")
        
        if response.lower() in ['y', 'yes', 'evet']:
            print("\n🔥 Fine-tuning başlatılıyor...")
            success = fine_tuner.fine_tune()
            
            if success:
                print("\n🎉 Başarıyla tamamlandı!")
                print(f"📁 Model: {fine_tuner.output_dir}")
            else:
                print("\n❌ Fine-tuning başarısız oldu.")
        else:
            print("❌ İptal edildi.")
            
    except ImportError as e:
        print(f"❌ Import hatası: {e}")
        print("Çözüm: run_finetune.py dosyasının aynı klasörde olduğundan emin olun")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main() 