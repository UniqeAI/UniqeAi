# -*- coding: utf-8 -*-
"""
🚀 Hugging Face Modelini Evrensel GGUF Formatına Dönüştürme Script'i (v2 - Basitleştirilmiş)
==========================================================================================

Bu script, Hugging Face Hub'daki bir transformatör modelini, evrensel
GGUF formatına dönüştürür.

ÖNEMLİ GEREKSİNİM:
-------------------
Bu script'i çalıştırmadan önce, terminalde aşağıdaki komutu çalıştırarak
Hugging Face hesabınıza giriş yapmış olmalısınız:
```bash
huggingface-cli login
```

KULLANIM:
----------
Script'i proje ana dizininden çalıştırın:
```bash
python UniqeAi/ai_model/scripts/convert_to_gguf.py
```

"""
import os
import sys
import subprocess
from pathlib import Path
import shutil

# --- Yapılandırma ---
# Proje ana dizinini belirle (bu script'in bulunduğu yerin 4 üst dizini)
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    # Etkileşimli bir ortamda çalıştırılıyorsa (örn. Jupyter)
    PROJECT_ROOT = Path.cwd()

# Dönüştürülecek modelin Hugging Face Hub adresi
MODEL_ID = "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"

# llama.cpp'nin klonlanacağı dizin
LLAMA_CPP_DIR = PROJECT_ROOT / "UniqeAi" / "llama.cpp"

# GGUF modelinin kaydedileceği dizin
OUTPUT_DIR = PROJECT_ROOT / "UniqeAi" / "ai_model" / "gguf_model"

# GGUF niceleme (quantization) formatı.
# Q8_0, kalite ve dosya boyutu arasında harika bir denge sunar.
QUANTIZATION_TYPE = "Q8_0"

# --- Script Mantığı ---

def run_command(command, cwd, check=True):
    """Belirtilen dizinde bir komut çalıştırır ve çıktısını canlı olarak yazdırır."""
    print(f"🔩 Komut çalıştırılıyor: `{' '.join(command)}` in `{cwd}`")
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(line.strip())
        process.wait()
        if check and process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        print(f"✅ Komut başarıyla tamamlandı.")
        return True
    except FileNotFoundError:
        print(f"❌ HATA: Komut bulunamadı: `{command[0]}`. PATH ortam değişkeninizi kontrol edin.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ HATA: Komut `{e.cmd}` {e.returncode} hata koduyla başarısız oldu.")
        return False
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")
        return False

def setup_llama_cpp():
    """llama.cpp reposunu klonlar ve bağımlılıklarını kurar."""
    if not (LLAMA_CPP_DIR / "convert_hf_to_gguf.py").exists():
        if LLAMA_CPP_DIR.exists():
            print(f"🧹 Mevcut ama eksik `llama.cpp` klasörü temizleniyor...")
            shutil.rmtree(LLAMA_CPP_DIR)
        print(f"📂 `llama.cpp` klonlanıyor...")
        if not run_command(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", str(LLAMA_CPP_DIR)], cwd=PROJECT_ROOT):
            print("HATA: `llama.cpp` klonlanamadı. Git'in yüklü ve erişilebilir olduğundan emin olun.")
            sys.exit(1)
    else:
         print(f"✅ `llama.cpp` zaten doğru bir şekilde mevcut: {LLAMA_CPP_DIR}")

    print("🐍 `llama.cpp` Python bağımlılıkları kuruluyor...")
    requirements_path = LLAMA_CPP_DIR / "requirements.txt"
    if not run_command([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], cwd=LLAMA_CPP_DIR):
        print("HATA: `llama.cpp` bağımlılıkları kurulamadı.")
        sys.exit(1)
    if not run_command([sys.executable, "-m", "pip", "install", "sentencepiece"], cwd=LLAMA_CPP_DIR):
        print("HATA: 'sentencepiece' kurulamadı.")
        sys.exit(1)

def convert_model():
    """Modeli GGUF formatına dönüştürür."""
    print("\n" + "="*50)
    print("🚀 Model GGUF formatına dönüştürülüyor...")
    print(f"Model: {MODEL_ID}")
    print(f"Niceleme: {QUANTIZATION_TYPE}")
    print("="*50 + "\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_filename = f"{MODEL_ID.split('/')[-1].lower()}-{QUANTIZATION_TYPE.lower()}.gguf"
    output_filepath = OUTPUT_DIR / output_filename
    
    model_download_path = LLAMA_CPP_DIR / "models" / MODEL_ID.split("/")[-1]

    convert_script = LLAMA_CPP_DIR / "convert_hf_to_gguf.py"

    command = [
        sys.executable,
        str(convert_script),
        MODEL_ID,
        "--remote",
        "--outfile",
        str(output_filepath),
        "--outtype",
        QUANTIZATION_TYPE.lower(),
    ]

    if not run_command(command, cwd=LLAMA_CPP_DIR):
        print("❌ HATA: Model dönüştürme işlemi başarısız oldu.")
        if model_download_path.exists():
            print(f"🧹 Temizlik: İndirilen model kalıntıları siliniyor: {model_download_path}")
            shutil.rmtree(model_download_path, ignore_errors=True)
        sys.exit(1)
        
    print("\n" + "*"*50)
    print("🎉 DÖNÜŞTÜRME BAŞARILI! 🎉")
    print(f"Modeliniz şuraya kaydedildi: {output_filepath}")
    if output_filepath.exists():
        print(f"Dosya Boyutu: {output_filepath.stat().st_size / (1024**3):.2f} GB")
    print("*"*50)
    
    if model_download_path.exists():
        print(f"🧹 Temizlik: İndirilen orijinal model siliniyor: {model_download_path}")
        shutil.rmtree(model_download_path, ignore_errors=True)


def main():
    """Ana çalışma fonksiyonu."""
    print("=== GGUF DÖNÜŞTÜRME SİHİRBAZI (v2) ===")
    os.chdir(PROJECT_ROOT)
    setup_llama_cpp()
    convert_model()
    print("\n✅ Tüm işlemler tamamlandı.")

if __name__ == "__main__":
    main() 