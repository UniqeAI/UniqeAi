# -*- coding: utf-8 -*-
"""
🤖 UniqeAi Telekom Agent - GGUF Terminal Uygulaması v6.0 (Orkestra Şefi Mimarisi)
=================================================================================

Bu, projenin son ve en gelişmiş sürümüdür. "Orkestra Şefi ve İcracı"
mimarisini uygulayarak hem hafıza (bağlam) sorunlarını hem de modelin
güvenilirlik (halüsinasyon) problemlerini kökten çözer.

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


# --- GGUF Model Yapılandırması ---
GGUF_MODEL_DIR = PROJECT_ROOT / "UniqeAi" / "ai_model" / "gguf_model_v2"
CONTEXT_SIZE = 4096
GPU_LAYERS = -1
TEMPERATURE = 0.1 # Yaratıcılık için hafif bir artış
DEFAULT_TEST_USER_ID = 12345

console = Console()
ALL_TOOL_DEFINITIONS = {tool['function']['name']: tool for tool in get_tool_definitions()}


def find_latest_gguf_model(model_dir: Path) -> Optional[Path]:
    console.print(f"[yellow]🤖 Model aranıyor: [cyan]{model_dir}[/cyan][/yellow]")
    if not model_dir.exists():
        console.print(f"[bold red]HATA: Model klasörü bulunamadı![/bold red]"); return None
    gguf_files = list(model_dir.glob("*.gguf"))
    if not gguf_files:
        console.print(f"[bold red]HATA: '{model_dir}' içinde hiç .gguf dosyası bulunamadı.[/bold red]"); return None
    latest_model_path = max(gguf_files, key=lambda p: p.stat().st_mtime)
    console.print(f"[green]✅ En yeni model bulundu: [bold cyan]{latest_model_path.name}[/bold cyan][/green]")
    return latest_model_path

def load_gguf_model():
    try: from llama_cpp import Llama
    except ImportError: console.print("[bold red]HATA: `llama-cpp-python` kütüphanesi kurulu değil.[/bold red]"); sys.exit(1)
    model_path = find_latest_gguf_model(GGUF_MODEL_DIR)
    if not model_path: sys.exit(1)
    console.print(f"[yellow]🚀 GGUF modeli yükleniyor: [cyan]{model_path.name}[/cyan][/yellow]")
    try:
        llm = Llama(
            model_path=str(model_path), n_ctx=CONTEXT_SIZE, n_gpu_layers=GPU_LAYERS,
            n_threads=os.cpu_count() - 1 if os.cpu_count() and os.cpu_count() > 1 else 1,
            verbose=False, chat_format="llama-3"
        )
        console.print("[green]✅ Model başarıyla GPU'ya yüklendi.[/green]")
        return llm
    except Exception as e:
        console.print(f"\n[bold red]HATA: Model yüklenirken kritik bir hata oluştu: {e}[/bold red]"); sys.exit(1)

# --- Katman 2: İcracı (Executor) ---
class Executor:
    """Tekil görevleri hafızasız ve hatasız bir şekilde yerine getiren katman."""

    def __init__(self, llm_model):
        self.llm = llm_model
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
        pattern_with_print = r"<\|begin_of_tool_code\|>\s*print\((\w+)\((.*?)\)\)\s*<\|end_of_tool_code\|>"
        pattern_without_print = r"<\|begin_of_tool_code\|>\s*(\w+)\((.*?)\)\s*<\|end_of_tool_code\|>"
        match = re.search(pattern_with_print, text, re.DOTALL) or re.search(pattern_without_print, text, re.DOTALL)
        if not match: return None
        
        function_name, args_str = match.group(1), match.group(2)
        params = {}
        if args_str:
            arg_pattern = re.compile(r"(\w+)\s*=\s*((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[\w.-]+)")
            for p_match in arg_pattern.finditer(args_str):
                key, raw_value = p_match.group(1), p_match.group(2)
                try: value = json.loads(raw_value)
                except (json.JSONDecodeError, TypeError): value = str(raw_value).strip("'\"")
                params[key] = value
        return [{"name": function_name, "arguments": params}]

    def execute_tool(self, tool_call: Dict[str, Any], context_data: Dict[str, Any] = None) -> str:
        func_name, func_args = tool_call["name"], tool_call["arguments"]
        
        # AKILLI ARA KATMAN: pay_bill için önce fatura kontrolü yap
        if func_name == "pay_bill":
            return self._handle_smart_payment(func_args, context_data)
        
        if func_name in ALL_TOOL_DEFINITIONS:
            func_def = ALL_TOOL_DEFINITIONS[func_name]["function"]
            required_params = func_def.get("parameters", {}).get("required", [])
            expected_params = func_def.get("parameters", {}).get("properties", {})
            
            # PARAMETRE DÜZELTMESİ VE TAMAMLAMA
            corrected_args = {}
            
            for expected_param, param_info in expected_params.items():
                # Yanlış parametre isimlerini düzelt
                if expected_param == "bill_id" and "fatura_id" in func_args:
                    corrected_args["bill_id"] = func_args["fatura_id"]
                    console.print(f"🔧 [italic yellow]İcracı: 'fatura_id' parametresi 'bill_id' olarak düzeltildi.[/italic yellow]")
                elif expected_param == "method" and "payment_method" in func_args:
                    corrected_args["method"] = func_args["payment_method"]
                    console.print(f"🔧 [italic yellow]İcracı: 'payment_method' parametresi 'method' olarak düzeltildi.[/italic yellow]")
                elif expected_param in func_args:
                    corrected_args[expected_param] = func_args[expected_param]
            
            # Eksik parametreleri tamamla
            if "user_id" in required_params and "user_id" not in corrected_args:
                corrected_args["user_id"] = DEFAULT_TEST_USER_ID
                console.print(f"🧠 [italic yellow]İcracı: 'user_id' parametresi varsayılan ID ({DEFAULT_TEST_USER_ID}) ile tamamlandı.[/italic yellow]")
            
            func_args = corrected_args
        
        console.print(f"🛠️  [bold yellow]İcracı Araç Çağrısı (Düzeltilmiş):[/bold yellow] [green]{func_name}({func_args})[/green]")
        response = get_tool_response(func_name, func_args)
        console.print(f"⚙️  [bold magenta]İcracı Araç Yanıtı:[/bold magenta] {response}")
        return response
        
    def _handle_smart_payment(self, func_args: Dict[str, Any], context_data: Dict[str, Any] = None) -> str:
        """Akıllı ödeme işlemi: Önce fatura kontrol et, sonra öde"""
        console.print("🧠 [bold cyan]İcracı: Akıllı ödeme modu - önce fatura kontrol ediliyor...[/bold cyan]")
        
        # 1. Adım: Önce mevcut faturayı kontrol et
        user_id = func_args.get("user_id", DEFAULT_TEST_USER_ID)
        bill_check_response = get_tool_response("get_current_bill", {"user_id": user_id})
        console.print(f"🔍 [bold blue]Fatura Kontrol Sonucu:[/bold blue] {bill_check_response}")
        
        # 2. Adım: Fatura var mı kontrol et
        try:
            bill_data = json.loads(bill_check_response)
            if not bill_data.get("success", False):
                return "Hata: Ödenmemiş faturanız bulunmamaktadır."
            
            # Fatura bilgilerini al
            current_bill_id = bill_data["data"]["bill_id"]
            amount = bill_data["data"]["amount"]
            
            # 3. Adım: Eğer kullanıcı belirli bir fatura ID'si verdiyse kontrol et
            requested_bill_id = func_args.get("bill_id")
            if requested_bill_id and requested_bill_id != current_bill_id:
                console.print(f"⚠️ [italic red]İcracı: İstenen fatura ID ({requested_bill_id}) mevcut fatura ID ({current_bill_id}) ile eşleşmiyor![/italic red]")
                return f"Hata: {requested_bill_id} numaralı fatura bulunamadı. Mevcut faturanız: {current_bill_id}"
            
            # 4. Adım: Ödeme işlemini gerçekleştir
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
        iron_cage_prompt = f"""Bir API'den aşağıdaki JSON yanıtı alındı:
```json
{tool_response_content}
```
Görevin:
1. Bu JSON verisinin dışına **ASLA** çıkma.
2. Kendi kendine bilgi veya rakam **EKLEME**.
3. **SADECE** bu JSON'daki bilgileri kullanarak, sonucu kullanıcıya **tek bir akıcı Türkçe paragrafta** özetle.
4. **HİÇBİR ŞEKİLDE** araç çağırma kodu (<|begin_of_tool_code|>) kullanma.
Yanıtın sadece ve sadece bu paragrafı içersin."""
        
        # Özetleme için özel sistem mesajı
        summarizer_prompt = """Sen, API yanıtlarını Türkçe özetleyen bir asistansın. 

KURALLAR:
- Sadece verilen JSON verisini kullan
- Kullanıcıya direkt hitap et ("Sizin için...", "Talebiniz...")
- ASLA üçüncü şahıs konuşması yapma ("kullanıcının", "müşterinin")
- HİÇBİR ZAMAN araç çağırma kodu kullanma
- Samimi ve kişisel bir ton kullan"""
        
        dialogue = [{"role": "system", "content": summarizer_prompt}, {"role": "user", "content": iron_cage_prompt}]
        
        console.print("[yellow]... İcracı veriye sadık kalarak özetliyor ...[/yellow]")
        summary_response = self.llm.create_chat_completion(messages=dialogue, temperature=0.1, stop=["<|eot_id|>"])
        raw_summary = summary_response['choices'][0]['message']['content']
        
        # Tool code kalıntılarını temizle
        clean_summary = re.sub(r'<\|begin_of_tool_code\|>.*?<\|end_of_tool_code\|>', '', raw_summary, flags=re.DOTALL).strip()
        clean_summary = re.sub(r'print\(.*?\)', '', clean_summary).strip()
        
        return clean_summary if clean_summary else raw_summary

    def run_task(self, user_input: str, context_data: Dict[str, Any] = None) -> Tuple[Optional[str], bool]:
        """Verilen tek bir görevi uçtan uca çalıştırır."""
        dialogue = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}]
        response = self.llm.create_chat_completion(messages=dialogue, temperature=TEMPERATURE, stop=["<|eot_id|>"])
        assistant_response_text = response['choices'][0]['message']['content']
        
        tool_calls = self.parse_tool_calls(assistant_response_text)
        if tool_calls:
            tool_response = self.execute_tool(tool_calls[0], context_data)
            final_summary = self.summarize_tool_result(tool_response)
            return final_summary, True
        
        return assistant_response_text, False

# --- Katman 1: Orkestra Şefi (ConversationManager) ---
class ConversationManager:
    """Sohbeti yöneten, hafızayı tutan ve Executor'ı tetikleyen katman."""

    def __init__(self, llm_model):
        self.llm = llm_model
        self.executor = Executor(llm_model)
        self.dialogue = [
            {"role": "system", "content": self._create_system_prompt()}
        ]
        # Bağlamsal bilgi deposu
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
        
        # 1. Adım: Niyet Analizi (Orkestra Şefi karar verir)
        console.print("[yellow]... Orkestra Şefi niyeti analiz ediyor ...[/yellow]")
        # Gelişmiş niyet algılama sistemi
        tool_keywords = ['fatura', 'paket', 'tarife', 'internet', 'roaming', 'yurt dışı', 'öde', 'iptal', 'kapat', 'sorgula', 'listele']
        
        # Fatura ile ilgili sorular için özel algılama
        bill_inquiry_patterns = [
            'faturasını öğren', 'faturamı göster', 'fatura bilgi', 'bu ayki fatura', 
            'güncel fatura', 'fatura sorgula', 'fatura durumu', 'ne kadar borç'
        ]
        
        # Temel anahtar kelime kontrolü
        has_tool_keyword = any(keyword in user_input.lower() for keyword in tool_keywords)
        
        # Fatura sorgusu özel kontrolü
        is_bill_inquiry = any(pattern in user_input.lower() for pattern in bill_inquiry_patterns)
        
        should_execute_tool = has_tool_keyword or is_bill_inquiry

        if should_execute_tool:
            # Kullanıcı girdisinden doğrudan fatura ID'si çıkar
            user_specified_bill_id = self._extract_bill_id_from_user_input(user_input)
            if user_specified_bill_id:
                self.context_data['last_bill_id'] = user_specified_bill_id
                console.print(f"🧠 [italic blue]Orkestra Şefi: Kullanıcının belirttiği fatura ID ({user_specified_bill_id}) hafızaya kaydedildi.[/italic blue]")
            
            # 2. Adım: Görevi İcracı'ya devret
            console.print("[cyan]Orkestra Şefi: Eylem gerektiren bir komut algılandı. Görev İcracı'ya devrediliyor...[/cyan]")
            summary, executed = self.executor.run_task(user_input, self.context_data)
            
            if executed:
                # 3. Adım: İcracı'dan gelen sonucu hafızaya ekle ve sun
                self.dialogue.append({"role": "assistant", "content": summary})
                
                # Bağlamsal bilgileri güncelle (fatura bilgilerini çıkar)
                self._extract_context_from_response(summary)
                
                console.print(f"🤖 [bold green]Asistan (Orkestra Şefi):[/bold green] ", end="")
                console.print(Markdown(summary))
            else:
                # İcracı araç bulamadı, normal sohbet olarak devam et
                self.handle_chat(summary)
        else:
            # 2. Adım (Alternatif): Normal sohbet et
            console.print("[cyan]Orkestra Şefi: Normal sohbet olarak devam ediliyor...[/cyan]")
            self.handle_chat(user_input)
    
    def _extract_context_from_response(self, response: str):
        """Yanıttan bağlamsal bilgileri çıkarır ve depolar."""
        # Fatura ID'sini yakala (F-2024-SIM-8901 formatında)
        import re
        bill_id_match = re.search(r'F-\d{4}-[A-Z]+-\d+', response)
        if bill_id_match:
            self.context_data['last_bill_id'] = bill_id_match.group(0)
            console.print(f"🧠 [italic blue]Orkestra Şefi: Fatura ID ({bill_id_match.group(0)}) hafızaya kaydedildi.[/italic blue]")
    
    def _extract_bill_id_from_user_input(self, user_input: str) -> Optional[str]:
        """Kullanıcı girdisinden fatura ID'sini çıkarır."""
        import re
        bill_id_match = re.search(r'F-\d{4,}-[A-Z0-9]+-\d+|F-\d{7,}', user_input)
        return bill_id_match.group(0) if bill_id_match else None
    
    def handle_chat(self, last_input: str):
        # Hafızayı koruyarak normal bir sohbet yanıtı üret
        response = self.llm.create_chat_completion(messages=self.dialogue, temperature=0.5, stop=["<|eot_id|>"])
        chat_response = response['choices'][0]['message']['content']
        self.dialogue.append({"role": "assistant", "content": chat_response})
        console.print(f"🤖 [bold green]Asistan (Orkestra Şefi):[/bold green] ", end="")
        console.print(Markdown(chat_response))


def main_loop(llm: "Llama"):
    console.print("\n" + "="*60, style="bold green")
    console.print("🤖 [bold green]UniqeAi Telekom Agent v7.0 (Akıllı Davranış Sistemi)[/bold green]")
    console.print("   🧠 Yeni: Akıllı ödeme - önce fatura kontrol, sonra ödeme!")
    console.print("   ⚡ Gelişmiş: Fatura sorguları artık direkt araç çağırıyor!")
    console.print("   🎯 İyileştirme: 'Hesap numaranızı paylaşın' hatası giderildi!")
    console.print("   Çıkmak için 'quit' veya 'exit' yazabilirsiniz.")
    console.print("="*60, style="bold green")
    
    manager = ConversationManager(llm)

    while True:
        try:
            user_input = console.input("\n[bold blue]👤 Siz:[/bold blue] ")
            if user_input.lower() in ["quit", "exit"]: break
            if user_input.lower() == "new":
                console.print("[bold yellow]Yeni bir sohbet oturumu başlatılıyor...[/bold yellow]")
                manager = ConversationManager(llm)
                continue
        except (KeyboardInterrupt, EOFError): break
        
        manager.handle_user_input(user_input)

    console.print("\n[bold red]Görüşmek üzere![/bold red]")

if __name__ == "__main__":
    llm_model = load_gguf_model()
    if llm_model:
        main_loop(llm_model)
