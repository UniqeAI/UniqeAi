#!/usr/bin/env python3
"""
ChoyrensAI-Telekom-Agent-v6-gguf modelini indiren script
"""

import os
import sys
from huggingface_hub import hf_hub_download
from pathlib import Path

def download_v6_model():
    """v6 modelini indir"""
    
    # Model bilgileri
    repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
    model_name = "ChoyrensAI-Telekom-Agent-v6-gguf.gguf"
    
    # İndirme dizini
    download_dir = Path("models/v6_model")
    download_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 {repo_id} modeli indiriliyor...")
    print(f"📁 İndirme dizini: {download_dir.absolute()}")
    
    try:
        # Modeli indir
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=model_name,
            local_dir=download_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"✅ Model başarıyla indirildi!")
        print(f"📍 Konum: {model_path}")
        print(f"📊 Boyut: {Path(model_path).stat().st_size / (1024**3):.2f} GB")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Model indirme hatası: {e}")
        return None

if __name__ == "__main__":
    print("🔍 v6 model indirme script'i başlatılıyor...")
    
    # Sanal ortam kontrolü
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Sanal ortam aktif değil! Önce 'source venv/bin/activate' çalıştırın.")
        sys.exit(1)
    
    # Modeli indir
    model_path = download_v6_model()
    
    if model_path:
        print("\n🎯 Model başarıyla indirildi!")
        print("🔄 Backend'i yeniden başlatmanız gerekebilir.")
    else:
        print("\n❌ Model indirilemedi!")
        sys.exit(1) 