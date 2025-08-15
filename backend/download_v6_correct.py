#!/usr/bin/env python3
"""
ChoyrensAI-Telekom-Agent-v6-gguf modelini doğru dosya adıyla indiren script
"""

from huggingface_hub import hf_hub_download
from pathlib import Path

def download_v6_model():
    """v6 modelini doğru dosya adıyla indir"""
    
    # Model bilgileri
    repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
    filename = "ChoyrensAi-8b-q5_k_m.gguf"  # Doğru dosya adı
    
    # İndirme dizini
    download_dir = Path("models/v6_model")
    download_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 {repo_id} modeli indiriliyor...")
    print(f"📁 Dosya: {filename}")
    print(f"📁 İndirme dizini: {download_dir.absolute()}")
    
    try:
        # Modeli indir
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=download_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"✅ Model başarıyla indirildi!")
        print(f"📍 Konum: {model_path}")
        print(f"📊 Boyut: {Path(model_path).stat().st_size / (1024**3):.2f} GB")
        
        # Model bilgilerini yazdır
        print(f"\n🎯 Model Bilgileri:")
        print(f"   - Base Model: meta-llama/Meta-Llama-3-8B-Instruct")
        print(f"   - Quantization: 5-bit Q5_K_M")
        print(f"   - Format: GGUF")
        print(f"   - Türkçe Telekom AI Agent")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Model indirme hatası: {e}")
        return None

if __name__ == "__main__":
    print("🔍 v6 model indirme script'i başlatılıyor...")
    print("📋 Model: ChoyrensAI-Telekom-Agent-v6-gguf")
    print("🔗 Base: Meta-Llama-3-8B-Instruct")
    
    # Modeli indir
    model_path = download_v6_model()
    
    if model_path:
        print("\n🎯 Model başarıyla indirildi!")
        print("🔄 Backend'i yeniden başlatmanız gerekebilir.")
        print("💡 v6 modeli daha güncel ve gelişmiş özelliklere sahip!")
    else:
        print("\n❌ Model indirilemedi!") 