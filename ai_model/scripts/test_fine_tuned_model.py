#!/usr/bin/env python3
"""
🧪 Fine-tuned Model Test Script - MEMORY OPTIMIZED
=================================================

QLoRA ile eğitilmiş modelin kalitesini test eder.
RTX 4060 8GB için optimize edilmiş.
"""

import os
import torch
import gc
import logging
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file at the project root
load_dotenv()

def setup_huggingface_token():
    """Setup Hugging Face token from environment variable."""
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if token:
        logger.info("✅ Hugging Face token found in environment")
        # Set environment variable for transformers library
        os.environ['HF_TOKEN'] = token
        return True
    else:
        logger.warning("⚠️ HUGGINGFACE_HUB_TOKEN environment variable not found. Relying on global login.")
        # transformers library will try to use cached token from `huggingface-cli login`
        return False

class ModelTester:
    def __init__(self, model_path="./qlora_fine_tuned_model"):
        setup_huggingface_token()
        self.model_path = model_path
        self.base_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.offload_dir = "./temp_offload"  # CPU offload directory
        
        # Create offload directory
        os.makedirs(self.offload_dir, exist_ok=True)
        
    def setup_quantization(self):
        """4-bit quantization for memory efficiency"""
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
    def load_model(self):
        """Load fine-tuned model with memory optimization"""
        print("🤖 Loading fine-tuned model (memory optimized)...")
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        # Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # 4-bit quantization for memory efficiency
        bnb_config = self.setup_quantization()
        
        print("📦 Loading base model with quantization...")
        # Base model with simple device mapping
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            quantization_config=bnb_config,
            device_map="auto",  # Let transformers decide
            torch_dtype=torch.float16,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            offload_buffers=True  # This fixes the offload buffer error
        )
        
        print("✅ Base model loaded, loading LoRA adapters...")
        
        # Load fine-tuned adapters
        model = PeftModel.from_pretrained(
            base_model, 
            self.model_path,
            torch_dtype=torch.float16
        )
        
        print("✅ Fine-tuned model loaded successfully!")
        return model, tokenizer
    
    def test_scenarios(self, model, tokenizer):
        """Test telekom scenarios with memory optimization"""
        print("🧪 Testing scenarios...")
        
        test_cases = [
            {
                "input": "Paketimi değiştirmek istiyorum",
                "expected_api": "backend_api.change_package",
                "expected_wrapper": "<tool_code>"
            },
            {
                "input": "Faturamı görmek istiyorum", 
                "expected_api": "backend_api.get_current_bill",
                "expected_wrapper": "<tool_code>"
            },
            {
                "input": "İnternetim çok yavaş",
                "expected_api": "backend_api.test_internet_speed",
                "expected_wrapper": "<tool_code>"
            },
            {
                "input": "Roaming'i açmak istiyorum",
                "expected_api": "backend_api.enable_roaming",
                "expected_wrapper": "<tool_code>"
            },
            {
                "input": "Arıza kaydı oluşturmak istiyorum",
                "expected_api": "backend_api.create_fault_ticket",
                "expected_wrapper": "<tool_code>"
            }
        ]
        
        correct = 0
        total = len(test_cases)
        
        for i, case in enumerate(test_cases):
            print(f"\n--- Test {i+1}/{total} ---")
            print(f"Input: {case['input']}")
            
            # Clear cache before each test
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Format prompt EXACTLY like training data
            prompt = f"### Instruction:\n{case['input'][:20].title()}\n\n### Input:\n{case['input']}\n\n### Response:\n"
            
            # Tokenize with smaller max length
            inputs = tokenizer(
                prompt, 
                return_tensors="pt", 
                max_length=512,  # Reduced from 1024
                truncation=True,
                padding=False
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda:0") for k, v in inputs.items()}
            
            try:
                # Generate with memory optimization
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=100,  # Increased to get full tool call
                        temperature=0.1,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id,
                        use_cache=False  # Disable cache for memory
                    )
                
                # Decode response
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                response = response.split("### Response:\n")[-1]
                
                print(f"Model Output: {response}")
                print(f"Expected API: {case['expected_api']}")
                
                # Check for both tool wrapper AND correct API
                has_tool_wrapper = case['expected_wrapper'] in response
                has_correct_api = case['expected_api'] in response
                
                print(f"  - Tool Wrapper: {'✅' if has_tool_wrapper else '❌'} ({case['expected_wrapper']})")
                print(f"  - Correct API: {'✅' if has_correct_api else '❌'} ({case['expected_api']})")
                
                if has_tool_wrapper and has_correct_api:
                    print("✅ PERFECT MATCH!")
                    correct += 1
                elif has_correct_api:
                    print("🟡 API CORRECT (wrapper missing)")
                    correct += 0.5  # Partial credit
                else:
                    print("❌ INCORRECT!")
                    
            except Exception as e:
                print(f"⚠️ Generation failed: {e}")
                print("❌ FAILED!")
            
            # Cleanup after each test
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
        
        accuracy = (correct / total) * 100
        print(f"\n📊 **SONUÇLAR:**")
        print(f"Doğru: {correct}/{total}")
        print(f"Doğruluk: {accuracy:.1f}%")
        
        if accuracy >= 80:
            print("🎉 MODEL BAŞARILI! (≥80%)")
        elif accuracy >= 60:
            print("🟡 MODEL KISMEN BAŞARILI (60-80%)")
        else:
            print("❌ Model daha fazla eğitime ihtiyacı var (<60%)")
        
        return accuracy
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.offload_dir):
            shutil.rmtree(self.offload_dir)

def main():
    print("🧪 Fine-tuned Model Test (Memory Optimized)")
    print("=" * 50)
    
    tester = ModelTester()
    
    try:
        model, tokenizer = tester.load_model()
        accuracy = tester.test_scenarios(model, tokenizer)
        
        print(f"\n🎯 Final Score: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Çözüm önerileri:")
        print("1. Diğer uygulamaları kapatın (Chrome, etc.)")
        print("2. GPU memory'i temizleyin")
        print("3. Daha küçük batch size kullanın")
        
    finally:
        # Cleanup
        tester.cleanup()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        print("🧹 Memory cleaned up")

if __name__ == "__main__":
    main() 