# -*- coding: utf-8 -*-
"""
🚀 ULTIMATE MODEL TEST SUITE v3.0 (Proje Final Sürümü)
==========================================================

Bu sürüm, `terminal_app.py v4.0` ile tam senkronize hale getirilmiştir.
Modelin en son yeteneklerini, en güncel ve doğru yöntemlerle ölçer.

--- YENİLİKLER (v3.0) ---
- ✅ **Tam Senkronizasyon:** Sistem mesajı, araç ayrıştırıcı ve ana mantık,
  projenin son sürüm `terminal_app.py` ile %100 aynıdır.
- ❌ **Gereksiz Kodlar Kaldırıldı:** Artık terk edilmiş olan `should_use_tool`
  ve "ikinci şans verme" mekanizmaları tamamen kaldırıldı.
- 🧠 **En Son Zeka Entegre Edildi:** "Akıllı Parametre Tamamlama" ve
  "Adım Adım Düşünme" gibi en son prompt mühendisliği teknikleri
  test sürecine dahil edildi.
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


class ModelCapabilityTester:
    """Modelin yeteneklerini sistematik olarak test eden ana sınıf"""
    
    def __init__(self, llm_model):
        self.llm = llm_model
        self.test_results = {}
        
    def create_system_prompt(self) -> str:
        """ terminal_app.py ile %100 aynı sistem mesajını oluşturur."""
        tools_string = "\n".join([
            f"  - `{name}`: {tool['function']['description']}"
            for name, tool in ALL_TOOL_DEFINITIONS.items()
        ])
        prompt = f"""Sen, UniqeAi tarafından geliştirilmiş, uzman bir Telekom Müşteri Hizmetleri Asistanısın.
**ANA GÖREVİN:** Kullanıcının talebini anında yerine getirmek. Asla sohbet etme, soru sorma veya açıklama yapma. **Sadece istenen eylemi gerçekleştir.**
**ARAÇ KULLANIM KURALI:** Bir aracı kullanman gerekiyorsa, başka hiçbir şey yazmadan **SADECE araç çağırma kodunu** şu formatta yaz: `<|begin_of_tool_code|>print(fonksiyon(parametre="değer"))<|end_of_tool_code|>`.

**ÖNEMLİ PARAMETRE KURALLARI:**
- get_current_bill: user_id parametresi GEREKLİ → get_current_bill(user_id=12345)
- get_past_bills: user_id parametresi GEREKLİ → get_past_bills(user_id=12345, limit=3)
- get_customer_package: user_id parametresi GEREKLİ → get_customer_package(user_id=12345)
- enable_roaming: user_id parametresi GEREKLİ → enable_roaming(user_id=12345)
- check_network_status: region parametresi GEREKLİ → check_network_status(region="İstanbul")
**KULLANABİLECEĞİN ARAÇLAR:**
{tools_string}
"""
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
        """Tek bir test senaryosunu, terminal_app.py v4.0 mantığıyla çalıştırır."""
        console.print(f"\n🎯 [bold blue]Test Senaryosu:[/bold blue] {scenario['name']}")
        console.print(f"📋 [italic]{scenario['description']}[/italic]")
        
        system_prompt = self.create_system_prompt()
        dialogue = [{"role": "system", "content": system_prompt}, {"role": "user", "content": scenario['user_input']}]
        
        console.print(f"\n👤 [bold blue]Kullanıcı:[/bold blue] {scenario['user_input']}")
        
        full_response = ""
        final_answer = ""
        tool_calls_detected = False

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("Model düşünüyor...", total=None)
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
                        
                        if func_name in ALL_TOOL_DEFINITIONS:
                            func_def = ALL_TOOL_DEFINITIONS[func_name]["function"]
                            required_params = func_def.get("parameters", {}).get("required", [])
                            
                            # Tüm gerekli parametreleri kontrol et ve eksik olanları ekle
                            for param in required_params:
                                if param not in func_args:
                                    if param == "user_id":
                                        func_args[param] = DEFAULT_TEST_USER_ID
                                        console.print(f"🧠 [italic yellow]Uyarı: Model '{param}' parametresini unuttu. Varsayılan değer ({DEFAULT_TEST_USER_ID}) ile tamamlandı.[/italic yellow]")
                                    elif param == "region" and func_name == "check_network_status":
                                        # İstanbul için region parametresi
                                        func_args[param] = "İstanbul"
                                        console.print(f"🧠 [italic yellow]Uyarı: Model '{param}' parametresini unuttu. 'İstanbul' ile tamamlandı.[/italic yellow]")
                                    else:
                                        console.print(f"⚠️ [italic red]Eksik parametre: {param} - Bu araç çağrısı başarısız olabilir.[/italic red]")
                        
                        console.print(f"🛠️ [bold yellow]Araç Çağrısı:[/bold yellow] {func_name}({json.dumps(func_args, ensure_ascii=False)})")
                        tool_response = get_tool_response(func_name, func_args)
                        console.print(f"⚙️ [bold magenta]Araç Yanıtı:[/bold magenta] {tool_response}")
                        dialogue.append({"role": "tool", "content": tool_response})

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
                    
                    console.print(f"\n🤖 [bold green]Model (Final):[/bold green]")
                    console.print(Markdown(final_answer))
                    full_response = assistant_response_text + "\n\n" + final_answer
                else:
                    final_answer = cleaned_response
                    dialogue.append({"role": "assistant", "content": final_answer})
                    console.print(f"\n🤖 [bold green]Model:[/bold green]")
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
        """Model yanıtını değerlendirir"""
        scores = {}
        scores['relevance'] = self.score_relevance(response, scenario.get('expected_topics', []))
        scores['empathy'] = self.score_empathy(response, scenario.get('emotional_context', 'neutral'))
        scores['depth'] = self.score_depth(response)
        scores['tool_usage'] = 10 if used_tools and scenario.get('expects_tool_usage', False) else (5 if not used_tools and not scenario.get('expects_tool_usage', False) else 0)
        scores['creativity'] = self.score_creativity(response, scenario.get('complexity_level', 'medium'))
        
        for criterion in scenario.get('evaluation_criteria', {}):
            if criterion == 'strategic_thinking': scores[criterion] = self.score_strategic_thinking(response)
            elif criterion == 'negotiation_skills': scores[criterion] = self.score_negotiation_skills(response)
            elif criterion == 'cultural_sensitivity': scores[criterion] = self.score_cultural_sensitivity(response)
        
        total_score = sum(scores.values()) / len(scores) if scores else 0
        return {"individual_scores": scores, "total_score": round(total_score, 2), "grade": self.get_grade(total_score)}

    def score_relevance(self, r: str, topics: List[str]) -> float:
        if not topics: return 8.0
        found = sum(1 for t in topics if t.lower() in r.lower())
        return min(10.0, (found / len(topics)) * 10)

    def score_empathy(self, r: str, context: str) -> float:
        indicators = ['anlıyorum', 'üzgünüm', 'hissediyorum', 'destek', 'yanınızda', 'yardım', 'hassas']
        found = sum(1 for i in indicators if i in r.lower())
        return min(10.0, found * (2 if context != 'neutral' else 1.5) + (0 if context != 'neutral' else 5))

    def score_depth(self, r: str) -> float:
        indicators = ['analiz', 'strateji', 'çözüm', 'plan', 'yaklaşım', 'değerlendirme', 'öneri', 'alternatif']
        return min(5.0, len(r.split()) / 50) + min(5.0, sum(1 for i in indicators if i in r.lower()) * 1.5)

    def score_creativity(self, r: str, complexity: str) -> float:
        indicators = ['inovatif', 'yaratıcı', 'özgün', 'farklı', 'yeni', 'benzersiz', 'alternatif']
        found = sum(1 for i in indicators if i in r.lower())
        return min(10.0, found * (2.5 if complexity == 'high' else 2) + (0 if complexity == 'high' else 3))

    def score_strategic_thinking(self, r: str) -> float:
        indicators = ['uzun vadeli', 'kısa vadeli', 'plan', 'strateji', 'roadmap', 'aşama', 'gelecek', 'öngörü']
        return min(10.0, sum(1 for i in indicators if i in r.lower()) * 2)

    def score_negotiation_skills(self, r: str) -> float:
        indicators = ['anlaşma', 'uzlaşma', 'karşılıklı', 'win-win', 'denge', 'esneklik', 'alternatif', 'teklif']
        return min(10.0, sum(1 for i in indicators if i in r.lower()) * 2.5)

    def score_cultural_sensitivity(self, r: str) -> float:
        indicators = ['kültür', 'gelenek', 'değer', 'saygı', 'anlayış', 'hassasiyet', 'toplum']
        return min(10.0, sum(1 for i in indicators if i in r.lower()) * 2 + 4)

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
    console.print(f"[yellow]🚀 Model yükleniyor: [cyan]{model_path.name}[/cyan][/yellow]")
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
        console.print("[green]✅ Model başarıyla yüklendi.[/green]")
        return llm
    except Exception as e:
        console.print(f"[bold red]HATA: Model yüklenemedi - {e}[/bold red]"); sys.exit(1)

def get_test_scenarios() -> List[Dict[str, Any]]:
    """Gerçek mevcut araçlarla uyumlu test senaryoları"""
    return [
        {"name": "Fatura Sorgulama", "description": "Temel fatura bilgisi alma yeteneğini test eder.", "user_input": "Bu ayki faturamı görebilir miyim?", "emotional_context": "neutral", "complexity_level": "low", "expects_tool_usage": True, "expected_topics": ["fatura", "ödeme", "tutar"], "evaluation_criteria": {}},
        
        {"name": "Geçmiş Faturalar", "description": "Geçmiş fatura bilgilerini alma yeteneğini test eder.", "user_input": "Son 3 ayın faturalarını göster lütfen.", "emotional_context": "neutral", "complexity_level": "low", "expects_tool_usage": True, "expected_topics": ["geçmiş", "fatura", "liste"], "evaluation_criteria": {}},
        
        {"name": "Paket Bilgisi", "description": "Mevcut paket bilgilerini alma yeteneğini test eder.", "user_input": "Hangi paketi kullanıyorum şu anda?", "emotional_context": "neutral", "complexity_level": "low", "expects_tool_usage": True, "expected_topics": ["paket", "tarife", "kullanım"], "evaluation_criteria": {}},
        
        {"name": "Ağ Durumu", "description": "Bölgesel ağ durumu kontrol yeteneğini test eder.", "user_input": "İstanbul'da internet sorunu var mı?", "emotional_context": "concerned", "complexity_level": "medium", "expects_tool_usage": True, "expected_topics": ["ağ", "durum", "sorun"], "evaluation_criteria": {}},
        
        {"name": "Roaming Aktivasyonu", "description": "Roaming hizmeti açma yeteneğini test eder.", "user_input": "Yarın Almanya'ya gidiyorum, roaming açar mısınız?", "emotional_context": "neutral", "complexity_level": "medium", "expects_tool_usage": True, "expected_topics": ["roaming", "yurt dışı", "aktivasyon"], "evaluation_criteria": {}},
        
        {"name": "Sohbet Testi", "description": "Araç gerektirmeyen genel sohbet yeteneğini test eder.", "user_input": "Merhaba, nasılsınız?", "emotional_context": "friendly", "complexity_level": "low", "expects_tool_usage": False, "expected_topics": ["selamlaşma", "nezaket"], "evaluation_criteria": {}}
    ]

def display_test_results(results: List[Dict[str, Any]]):
    """Test sonuçlarını görsel olarak sunar"""
    table = Table(title="🏆 ULTIMATE MODEL TEST RESULTS (v3.0)")
    table.add_column("Test Senaryosu", style="cyan"); table.add_column("Toplam Skor", justify="center", style="green")
    table.add_column("Harf Notu", justify="center", style="yellow"); table.add_column("Araç Kullanımı", justify="center", style="blue")
    total_score, valid_results = 0, 0
    for result in results:
        if 'error' not in result:
            score, grade, used_tools = result['evaluation']['total_score'], result['evaluation']['grade'], "✅" if result['used_tools'] else "❌"
            table.add_row(result['scenario_name'], f"{score:.1f}/10", grade, used_tools)
            total_score += score; valid_results += 1
        else:
            table.add_row(result['scenario_name'], "ERROR", "F", "❌")
    console.print(table)
    if valid_results > 0:
        avg_score = total_score / valid_results
        console.print(Panel(f"🎯 **Genel Performans:** {avg_score:.1f}/10 ({ModelCapabilityTester(None).get_grade(avg_score)})\n\n💡 **Değerlendirme:**\n{get_performance_assessment(avg_score)}", title="🚀 ULTIMATE MODEL ASSESSMENT", expand=False))

def get_performance_assessment(s: float) -> str:
    if s >= 9.0: return "🌟 Model olağanüstü performans sergiliyor! Empati, strateji ve yaratıcılıkta insan seviyesinde yetenek gösteriyor."
    elif s >= 8.0: return "🎉 Model mükemmel performans gösteriyor! Karmaşık senaryoları başarıyla çözebiliyor."
    elif s >= 7.0: return "👍 Model çok iyi performans sergiliyor. Çoğu durumda tatmin edici çözümler sunuyor."
    else: return "⚠️ Modelin gelişime açık alanları var. Özellikle karmaşık muhakeme gerektiren konularda daha fazla eğitim faydalı olabilir."

def main():
    """Ana program"""
    console.print("\n" + "="*80, style="bold green")
    console.print("🚀 [bold green]ULTIMATE MODEL TEST SUITE v4.0 (Gerçekçi Test Sürümü)[/bold green]", justify="center")
    console.print("   ✅ terminal_app_gguf.py v8.0 ile senkronize")
    console.print("   🎯 Gerçek mevcut araçlarla uyumlu test senaryoları")
    console.print("   ⚡ Performans optimizasyonları dahil")
    console.print("="*80, style="bold green")
    llm_model = load_gguf_model()
    tester = ModelCapabilityTester(llm_model)
    test_scenarios = get_test_scenarios()
    console.print(f"\n📋 [bold blue]{len(test_scenarios)} adet nihai test senaryosu yüklendi.[/bold blue]")
    start_test = console.input("🚀 Teste başlamak için ENTER'a basın (çıkmak için 'q'): ")
    if start_test.lower() == 'q': return
    results = [tester.run_test_scenario(s) for s in test_scenarios]
    console.print(f"\n{'='*80}\n📊 [bold green]TEST TAMAMLANDI - SONUÇLAR[/bold green]\n{'='*80}")
    display_test_results(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = PROJECT_ROOT / f"UniqeAi/ai_model/test_results_{timestamp}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    console.print(f"\n💾 [green]Test sonuçları kaydedildi: {results_file}[/green]")
    console.print("\n🎉 [bold green]Ultimate Model Test Suite tamamlandı![/bold green]")

if __name__ == "__main__":
    main()
