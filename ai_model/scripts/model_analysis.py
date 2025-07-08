#!/usr/bin/env python3
"""
🔍 Model Analysis - Model'in ne öğrendiğini detaylı analiz eder
============================================================

Model'in API pattern'larını ne kadar öğrendiğini test eder.
"""

import torch
import warnings
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

warnings.filterwarnings("ignore")

class ModelAnalyzer:
    def __init__(self):
        self.model_path = "./qlora_fine_tuned_model"
        self.base_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load model for analysis"""
        print("🔍 Model analiz için yükleniyor...")
        
        try:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model_name,
                trust_remote_code=True
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
                offload_buffers=True
            )
            
            self.model = PeftModel.from_pretrained(
                base_model,
                self.model_path,
                device_map="auto"
            )
            
            print("✅ Model yüklendi")
            return True
            
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            return False
    
    def test_api_understanding(self):
        """Test if model understands API patterns"""
        print("\n🧪 API Pattern Analizi")
        print("=" * 50)
        
        # Dataset'teki gerçek API'ler
        correct_apis = [
            "get_current_bill",
            "update_customer_contact", 
            "create_fault_ticket",
            "test_internet_speed",
            "enable_roaming",
            "change_package",
            "get_customer_profile",
            "suspend_line",
            "reactivate_line"
        ]
        
        test_prompts = [
            "Faturamı görmek istiyorum",
            "Telefon numaramı değiştirmek istiyorum", 
            "Arıza kaydı oluşturmak istiyorum",
            "İnternet hızımı test etmek istiyorum",
            "Roaming açmak istiyorum",
            "Paketimi değiştirmek istiyorum",
            "Profil bilgilerimi görmek istiyorum",
            "Hattımı dondurmak istiyorum",
            "Hattımı aktive etmek istiyorum"
        ]
        
        results = []
        
        for i, prompt in enumerate(test_prompts):
            print(f"\n🔸 Test {i+1}: {prompt}")
            
            # Generate response
            response = self.generate_simple(prompt)
            print(f"Model: {response}")
            
            # Check for correct API
            expected_api = correct_apis[i]
            has_correct_api = expected_api in response
            has_tool_wrapper = "<tool_code>" in response
            has_backend_prefix = "backend_api." in response
            
            print(f"  ✓ Tool wrapper: {'✅' if has_tool_wrapper else '❌'}")
            print(f"  ✓ Backend prefix: {'✅' if has_backend_prefix else '❌'}")
            print(f"  ✓ Correct API ({expected_api}): {'✅' if has_correct_api else '❌'}")
            
            results.append({
                'prompt': prompt,
                'response': response,
                'has_wrapper': has_tool_wrapper,
                'has_prefix': has_backend_prefix,
                'has_correct_api': has_correct_api,
                'expected_api': expected_api
            })
        
        return results
    
    def analyze_results(self, results):
        """Analyze test results"""
        print("\n📊 SONUÇ ANALİZİ")
        print("=" * 50)
        
        total = len(results)
        wrapper_correct = sum(1 for r in results if r['has_wrapper'])
        prefix_correct = sum(1 for r in results if r['has_prefix'])
        api_correct = sum(1 for r in results if r['has_correct_api'])
        
        print(f"📋 Test edilen senaryo: {total}")
        print(f"🔧 Tool wrapper (<tool_code>): {wrapper_correct}/{total} ({wrapper_correct/total*100:.1f}%)")
        print(f"🔌 Backend prefix (backend_api.): {prefix_correct}/{total} ({prefix_correct/total*100:.1f}%)")
        print(f"🎯 Doğru API: {api_correct}/{total} ({api_correct/total*100:.1f}%)")
        
        print(f"\n💡 DEĞERLENDIRME:")
        if wrapper_correct >= total * 0.8:
            print("✅ Model tool format'ını öğrenmiş")
        else:
            print("❌ Model tool format'ını öğrenememiş")
            
        if prefix_correct >= total * 0.8:
            print("✅ Model backend_api prefix'ini öğrenmiş")
        else:
            print("❌ Model backend_api prefix'ini öğrenememiş")
            
        if api_correct >= total * 0.5:
            print("🟡 Model API'leri kısmen öğrenmiş")
        elif api_correct >= total * 0.2:
            print("⚠️ Model API'leri çok az öğrenmiş")
        else:
            print("❌ Model API'leri hiç öğrenememiş")
        
        # Recommendation
        print(f"\n🎯 ÖNERİ:")
        if api_correct < total * 0.3:
            print("🔄 FULL RETRAIN öneriliyor - Model temelden yeniden eğitilmeli")
            print("   - Learning rate düşürülmeli")
            print("   - Epoch sayısı artırılmalı") 
            print("   - Dataset quality kontrol edilmeli")
        elif api_correct < total * 0.7:
            print("🔧 TARGETED FIX öneriliyor - Belirli API'ler için ek eğitim")
        else:
            print("✨ Model iyi durumda - Küçük iyileştirmeler yeterli")
            
        return {
            'wrapper_rate': wrapper_correct/total,
            'prefix_rate': prefix_correct/total,
            'api_rate': api_correct/total
        }
    
    def generate_simple(self, prompt):
        """Simple generation for testing"""
        if not self.model:
            return "Model yüklü değil"
            
        formatted_prompt = f"### Instruction:\n{prompt[:20].title()}\n\n### Input:\n{prompt}\n\n### Response:\n"
        
        try:
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda:0") for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=60,
                    temperature=0.1,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    use_cache=False
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.split("### Response:\n")[-1].strip()
            response = response.replace("<|endoftext|>", "")
            response = response.split("### Instruction:")[0].strip()
            
            return response
            
        except Exception as e:
            return f"Hata: {e}"

def main():
    analyzer = ModelAnalyzer()
    
    if not analyzer.load_model():
        return
    
    # Test API understanding
    results = analyzer.test_api_understanding()
    
    # Analyze results
    scores = analyzer.analyze_results(results)
    
    # Summary
    print(f"\n🏆 ÖZET SKOR:")
    print(f"Format: {scores['wrapper_rate']*100:.1f}%")
    print(f"Prefix: {scores['prefix_rate']*100:.1f}%") 
    print(f"API Doğruluk: {scores['api_rate']*100:.1f}%")

if __name__ == "__main__":
    main() 