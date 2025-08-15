# -*- coding: utf-8 -*-
"""
🔍 DEBUG MODEL OUTPUT - Model Çıktısı Analizi
=============================================

Bu script, modelin ham çıktısını analiz ederek hangi formatta
araç çağrıları yaptığını tespit eder.
"""

import os
import sys
from pathlib import Path
from rich.console import Console

# --- Proje Kök Dizini ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except (NameError, IndexError):
    PROJECT_ROOT = Path.cwd()

GGUF_MODEL_DIR = PROJECT_ROOT / "UniqeAi/ai_model/gguf_model"

console = Console()

def find_latest_gguf_model(model_dir: Path):
    """En yeni GGUF modelini bulur"""
    if not model_dir.exists():
        return None
    gguf_files = list(model_dir.glob("*.gguf"))
    if not gguf_files:
        return None
    return max(gguf_files, key=lambda p: p.stat().st_mtime)

def debug_model_response():
    """Model yanıtını debug eder"""
    
    try:
        from llama_cpp import Llama
    except ImportError:
        console.print("[bold red]HATA: llama-cpp-python kurulu değil.[/bold red]")
        return

    model_path = find_latest_gguf_model(GGUF_MODEL_DIR)
    if not model_path:
        console.print("[bold red]HATA: GGUF model bulunamadı![/bold red]")
        return

    console.print(f"[yellow]🔍 Model yükleniyor: {model_path.name}[/yellow]")

    llm = Llama(
        model_path=str(model_path),
        n_ctx=4096,
        n_gpu_layers=-1,
        n_threads=os.cpu_count() - 1 if os.cpu_count() and os.cpu_count() > 1 else 1,
        verbose=False,
        chat_format="llama-3"
    )

    # Test mesajları
    test_cases = [
        {
            "name": "Basit Fatura Sorgusu",
            "input": "Faturamı görmek istiyorum"
        },
        {
            "name": "Veri Seti Tarzı Karmaşık",
            "input": "Babam geçen ay vefat etti. Onun telefonunu ve internet aboneliğini kapatmak istiyorum ama çok zor geliyor. Bu süreçte bana nasıl yardımcı olabilirsiniz?"
        }
    ]

    system_prompt = """Sen, UniqeAi tarafından geliştirilmiş uzman bir Telekom Müşteri Hizmetleri Asistanısın. 

Kullanabileceğin araçlar:
- get_current_bill: Güncel fatura bilgilerini getirir
- get_customer_profile: Müşteri profil bilgilerini getirir  
- pay_bill: Fatura ödeme işlemi yapar

Bir aracı kullanman gerektiğinde, şu formatlardan birini kullan:
1. <|begin_of_tool_code|>print(fonksiyon_adi(parametre=deger))<|end_of_tool_code|>
2. arac_cagrilari: [{"fonksiyon": "fonksiyon_adi", "parametreler": {"parametre": "deger"}}]

Her iki formatı da dene ve hangi birini tercih ettiğini göster."""

    for test_case in test_cases:
        console.print(f"\n{'='*60}")
        console.print(f"🧪 [bold blue]Test: {test_case['name']}[/bold blue]")
        console.print(f"{'='*60}")
        
        console.print(f"👤 [bold blue]Kullanıcı:[/bold blue] {test_case['input']}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": test_case['input']}
        ]
        
        console.print("[yellow]... model düşünüyor ...[/yellow]")
        
        response = llm.create_chat_completion(
            messages=messages,
            temperature=0.2,
            stop=["<|eot_id|>"],
        )
        
        raw_response = response['choices'][0]['message']['content']
        
        console.print(f"\n🤖 [bold green]Model (HAM ÇIKTI):[/bold green]")
        console.print(f"[cyan]{raw_response}[/cyan]")
        
        # Format analizi
        console.print(f"\n🔍 [bold yellow]FORMAT ANALİZİ:[/bold yellow]")
        
        if "<|begin_of_tool_code|>" in raw_response:
            console.print("✅ İngilizce tool code formatı BULUNDU")
        else:
            console.print("❌ İngilizce tool code formatı bulunamadı")
            
        if "arac_cagrilari" in raw_response:
            console.print("✅ Türkçe araç çağrısı formatı BULUNDU")
        else:
            console.print("❌ Türkçe araç çağrısı formatı bulunamadı")
            
        if "print(" in raw_response:
            console.print("✅ Print formatı BULUNDU")
        else:
            console.print("❌ Print formatı bulunamadı")

        console.print(f"\n📊 [bold magenta]SONUÇ:[/bold magenta]")
        if "<|begin_of_tool_code|>" in raw_response or "arac_cagrilari" in raw_response:
            console.print("🎯 Model araç çağrısı yapmaya çalışıyor!")
        else:
            console.print("⚠️ Model araç çağrısı yapmıyor - sadece metin yanıt veriyor")

if __name__ == "__main__":
    console.print("\n🔍 [bold green]DEBUG MODEL OUTPUT - Model Format Analizi[/bold green]")
    console.print("="*60)
    debug_model_response()