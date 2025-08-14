# -*- coding: utf-8 -*-
"""
🚀 Uzman Seviye İnteraktif Test Alanı (Advanced Interactive Playground) - v4 (Diagnostik Modlu)
================================================================================================

Bu script, eğitilmiş ve birleştirilmiş (merged) QLoRA modelinizin
hem temel akıl sağlığını hem de araç kullanma yeteneklerini test etmek
için bir "basit mod" içerir.

Önceki hataların tümü giderilmiştir:
- ✅ **KESİN ÇÖZÜM:** Tensor oluşturma süreci manueldir.
- ✅ **YENİ - Diagnostik Modu:** '!simple' komutu ile modelin temel konuşma
  yetenekleri, araç-çağırma mantığı olmadan test edilebilir. Bu, sorunun
  modelin kendisinde mi yoksa tool-following yeteneğinde mi olduğunu anlamamızı sağlar.
"""

import os
import torch
import json
import re
import sys
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from rich.console import Console
from rich.markdown import Markdown

try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

sys.path.append(str(PROJECT_ROOT))

from UniqeAi.ai_model.scripts.tool_definitions import get_tool_definitions, get_tool_response

console = Console()

MODEL_PATH = PROJECT_ROOT / "UniqeAi/ai_model/merged_model_bf16"

def load_model_and_tokenizer(model_path: Path):
    console.print(f"[yellow]🚀 Model yükleniyor: [cyan]{model_path}[/cyan][/yellow]")
    if not model_path.exists():
        console.print(f"[bold red]HATA: Model yolu bulunamadı![/bold red]")
        sys.exit(1)

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_path)
    except Exception as e:
        console.print(f"[bold red]Model veya Tokenizer yüklenirken hata oluştu: {e}[/bold red]")
        sys.exit(1)

    console.print("[green]✅ Model ve Tokenizer başarıyla yüklendi.[/green]")
    return model, tokenizer

def parse_tool_calls(text: str):
    """
    Modelin çıktısındaki DÜZELTİLMİŞ tool-call formatını yakalar.
    <|begin_of_tool_code|> ... <|end_of_tool_code|>
    """
    pattern = r"<\|begin_of_tool_code\|>([\s\S]*?)<\|end_of_tool_code\|>"
    match = re.search(pattern, text)
    if not match:
        return None
    
    tool_code_str = match.group(1).strip()
    
    # "print(fonksiyon(arg=val))" formatını yakalamak için daha esnek bir regex
    call_pattern = re.compile(r"print\((\w+)\((.*)\)\)")
    call_match = call_pattern.search(tool_code_str)
    
    if not call_match:
        return None
        
    function_name = call_match.group(1)
    args_str = call_match.group(2)
    
    try:
        params = {}
        # String değerleri doğru şekilde yakalamak için daha sağlam bir regex
        arg_pattern = re.compile(r"(\w+)=((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[^,)]+)")
        for p_match in arg_pattern.finditer(args_str):
            key = p_match.group(1)
            raw_value = p_match.group(2)

            # Değerin tırnak içinde olup olmadığını kontrol et ve temizle
            if (raw_value.startswith('"') and raw_value.endswith('"')) or \
               (raw_value.startswith("'") and raw_value.endswith("'")):
                # JSON'un string ayrıştırma yeteneğini kullanarak kaçış karakterlerini doğru yönet
                value = json.loads(raw_value)
            else:
                # Sayısal veya boolean olabilir
                try:
                    # json.loads() sayıları ve boolean'ları da doğru şekilde işler
                    value = json.loads(raw_value.lower()) # 'True' -> true
                except (json.JSONDecodeError, AttributeError):
                    value = raw_value # Ham string olarak bırak

            params[key] = value

        return [{
            "id": f"tool_call_{os.urandom(4).hex()}",
            "type": "function",
            "function": {
                "name": function_name,
                "arguments": json.dumps(params, ensure_ascii=False)
            }
        }]
    except Exception as e:
        console.print(f"[red]Araç parametreleri ayrıştırılamadı: {args_str}, Hata: {e}[/red]")
        return None

def main():
    model, tokenizer = load_model_and_tokenizer(MODEL_PATH)
    tools = get_tool_definitions() # Bu script OpenAI formatını kullandığı için tool tanımlarına ihtiyaç duyar.
    terminators = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    dialogue = []

    console.print("\n" + "="*50, style="bold green")
    console.print("🤖 [bold green]Diagnostik Test Alanına Hoş Geldiniz (v4 - Geri Yüklendi)[/bold green]")
    console.print("   - Normal komut girerek [bold]araç kullanma[/bold] yeteneğini test edin.")
    console.print("   - `!simple <sorunuz>` yazarak modelin [bold]temel konuşma[/bold] yeteneğini test edin.")
    console.print("   - Çıkmak için 'quit' veya 'exit' yazın.")
    console.print("="*50, style="bold green")

    while True:
        try:
            user_input = console.input("[bold blue]👤 Siz: [/bold blue]")
            if user_input.lower() in ["quit", "exit"]: break
        except (KeyboardInterrupt, EOFError): break

        # --- Diagnostik Mantığı ---
        if user_input.startswith("!simple "):
            # --- BASİT TEST MODU ---
            simple_question = user_input[len("!simple "):]
            simple_dialogue = [{"role": "user", "content": simple_question}]
            
            console.print("[yellow]... model basit modda düşünüyor ...[/yellow]")
            
            # Araçlar olmadan, basit bir şablon uygula
            token_ids = tokenizer.apply_chat_template(simple_dialogue, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)
            attention_mask = torch.ones_like(token_ids)

            outputs = model.generate(
                input_ids=token_ids,
                attention_mask=attention_mask,
                max_new_tokens=256,
                eos_token_id=terminators,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
            response_text = tokenizer.decode(outputs[0][token_ids.shape[-1]:], skip_special_tokens=True)
            console.print(f"🤖 [bold green]Asistan (Basit Yanıt):[/bold green]", end="")
            console.print(Markdown(response_text))
            # Basit testler ana konuşma geçmişine eklenmez, her seferinde temiz başlar.
        
        else:
            # --- NORMAL ARAÇ KULLANIM MODU (OpenAI Stili) ---
            # Bu script'in kullandığı diyalog formatı, `terminal_app.py`den farklıdır.
            # Bu format OpenAI API'sine daha yakındır.
            dialogue.append({"role": "user", "content": user_input})
            console.print("[yellow]... model düşünüyor ...[/yellow]")

            # Not: Bu script'in kullandığı `apply_chat_template` formatı (tools parametresi ile)
            # aslında Llama-3'ün standart tool kullanımı için önerilmez, ama test için bir yöntemdir.
            token_ids = tokenizer.apply_chat_template(dialogue, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)
            attention_mask = torch.ones_like(token_ids)

            outputs = model.generate(
                input_ids=token_ids,
                attention_mask=attention_mask,
                max_new_tokens=1024,
                eos_token_id=terminators,
                do_sample=True, temperature=0.6, top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
            response_text = tokenizer.decode(outputs[0][token_ids.shape[-1]:], skip_special_tokens=False)
            
            # Bu script'in `parse_tool_calls` fonksiyonu, `terminal_app.py`'daki ile aynı.
            tool_calls = parse_tool_calls(response_text)
            
            if tool_calls:
                # `tool_calls` formatı OpenAI API'sinin beklediği formattır.
                # Eğitim verimiz bu formatı doğrudan içermese de, Llama-3 bazen bu formatı üretebilir.
                # `terminal_app.py`deki metin bazlı yaklaşım daha güvenilirdir.
                dialogue.append({"role": "assistant", "content": None, "tool_calls": tool_calls})
                
                for call in tool_calls:
                    func_name = call["function"]["name"]
                    func_args = json.loads(call["function"]["arguments"])
                    tool_call_id = call["id"]
                    console.print(f"🛠️  [bold yellow]Araç Çağrısı:[/bold yellow] [green]{func_name}[/green]({json.dumps(func_args, ensure_ascii=False)})")
                    
                    tool_response_content = get_tool_response(func_name, func_args)
                    console.print(f"⚙️  [bold magenta]Araç Yanıtı:[/bold magenta] {tool_response_content}")
                    
                    dialogue.append({"role": "tool", "name": func_name, "tool_call_id": tool_call_id, "content": tool_response_content})

                console.print("[yellow]... model araç sonuçlarını özetliyor ...[/yellow]")

                final_token_ids = tokenizer.apply_chat_template(dialogue, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)
                final_attention_mask = torch.ones_like(final_token_ids)

                final_outputs = model.generate(
                    input_ids=final_token_ids,
                    attention_mask=final_attention_mask,
                    max_new_tokens=1024,
                    eos_token_id=terminators,
                    do_sample=True, temperature=0.6, top_p=0.9,
                    pad_token_id=tokenizer.eos_token_id
                )
                final_response_text = tokenizer.decode(final_outputs[0][final_token_ids.shape[-1]:], skip_special_tokens=True)
                console.print(f"🤖 [bold green]Asistan:[/bold green] ", end="")
                console.print(Markdown(final_response_text))
                dialogue.append({"role": "assistant", "content": final_response_text})
            else:
                cleaned_response = re.sub(r'<\|.*?\|>', '', response_text).strip()
                console.print(f"🤖 [bold green]Asistan:[/bold green] ", end="")
                console.print(Markdown(cleaned_response))
                dialogue.append({"role": "assistant", "content": cleaned_response})
    
    console.print("\n[bold red]Görüşmek üzere![/bold red]")

if __name__ == "__main__":
    main() 