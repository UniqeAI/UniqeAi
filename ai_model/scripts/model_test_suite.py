# -*- coding: utf-8 -*-
"""
🤖 ChoyrensAI Telekom Agent - Model Test Suite
==============================================

Eğitilmiş Meta Llama 3 Instruct modelini kapsamlı şekilde test eder.
"""

import os
import sys
import json
import time
import torch
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import box

# Proje yolu ayarları
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))
from UniqeAi.ai_model.scripts.tool_definitions import get_tool_definitions, get_tool_response

console = Console()

class TestType(Enum):
    BASIC = "basic"
    TOOL_USAGE = "tool_usage"
    MULTI_INTENT = "multi_intent"
    ERROR_HANDLING = "error_handling"
    COMPLEX = "complex"

@dataclass
class TestCase:
    type: TestType
    input_text: str
    expected_tools: List[str] = None
    expected_keywords: List[str] = None
    description: str = ""

@dataclass
class TestResult:
    test_case: TestCase
    actual_output: str = ""
    tool_calls: List[Dict] = None
    response_time: float = 0.0
    success: bool = False
    quality_score: float = 0.0
    error: str = ""

class ModelTester:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.results = []
        
        # Test verileri
        self.test_cases = self._create_test_cases()
    
    def _create_test_cases(self) -> List[TestCase]:
        """Test senaryolarını oluştur"""
        return [
            # Temel konuşma testleri
            TestCase(
                type=TestType.BASIC,
                input_text="Merhaba, nasılsınız?",
                expected_keywords=["merhaba", "iyi", "yardım"],
                description="Temel selamlama testi"
            ),
            TestCase(
                type=TestType.BASIC,
                input_text="Telekom hizmetleriniz hakkında bilgi almak istiyorum",
                expected_keywords=["telekom", "hizmet", "bilgi"],
                description="Genel bilgi sorgusu"
            ),
            
            # Tool kullanım testleri
            TestCase(
                type=TestType.TOOL_USAGE,
                input_text="Faturamı kontrol etmek istiyorum",
                expected_tools=["get_billing_info"],
                description="Fatura sorgulama testi"
            ),
            TestCase(
                type=TestType.TOOL_USAGE,
                input_text="Tarifemi değiştirmek istiyorum",
                expected_tools=["change_package"],
                description="Paket değiştirme testi"
            ),
            TestCase(
                type=TestType.TOOL_USAGE,
                input_text="İnternet hızımı test etmek istiyorum",
                expected_tools=["test_internet_speed"],
                description="İnternet hız testi"
            ),
            
            # Çoklu amaç testleri
            TestCase(
                type=TestType.MULTI_INTENT,
                input_text="Faturamı kontrol etmek ve internet hızımı test etmek istiyorum",
                expected_tools=["get_billing_info", "test_internet_speed"],
                description="Çoklu işlem testi"
            ),
            TestCase(
                type=TestType.MULTI_INTENT,
                input_text="Tarifemi değiştirmek ve fatura bilgilerimi görmek istiyorum",
                expected_tools=["change_package", "get_billing_info"],
                description="Paket değiştirme + fatura sorgulama"
            ),
            
            # Hata yönetimi testleri
            TestCase(
                type=TestType.ERROR_HANDLING,
                input_text="Yanlış numara girdim, ne yapmalıyım?",
                expected_keywords=["yanlış", "numara", "yardım"],
                description="Hata durumu yönetimi"
            ),
            TestCase(
                type=TestType.ERROR_HANDLING,
                input_text="İnternet bağlantım çok yavaş, ne yapabilirim?",
                expected_tools=["test_internet_speed"],
                description="Teknik sorun çözümü"
            ),
            
            # Karmaşık senaryolar
            TestCase(
                type=TestType.COMPLEX,
                input_text="Bu ay faturası çok yüksek geldi, daha uygun bir tarife önerir misiniz?",
                expected_tools=["get_billing_info", "get_available_packages"],
                description="Karmaşık müşteri sorgusu"
            ),
            TestCase(
                type=TestType.COMPLEX,
                input_text="Yurtdışına gideceğim, roaming hizmetini nasıl aktif edebilirim?",
                expected_tools=["enable_roaming"],
                description="Roaming hizmeti aktivasyonu"
            ),
        ]
    
    def load_model(self):
        """Modeli yükle"""
        console.print("[bold blue]🤖 Model yükleniyor...[/bold blue]")
        
        try:
            # Kuantizasyon ayarları
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            
            # Model ve tokenizer yükleme
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=quantization_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            console.print("[bold green]✅ Model başarıyla yüklendi![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Model yükleme hatası: {str(e)}[/bold red]")
            raise
    
    def parse_tool_calls(self, text: str) -> List[Dict]:
        """Tool çağrılarını parse et"""
        tool_calls = []
        
        # Tool call pattern'ini ara
        import re
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
                    # Basit parametre parsing
                    params = {}
                    if args_str.strip():
                        # Basit key=value parsing
                        for arg in args_str.split(','):
                            if '=' in arg:
                                key, value = arg.split('=', 1)
                                key = key.strip()
                                value = value.strip().strip('"\'')
                                params[key] = value
                    
                    tool_calls.append({
                        "function": {
                            "name": function_name,
                            "arguments": json.dumps(params, ensure_ascii=False)
                        }
                    })
                    
                except Exception as e:
                    console.print(f"[yellow]Tool parse hatası: {e}[/yellow]")
        
        return tool_calls
    
    def evaluate_response(self, result: TestResult) -> float:
        """Yanıt kalitesini değerlendir"""
        score = 0.0
        
        try:
            # Tool kullanımı kontrolü (40 puan)
            if result.test_case.expected_tools:
                actual_tools = {call["function"]["name"] for call in result.tool_calls or []}
                expected_tools = set(result.test_case.expected_tools)
                if expected_tools.issubset(actual_tools):
                    score += 40
            
            # Anahtar kelime kontrolü (30 puan)
            if result.test_case.expected_keywords:
                text_lower = result.actual_output.lower()
                found_keywords = sum(1 for keyword in result.test_case.expected_keywords 
                                   if keyword.lower() in text_lower)
                score += (found_keywords / len(result.test_case.expected_keywords)) * 30
            
            # Yanıt uzunluğu (20 puan)
            if 50 <= len(result.actual_output) <= 500:
                score += 20
            elif len(result.actual_output) > 500:
                score += 15
            
            # Türkçe karakter kontrolü (10 puan)
            turkish_chars = set('çğıöşüÇĞIİÖŞÜ')
            turkish_count = sum(1 for c in result.actual_output if c in turkish_chars)
            if turkish_count > 0:
                score += 10
            
            result.quality_score = min(score, 100.0)
            
        except Exception as e:
            console.print(f"[yellow]Değerlendirme hatası: {e}[/yellow]")
            result.quality_score = 0.0
        
        return result.quality_score
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """Tek bir testi çalıştır"""
        result = TestResult(test_case=test_case)
        
        try:
            start_time = time.time()
            
            # Model girişini hazırla
            dialogue = [{"role": "user", "content": test_case.input_text}]
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
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
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
            result.success = self._check_success(result)
            
            # Kalite değerlendirmesi
            self.evaluate_response(result)
            
        except Exception as e:
            result.error = str(e)
            result.success = False
        
        return result
    
    def _check_success(self, result: TestResult) -> bool:
        """Test başarısını kontrol et"""
        try:
            # Tool kontrolü
            if result.test_case.expected_tools:
                actual_tools = {call["function"]["name"] for call in result.tool_calls or []}
                expected_tools = set(result.test_case.expected_tools)
                if not expected_tools.issubset(actual_tools):
                    return False
            
            # Anahtar kelime kontrolü
            if result.test_case.expected_keywords:
                text_lower = result.actual_output.lower()
                found_keywords = sum(1 for keyword in result.test_case.expected_keywords 
                                   if keyword.lower() in text_lower)
                if found_keywords == 0:
                    return False
            
            # Hata kontrolü
            if result.error:
                return False
            
            return True
            
        except Exception:
            return False
    
    def run_all_tests(self):
        """Tüm testleri çalıştır"""
        console.print("[bold blue]🚀 Testler başlatılıyor...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Testler çalıştırılıyor...", total=len(self.test_cases))
            
            for test_case in self.test_cases:
                result = self.run_single_test(test_case)
                self.results.append(result)
                progress.advance(task)
        
        self._calculate_metrics()
        self._save_results()
    
    def _calculate_metrics(self):
        """Test metriklerini hesapla"""
        if not self.results:
            return
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        
        self.metrics = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": (successful_tests / total_tests) * 100,
            "average_response_time": sum(r.response_time for r in self.results) / total_tests,
            "average_quality_score": sum(r.quality_score for r in self.results) / total_tests,
            "type_breakdown": defaultdict(lambda: {"total": 0, "successful": 0})
        }
        
        # Tip bazlı analiz
        for result in self.results:
            test_type = result.test_case.type.value
            self.metrics["type_breakdown"][test_type]["total"] += 1
            if result.success:
                self.metrics["type_breakdown"][test_type]["successful"] += 1
    
    def _save_results(self):
        """Sonuçları kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Detaylı sonuçlar
        detailed_results = []
        for result in self.results:
            detailed_results.append({
                "type": result.test_case.type.value,
                "description": result.test_case.description,
                "input_text": result.test_case.input_text,
                "actual_output": result.actual_output,
                "tool_calls": result.tool_calls,
                "response_time": result.response_time,
                "success": result.success,
                "quality_score": result.quality_score,
                "error": result.error
            })
        
        # JSON dosyasına kaydet
        output_dir = Path("test_results")
        output_dir.mkdir(exist_ok=True)
        
        results_file = output_dir / f"test_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "model_path": self.model_path,
                "metrics": self.metrics,
                "detailed_results": detailed_results
            }, f, ensure_ascii=False, indent=2)
        
        console.print(f"[green]✅ Sonuçlar kaydedildi: {results_file}[/green]")
    
    def display_results(self):
        """Sonuçları göster"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 TEST SONUÇLARI[/bold blue]")
        console.print("="*80)
        
        # Genel özet
        summary_table = Table(title="Genel Test Özeti", box=box.ROUNDED)
        summary_table.add_column("Metrik", style="cyan")
        summary_table.add_column("Değer", style="green")
        
        summary_table.add_row("Toplam Test", str(self.metrics["total_tests"]))
        summary_table.add_row("Başarılı Test", str(self.metrics["successful_tests"]))
        summary_table.add_row("Başarı Oranı", f"{self.metrics['success_rate']:.1f}%")
        summary_table.add_row("Ortalama Yanıt Süresi", f"{self.metrics['average_response_time']:.2f}s")
        summary_table.add_row("Ortalama Kalite Skoru", f"{self.metrics['average_quality_score']:.1f}/100")
        
        console.print(summary_table)
        
        # Tip bazlı sonuçlar
        type_table = Table(title="Test Tipi Bazlı Sonuçlar", box=box.ROUNDED)
        type_table.add_column("Test Tipi", style="cyan")
        type_table.add_column("Toplam", style="white")
        type_table.add_column("Başarılı", style="green")
        type_table.add_column("Başarı Oranı", style="yellow")
        
        for test_type, stats in self.metrics["type_breakdown"].items():
            if stats["total"] > 0:
                success_rate = (stats["successful"] / stats["total"]) * 100
                type_table.add_row(
                    test_type,
                    str(stats["total"]),
                    str(stats["successful"]),
                    f"{success_rate:.1f}%"
                )
        
        console.print(type_table)
        
        # Örnek sonuçlar
        successful_tests = [r for r in self.results if r.success][:2]
        failed_tests = [r for r in self.results if not r.success][:2]
        
        if successful_tests:
            console.print("\n[bold green]✅ Örnek Başarılı Testler:[/bold green]")
            for i, result in enumerate(successful_tests, 1):
                console.print(Panel(
                    f"[bold]Giriş:[/bold] {result.test_case.input_text}\n"
                    f"[bold]Çıkış:[/bold] {result.actual_output[:200]}...\n"
                    f"[bold]Kalite:[/bold] {result.quality_score:.1f}/100",
                    title=f"Başarılı Test {i}",
                    border_style="green"
                ))
        
        if failed_tests:
            console.print("\n[bold red]❌ Örnek Başarısız Testler:[/bold red]")
            for i, result in enumerate(failed_tests, 1):
                console.print(Panel(
                    f"[bold]Giriş:[/bold] {result.test_case.input_text}\n"
                    f"[bold]Hata:[/bold] {result.error or 'Bilinmeyen hata'}\n"
                    f"[bold]Kalite:[/bold] {result.quality_score:.1f}/100",
                    title=f"Başarısız Test {i}",
                    border_style="red"
                ))

def main():
    """Ana fonksiyon"""
    console.print("[bold blue]🤖 ChoyrensAI Telekom Agent - Model Test Suite[/bold blue]")
    console.print("="*80)
    
    # Model yolu - eğitilmiş modelinizin yolunu buraya yazın
    model_path = "UniqeAi/ai_model/final-model_v5_bf16"
    
    try:
        # Test suite'ini oluştur ve çalıştır
        tester = ModelTester(model_path)
        tester.load_model()
        
        # Testleri çalıştır
        tester.run_all_tests()
        
        # Sonuçları göster
        tester.display_results()
        
        console.print("\n[bold green]🎉 Test Suite tamamlandı![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ Test kullanıcı tarafından durduruldu.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Kritik hata: {str(e)}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 