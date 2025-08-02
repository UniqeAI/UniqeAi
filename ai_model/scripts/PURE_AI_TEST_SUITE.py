# -*- coding: utf-8 -*-
"""
🧠 PURE AI TEST SUITE v1.0 (Gerçek AI Yetenek Testi)
=====================================================

Bu test, modelin EĞİTİMDEN öğrendiklerini kullanmasını test eder.
- ❌ Araç listesi verilmez
- ❌ Parametre örnekleri verilmez  
- ✅ Model sadece eğitiminden bildiği araçları kullanır
- ✅ Gerçek AI yeteneği ölçülür

Bu, modelin gerçek zekasını ve öğrenme kapasitesini test eder!
"""

import os
import json
import re
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

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
    print(f"\n[HATA] 'tool_definitions' modülü bulunamadı. Aranan yol: {AI_MODEL_SCRIPTS_PATH}")
    sys.exit(1)

# --- Model Yapılandırması (terminal_app_gguf.py v8.0 ile senkronize) ---
GGUF_MODEL_DIR = PROJECT_ROOT / "UniqeAi" / "ai_model" / "results_2" / "gguf_model_v2"
CONTEXT_SIZE = 2048  # Performans için optimize edildi
GPU_LAYERS = 35      # Optimum GPU katman sayısı
TEMPERATURE = 0.2    # Yaratıcılık için hafif artırıldı (0.0 çok katıydı)
DEFAULT_TEST_USER_ID = 12345

console = Console()
ALL_TOOL_DEFINITIONS = {tool['function']['name']: tool for tool in get_tool_definitions()}


class PureAITester:
    """Modelin GERÇEK AI yeteneğini test eden sınıf - Araç listesi verilmez!"""
    
    def __init__(self, llm_model):
        self.llm = llm_model
        self.test_results = {}
        
    def create_system_prompt(self) -> str:
        """🧠 GERÇEK AI YETENEĞİ TESTİ - Minimal prompt, araç listesi YOK!"""
        # ARAÇ LİSTESİ VERİLMİYOR - Model eğitiminden öğrendiklerini kullanacak
        prompt = """Sen, UniqeAi tarafından geliştirilmiş, uzman bir Telekom Müşteri Hizmetleri Asistanısın.

**ANA GÖREVİN:** Kullanıcının talebini anında yerine getirmek. Asla sohbet etme, soru sorma veya açıklama yapma. **Sadece istenen eylemi gerçekleştir.**

**ARAÇ KULLANIM KURALI:** Bir aracı kullanman gerekiyorsa, başka hiçbir şey yazmadan **SADECE araç çağırma kodunu** şu formatta yaz: 
`<|begin_of_tool_code|>print(fonksiyon(parametre="değer"))<|end_of_tool_code|>`

**NOT:** Hangi araçların mevcut olduğunu eğitiminden biliyorsun. Uygun olanı seç ve kullan."""
        return prompt.strip()

    def parse_tool_calls(self, text: str) -> Tuple[Optional[List[Dict[str, Any]]], str]:
        """HATA TOLERANSLI AYRIŞTIRICI: print() olsa da olmasa da araç çağrısını yakalar."""
        pattern_with_print = r"<\|begin_of_tool_code\|>\s*print\((\w+)\((.*?)\)\)\s*<\|end_of_tool_code\|>"
        pattern_without_print = r"<\|begin_of_tool_code\|>\s*(\w+)\((.*?)\)\s*<\|end_of_tool_code\|>"
        
        match = re.search(pattern_with_print, text, re.DOTALL)
        pattern_used = pattern_with_print
        if not match:
            match = re.search(pattern_without_print, text, re.DOTALL)
            pattern_used = pattern_without_print

        if not match: return None, text

        function_name, args_str = match.group(1), match.group(2)
        params = {}
        if args_str:
            arg_pattern = re.compile(r"(\w+)\s*=\s*((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[\w.-]+)")
            for p_match in arg_pattern.finditer(args_str):
                key, raw_value = p_match.group(1), p_match.group(2)
                try: value = json.loads(raw_value)
                except (json.JSONDecodeError, TypeError): value = str(raw_value).strip("'\"")
                params[key] = value

        cleaned_text = re.sub(pattern_used, '', text).strip()
        tool_call = {"function": {"name": function_name, "arguments": params}}
        return [tool_call], cleaned_text

    def run_test_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Tek bir test senaryosunu çalıştırır - PURE AI MOD!"""
        console.print(f"\n🧠 [bold blue]PURE AI Test:[/bold blue] {scenario['name']}")
        console.print(f"📋 [italic]{scenario['description']}[/italic]")
        
        system_prompt = self.create_system_prompt()
        dialogue = [{"role": "system", "content": system_prompt}, {"role": "user", "content": scenario['user_input']}]
        
        console.print(f"\n👤 [bold blue]Kullanıcı:[/bold blue] {scenario['user_input']}")
        
        full_response = ""
        final_answer = ""
        tool_calls_detected = False

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("🧠 Model eğitiminden hatırlıyor...", total=None)
            try:
                response = self.llm.create_chat_completion(
                    messages=dialogue, temperature=TEMPERATURE, stop=["<|eot_id|>"]
                )
                assistant_response_text = response['choices'][0]['message']['content']
                
                tool_calls, cleaned_response = self.parse_tool_calls(assistant_response_text)
                progress.update(task, description="Yanıt analiz ediliyor...")

                if tool_calls:
                    tool_calls_detected = True
                    dialogue.append({"role": "assistant", "content": assistant_response_text})
                    
                    for call in tool_calls:
                        func_name, func_args = call["function"]["name"], call["function"]["arguments"]
                        
                        # GERÇEK AI TESTİ - Parametre eksikse model başarısız!
                        if func_name in ALL_TOOL_DEFINITIONS:
                            func_def = ALL_TOOL_DEFINITIONS[func_name]["function"]
                            required_params = func_def.get("parameters", {}).get("required", [])
                            
                            # Sadece user_id için yardım et (çünkü test ortamında sabit)
                            if "user_id" in required_params and "user_id" not in func_args:
                                func_args["user_id"] = DEFAULT_TEST_USER_ID
                                console.print(f"🧠 [italic yellow]AI Eksikliği: Model 'user_id' parametresini unuttu.[/italic yellow]")
                        
                        console.print(f"🛠️ [bold yellow]AI'nın Seçtiği Araç:[/bold yellow] {func_name}({json.dumps(func_args, ensure_ascii=False)})")
                        tool_response = get_tool_response(func_name, func_args)
                        console.print(f"⚙️ [bold magenta]Araç Yanıtı:[/bold magenta] {tool_response}")
                        dialogue.append({"role": "tool", "content": tool_response})

                    # Özetleme prompt'u - Gerçek veriyi kullanması için
                    chain_of_thought_prompt = f"""UYARI: Yukarıdaki API yanıtı gerçek veridir. Bu veriyi AYNEN kullan.

Aşağıdaki JSON'u KELIME KELIME kopyala ve Türkçe açıkla:

{tool_response}

KURALLARI:
1. Bu JSON'daki rakamları AYNEN kullan
2. Kendi rakam EKLEME
3. Kendi JSON yaratma
4. Sadece bu gerçek veriyi özetle

Gerçek JSON'dan Türkçe özet:"""
                    dialogue.append({"role": "user", "content": chain_of_thought_prompt})
                    
                    progress.update(task, description="Model sonuçları özetliyor...")
                    
                    summary_response = self.llm.create_chat_completion(
                        messages=dialogue, 
                        temperature=0.0,  # Halüsinasyonu önlemek için sıfır
                        stop=["<|eot_id|>"],
                        max_tokens=256,
                        repeat_penalty=1.2,
                        top_k=1,  # En muhtemel kelimeyi seç
                        top_p=0.1  # Çok düşük yaratıcılık
                    )
                    final_answer = summary_response['choices'][0]['message']['content']
                    dialogue.pop() # Geçici CoT prompt'unu kaldır
                    dialogue.append({"role": "assistant", "content": final_answer})
                    
                    console.print(f"\n🧠 [bold green]Pure AI Yanıtı:[/bold green]")
                    console.print(Markdown(final_answer))
                    full_response = assistant_response_text + "\n\n" + final_answer
                else:
                    final_answer = cleaned_response
                    dialogue.append({"role": "assistant", "content": final_answer})
                    console.print(f"\n🧠 [bold green]Pure AI Yanıtı:[/bold green]")
                    console.print(Markdown(final_answer))
                    full_response = final_answer
                
                progress.remove_task(task)
                score = self.evaluate_response(scenario, final_answer, tool_calls_detected)
                
                return {
                    "scenario_name": scenario['name'], "user_input": scenario['user_input'],
                    "model_response": full_response, "used_tools": tool_calls_detected,
                    "evaluation": score, "dialogue": dialogue
                }
            except Exception as e:
                progress.remove_task(task)
                console.print(f"[bold red]HATA:[/bold red] {e}")
                return {"scenario_name": scenario['name'], "error": str(e), "evaluation": {"total_score": 0}}

    def evaluate_response(self, scenario: Dict[str, Any], response: str, used_tools: bool) -> Dict[str, Any]:
        """Model yanıtını değerlendirir - PURE AI için özel kriterler"""
        scores = {}
        scores['tool_selection'] = 10 if used_tools and scenario.get('expects_tool_usage', False) else (8 if not used_tools and not scenario.get('expects_tool_usage', False) else 0)
        scores['accuracy'] = self.score_accuracy(response, scenario.get('expected_topics', []))
        scores['completeness'] = self.score_completeness(response)
        scores['natural_language'] = self.score_natural_language(response)
        
        total_score = sum(scores.values()) / len(scores) if scores else 0
        return {"individual_scores": scores, "total_score": round(total_score, 2), "grade": self.get_grade(total_score)}

    def score_accuracy(self, r: str, topics: List[str]) -> float:
        if not topics: return 8.0
        found = sum(1 for t in topics if t.lower() in r.lower())
        return min(10.0, (found / len(topics)) * 10)

    def score_completeness(self, r: str) -> float:
        # Yanıt uzunluğu ve detay seviyesi
        return min(10.0, len(r.split()) / 20)

    def score_natural_language(self, r: str) -> float:
        # Doğal dil kalitesi
        indicators = ['size', 'sizin', 'faturanız', 'paketiniz', 'hizmetiniz']
        found = sum(1 for i in indicators if i in r.lower())
        return min(10.0, found * 2 + 2)

    def get_grade(self, s: float) -> str:
        if s >= 9.0: return "A+ (Olağanüstü)"
        elif s >= 8.0: return "A (Mükemmel)"
        elif s >= 7.0: return "B+ (Çok İyi)"
        elif s >= 6.0: return "B (İyi)"
        elif s >= 5.0: return "C+ (Orta)"
        else: return "F (Başarısız)"

def find_latest_gguf_model(model_dir: Path) -> Optional[Path]:
    if not model_dir.exists(): return None
    gguf_files = list(model_dir.glob("*.gguf"))
    if not gguf_files: return None
    return max(gguf_files, key=lambda p: p.stat().st_mtime)

def load_gguf_model():
    try: from llama_cpp import Llama
    except ImportError: console.print("[bold red]HATA: `llama-cpp-python` kurulu değil.[/bold red]"); sys.exit(1)
    model_path = find_latest_gguf_model(GGUF_MODEL_DIR)
    if not model_path: console.print("[bold red]HATA: GGUF model bulunamadı![/bold red]"); sys.exit(1)
    console.print(f"[yellow]🧠 Pure AI Model yükleniyor: [cyan]{model_path.name}[/cyan][/yellow]")
    try:
        llm = Llama(
            model_path=str(model_path), 
            n_ctx=CONTEXT_SIZE, 
            n_gpu_layers=GPU_LAYERS,
            n_threads=os.cpu_count() - 1 if os.cpu_count() and os.cpu_count() > 1 else 1,
            verbose=False, 
            chat_format="llama-3",
            # Performans optimizasyonları (terminal_app_gguf.py ile aynı)
            n_batch=512,
            use_mlock=True,
            use_mmap=True
        )
        console.print("[green]✅ Pure AI Model başarıyla yüklendi.[/green]")
        return llm
    except Exception as e:
        console.print(f"[bold red]HATA: Model yüklenemedi - {e}[/bold red]"); sys.exit(1)

def get_test_scenarios() -> List[Dict[str, Any]]:
    """Gerçek AI yeteneğini test eden senaryolar"""
    return [
        {"name": "🧠 AI Fatura Testi", "description": "Model eğitiminden hangi aracı seçeceğini biliyor mu?", "user_input": "Bu ayki faturamı görebilir miyim?", "expects_tool_usage": True, "expected_topics": ["fatura", "tutar"], "ai_challenge": "get_current_bill araçını hatırlayabilecek mi?"},
        
        {"name": "🧠 AI Geçmiş Testi", "description": "Model geçmiş faturalar için doğru aracı seçebilir mi?", "user_input": "Son 3 ayın faturalarını göster lütfen.", "expects_tool_usage": True, "expected_topics": ["geçmiş", "fatura", "liste"], "ai_challenge": "get_past_bills araçını bulabilecek mi?"},
        
        {"name": "🧠 AI Paket Testi", "description": "Model paket bilgisi için uygun aracı hatırlıyor mu?", "user_input": "Hangi paketi kullanıyorum şu anda?", "expects_tool_usage": True, "expected_topics": ["paket", "tarife"], "ai_challenge": "get_customer_package araçını seçebilecek mi?"},
        
        {"name": "🧠 AI Ağ Testi", "description": "Model ağ durumu kontrolü için doğru aracı biliyor mu?", "user_input": "İstanbul'da internet sorunu var mı?", "expects_tool_usage": True, "expected_topics": ["ağ", "durum", "sorun"], "ai_challenge": "check_network_status araçını hatırlayabilecek mi?"},
        
        {"name": "🧠 AI Roaming Testi", "description": "Model roaming aktivasyonu için uygun aracı seçebilir mi?", "user_input": "Yarın Almanya'ya gidiyorum, roaming açar mısınız?", "expects_tool_usage": True, "expected_topics": ["roaming", "aktivasyon"], "ai_challenge": "enable_roaming araçını bulabilecek mi?"},
        
        {"name": "🧠 AI Sohbet Testi", "description": "Model ne zaman araç kullanmayacağını biliyor mu?", "user_input": "Merhaba, nasılsınız?", "expects_tool_usage": False, "expected_topics": ["selamlaşma"], "ai_challenge": "Gereksiz araç çağrısı yapmayacak mı?"}
    ]

def display_test_results(results: List[Dict[str, Any]]):
    """Pure AI test sonuçlarını görsel olarak sunar"""
    table = Table(title="🧠 PURE AI TEST RESULTS - Gerçek Zeka Testi")
    table.add_column("AI Test Senaryosu", style="cyan")
    table.add_column("AI Skoru", justify="center", style="green")
    table.add_column("AI Notu", justify="center", style="yellow")
    table.add_column("Araç Seçimi", justify="center", style="blue")
    table.add_column("AI Challenge", style="magenta")
    
    total_score, valid_results = 0, 0
    for result in results:
        if 'error' not in result:
            score, grade, used_tools = result['evaluation']['total_score'], result['evaluation']['grade'], "🧠✅" if result['used_tools'] else "🧠❌"
            # Test senaryosundan AI challenge bilgisini al
            challenge = next((s['ai_challenge'] for s in get_test_scenarios() if s['name'] == result['scenario_name']), "Bilinmiyor")
            table.add_row(result['scenario_name'], f"{score:.1f}/10", grade, used_tools, challenge)
            total_score += score; valid_results += 1
        else:
            table.add_row(result['scenario_name'], "ERROR", "F", "🧠❌", "Test başarısız")
    
    console.print(table)
    if valid_results > 0:
        avg_score = total_score / valid_results
        console.print(Panel(f"🧠 **Pure AI Performansı:** {avg_score:.1f}/10 ({PureAITester(None).get_grade(avg_score)})\n\n💡 **AI Değerlendirmesi:**\n{get_ai_assessment(avg_score)}", title="🧠 PURE AI ASSESSMENT", expand=False))

def get_ai_assessment(s: float) -> str:
    if s >= 9.0: return "🌟 Model olağanüstü AI yeteneği sergiliyor! Eğitimden öğrendiklerini mükemmel şekilde hatırlıyor."
    elif s >= 8.0: return "🎉 Model mükemmel AI performansı gösteriyor! Araçları doğru seçip kullanabiliyor."
    elif s >= 7.0: return "👍 Model iyi AI yeteneği sergiliyor. Çoğu durumda doğru araçları hatırlıyor."
    elif s >= 5.0: return "⚠️ Model orta seviye AI yeteneği gösteriyor. Bazı araçları hatırlıyor ama gelişime açık."
    else: return "🔴 Model AI eğitimini tam olarak öğrenememiş. Araçları hatırlamakta zorlanıyor."

def main():
    """Pure AI Test Ana Programı"""
    console.print("\n" + "="*80, style="bold blue")
    console.print("🧠 [bold blue]PURE AI TEST SUITE v1.0 (Gerçek Zeka Testi)[/bold blue]", justify="center")
    console.print("   ❌ Araç listesi verilmez")
    console.print("   ❌ Parametre örnekleri verilmez")
    console.print("   ✅ Model sadece eğitiminden hatırladıklarını kullanır")
    console.print("   🧠 Gerçek AI yeteneği test edilir")
    console.print("="*80, style="bold blue")
    
    llm_model = load_gguf_model()
    tester = PureAITester(llm_model)
    test_scenarios = get_test_scenarios()
    
    console.print(f"\n🧠 [bold blue]{len(test_scenarios)} adet Pure AI test senaryosu yüklendi.[/bold blue]")
    start_test = console.input("🧠 Pure AI testine başlamak için ENTER'a basın (çıkmak için 'q'): ")
    if start_test.lower() == 'q': return
    
    results = [tester.run_test_scenario(s) for s in test_scenarios]
    console.print(f"\n{'='*80}\n🧠 [bold blue]PURE AI TEST TAMAMLANDI - SONUÇLAR[/bold blue]\n{'='*80}")
    display_test_results(results)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = PROJECT_ROOT / f"UniqeAi/ai_model/pure_ai_test_results_{timestamp}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    console.print(f"\n💾 [green]Pure AI test sonuçları kaydedildi: {results_file}[/green]")
    console.print("\n🧠 [bold blue]Pure AI Test Suite tamamlandı![/bold blue]")

if __name__ == "__main__":
    main()