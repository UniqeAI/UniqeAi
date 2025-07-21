# -*- coding: utf-8 -*-
"""
✅ Güvenilir Model Birleştirme Script'i (Reliable Model Merging Script)
======================================================================

Bu script, QLoRA eğitiminin çıktısı olan adaptör (LoRA) ağırlıklarını,
temel Llama-3 modeliyle birleştirerek tek parça, dağıtıma hazır bir
model oluşturur.

Bu süreç, "beyni ölmüş" model sorununu çözmek için kritik öneme sahiptir.
"""
import torch
import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from rich.console import Console
from dotenv import load_dotenv

console = Console()

# --- Proje Kök Dizini Tanımlaması ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

# --- Yapılandırma ---

# 1. Orijinal, temel modelin adı. Eğitimde hangi modeli kullandıysanız o olmalı.
BASE_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# 2. `expert_trainer.py`'nin ürettiği ve adaptör ağırlıklarını içeren klasör.
ADAPTER_MODEL_PATH = PROJECT_ROOT / "UniqeAi/ai_model/final-model_v2/final_model"

# 3. Birleştirilmiş yeni modelin kaydedileceği klasör.
#    Eski, bozuk olandan ayırmak için yeni bir isim veriyoruz.
MERGED_MODEL_SAVE_PATH = PROJECT_ROOT / "UniqeAi/ai_model/merged_model_v3"

# --- YENİ: HUGGING FACE HUB YAPILANDIRMASI ---
# 4. Modeli Hugging Face Hub'a yüklemek için bayrak.
#    Bunu `True` yaparsanız, script birleştirmeden sonra modeli Hub'a yükler.
PUSH_TO_HUB = True 

# 5. Modelin Hugging Face Hub'da alacağı isim.
#    Bunu kendi kullanıcı adınızla değiştirmelisiniz: "kullanici_adiniz/model_adi"
HF_REPO_NAME = "Choyrens/ChoyrensAI-Telekom-Agent-v1"


def main():
    """Ana birleştirme ve yükleme fonksiyonu."""
    console.print("\n" + "="*50, style="bold green")
    console.print("🚀 [bold green]Güvenilir Model Birleştirme Süreci Başlatılıyor...[/bold green]")
    console.print("="*50, style="bold green")

    console.print(f"📖 [cyan]Temel Model:[/cyan] {BASE_MODEL_NAME}")
    console.print(f"🔩 [cyan]Adaptör Modeli:[/cyan] {ADAPTER_MODEL_PATH}")
    console.print(f"💾 [cyan]Hedef Klasör:[/cyan] {MERGED_MODEL_SAVE_PATH}")
    if PUSH_TO_HUB:
        console.print(f"☁️  [cyan]Hub Repo:[/cyan] {HF_REPO_NAME}")

    # --- Token Kontrolü (Düzeltilmiş) ---
    # Ortam değişkenlerini yüklemeden önce .env dosyasını okumasını sağlıyoruz
    dotenv_path = PROJECT_ROOT / ".env"
    if dotenv_path.exists():
        console.print(f"Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    
    hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HF_TOKEN')

    if not hf_token:
        console.print("[bold red]HATA: Hugging Face token bulunamadı![/bold red]")
        console.print("Lütfen proje kök dizinindeki `.env` dosyasında `HUGGINGFACE_HUB_TOKEN='hf_...'` satırının olduğundan emin olun.")
        return

    # --- Adım 1: Temel Modeli Yükle ---
    console.print("\n[yellow]1. Temel model (Llama-3) yükleniyor...[/yellow]")
    try:
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            token=hf_token # Token'ı doğrudan kullanıyoruz
        )
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, token=hf_token)
        console.print("[green]✅ Temel model başarıyla yüklendi.[/green]")
    except Exception as e:
        console.print(f"[bold red]HATA: Temel model yüklenemedi. İnternet bağlantınızı veya model adını kontrol edin.[/bold red]")
        console.print(e)
        return

    # --- Adım 2: LoRA Adaptörünü Yükle ve Birleştir ---
    console.print("\n[yellow]2. LoRA adaptörü yükleniyor ve birleştiriliyor...[/yellow]")
    try:
        # PeftModel, adaptörü temel modelin üzerine yükler
        merged_model = PeftModel.from_pretrained(base_model, str(ADAPTER_MODEL_PATH))
        # `merge_and_unload` ile adaptör ağırlıklarını temel modele kalıcı olarak işler
        merged_model = merged_model.merge_and_unload()
        console.print("[green]✅ Adaptör başarıyla birleştirildi.[/green]")
    except Exception as e:
        console.print(f"[bold red]HATA: Adaptör yüklenemedi veya birleştirilemedi.[/bold red]")
        console.print(f"Lütfen '{ADAPTER_MODEL_PATH}' klasörünün geçerli bir adaptör içerdiğinden emin olun.")
        console.print(e)
        return

    # --- Adım 3: Birleştirilmiş Modeli Kaydet ---
    console.print(f"\n[yellow]3. Yeni, birleştirilmiş model '{MERGED_MODEL_SAVE_PATH}' klasörüne kaydediliyor...[/yellow]")
    try:
        os.makedirs(MERGED_MODEL_SAVE_PATH, exist_ok=True)
        merged_model.save_pretrained(str(MERGED_MODEL_SAVE_PATH))
        tokenizer.save_pretrained(str(MERGED_MODEL_SAVE_PATH))
        console.print(f"[bold green]🎉 Harika! Model başarıyla birleştirildi ve kaydedildi.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]HATA: Birleştirilmiş model kaydedilemedi.[/bold red]")
        console.print(e)
        return

    # --- YENİ: Adım 4: Modeli Hugging Face Hub'a Yükle ---
    if PUSH_TO_HUB:
        console.print(f"\n[yellow]4. Model Hugging Face Hub'a yükleniyor: '{HF_REPO_NAME}'...[/yellow]")
        try:
            # `blocking=False` ile yüklemenin asenkron yapılmasını sağlayarak büyük dosyalarda
            # terminalin donmasını engelleriz. `True` daha basit ve sıralıdır.
            merged_model.push_to_hub(HF_REPO_NAME, token=hf_token, safe_serialization=True)
            tokenizer.push_to_hub(HF_REPO_NAME, token=hf_token)
            console.print(f"[bold green]🚀 Model başarıyla Hugging Face Hub'a yüklendi![/bold green]")
            console.print(f"   Modelinize şuradan erişebilirsiniz: [link]https://huggingface.co/{HF_REPO_NAME}[/link]")
        except Exception as e:
            console.print(f"[bold red]HATA: Model Hugging Face Hub'a yüklenemedi.[/bold red]")
            console.print("Repo'nun Hugging Face sitesinde oluşturulduğundan ve token'ınızın 'write' yetkisine sahip olduğundan emin olun.")
            console.print(e)
            return


if __name__ == "__main__":
    main() 