#!/usr/bin/env python3
"""
ChoyrensAI-Telekom-Agent-v6-gguf repository'sindeki dosyaları listeleyen script
"""

from huggingface_hub import list_repo_files
from huggingface_hub import hf_hub_download

def list_v6_files():
    """v6 repository'sindeki dosyaları listele"""
    
    repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
    
    print(f"🔍 {repo_id} repository'sindeki dosyalar listeleniyor...")
    
    try:
        # Repository'deki tüm dosyaları listele
        files = list_repo_files(repo_id)
        
        print(f"📁 Bulunan dosyalar ({len(files)} adet):")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file}")
            
        # GGUF dosyalarını bul
        gguf_files = [f for f in files if f.endswith('.gguf')]
        
        if gguf_files:
            print(f"\n🎯 GGUF model dosyaları ({len(gguf_files)} adet):")
            for i, file in enumerate(gguf_files, 1):
                print(f"  {i}. {file}")
                
            # İlk GGUF dosyasını indir
            if gguf_files:
                print(f"\n🚀 İlk GGUF dosyası indiriliyor: {gguf_files[0]}")
                download_v6_model(gguf_files[0])
        else:
            print("\n❌ GGUF dosyası bulunamadı!")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

def download_v6_model(filename):
    """Belirtilen dosyayı indir"""
    
    repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
    
    # İndirme dizini
    from pathlib import Path
    download_dir = Path("models/v6_model")
    download_dir.mkdir(parents=True, exist_ok=True)
    
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
        
        return model_path
        
    except Exception as e:
        print(f"❌ Model indirme hatası: {e}")
        return None

if __name__ == "__main__":
    print("🔍 v6 model dosyaları kontrol ediliyor...")
    list_v6_files() 