# -*- coding: utf-8 -*-
"""
🤖 UniqeAi Telekom Agent - FP16 Terminal Uygulaması v7.0 (Orkestra Şefi Mimarisi)
=================================================================================

Bu, projenin son ve en gelişmiş sürümüdür ve yüksek hassasiyetli FP16 
modelini kullanır. "Orkestra Şefi ve İcracı" mimarisini uygulayarak hem 
hafıza (bağlam) sorunlarını hem de modelin güvenilirlik (halüsinasyon) 
problemlerini kökten çözer.

--- MİMARİ AÇIKLAMASI ---
- **ConversationManager (Orkestra Şefi):** Kullanıcıyla olan tüm sohbeti
  yönetir, geçmişi tutar ve bağlamı korur. Bir sonraki adımın ne olacağına
  (araç çağırma mı, sohbet mi) karar verir.
- **Executor (İcracı):** "Orkestra Şefi"nden bir görev aldığında, hafızasız
  ve hatasız bir şekilde o tekil görevi yerine getirir (araç çağırır ve
  API verisine sadık kalarak özetler).
- **Sonuç:** Sistem, hem uzun sohbetleri hatırlayabilen (hafıza) hem de
  araç kullanırken asla hata yapmayan (güvenilirlik) bir yapıya kavuşur.
"""

import os
import json
import re
import sys
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from typing import Optional, List, Dict, Any, Tuple
import warnings
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Proje Kök Dizini ve Modül Yolu ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except (NameError, IndexError):
    PROJECT_ROOT = Path.cwd()

AI_MODEL_SCRIPTS_PATH = PROJECT_ROOT / "UniqeAi" / "ai_model" / "scripts"
if str(AI_MODEL_SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(AI_MODEL_SCRIPTS_PATH))

try:
    from tool_definitions import get_tool_definitions, get_tool_response
except ImportError:
    print(f"\n[HATA] Gerekli 'tool_definitions' modülü bulunamadı. Aranan yol: {AI_MODEL_SCRIPTS_PATH}")
    sys.exit(1)

# --- FP16 Model Yapılandırması ---
FP16_MODEL_DIR = PROJECT_ROOT / "UniqeAi" / "ai_model" / "merged_model_fp16_v2"
CONTEXT_SIZE = 4096
TEMPERATURE = 0.1 # Yaratıcılık için hafif bir artış
DEFAULT_TEST_USER_ID = 12345

console = Console()
ALL_TOOL_DEFINITIONS = {tool['function']['name']: tool for tool in get_tool_definitions()}
warnings.filterwarnings("ignore", category=UserWarning)


def find_fp16_model(model_dir: Path) -> Optional[Path]:
    console.print(f"[yellow]🤖 FP16 Model aranıyor: [cyan]{model_dir}[/cyan][/yellow]")
    if not model_dir.exists():
        console.print(f"[bold red]HATA: Model klasörü bulunamadı![/bold red]"); return None
    
    config_file = model_dir / "config.json"
    if not config_file.exists():
        console.print(f"[bold red]HATA: config.json dosyası bulunamadı: {config_file}[/bold red]"); return None
    
    console.print(f"[green]✅ FP16 model bulundu: [bold cyan]{model_dir.name}[/bold cyan][/green]")
    return model_dir

def load_fp16_model():
    model_path = find_fp16_model(FP16_MODEL_DIR)
    if not model_path: sys.exit(1)
    
    console.print(f"[yellow]🚀 FP16 modeli yükleniyor: [cyan]{model_path.name}[/cyan][/yellow]")
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        console.print(f"[blue]🔧 Cihaz: {device}[/blue]")
        if device == "cpu":
            console.print("[yellow]⚠️  GPU bulunamadı, CPU kullanılacak (yavaş olabilir)[/yellow]")
        
        console.print("[yellow]📝 Tokenizer yükleniyor...[/yellow]")
        tokenizer = AutoTokenizer.from_pretrained(str(model_path), trust_remote_code=True, padding_side="left")
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        console.print("[yellow]🧠 FP16 Model yükleniyor...[/yellow]")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            attn_implementation="eager" if (device == "cuda" and hasattr(torch.nn.functional, 'scaled_dot_product_attention')) else "eager"
        )
        
        if device == "cpu":
            model = model.to(device)
        
        console.print("[green]✅ FP16 Model başarıyla yüklendi.[/green]")
        console.print(f"[blue]📊 Model Precision: {model.dtype}[/blue]")
        
        return {"model": model, "tokenizer": tokenizer, "device": device}
        
    except Exception as e:
        console.print(f"\n[bold red]HATA: FP16 Model yüklenirken kritik bir hata oluştu: {e}[/bold red]"); sys.exit(1)

# --- Ortak Yanıt Üretme Fonksiyonu ---
def generate_response(model_data: Dict[str, Any], messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> str:
    try:
        tokenizer = model_data["tokenizer"]
        model = model_data["model"]
        device = model_data["device"]

        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=CONTEXT_SIZE - max_tokens).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature if temperature > 0 else None,
                do_sample=temperature > 0,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                use_cache=True
            )
        
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return response.strip()
        
    except Exception as e:
        console.print(f"[bold red]HATA: Yanıt üretilirken hata oluştu: {e}[/bold red]")
        return "Üzgünüm, bir hata oluştu."

# --- Katman 2: İcracı (Executor) ---
class Executor:
    """Tekil görevleri hafızasız ve hatasız bir şekilde yerine getiren katman."""

    def __init__(self, model_data: Dict[str, Any]):
        self.model_data = model_data
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        tools_string = "\n".join([f"  - `{name}`: {d['function']['description']}" for name, d in ALL_TOOL_DEFINITIONS.items()])
        return f"""Sen, Türkçe konuşan bir AI motorusun. Görevin, sana verilen kullanıcı komutunu analiz edip ilgili aracı çağırmaktır. 
**KRİTİK KURAL: ASLA SOHBET ETME, SADECE ARAÇ ÇAĞIR!**
**ÖRNEKLER:**
- "faturamı öğrenebilir miyim" → HEMEN `get_current_bill` çağır
- "hesabımın faturası" → HEMEN `get_current_bill` çağır  
- "internet hızım" → HEMEN `test_internet_speed` çağır
- "faturamı öde" → HEMEN `pay_bill` çağır
**YAPMA:**
- Hesap numarası sorma (zaten user_id=12345 var)
- "Tabii ki yardımcı olabilirim" gibi sohbet
- Açıklama yapma
**ARAÇ KULLANIM KURALI:** `<|begin_of_tool_code|>print(fonksiyon(parametre="değer"))<|end_of_tool_code|>`
**KULLANABİLECEĞİN ARAÇLAR:**
{tools_string}"""

    def parse_tool_calls(self, text: str) -> Optional[List[Dict[str, Any]]]:
        pattern = r"<\|begin_of_tool_code\|>\s*print\((.*?)\)\s*<\|end_of_tool_code\|>"
        match = re.search(pattern, text, re.DOTALL)
        if not match: return None
        
        call_str = match.group(1)
        func_name_match = re.match(r"(\w+)\(", call_str)
        if not func_name_match: return None
        function_name = func_name_match.group(1)

        params = {}
        arg_pattern = re.compile(r"(\w+)\s*=\s*((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[\w.-]+)")
        for p_match in arg_pattern.finditer(call_str):
            key, raw_value = p_match.group(1), p_match.group(2)
            try: value = json.loads(raw_value)
            except (json.JSONDecodeError, TypeError): value = str(raw_value).strip("'\"")
            params[key] = value
        return [{"name": function_name, "arguments": params}]

    def execute_tool(self, tool_call: Dict[str, Any], context_data: Dict[str, Any] = None) -> str:
        func_name, func_args = tool_call["name"], tool_call["arguments"]
        
        if func_name == "pay_bill":
            return self._handle_smart_payment(func_args, context_data)
        
        if "user_id" not in func_args:
            func_args["user_id"] = DEFAULT_TEST_USER_ID
            console.print(f"🧠 [italic yellow]İcracı: 'user_id' parametresi varsayılan ID ({DEFAULT_TEST_USER_ID}) ile tamamlandı.[/italic yellow]")

        console.print(f"🛠️  [bold yellow]İcracı Araç Çağrısı:[/bold yellow] [green]{func_name}({func_args})[/green]")
        response = get_tool_response(func_name, func_args)
        console.print(f"⚙️  [bold magenta]İcracı Araç Yanıtı:[/bold magenta] {response}")
        return response
        
    def _handle_smart_payment(self, func_args: Dict[str, Any], context_data: Dict[str, Any] = None) -> str:
        console.print("🧠 [bold cyan]İcracı: Akıllı ödeme modu - önce fatura kontrol ediliyor...[/bold cyan]")
        user_id = func_args.get("user_id", DEFAULT_TEST_USER_ID)
        bill_check_response = get_tool_response("get_current_bill", {"user_id": user_id})
        console.print(f"🔍 [bold blue]Fatura Kontrol Sonucu:[/bold blue] {bill_check_response}")
        
        try:
            bill_data = json.loads(bill_check_response)
            if not bill_data.get("success", False):
                return "Hata: Ödenmemiş faturanız bulunmamaktadır."
            
            current_bill_id = bill_data["data"]["bill_id"]
            amount = bill_data["data"]["amount"]
            
            requested_bill_id = func_args.get("bill_id")
            if requested_bill_id and requested_bill_id != current_bill_id:
                return f"Hata: {requested_bill_id} numaralı fatura bulunamadı. Mevcut faturanız: {current_bill_id}"
            
            payment_args = {
                "bill_id": current_bill_id,
                "method": func_args.get("method", "credit_card"),
                "user_id": user_id
            }
            
            console.print(f"💳 [bold green]İcracı: {current_bill_id} numaralı fatura ({amount} TL) ödeme işlemi başlatılıyor...[/bold green]")
            payment_response = get_tool_response("pay_bill", payment_args)
            console.print(f"⚙️  [bold magenta]Ödeme Sonucu:[/bold magenta] {payment_response}")
            return payment_response
            
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"⚠️ [italic red]İcracı: Fatura kontrol edilirken hata oluştu: {e}[/italic red]")
            return "Hata: Fatura bilgileri alınırken bir sorun oluştu."
        
    def summarize_tool_result(self, tool_response_content: str) -> str:
        summarizer_prompt = """Sen, API yanıtlarını Türkçe özetleyen bir asistansın. KURALLAR: Sadece verilen JSON verisini kullan, kullanıcıya direkt hitap et ("Sizin için..."), ASLA üçüncü şahıs konuşması yapma ("kullanıcının"), HİÇBİR ZAMAN araç çağırma kodu kullanma, samimi ve kişisel bir ton kullan."""
        
        iron_cage_prompt = f"""Bir API'den aşağıdaki JSON yanıtı alındı:
```json
{tool_response_content}
```
Görevin: Bu JSON verisinin dışına **ASLA** çıkma. Kendi kendine bilgi veya rakam **EKLEME**. **SADECE** bu JSON'daki bilgileri kullanarak, sonucu kullanıcıya **tek bir akıcı Türkçe paragrafta** özetle. **HİÇBİR ŞEKİLDE** araç çağırma kodu (<|begin_of_tool_code|>) kullanma. Yanıtın sadece ve sadece bu paragrafı içersin."""
        
        dialogue = [{"role": "system", "content": summarizer_prompt}, {"role": "user", "content": iron_cage_prompt}]
        
        console.print("[yellow]... İcracı veriye sadık kalarak özetliyor ...[/yellow]")
        raw_summary = generate_response(self.model_data, dialogue, max_tokens=512, temperature=0.05)
        
        clean_summary = re.sub(r'<\|begin_of_tool_code\|>.*?<\|end_of_tool_code\|>', '', raw_summary, flags=re.DOTALL).strip()
        clean_summary = re.sub(r'print\(.*?\)', '', clean_summary).strip()
        
        return clean_summary if clean_summary else raw_summary

    def run_task(self, user_input: str, context_data: Dict[str, Any] = None) -> Tuple[Optional[str], bool]:
        dialogue = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}]
        assistant_response_text = generate_response(self.model_data, dialogue, max_tokens=256, temperature=TEMPERATURE)
        
        tool_calls = self.parse_tool_calls(assistant_response_text)
        if tool_calls:
            tool_response = self.execute_tool(tool_calls[0], context_data)
            final_summary = self.summarize_tool_result(tool_response)
            return final_summary, True
        
        return assistant_response_text, False

# --- Katman 1: Orkestra Şefi (ConversationManager) ---
class ConversationManager:
    """Sohbeti yöneten, hafızayı tutan ve Executor'ı tetikleyen katman."""

    def __init__(self, model_data: Dict[str, Any]):
        self.model_data = model_data
        self.executor = Executor(model_data)
        self.dialogue = [{"role": "system", "content": self._create_system_prompt()}]
        self.context_data = {}

    def _create_system_prompt(self) -> str:
        return """Sen, UniqeAi tarafından geliştirilmiş, nazik, yardımsever ve Türkçe konuşan bir Telekom Müşteri Hizmetleri Asistanısın. 
ÖNEMLI KONUŞMA KURALLARI:
- Her zaman kullanıcıya direkt hitap et ("Sizin faturanız...", "Size yardımcı olabilirim...")
- ASLA üçüncü şahıs konuşması yapma ("müşterimize", "kullanıcının" gibi)
- Sıcak, samimi ve kişisel bir ton kullan
- Kullanıcının sorularını anla ve uygun eylemi gerçekleştir
Görevin, kullanıcıyla sohbet etmek, konuşmanın geçmişini hatırlamak ve bir eylem gerçekleştirilmesi gerektiğinde ilgili aracı çağırmaktır."""

    def handle_user_input(self, user_input: str):
        self.dialogue.append({"role": "user", "content": user_input})
        
        console.print("[yellow]... Orkestra Şefi niyeti analiz ediyor ...[/yellow]")
        tool_keywords = ['fatura', 'paket', 'tarife', 'internet', 'roaming', 'öde', 'iptal', 'sorgula', 'listele']
        bill_inquiry_patterns = ['faturasını öğren', 'faturamı göster', 'fatura bilgi', 'bu ayki fatura', 'güncel fatura']
        
        has_tool_keyword = any(keyword in user_input.lower() for keyword in tool_keywords)
        is_bill_inquiry = any(pattern in user_input.lower() for pattern in bill_inquiry_patterns)
        
        if has_tool_keyword or is_bill_inquiry:
            console.print("[cyan]Orkestra Şefi: Eylem gerektiren bir komut algılandı. Görev İcracı'ya devrediliyor...[/cyan]")
            summary, executed = self.executor.run_task(user_input, self.context_data)
            
            if executed:
                self.dialogue.append({"role": "assistant", "content": summary})
                console.print(f"🤖 [bold green]Asistan (Orkestra Şefi):[/bold green] ", end="")
                console.print(Markdown(summary))
            else:
                self.handle_chat(summary)
        else:
            console.print("[cyan]Orkestra Şefi: Normal sohbet olarak devam ediliyor...[/cyan]")
            self.handle_chat(user_input)
    
    def handle_chat(self, last_input: str):
        chat_response = generate_response(self.model_data, self.dialogue, max_tokens=512, temperature=0.5)
        self.dialogue.append({"role": "assistant", "content": chat_response})
        console.print(f"🤖 [bold green]Asistan (Orkestra Şefi):[/bold green] ", end="")
        console.print(Markdown(chat_response))

def main_loop(model_data: Dict[str, Any]):
    console.print("\n" + "="*60, style="bold green")
    console.print("🤖 [bold green]UniqeAi Telekom Agent v7.0 (FP16 - Orkestra Şefi Mimarisi)[/bold green]")
    console.print("   🚀 Native FP16 modeli ile maksimum performans ve hassasiyet!")
    console.print("   🧠 Akıllı: Önce fatura kontrolü, sonra ödeme!")
    console.print("   ⚡ Gelişmiş: 'Orkestra Şefi' mimarisi ile güvenilir araç kullanımı!")
    console.print("   Çıkmak için 'quit' veya 'exit' yazabilirsiniz.")
    console.print("="*60, style="bold green")
    
    manager = ConversationManager(model_data)

    while True:
        try:
            user_input = console.input("\n[bold blue]👤 Siz:[/bold blue] ")
            if user_input.lower() in ["quit", "exit"]: break
            if user_input.lower() == "new":
                console.print("[bold yellow]Yeni bir sohbet oturumu başlatılıyor...[/bold yellow]")
                manager = ConversationManager(model_data)
                continue
        except (KeyboardInterrupt, EOFError): break
        
        manager.handle_user_input(user_input)

    console.print("\n[bold red]Görüşmek üzere![/bold red]")

if __name__ == "__main__":
    model_data = load_fp16_model()
    if model_data:
        main_loop(model_data)
