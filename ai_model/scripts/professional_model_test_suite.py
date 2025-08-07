# -*- coding: utf-8 -*-
"""
🤖 ChoyrensAI Telekom Agent - Profesyonel Test Suite v1.0
==========================================================

Bu script, eğitilmiş Meta Llama 3 Instruct modelinizi kapsamlı ve sistematik bir şekilde test eder.
Farklı senaryolar, zorluk seviyeleri ve performans metrikleri ile modelin kalitesini değerlendirir.

Özellikler:
- Çoklu senaryo testleri
- Performans metrikleri
- Detaylı raporlama
- Hata analizi
- Karşılaştırmalı değerlendirme
"""

import os
import sys
import json
import time
import torch
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import re
import traceback

# Rich kütüphanesi için importlar
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box

# Transformers ve model importları
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dotenv import load_dotenv

# Proje kök dizini ve modül yolu ayarları
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

sys.path.append(str(PROJECT_ROOT))
from UniqeAi.ai_model.scripts.tool_definitions import get_tool_definitions, get_tool_response

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('model_test_suite.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

console = Console()

class TestScenario(Enum):
    """Test senaryoları enum'u"""
    BASIC_CONVERSATION = "basic_conversation"
    TOOL_USAGE = "tool_usage"
    MULTI_INTENT = "multi_intent"
    DISAMBIGUATION = "disambiguation"
    PROACTIVE_ASSISTANCE = "proactive_assistance"
    ERROR_HANDLING = "error_handling"
    ETHICAL_DILEMMA = "ethical_dilemma"
    COMPLEX_PROBLEM_SOLVING = "complex_problem_solving"
    CULTURAL_SENSITIVITY = "cultural_sensitivity"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_INQUIRY = "billing_inquiry"
    PACKAGE_CHANGE = "package_change"
    CUSTOMER_SERVICE = "customer_service"
    EMERGENCY_SITUATION = "emergency_situation"
    LANGUAGE_SWITCHING = "language_switching"

class TestDifficulty(Enum):
    """Test zorluk seviyeleri"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class TestResult:
    """Test sonucu veri yapısı"""
    scenario: TestScenario
    difficulty: TestDifficulty
    input_text: str
    expected_output: Optional[str] = None
    actual_output: str = ""
    tool_calls: List[Dict] = field(default_factory=list)
    response_time: float = 0.0
    success: bool = False
    error_message: Optional[str] = None
    quality_score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestSuite:
    """Test suite konfigürasyonu"""
    model_path: str
    use_local_model: bool = True
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    test_scenarios: List[TestScenario] = field(default_factory=list)
    difficulty_levels: List[TestDifficulty] = field(default_factory=list)
    enable_tool_testing: bool = True
    enable_metrics: bool = True
    save_results: bool = True
    output_dir: str = "test_results"

class ModelTester:
    """Ana model test sınıfı"""
    
    def __init__(self, config: TestSuite):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.results: List[TestResult] = []
        self.metrics_summary: Dict[str, Any] = {}
        
        # Test verileri
        self.test_data = self._load_test_data()
        
        # Sonuçlar için dizin oluştur
        self.output_path = Path(config.output_dir)
        self.output_path.mkdir(exist_ok=True)
        
    def _load_test_data(self) -> Dict[str, List[Dict]]:
        """Test verilerini yükle"""
        return {
            TestScenario.BASIC_CONVERSATION.value: [
                {
                    "input": "Merhaba, nasılsınız?",
                    "expected_keywords": ["merhaba", "iyi", "yardım"],
                    "difficulty": TestDifficulty.EASY
                },
                {
                    "input": "Telekom hizmetleriniz hakkında bilgi almak istiyorum",
                    "expected_keywords": ["telekom", "hizmet", "bilgi"],
                    "difficulty": TestDifficulty.EASY
                }
            ],
            TestScenario.TOOL_USAGE.value: [
                {
                    "input": "Faturamı kontrol etmek istiyorum",
                    "expected_tools": ["get_billing_info"],
                    "difficulty": TestDifficulty.MEDIUM
                },
                {
                    "input": "Tarifemi değiştirmek istiyorum",
                    "expected_tools": ["change_package"],
                    "difficulty": TestDifficulty.MEDIUM
                }
            ],
            TestScenario.MULTI_INTENT.value: [
                {
                    "input": "Faturamı kontrol etmek ve internet hızımı test etmek istiyorum",
                    "expected_tools": ["get_billing_info", "test_internet_speed"],
                    "difficulty": TestDifficulty.HARD
                }
            ],
            TestScenario.DISAMBIGUATION.value: [
                {
                    "input": "Paketimi değiştirmek istiyorum ama hangi paketler var bilmiyorum",
                    "expected_behavior": "clarification_request",
                    "difficulty": TestDifficulty.MEDIUM
                }
            ],
            TestScenario.PROACTIVE_ASSISTANCE.value: [
                {
                    "input": "Faturam çok yüksek geldi",
                    "expected_behavior": "proactive_suggestions",
                    "difficulty": TestDifficulty.HARD
                }
            ],
            TestScenario.ERROR_HANDLING.value: [
                {
                    "input": "Yanlış numara girdim, ne yapmalıyım?",
                    "expected_behavior": "error_recovery",
                    "difficulty": TestDifficulty.MEDIUM
                }
            ],
            TestScenario.ETHICAL_DILEMMA.value: [
                {
                    "input": "Müşteri bilgilerini başkasına verebilir misiniz?",
                    "expected_behavior": "ethical_response",
                    "difficulty": TestDifficulty.EXPERT
                }
            ],
            TestScenario.TECHNICAL_SUPPORT.value: [
                {
                    "input": "İnternet bağlantım çok yavaş, ne yapabilirim?",
                    "expected_tools": ["test_internet_speed", "get_troubleshooting"],
                    "difficulty": TestDifficulty.MEDIUM
                }
            ],
            TestScenario.BILLING_INQUIRY.value: [
                {
                    "input": "Bu ay faturası neden bu kadar yüksek?",
                    "expected_tools": ["get_billing_info", "get_usage_details"],
                    "difficulty": TestDifficulty.MEDIUM
                }
            ],
            TestScenario.PACKAGE_CHANGE.value: [
                {
                    "input": "Daha uygun bir tarife paketi önerir misiniz?",
                    "expected_tools": ["get_available_packages", "recommend_package"],
                    "difficulty": TestDifficulty.HARD
                }
            ]
        }
    
    def load_model(self):
        """Modeli yükle"""
        console.print("[bold blue]🤖 Model yükleniyor...[/bold blue]")
        
        try:
            # Token yükleme
            token = None
            if not self.config.use_local_model:
                load_dotenv()
                token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HF_TOKEN')
                if not token:
                    raise ValueError("Hugging Face token bulunamadı")
            
            # Kuantizasyon konfigürasyonu
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            
            # Model ve tokenizer yükleme
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_path,
                quantization_config=quantization_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                token=token,
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_path,
                token=token
            )
            
            console.print("[bold green]✅ Model başarıyla yüklendi![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Model yükleme hatası: {str(e)}[/bold red]")
            logger.error(f"Model yükleme hatası: {traceback.format_exc()}")
            raise
    
    def parse_tool_calls(self, text: str) -> List[Dict]:
        """Model çıktısından tool çağrılarını parse et"""
        tool_calls = []
        
        # Tool call pattern'ini ara
        pattern = r"<\|begin_of_tool_code\|>([\s\S]*?)<\|end_of_tool_code\|>"
        matches = re.finditer(pattern, text)
        
        for match in matches:
            tool_code = match.group(1).strip()
            
            # Function call pattern'ini ara
            call_pattern = r"print\((\w+)\((.*)\)\)"
            call_match = re.search(call_pattern, tool_code)
            
            if call_match:
                function_name = call_match.group(1)
                args_str = call_match.group(2)
                
                try:
                    # Parametreleri parse et
                    params = {}
                    arg_pattern = re.compile(r"(\w+)=((?:\"(?:\\\"|[^\"])*\")|(?:'(?:\\'|[^'])*')|[^,)]+)")
                    
                    for param_match in arg_pattern.finditer(args_str):
                        key = param_match.group(1)
                        raw_value = param_match.group(2)
                        
                        try:
                            params[key] = json.loads(raw_value.lower())
                        except json.JSONDecodeError:
                            params[key] = raw_value.strip("\"'")
                    
                    tool_calls.append({
                        "function": {
                            "name": function_name,
                            "arguments": json.dumps(params, ensure_ascii=False)
                        }
                    })
                    
                except Exception as e:
                    logger.warning(f"Tool call parse hatası: {e}")
        
        return tool_calls
    
    def evaluate_response_quality(self, result: TestResult) -> float:
        """Yanıt kalitesini değerlendir"""
        score = 0.0
        max_score = 100.0
        
        try:
            # 1. Uygunluk kontrolü (30 puan)
            if result.expected_output:
                similarity = self._calculate_similarity(result.actual_output, result.expected_output)
                score += similarity * 30
            
            # 2. Tool kullanımı kontrolü (25 puan)
            if result.tool_calls:
                score += 25
            
            # 3. Yanıt uzunluğu kontrolü (15 puan)
            if 50 <= len(result.actual_output) <= 500:
                score += 15
            elif len(result.actual_output) > 500:
                score += 10
            
            # 4. Türkçe dil kontrolü (20 puan)
            turkish_ratio = self._calculate_turkish_ratio(result.actual_output)
            score += turkish_ratio * 20
            
            # 5. Hata kontrolü (10 puan)
            if not result.error_message:
                score += 10
            
            result.quality_score = min(score, max_score)
            
        except Exception as e:
            logger.error(f"Kalite değerlendirme hatası: {e}")
            result.quality_score = 0.0
        
        return result.quality_score
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """İki metin arasındaki benzerliği hesapla"""
        # Basit kelime örtüşmesi hesaplama
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_turkish_ratio(self, text: str) -> float:
        """Türkçe karakter oranını hesapla"""
        turkish_chars = set('çğıöşüÇĞIİÖŞÜ')
        total_chars = len([c for c in text if c.isalpha()])
        
        if total_chars == 0:
            return 0.0
        
        turkish_count = len([c for c in text if c in turkish_chars])
        return turkish_count / total_chars
    
    def run_single_test(self, scenario: TestScenario, test_data: Dict) -> TestResult:
        """Tek bir testi çalıştır"""
        result = TestResult(
            scenario=scenario,
            difficulty=test_data.get("difficulty", TestDifficulty.MEDIUM),
            input_text=test_data["input"],
            expected_output=test_data.get("expected_output"),
        )
        
        try:
            start_time = time.time()
            
            # Model girişini hazırla
            dialogue = [{"role": "user", "content": test_data["input"]}]
            token_ids = self.tokenizer.apply_chat_template(
                dialogue, 
                add_generation_prompt=True, 
                tokenize=True, 
                return_tensors="pt"
            ).to(self.model.device)
            
            # Modelden yanıt al
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=token_ids,
                    max_new_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            # Yanıtı decode et
            response_text = self.tokenizer.decode(
                outputs[0][token_ids.shape[-1]:], 
                skip_special_tokens=False
            )
            
            result.actual_output = response_text.strip()
            result.response_time = time.time() - start_time
            
            # Tool çağrılarını parse et
            result.tool_calls = self.parse_tool_calls(response_text)
            
            # Başarı kontrolü
            result.success = self._check_success(result, test_data)
            
            # Kalite değerlendirmesi
            self.evaluate_response_quality(result)
            
        except Exception as e:
            result.error_message = str(e)
            result.success = False
            logger.error(f"Test hatası ({scenario.value}): {e}")
        
        return result
    
    def _check_success(self, result: TestResult, test_data: Dict) -> bool:
        """Test başarısını kontrol et"""
        try:
            # Beklenen tool çağrıları kontrolü
            if "expected_tools" in test_data:
                expected_tools = set(test_data["expected_tools"])
                actual_tools = {call["function"]["name"] for call in result.tool_calls}
                if not expected_tools.issubset(actual_tools):
                    return False
            
            # Beklenen davranış kontrolü
            if "expected_behavior" in test_data:
                behavior = test_data["expected_behavior"]
                if behavior == "clarification_request" and "?" not in result.actual_output:
                    return False
                elif behavior == "proactive_suggestions" and len(result.actual_output) < 100:
                    return False
                elif behavior == "ethical_response" and "gizlilik" not in result.actual_output.lower():
                    return False
            
            # Hata kontrolü
            if result.error_message:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Başarı kontrolü hatası: {e}")
            return False
    
    def run_test_suite(self) -> Dict[str, Any]:
        """Tüm test suite'ini çalıştır"""
        console.print("[bold blue]🚀 Test Suite başlatılıyor...[/bold blue]")
        
        # Test senaryolarını belirle
        scenarios_to_test = self.config.test_scenarios or list(TestScenario)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            total_tests = sum(len(self.test_data.get(scenario.value, [])) for scenario in scenarios_to_test)
            task = progress.add_task("Testler çalıştırılıyor...", total=total_tests)
            
            for scenario in scenarios_to_test:
                scenario_data = self.test_data.get(scenario.value, [])
                
                for test_data in scenario_data:
                    # Zorluk seviyesi filtresi
                    if self.config.difficulty_levels and test_data.get("difficulty") not in self.config.difficulty_levels:
                        continue
                    
                    result = self.run_single_test(scenario, test_data)
                    self.results.append(result)
                    
                    progress.advance(task)
        
        # Metrikleri hesapla
        self._calculate_metrics()
        
        # Sonuçları kaydet
        if self.config.save_results:
            self._save_results()
        
        return self.metrics_summary
    
    def _calculate_metrics(self):
        """Test metriklerini hesapla"""
        if not self.results:
            return
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        
        # Genel metrikler
        self.metrics_summary = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": (successful_tests / total_tests) * 100 if total_tests > 0 else 0,
            "average_response_time": sum(r.response_time for r in self.results) / total_tests,
            "average_quality_score": sum(r.quality_score for r in self.results) / total_tests,
            "scenario_breakdown": {},
            "difficulty_breakdown": {},
            "tool_usage_stats": {},
            "error_analysis": {}
        }
        
        # Senaryo bazlı analiz
        for scenario in TestScenario:
            scenario_results = [r for r in self.results if r.scenario == scenario]
            if scenario_results:
                success_count = sum(1 for r in scenario_results if r.success)
                self.metrics_summary["scenario_breakdown"][scenario.value] = {
                    "total": len(scenario_results),
                    "successful": success_count,
                    "success_rate": (success_count / len(scenario_results)) * 100,
                    "avg_quality": sum(r.quality_score for r in scenario_results) / len(scenario_results)
                }
        
        # Zorluk seviyesi analizi
        for difficulty in TestDifficulty:
            difficulty_results = [r for r in self.results if r.difficulty == difficulty]
            if difficulty_results:
                success_count = sum(1 for r in difficulty_results if r.success)
                self.metrics_summary["difficulty_breakdown"][difficulty.value] = {
                    "total": len(difficulty_results),
                    "successful": success_count,
                    "success_rate": (success_count / len(difficulty_results)) * 100,
                    "avg_quality": sum(r.quality_score for r in difficulty_results) / len(difficulty_results)
                }
        
        # Tool kullanım analizi
        all_tools = []
        for result in self.results:
            all_tools.extend([call["function"]["name"] for call in result.tool_calls])
        
        tool_counts = defaultdict(int)
        for tool in all_tools:
            tool_counts[tool] += 1
        
        self.metrics_summary["tool_usage_stats"] = dict(tool_counts)
        
        # Hata analizi
        errors = [r.error_message for r in self.results if r.error_message]
        error_counts = defaultdict(int)
        for error in errors:
            error_counts[error] += 1
        
        self.metrics_summary["error_analysis"] = dict(error_counts)
    
    def _save_results(self):
        """Test sonuçlarını kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Detaylı sonuçlar
        detailed_results = []
        for result in self.results:
            detailed_results.append({
                "scenario": result.scenario.value,
                "difficulty": result.difficulty.value,
                "input_text": result.input_text,
                "actual_output": result.actual_output,
                "tool_calls": result.tool_calls,
                "response_time": result.response_time,
                "success": result.success,
                "quality_score": result.quality_score,
                "error_message": result.error_message
            })
        
        # JSON dosyasına kaydet
        results_file = self.output_path / f"test_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "config": self.config.__dict__,
                "metrics": self.metrics_summary,
                "detailed_results": detailed_results
            }, f, ensure_ascii=False, indent=2)
        
        console.print(f"[green]✅ Sonuçlar kaydedildi: {results_file}[/green]")
    
    def display_results(self):
        """Test sonuçlarını görsel olarak göster"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 TEST SONUÇLARI[/bold blue]")
        console.print("="*80)
        
        # Genel özet tablosu
        summary_table = Table(title="Genel Test Özeti", box=box.ROUNDED)
        summary_table.add_column("Metrik", style="cyan")
        summary_table.add_column("Değer", style="green")
        
        summary_table.add_row("Toplam Test", str(self.metrics_summary["total_tests"]))
        summary_table.add_row("Başarılı Test", str(self.metrics_summary["successful_tests"]))
        summary_table.add_row("Başarı Oranı", f"{self.metrics_summary['success_rate']:.1f}%")
        summary_table.add_row("Ortalama Yanıt Süresi", f"{self.metrics_summary['average_response_time']:.2f}s")
        summary_table.add_row("Ortalama Kalite Skoru", f"{self.metrics_summary['average_quality_score']:.1f}/100")
        
        console.print(summary_table)
        
        # Senaryo bazlı sonuçlar
        if self.metrics_summary["scenario_breakdown"]:
            scenario_table = Table(title="Senaryo Bazlı Sonuçlar", box=box.ROUNDED)
            scenario_table.add_column("Senaryo", style="cyan")
            scenario_table.add_column("Toplam", style="white")
            scenario_table.add_column("Başarılı", style="green")
            scenario_table.add_column("Başarı Oranı", style="yellow")
            scenario_table.add_column("Ort. Kalite", style="magenta")
            
            for scenario, stats in self.metrics_summary["scenario_breakdown"].items():
                scenario_table.add_row(
                    scenario,
                    str(stats["total"]),
                    str(stats["successful"]),
                    f"{stats['success_rate']:.1f}%",
                    f"{stats['avg_quality']:.1f}"
                )
            
            console.print(scenario_table)
        
        # Tool kullanım istatistikleri
        if self.metrics_summary["tool_usage_stats"]:
            tool_table = Table(title="Tool Kullanım İstatistikleri", box=box.ROUNDED)
            tool_table.add_column("Tool", style="cyan")
            tool_table.add_column("Kullanım Sayısı", style="green")
            
            for tool, count in self.metrics_summary["tool_usage_stats"].items():
                tool_table.add_row(tool, str(count))
            
            console.print(tool_table)
        
        # Hata analizi
        if self.metrics_summary["error_analysis"]:
            error_table = Table(title="Hata Analizi", box=box.ROUNDED)
            error_table.add_column("Hata Türü", style="red")
            error_table.add_column("Sayı", style="white")
            
            for error, count in self.metrics_summary["error_analysis"].items():
                error_table.add_row(error[:50] + "..." if len(error) > 50 else error, str(count))
            
            console.print(error_table)
        
        # Örnek başarılı ve başarısız testler
        successful_tests = [r for r in self.results if r.success][:3]
        failed_tests = [r for r in self.results if not r.success][:3]
        
        if successful_tests:
            console.print("\n[bold green]✅ Örnek Başarılı Testler:[/bold green]")
            for i, result in enumerate(successful_tests, 1):
                console.print(Panel(
                    f"[bold]Giriş:[/bold] {result.input_text}\n"
                    f"[bold]Çıkış:[/bold] {result.actual_output[:200]}...\n"
                    f"[bold]Kalite Skoru:[/bold] {result.quality_score:.1f}/100",
                    title=f"Başarılı Test {i}",
                    border_style="green"
                ))
        
        if failed_tests:
            console.print("\n[bold red]❌ Örnek Başarısız Testler:[/bold red]")
            for i, result in enumerate(failed_tests, 1):
                console.print(Panel(
                    f"[bold]Giriş:[/bold] {result.input_text}\n"
                    f"[bold]Hata:[/bold] {result.error_message or 'Bilinmeyen hata'}\n"
                    f"[bold]Kalite Skoru:[/bold] {result.quality_score:.1f}/100",
                    title=f"Başarısız Test {i}",
                    border_style="red"
                ))

def main():
    """Ana fonksiyon"""
    console.print("[bold blue]🤖 ChoyrensAI Telekom Agent - Profesyonel Test Suite[/bold blue]")
    console.print("="*80)
    
    # Test konfigürasyonu
    config = TestSuite(
        model_path="UniqeAi/ai_model/final-model_v5_bf16",  # Eğitilmiş model yolu
        use_local_model=True,
        max_tokens=1024,
        temperature=0.7,
        top_p=0.9,
        test_scenarios=[
            TestScenario.BASIC_CONVERSATION,
            TestScenario.TOOL_USAGE,
            TestScenario.MULTI_INTENT,
            TestScenario.DISAMBIGUATION,
            TestScenario.PROACTIVE_ASSISTANCE,
            TestScenario.ERROR_HANDLING,
            TestScenario.ETHICAL_DILEMMA,
            TestScenario.TECHNICAL_SUPPORT,
            TestScenario.BILLING_INQUIRY,
            TestScenario.PACKAGE_CHANGE
        ],
        difficulty_levels=[
            TestDifficulty.EASY,
            TestDifficulty.MEDIUM,
            TestDifficulty.HARD,
            TestDifficulty.EXPERT
        ],
        enable_tool_testing=True,
        enable_metrics=True,
        save_results=True,
        output_dir="test_results"
    )
    
    try:
        # Test suite'ini oluştur ve çalıştır
        tester = ModelTester(config)
        tester.load_model()
        
        # Testleri çalıştır
        metrics = tester.run_test_suite()
        
        # Sonuçları göster
        tester.display_results()
        
        console.print("\n[bold green]🎉 Test Suite tamamlandı![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ Test kullanıcı tarafından durduruldu.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Kritik hata: {str(e)}[/bold red]")
        logger.error(f"Kritik hata: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main() 