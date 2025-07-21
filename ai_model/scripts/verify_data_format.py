# -*- coding: utf-8 -*-
"""
🕵️ Veri Formatı Doğrulama Script'i (Data Format Verification Script)
======================================================================

Bu script'in tek amacı, eğitim verimizdeki bir örneğin, `expert_trainer.py`
içindeki formatlama mantığı ve tokenizer tarafından işlendiğinde, Llama-3'ün
beklediği nihai string formatına doğru bir şekilde dönüştürülüp
dönüştürülmediğini kontrol etmektir.

Bu, yeniden eğitim yapmadan önce, sorunun veri formatlamasında olup
olmadığını anlamak için kritik bir adımdır.
"""
import torch
import json
import os
import sys
from pathlib import Path
from transformers import AutoTokenizer
from rich.console import Console
from rich.syntax import Syntax
from dotenv import load_dotenv
import uuid  # expert_trainer'daki mantıkla aynı olması için

# --- Proje Kökü ve Sistem Yolu ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

sys.path.append(str(PROJECT_ROOT))
console = Console()

# --- Yapılandırma ---
BASE_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
DATA_FILE_PATH = PROJECT_ROOT / "UniqeAi/ai_model/data/expert_tool_chaining_data_v2_validated.json"

# --- Token Yükleme ---
def setup_huggingface_token():
    dotenv_path = PROJECT_ROOT / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    
    token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HF_TOKEN')
    if not token:
        console.print("[bold red]HATA: Hugging Face token bulunamadı![/bold red]")
        return None
    return token

# --- `expert_trainer.py`'den Kopyalanan Formatlama Fonksiyonu ---
# Bu fonksiyonun, ana eğitim script'indeki ile %100 aynı olması önemlidir.
def _format_dialogue(item):
    dialogue = []
    for turn in item["donguler"]:
        role = turn["rol"]
        content = turn.get("icerik")
        if role == "kullanici":
            dialogue.append({"role": "user", "content": content})
        elif role == "asistan":
            if content:
                dialogue.append({"role": "assistant", "content": content})
            if "arac_cagrilari" in turn and turn["arac_cagrilari"]:
                tool_calls = []
                for call in turn["arac_cagrilari"]:
                    tool_call_id = str(uuid.uuid4())
                    tool_calls.append({
                        "id": tool_call_id,
                        "type": "function",
                        "function": {"name": call["fonksiyon"], "arguments": json.dumps(call["parametreler"])}
                    })
                dialogue.append({"role": "assistant", "content": None, "tool_calls": tool_calls})
        elif role == "arac":
            try:
                last_tool_call_id = dialogue[-1]["tool_calls"][0]["id"]
                dialogue.append({"role": "tool", "content": content, "tool_call_id": last_tool_call_id})
            except (KeyError, IndexError):
                pass
    return dialogue

# --- Ana Doğrulama Fonksiyonu ---
def main():
    console.print("\n" + "="*60, style="bold yellow")
    console.print("🕵️  [bold yellow]Eğitim Veri Formatı Doğrulama Aracı[/bold yellow]")
    console.print("="*60)

    token = setup_huggingface_token()
    if not token:
        return

    # --- Tokenizer'ı Yükle ---
    try:
        console.print(f"\n[cyan]1. Tokenizer yükleniyor:[/cyan] {BASE_MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, token=token)
        console.print("[green]✅ Tokenizer başarıyla yüklendi.[/green]")
    except Exception as e:
        console.print(f"[bold red]HATA: Tokenizer yüklenemedi: {e}[/bold red]")
        return
        
    # --- Veri Örneğini Yükle ---
    try:
        console.print(f"\n[cyan]2. Veri dosyası okunuyor:[/cyan] {DATA_FILE_PATH}")
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Sadece ilk diyalog örneğini alıyoruz
        sample_item = data[0]
        console.print("[green]✅ İlk veri örneği başarıyla okundu.[/green]")
        console.print(f"   [dim]Senaryo: {sample_item['senaryo']}[/dim]")
    except Exception as e:
        console.print(f"[bold red]HATA: Veri dosyası okunamadı: {e}[/bold red]")
        return

    # --- Formatlama ve Çevirme İşlemi ---
    console.print("\n[cyan]3. Örnek veri, Llama-3 formatına çevriliyor...[/cyan]")
    
    # Adım a: Diyalogu sözlük listesine çevir
    dialogue_dict_list = _format_dialogue(sample_item)
    
    # Adım b: Tokenizer'ın `apply_chat_template` fonksiyonunu kullan
    # Bu, tüm özel Llama-3 token'larını ekleyerek nihai string'i oluşturur.
    final_formatted_string = tokenizer.apply_chat_template(
        dialogue_dict_list, 
        tokenize=False, 
        add_generation_prompt=False # Eğitimde de False kullanıyoruz
    )
    
    console.print("[green]✅ Çevirme işlemi tamamlandı.[/green]")
    
    # --- Sonucu Göster ---
    console.print("\n" + "-"*60, style="bold blue")
    console.print("✨ [bold blue]İŞLENMİŞ NİHAİ METİN (Modelin eğitimde gördüğü hali):[/bold blue]")
    console.print("-"*60)
    
    # Çıktıyı daha okunaklı hale getirmek için rich.Syntax kullanıyoruz
    syntax = Syntax(final_formatted_string, "html", theme="monokai", line_numbers=False)
    console.print(syntax)
    console.print("\n" + "-"*60, style="bold blue")
    console.print("❓ [bold]KONTROL EDİLECEKLER:[/bold]")
    console.print("   - Çıktıda `<|start_header_id|>tool_calls<|end_header_id|>` gibi özel token'lar görünüyor mu?")
    console.print("   - Araç çağırma parametreleri düzgün bir JSON string'i olarak görünüyor mu?")
    console.print("   - Genel yapı, Llama-3'ün resmi dökümantasyonundaki sohbet formatına benziyor mu?")
    console.print("-"*60)

if __name__ == "__main__":
    main() 