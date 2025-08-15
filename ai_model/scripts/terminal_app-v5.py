# -*- coding: utf-8 -*-
"""
🤖 ChoyrensAI Telekom Agent - Terminal Uygulaması v1.0
======================================================

Bu uygulama, Hugging Face Hub'a yüklenmiş olan "ChoyrensAI-Telekom-Agent"
modeli ile interaktif bir sohbet oturumu başlatır.

Kullanıcılar, Python veya herhangi bir kütüphane bilgisine ihtiyaç duymadan,
doğrudan bu uygulama üzerinden modelin araç kullanma ve akıl yürütme
yeteneklerini test edebilirler.

Nasıl Çalışır?
1. Başlangıçta modeli Hugging Face Hub'dan indirir (veya önbellekten yükler).
2. Renkli ve temiz bir sohbet arayüzü sunar.
3. Arka planda tüm araç çağırma ve yanıt işleme mantığını yönetir.
"""

import os
import torch
import json
import re
import sys
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextStreamer
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
# rich.markup.escape artık kullanılmayacağı için kaldırılabilir veya kalabilir.
# Temizlik açısından kaldırmak daha iyidir ama bırakmak da sorun yaratmaz.

# --- Proje Kök Dizini ve Modül Yolu ---
try:
    # Bu script 'scripts' klasöründe olduğu için 3 seviye yukarı çıkıyoruz.
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    # Alternatif olarak, mevcut çalışma dizinini kök olarak kabul et.
    PROJECT_ROOT = Path.cwd()

# tool_definitions.py'yi import edebilmek için yolu sisteme ekliyoruz.
sys.path.append(str(PROJECT_ROOT))
from UniqeAi.ai_model.scripts.tool_definitions_v5 import get_tool_definitions, get_tool_response

console = Console()

# --- YENİ: Model Yapılandırması ---
# Yerel modeli mi (True) yoksa Hugging Face Hub'daki modeli mi (False) kullanacağınızı seçin.
# ŞİMDİLİK YEREL TEST İÇİN AYARLANDI.
USE_LOCAL_MODEL = True

if USE_LOCAL_MODEL:
    # merge_lora.py'nin oluşturduğu yerel birleştirilmiş modelin yolu
    MODEL_PATH_OR_REPO_ID = PROJECT_ROOT / "UniqeAi/ai_model/merged_model_v5"
else:
    # Arkadaşlarınızla paylaşmak için Hugging Face Hub'daki repo adı
    MODEL_PATH_OR_REPO_ID = "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"

# --- YENİ: Konuşma Geçmişi Limiti ---
# Modelin "odaklanacağı" en son kaç mesajın (kullanıcı + asistan) seçileceğini belirler.
# Bu, "context" sorununu (kafa karışıklığını) çözerken uzun hafızayı korur.
FOCUSED_HISTORY_TURNS = 4

def load_huggingface_token():
    """Token'ı .env dosyasından okur ve doğrular."""
    # --- YENİ: Paketlenmiş uygulama için .env yolu düzeltmesi ---
    if getattr(sys, 'frozen', False):
        # Eğer uygulama paketlenmişse (.exe ise), .env dosyasını .exe'nin yanından arar.
        base_path = Path.cwd()
    else:
        # Normal script olarak çalışıyorsa, proje kök dizininden arar.
        base_path = PROJECT_ROOT

    dotenv_path = base_path / ".env"
    
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    
    token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HF_TOKEN')
    if not token:
        console.print("[bold red]HATA: Hugging Face token'ı bulunamadı.[/bold red]")
        console.print("Uygulamanın modeli indirebilmesi için .exe'nin yanında bir `.env` dosyası ve içinde `HUGGINGFACE_HUB_TOKEN` bulunmalıdır.")
        return None
    return token

def load_model_and_tokenizer(model_path_or_repo_id, token: str):
    """Modeli ve tokenizer'ı yerel yoldan veya Hugging Face Hub'dan yükler."""
    console.print(f"[yellow]🚀 Model yükleniyor: [cyan]{model_path_or_repo_id}[/cyan][/yellow]")
    
    # Sadece Hub'dan indiriliyorsa ek bilgilendirme mesajı göster
    if not isinstance(model_path_or_repo_id, Path):
        console.print("[italic]Bu işlem ilk çalıştırmada internet hızınıza bağlı olarak birkaç dakika sürebilir.[/italic]")

    # Daha verimli yükleme için 4-bit kuantizasyon ayarları
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            token=token,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_path_or_repo_id, token=token)
    except Exception as e:
        # --- KESİN ÇÖZÜM: Hata mesajını rich yerine standart print ile yazdır ---
        # Bu, rich kütüphanesinden kaynaklanan tüm çökmeleri engeller ve asıl hatayı gösterir.
        print("\n\033[91mHATA: Model veya Tokenizer yüklenirken kritik bir hata oluştu.\033[0m")
        print("\033[93m================== ASIL HATA MESAJI ==================\033[0m")
        import traceback
        traceback.print_exc() # En detaylı hata dökümünü verir
        print("\033[93m=====================================================\033[0m\n")
        print("\033[93mOlası Çözümler:\033[0m")
        print("1. İnternet bağlantınızı kontrol edin.")
        if isinstance(model_path_or_repo_id, Path):
             print(f"2. '{model_path_or_repo_id}' yolunun doğru olduğundan emin olun.")
        else:
             print(f"2. Hugging Face repo adının ('{model_path_or_repo_id}') doğru olduğundan ve erişim izniniz olduğundan emin olun.")
        sys.exit(1)

    console.print("[green]✅ Model ve Tokenizer başarıyla yüklendi.[/green]")
    return model, tokenizer

def parse_tool_calls(text: str):
    """Modelin çıktısındaki tool-call formatını yakalar."""
    pattern = r"<\|begin_of_tool_code\|>([\s\S]*?)<\|end_of_tool_code\|>"
    match = re.search(pattern, text)
    if not match:
        return None
    
    tool_code_str = match.group(1).strip()
    call_pattern = re.compile(r"print\((\w+)\((.*)\)\)")
    call_match = call_pattern.search(tool_code_str)
    
    if not call_match:
        return None
        
    function_name = call_match.group(1)
    args_str = call_match.group(2)
    
    try:
        params = {}
        # Parametreleri ayrıştırmak için daha güvenilir bir regex
        arg_pattern = re.compile(r"(\w+)=((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[^,)]+)")
        for p_match in arg_pattern.finditer(args_str):
            key = p_match.group(1)
            raw_value = p_match.group(2)
            try:
                # json.loads kullanarak string, sayı, boolean gibi değerleri doğru şekilde işleyelim
                params[key] = json.loads(raw_value.lower())
            except json.JSONDecodeError:
                # Eğer json.loads başarısız olursa (örneğin tırnaksız bir metinse), ham string olarak al
                params[key] = raw_value.strip("\"'")
        
        return [{
            "id": f"tool_call_{os.urandom(4).hex()}",
            "type": "function",
            "function": { "name": function_name, "arguments": json.dumps(params, ensure_ascii=False) }
        }]
    except Exception as e:
        console.print(f"[red]HATA: Araç parametreleri ayrıştırılamadı: {args_str}. Detay: {e}[/red]")
        return None

def main():
    """Ana sohbet döngüsünü çalıştırır."""
    token = None
    # Sadece Hub'dan model indirirken token gerekli.
    if not USE_LOCAL_MODEL:
        token = load_huggingface_token()
        if not token:
            sys.exit(1)

    model, tokenizer = load_model_and_tokenizer(MODEL_PATH_OR_REPO_ID, token)
    
    # Konuşma geçmişini tutacak olan liste
    dialogue = []
    
    # Llama-3'ün konuşmayı bitirdiğini anladığı özel tokenlar
    terminators = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]

    # --- Uygulama Başlangıç Mesajı ---
    console.print("\n" + "="*60, style="bold green")
    console.print("🤖 [bold green]ChoyrensAI Telekom Agent'a Hoş Geldiniz[/bold green]")
    console.print("   Fatura, tarife ve teknik destek konularında size yardımcı olabilirim.")
    console.print("   `!simple <sorunuz>` yazarak modelin temel konuşma yeteneğini test edebilirsiniz.")
    console.print("   Çıkmak için 'quit' veya 'exit' yazabilirsiniz.")
    console.print("="*60, style="bold green")

    while True:
        try:
            user_input = console.input("\n[bold blue]👤 Siz:[/bold blue] ")
            if user_input.lower() in ["quit", "exit"]:
                break
        except (KeyboardInterrupt, EOFError):
            break

        # --- YENİ: Diagnostik Mantığı (advanced_playground'dan taşındı) ---
        if user_input.startswith("!simple "):
            simple_question = user_input[len("!simple "):]
            simple_dialogue = [{"role": "user", "content": simple_question}]
            
            console.print("[yellow]... model basit modda düşünüyor ...[/yellow]")
            
            token_ids = tokenizer.apply_chat_template(simple_dialogue, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)
            attention_mask = torch.ones_like(token_ids)

            # Basit mod için yanıtta akıtma (streaming) kullanmıyoruz, tek seferde alıyoruz.
            console.print(f"🤖 [bold green]Asistan (Basit Yanıt):[/bold green] ", end="")
            outputs = model.generate(
                input_ids=token_ids,
                attention_mask=attention_mask,
                max_new_tokens=256,
                eos_token_id=terminators,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
            response_text = tokenizer.decode(outputs[0][token_ids.shape[-1]:], skip_special_tokens=True)
            console.print(Markdown(response_text))
            
            # Bu konuşma ana diyalog geçmişine eklenmez, döngüye yeniden başla.
            continue
            
        # --- Normal Konuşma Döngüsü ---

        # Konuşma geçmişini budama ve yönetme
        if len(dialogue) > FOCUSED_HISTORY_TURNS:
            # En son N mesajı alarak odaklanmış bir bağlam oluştur
            focused_dialogue = dialogue[-FOCUSED_HISTORY_TURNS:]
        else:
            # Eğer konuşma yeterince kısaysa, tamamını kullan
            focused_dialogue = dialogue

        # Kullanıcının mesajını diyalog geçmişine ekle
        dialogue.append({"role": "user", "content": user_input})
        
        console.print("[yellow]... model düşünüyor ...[/yellow]")

        # Modelin kafasını karıştırmamak için ona tüm geçmişi değil, sadece
        # en ilgili kısımları gönderiyoruz.
        if len(dialogue) > FOCUSED_HISTORY_TURNS:
            focused_dialogue = dialogue[-FOCUSED_HISTORY_TURNS:]
            console.print(f"[italic grey50](Sadece son {FOCUSED_HISTORY_TURNS} mesaja odaklanılıyor...)[/italic grey50]")
        else:
            # Eğer konuşma yeterince kısaysa, tamamını kullan
            focused_dialogue = dialogue

        # Konuşma geçmişini modele uygun formata çevir
        token_ids = tokenizer.apply_chat_template(focused_dialogue, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)

        # Modelden bir yanıt üretmesini iste
        run_generation_loop(model, tokenizer, dialogue, token_ids, terminators, do_sample=True)

def run_generation_loop(model, tokenizer, dialogue, token_ids, terminators, do_sample=True):
    """
    Modelden yanıt üretme, araç çağırma ve özetleme döngüsünü yönetir.
    Bu, kod tekrarını önler ve mantığı merkezileştirir.
    """
    # --- YENİ: TextStreamer Entegrasyonu ---
    # Yanıtları kelime kelime ekrana yazdırmak için bir streamer oluşturuyoruz.
    streamer = TextStreamer(tokenizer, skip_prompt=True)
    
    # Modelden bir yanıt üretmesini iste
    # `do_sample=True` olduğunda kullanılacak yaratıcılık ayarları.
    generation_params = {
        "max_new_tokens": 1024,
        "eos_token_id": terminators,
        "pad_token_id": tokenizer.eos_token_id,
        "streamer": streamer  # Streamer'ı generate fonksiyonuna ekliyoruz
    }
    if do_sample:
        generation_params["temperature"] = 0.6
        generation_params["top_p"] = 0.9

    # --- YENİ: Attention Mask'ı manuel olarak ekliyoruz ---
    # Bu, kütüphanenin uyarısını giderir ve daha güvenilir sonuçlar sağlar.
    attention_mask = torch.ones_like(token_ids)

    # --- YENİ: Akış için Thread Kullanımı ---
    # Streamer'ın düzgün çalışması için `generate` fonksiyonunu ayrı bir thread'de
    # çalıştırmak en iyi pratiktir. Bu, ana programın takılmasını önler.
    # Ancak basitlik adına şimdilik doğrudan çağırıyoruz. `generate` zaten
    # akışı destekleyecek şekilde tasarlanmıştır.

    console.print(f"🤖 [bold green]Asistan:[/bold green] ", end="")
    outputs = model.generate(
        input_ids=token_ids,
        attention_mask=attention_mask,
        do_sample=do_sample,
        **generation_params
    )
    
    # Streamer çıktıyı zaten ekrana yazdırdığı için burada tekrar yazdırmıyoruz.
    # Sadece tam metni alıp tool-call var mı diye kontrol edeceğiz.
    response_text = tokenizer.decode(outputs[0][token_ids.shape[-1]:], skip_special_tokens=False)

    # Modelin bir araç çağırıp çağırmadığını kontrol et
    tool_calls = parse_tool_calls(response_text)

    if tool_calls:
        # Araç çağrıldıysa...
        console.print(f"🛠️  [bold yellow]Araç Çağrısı Algılandı:[/bold yellow] [green]{response_text.strip()}[/green]")
        dialogue.append({"role": "assistant", "content": response_text})

        # Tüm araçları çalıştır ve sonuçları topla
        for call in tool_calls:
            func_name = call["function"]["name"]
            func_args = json.loads(call["function"]["arguments"])

            # Sahte API'den (tool_definitions.py) yanıtı al
            tool_response_content = get_tool_response(func_name, func_args)

            console.print(f"⚙️  [bold magenta]Araç Yanıtı ({func_name}):[/bold magenta] {tool_response_content}")

            # Aracın yanıtını diyalog geçmişine ekle
            dialogue.append({
                "role": "tool",
                "content": tool_response_content,
            })

        console.print("[yellow]... model araç sonuçlarını değerlendirip özetliyor ...[/yellow]")

        # --- YENİ: Özetleme için de Odaklanmış Bağlam Kullanımı ---
        # Güncellenmiş diyalog geçmişiyle tekrar modele git ve nihai yanıtı al
        if len(dialogue) > FOCUSED_HISTORY_TURNS:
            focused_dialogue_for_summary = dialogue[-FOCUSED_HISTORY_TURNS:]
        else:
            focused_dialogue_for_summary = dialogue
            
        final_token_ids = tokenizer.apply_chat_template(focused_dialogue_for_summary, add_generation_prompt=True, tokenize=True, return_tensors="pt").to(model.device)
        
        # Özetleme adımını tekrar çağır, bu sefer `do_sample=False` ile
        # Bu, iç içe geçmiş bir döngü gibi davranır ve özetlemenin de araç çağırabilmesine olanak tanır (ileride).
        # Dikkat: `dialogue` listesinin tamamını paslamaya devam ediyoruz ki tam geçmiş korunabilsin.
        run_generation_loop(model, tokenizer, dialogue, final_token_ids, terminators, do_sample=False)
        
    else:
        # Streamer zaten yazdığı için, burada sadece konuşma geçmişini güncelliyoruz.
        # Temizlenmiş yanıtı geçmişe eklemek daha iyi olabilir.
        cleaned_response = re.sub(r'<\|.*?\|>', '', response_text).strip()
        dialogue.append({"role": "assistant", "content": cleaned_response})

    console.print("\n[bold red]Görüşmek üzere![/bold red]")

if __name__ == "__main__":
    main()
