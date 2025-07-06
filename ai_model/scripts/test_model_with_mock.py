"""
Model Test Sistemi - Mock Backend ile Entegrasyon

Bu script, mock backend API kullanarak modelin doğru çalışıp çalışmadığını test eder.
Gerçek backend hazır olmadan model eğitimi yapabilmemizi sağlar.
"""

import json
import sys
import os
import re
from datetime import datetime
from mock_backend_api import backend_api

class ModelTester:
    """
    AI modelinin mock backend ile entegrasyonunu test eden sınıf.
    """
    
    def __init__(self, dataset_path: str):
        """Test dataset'ini yükler."""
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
        self.test_results = []
        
    def _load_dataset(self):
        """Dataset'i JSON dosyasından yükler."""
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Dataset dosyası bulunamadı: {self.dataset_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Dataset JSON formatı bozuk: {self.dataset_path}")
            sys.exit(1)
    
    def _extract_function_call(self, output_text: str):
        """
        Model output'undan API fonksiyon çağrısını çıkarır.
        
        Input: "<tool_code>print(backend_api.get_current_bill(user_id=6450))</tool_code>"
        Output: ("get_current_bill", {"user_id": 6450})
        """
        # Tool code kısmını çıkar
        tool_pattern = r'<tool_code>(.*?)</tool_code>'
        match = re.search(tool_pattern, output_text, re.DOTALL)
        
        if not match:
            return None, None
        
        code = match.group(1).strip()
        
        # API fonksiyon çağrısını parse et
        api_pattern = r'backend_api\.(\w+)\((.*?)\)'
        api_match = re.search(api_pattern, code)
        
        if not api_match:
            return None, None
        
        function_name = api_match.group(1)
        params_str = api_match.group(2)
        
        # Parametreleri parse et
        params = self._parse_parameters(params_str)
        
        return function_name, params
    
    def _parse_parameters(self, params_str: str):
        """
        Fonksiyon parametrelerini parse eder.
        
        Input: "user_id=6450, status=True"
        Output: {"user_id": 6450, "status": True}
        """
        params = {}
        
        # Basit parameter parsing (gerçek bir parser kadar güçlü değil ama test için yeterli)
        if not params_str.strip():
            return params
        
        # Split by comma and process each parameter
        for param in params_str.split(','):
            param = param.strip()
            if '=' in param:
                key, value = param.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes and convert types
                if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    # String value
                    params[key] = value[1:-1]
                elif value.lower() == 'true':
                    params[key] = True
                elif value.lower() == 'false':
                    params[key] = False
                elif value.isdigit():
                    params[key] = int(value)
                elif value.replace('.', '').isdigit():
                    params[key] = float(value)
                else:
                    params[key] = value
        
        return params
    
    def test_single_example(self, example: dict) -> dict:
        """
        Tek bir dataset örneğini test eder.
        """
        input_text = example.get("input", "")
        output_text = example.get("output", "")
        instruction = example.get("instruction", "")
        
        # API fonksiyon çağrısını çıkar
        function_name, params = self._extract_function_call(output_text)
        
        if not function_name:
            return {
                "input": input_text,
                "instruction": instruction,
                "status": "PARSE_ERROR",
                "error": "API fonksiyon çağrısı parse edilemedi",
                "original_output": output_text
            }
        
        # Mock API'de fonksiyon var mı kontrol et
        if not hasattr(backend_api, function_name):
            return {
                "input": input_text,
                "instruction": instruction,
                "function": function_name,
                "status": "FUNCTION_NOT_FOUND",
                "error": f"Mock API'de {function_name} fonksiyonu bulunamadı"
            }
        
        # API fonksiyonunu çağır
        try:
            api_function = getattr(backend_api, function_name)
            result = api_function(**params)
            
            return {
                "input": input_text,
                "instruction": instruction,
                "function": function_name,
                "params": params,
                "status": "SUCCESS",
                "api_result": result,
                "api_success": result.get("success", False)
            }
            
        except Exception as e:
            return {
                "input": input_text,
                "instruction": instruction,
                "function": function_name,
                "params": params,
                "status": "API_ERROR",
                "error": str(e)
            }
    
    def run_full_test(self, sample_size: int = 50) -> dict:
        """
        Dataset'in bir kısmını test eder ve sonuçları raporlar.
        """
        print(f"\n🧪 MODEL TEST SİSTEMİ BAŞLATILIYOR")
        print(f"📊 Dataset boyutu: {len(self.dataset)}")
        print(f"🎯 Test edilecek örnek sayısı: {min(sample_size, len(self.dataset))}")
        print("=" * 60)
        
        # Sample test data
        test_data = self.dataset[:sample_size] if sample_size < len(self.dataset) else self.dataset
        
        results = {
            "total_tests": len(test_data),
            "successful_calls": 0,
            "parse_errors": 0,
            "function_not_found": 0,
            "api_errors": 0,
            "api_success_calls": 0,
            "function_coverage": {},
            "detailed_results": []
        }
        
        # Reset API call log
        backend_api.reset_call_log()
        
        for i, example in enumerate(test_data):
            test_result = self.test_single_example(example)
            results["detailed_results"].append(test_result)
            
            # Update statistics
            status = test_result["status"]
            if status == "SUCCESS":
                results["successful_calls"] += 1
                function_name = test_result["function"]
                results["function_coverage"][function_name] = results["function_coverage"].get(function_name, 0) + 1
                
                if test_result.get("api_success", False):
                    results["api_success_calls"] += 1
                    
            elif status == "PARSE_ERROR":
                results["parse_errors"] += 1
            elif status == "FUNCTION_NOT_FOUND":
                results["function_not_found"] += 1
            elif status == "API_ERROR":
                results["api_errors"] += 1
            
            # Progress indicator
            if (i + 1) % 10 == 0 or (i + 1) == len(test_data):
                print(f"✅ {i+1}/{len(test_data)} test tamamlandı...")
        
        # Calculate percentages
        total = results["total_tests"]
        results["success_rate"] = (results["successful_calls"] / total * 100) if total > 0 else 0
        results["api_success_rate"] = (results["api_success_calls"] / total * 100) if total > 0 else 0
        
        return results
    
    def print_test_report(self, results: dict):
        """
        Test sonuçlarının detaylı raporunu yazdırır.
        """
        print("\n" + "=" * 60)
        print("📋 TEST SONUÇLARI RAPORU")
        print("=" * 60)
        
        # Genel İstatistikler
        print(f"\n📊 GENEL İSTATİSTİKLER:")
        print(f"   Toplam Test: {results['total_tests']}")
        print(f"   ✅ Başarılı API Çağrısı: {results['successful_calls']} ({results['success_rate']:.1f}%)")
        print(f"   🎯 API Başarı Oranı: {results['api_success_calls']} ({results['api_success_rate']:.1f}%)")
        print(f"   ❌ Parse Hatası: {results['parse_errors']}")
        print(f"   🔍 Fonksiyon Bulunamadı: {results['function_not_found']}")
        print(f"   ⚠️  API Hatası: {results['api_errors']}")
        
        # Fonksiyon Kapsamı
        print(f"\n🔧 KULLANILAN FONKSİYONLAR:")
        if results["function_coverage"]:
            for func, count in sorted(results["function_coverage"].items(), key=lambda x: x[1], reverse=True):
                print(f"   {func}: {count} çağrı")
        else:
            print("   Hiç fonksiyon başarıyla çağrılmadı!")
        
        # API İstatistikleri
        api_stats = backend_api.get_call_statistics()
        print(f"\n📈 MOCK API İSTATİSTİKLERİ:")
        print(f"   Toplam API Çağrısı: {api_stats['total_calls']}")
        print(f"   Başarı Oranı: {api_stats['success_rate']}%")
        
        # Hata Örnekleri
        error_examples = [r for r in results["detailed_results"] if r["status"] != "SUCCESS"]
        if error_examples:
            print(f"\n❌ HATA ÖRNEKLERİ (İlk 5):")
            for i, error in enumerate(error_examples[:5]):
                print(f"   {i+1}. {error['status']}: {error.get('error', 'Bilinmeyen hata')}")
                if 'function' in error:
                    print(f"      Fonksiyon: {error['function']}")
                print(f"      Input: {error['input'][:100]}...")
        
        # Başarı Değerlendirmesi
        print(f"\n🎯 GENEL DEĞERLENDİRME:")
        if results['success_rate'] >= 90:
            print("   🌟 MÜKEMMEL! Model çok iyi çalışıyor.")
        elif results['success_rate'] >= 75:
            print("   ✅ İYİ! Model genel olarak başarılı.")
        elif results['success_rate'] >= 50:
            print("   ⚠️  ORTA! Bazı iyileştirmeler gerekli.")
        else:
            print("   ❌ ZAYIF! Major sorunlar var, inceleme gerekli.")

def main():
    """Ana test fonksiyonu."""
    
    # Dataset path
    dataset_path = "../data/telekom_training_dataset_enhanced.json"
    
    # Test runner
    tester = ModelTester(dataset_path)
    
    # Run tests
    results = tester.run_full_test(sample_size=100)  # İlk 100 örneği test et
    
    # Print report
    tester.print_test_report(results)
    
    # Save detailed results
    output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detaylı sonuçlar kaydedildi: {output_file}")
    
    return results['success_rate'] >= 75  # Return True if tests pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 