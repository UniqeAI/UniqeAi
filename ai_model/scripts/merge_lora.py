# -*- coding: utf-8 -*-
"""
✅ Güvenilir Model Birleştirme Script'i (Reliable Model Merging Script)
======================================================================

QLoRA adaptör ağırlıklarını temel model ile birleştirir,
tek parça, dağıtıma hazır model üretir.
"""

import torch
import os
import sys
from pathlib import Path
import tempfile
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from dotenv import load_dotenv

# Rich kullanılamazsa fallback olarak logging'e geç
try:
    from rich.console import Console
    console = Console()
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    class ConsoleFallback:
        def print(self, msg, **kwargs):
            logging.info(msg)
    console = ConsoleFallback()

# --- Proje kök dizini tanımlama ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

# --- Yapılandırmalar ---
BASE_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
ADAPTER_MODEL_PATH = PROJECT_ROOT / "UniqeAi/ai_model/results/final_model_v6"
MERGED_MODEL_SAVE_PATH = PROJECT_ROOT / "UniqeAi/ai_model/merged_model_v6"
PUSH_TO_HUB = False
HF_REPO_NAME = "Choyrens/ChoyrensAI-Telekom-Agent-v5"

def main():
    # --- Python sürüm kontrolü ---
    if sys.version_info < (3, 9):
        console.print("[bold red]⚠️ Python 3.9+ sürümü önerilir.[/bold red]")

    console.print("\n" + "="*50, style="bold green")
    console.print("🚀 [bold green]Güvenilir Model Birleştirme Süreci Başlatılıyor...[/bold green]")
    console.print("="*50, style="bold green")

    console.print(f"📖 [cyan]Temel Model:[/cyan] {BASE_MODEL_NAME}")
    console.print(f"🔩 [cyan]Adaptör Modeli:[/cyan] {ADAPTER_MODEL_PATH}")
    console.print(f"💾 [cyan]Hedef Klasör:[/cyan] {MERGED_MODEL_SAVE_PATH}")
    if PUSH_TO_HUB:
        console.print(f"☁️  [cyan]Hub Repo:[/cyan] {HF_REPO_NAME}")

    # .env dosyası yükleniyor
    dotenv_path = PROJECT_ROOT / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)

    hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HF_TOKEN')
    if not hf_token:
        console.print("[bold red]HATA: Hugging Face token bulunamadı![/bold red]")
        sys.exit(1)

    # --- Temel model yükleniyor ---
    console.print("\n[yellow]1. Temel model (Llama-3) yükleniyor...[/yellow]")
    try:
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            token=hf_token
        )
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, token=hf_token)

        # Tokenizer pad_token kontrolü
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            console.print("[blue]ℹ️ Tokenizer pad_token ayarlandı.[/blue]")

        device_info = next(base_model.parameters()).device
        console.print(f"✅ Model yüklendi. [cyan]Cihaz:[/cyan] {device_info}")
    except Exception as e:
        console.print("[bold red]HATA: Temel model yüklenemedi.[/bold red]")
        console.print(e)
        sys.exit(1)

    # --- LoRA adaptörü birleştiriliyor ---
    console.print("\n[yellow]2. LoRA adaptörü yükleniyor ve birleştiriliyor...[/yellow]")
    try:
        # Geçici offload klasörü oluşturuluyor
        offload_dir = tempfile.mkdtemp(prefix="offload_")
        merged_model = PeftModel.from_pretrained(
            base_model,
            str(ADAPTER_MODEL_PATH),
            device_map="auto",
            offload_folder=offload_dir
        )
        merged_model = merged_model.merge_and_unload()
        console.print("[green]✅ Adaptör başarıyla birleştirildi.[/green]")
    except Exception as e:
        console.print("[bold red]HATA: Adaptör yüklenemedi veya birleştirilemedi.[/bold red]")
        console.print(e)
        sys.exit(1)

    # --- Hedef klasör kontrolü ---
    if MERGED_MODEL_SAVE_PATH.exists():
        console.print(f"[bold yellow]⚠️ Uyarı: '{MERGED_MODEL_SAVE_PATH}' klasörü mevcut, üzerine yazılacak.[/bold yellow]")

    # --- Model kaydediliyor ---
    console.print(f"\n[yellow]3. Model '{MERGED_MODEL_SAVE_PATH}' klasörüne kaydediliyor...[/yellow]")
    try:
        os.makedirs(MERGED_MODEL_SAVE_PATH, exist_ok=True)
        merged_model.save_pretrained(str(MERGED_MODEL_SAVE_PATH), max_shard_size="2GB")
        tokenizer.save_pretrained(str(MERGED_MODEL_SAVE_PATH))

        # config.json kontrolü
        if not (MERGED_MODEL_SAVE_PATH / "config.json").exists():
            console.print("[red]⚠️ Uyarı: config.json eksik olabilir![/red]")

        console.print("[bold green]🎉 Model başarıyla kaydedildi.[/bold green]")
    except Exception as e:
        console.print("[bold red]HATA: Model kaydedilemedi.[/bold red]")
        console.print(e)
        sys.exit(1)

    # --- Hugging Face Hub'a yükleme ---
    if PUSH_TO_HUB:
        console.print(f"\n[yellow]4. Hugging Face Hub'a yükleniyor: '{HF_REPO_NAME}'...[/yellow]")
        try:
            merged_model.push_to_hub(HF_REPO_NAME, token=hf_token, safe_serialization=True)
            tokenizer.push_to_hub(HF_REPO_NAME, token=hf_token)
            console.print(f"[bold green]🚀 Model Hugging Face Hub'a yüklendi: https://huggingface.co/{HF_REPO_NAME}[/bold green]")
        except Exception as e:
            console.print("[bold red]HATA: Hugging Face Hub'a yükleme başarısız oldu.[/bold red]")
            console.print(e)
            sys.exit(1)

if __name__ == "__main__":
    main()
