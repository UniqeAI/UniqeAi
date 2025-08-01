# -*- coding: utf-8 -*-
"""
🚀 GGUF Modelini Hugging Face Hub'a Yükleme Betiği v1.0
=========================================================

Bu betik, yerel bir klasörde bulunan en güncel GGUF modelini 
belirtilen bir Hugging Face deposuna yüklemek için tasarlanmıştır.

KULLANIM:
1.  **`.env` Dosyasını Hazırlayın:**
    Projenizin kök dizininde (`tddi_proje_planlama/`) bir `.env` dosyası 
    oluşturun ve içine Hugging Face token'ınızı ekleyin:
    
    ```
    HUGGINGFACE_HUB_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxx"
    ```

2.  **Gerekli Kütüphaneyi Kurun:**
    ```bash
    pip install huggingface_hub
    ```

3.  **Betiği Çalıştırın:**
    Terminalde `UniqeAi/ai_model/scripts/` klasöründeyken aşağıdaki komutu
    kullanarak betiği çalıştırın. `YOUR_USERNAME` ve `YOUR_REPO_NAME` 
    kısımlarını kendi bilgilerinizle değiştirin.

    ```bash
    python upload_gguf_to_hf.py --repo_id "YOUR_USERNAME/YOUR_REPO_NAME"
    ```

    Eğer model farklı bir klasördeyse `--model_dir` argümanını kullanabilirsiniz:
    ```bash
    python upload_gguf_to_hf.py --repo_id "MyUser/MyTelcoLLM-GGUF" --model_dir "../gguf_model_v2"
    ```
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import HfApi, HfFolder

# --- Proje Kök Dizini ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except (NameError, IndexError):
    PROJECT_ROOT = Path.cwd()

def setup_huggingface_token() -> str:
    """
    .env dosyasından Hugging Face token'ını yükler ve doğrular.
    """
    print("🔑 Hugging Face token'ı ayarlanıyor...")
    dotenv_path = PROJECT_ROOT / ".env"
    if not dotenv_path.exists():
        raise FileNotFoundError(
            f"Lütfen proje kök dizinine (.env) adında bir dosya oluşturun ve "
            f"'HUGGINGFACE_HUB_TOKEN=\"hf_...\"' formatında token'ınızı ekleyin."
        )
        
    load_dotenv(dotenv_path=dotenv_path)
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    
    if not token:
        raise ValueError("HUGGINGFACE_HUB_TOKEN .env dosyasında bulunamadı.")
        
    HfFolder.save_token(token)
    print("✅ Token başarıyla ayarlandı.")
    return token

def find_latest_gguf_model(model_dir: Path) -> Path:
    """
    Verilen klasördeki en güncel .gguf dosyasını bulur.
    """
    print(f"🤖 Model aranıyor: {model_dir}")
    if not model_dir.exists():
        raise FileNotFoundError(f"HATA: Model klasörü bulunamadı: {model_dir}")
        
    gguf_files = list(model_dir.glob("*.gguf"))
    if not gguf_files:
        raise FileNotFoundError(f"HATA: '{model_dir}' içinde hiç .gguf dosyası bulunamadı.")
        
    latest_model_path = max(gguf_files, key=lambda p: p.stat().st_mtime)
    print(f"✅ En yeni model bulundu: {latest_model_path.name}")
    return latest_model_path

def upload_model(repo_id: str, model_path: Path, token: str):
    """
    Modeli Hugging Face Hub'a yükler.
    """
    api = HfApi(token=token)
    
    print(f"🌍 Hugging Face deposu kontrol ediliyor: {repo_id}")
    try:
        api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
        print(f"✅ Depo mevcut veya yeni oluşturuldu: {repo_id}")
    except Exception as e:
        print(f"❌ Depo oluşturulurken bir hata oluştu: {e}")
        return

    print(f"🚀 Model yükleniyor: {model_path.name} -> {repo_id}")
    try:
        url = api.upload_file(
            path_or_fileobj=str(model_path),
            path_in_repo=model_path.name,
            repo_id=repo_id,
            repo_type="model",
        )
        print("\n" + "="*50)
        print("🎉 YÜKLEME BAŞARILI! 🎉")
        print(f"Model URL: {url}")
        print("="*50)
    except Exception as e:
        print(f"❌ Model yüklenirken kritik bir hata oluştu: {e}")

def main():
    parser = argparse.ArgumentParser(description="GGUF modelini Hugging Face Hub'a yükle.")
    parser.add_argument(
        "--repo_id",
        type=str,
        required=True,
        help="Hugging Face Hub'daki depo ID'si (ör. 'kullanici_adi/repo_adi')."
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="UniqeAi/ai_model/gguf_model_v2",
        help="GGUF model dosyalarının bulunduğu klasörün yolu."
    )
    
    args = parser.parse_args()
    
    model_dir_path = PROJECT_ROOT / args.model_dir

    try:
        token = setup_huggingface_token()
        model_to_upload = find_latest_gguf_model(model_dir_path)
        upload_model(args.repo_id, model_to_upload, token)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n❌ Hata: {e}")
    except Exception as e:
        print(f"\n❌ Beklenmedik bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
