#!/usr/bin/env python3
"""
Basit v6 model indirme script'i
"""

from huggingface_hub import hf_hub_download
from pathlib import Path

def main():
    print("🚀 v6 model indiriliyor...")
    
    try:
        # Model bilgileri
        repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
        filename = "ChoyrensAi-8b-q5_k_m.gguf"
        
        # İndirme dizini
        download_dir = Path("models/v6_model")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 İndirme dizini: {download_dir.absolute()}")
        print(f"📁 Dosya: {filename}")
        
        # Modeli indir
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=download_dir
        )
        
        print(f"✅ Model başarıyla indirildi!")
        print(f"📍 Konum: {model_path}")
        
        # Boyut bilgisi
        size_gb = Path(model_path).stat().st_size / (1024**3)
        print(f"📊 Boyut: {size_gb:.2f} GB")
        
        print("\n🎯 v6 model hazır! Backend'i yeniden başlatın.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main() 