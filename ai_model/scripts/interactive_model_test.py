#!/usr/bin/env python3
"""
🤖 Interaktif Model Test - QLoRA Fine-tuned Llama 3
==================================================

Bu script fine-tuned modelinizle direkt sohbet etmenizi sağlar.
Telekom senaryolarını test edebilir ve model yanıtlarını görebilirsiniz.

Kullanım:
    python interactive_model_test.py
    
Çıkmak için: 'exit' veya 'quit' yazın
"""

import torch
import gc
import warnings
import os
import logging
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

warnings.filterwarnings("ignore")

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

class InteractiveModelTester:
    def __init__(self):
        setup_huggingface_token()
        self.model_path = "./qlora_fine_tuned_model"
        self.base_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load the fine-tuned model with optimizations"""
        print("🤖 Model yükleniyor...")
        print("⏳ Bu birkaç dakika sürebilir...")
        
        try:
            # Quantization config for memory efficiency
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            
            # Load tokenizer
            print("📝 Tokenizer yükleniyor...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model_name,
                trust_remote_code=True
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load base model
            print("🧠 Base model yükleniyor...")
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
                offload_buffers=True  # Memory optimization
            )
            
            # Load fine-tuned adapters
            print("🎯 Fine-tuned adapters yükleniyor...")
            self.model = PeftModel.from_pretrained(
                base_model,
                self.model_path,
                device_map="auto"
            )
            
            print("✅ Model başarıyla yüklendi!")
            print(f"💾 GPU Memory: {torch.cuda.memory_allocated()/1024**3:.1f}GB")
            
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            print("\n🔧 Sorun giderme önerileri:")
            print("1. QLoRA eğitimi tamamlandı mı?")
            print("2. Model dosyaları ./qlora_fine_tuned_model/ klasöründe mi?")
            print("3. GPU memory yeterli mi? (nvidia-smi ile kontrol edin)")
            return False
            
        return True
    
    def generate_response(self, user_input):
        """Generate response from the model"""
        if not self.model or not self.tokenizer:
            return "❌ Model yüklü değil!"
        
        # Clear cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Format prompt like training data
        prompt = f"### Instruction:\n{user_input[:20].title()}\n\n### Input:\n{user_input}\n\n### Response:\n"
        
        try:
            # Tokenize with longer context
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=1024,  # Increased for better context
                truncation=True,
                padding=False
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda:0") for k, v in inputs.items()}
            
            # Generate with optimized parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=80,  # Reduced for cleaner output
                    temperature=0.3,    # Slightly higher for variety
                    top_p=0.9,         # Top-p sampling
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    use_cache=False,
                    repetition_penalty=1.3,  # Higher to prevent repetition
                    no_repeat_ngram_size=3   # Prevent 3-gram repetition
                )
            
            # Decode response
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the model's response part
            if "### Response:\n" in full_response:
                response = full_response.split("### Response:\n")[-1].strip()
            else:
                response = full_response.strip()
            
            # Clean up common artifacts
            response = response.replace("<|endoftext|>", "")
            response = response.split("### Instruction:")[0]  # Stop at next instruction
            response = response.split("### Input:")[0]        # Stop at next input
            response = response.strip()
            
            return response
            
        except Exception as e:
            return f"❌ Yanıt oluşturma hatası: {e}"
    
    def chat_loop(self):
        """Main interactive chat loop"""
        print("\n" + "="*60)
        print("🤖 TelekomAI Fine-tuned Model Test")
        print("="*60)
        print("💬 Telekom ile ilgili sorularınızı sorabilirsiniz!")
        print("📋 Örnek sorular:")
        print("   • Paketimi değiştirmek istiyorum")
        print("   • Faturamı görmek istiyorum") 
        print("   • İnternetim çok yavaş")
        print("   • Roaming'i açmak istiyorum")
        print("   • Arıza kaydı oluşturmak istiyorum")
        print("\n💡 Çıkmak için: 'exit' veya 'quit' yazın")
        print("="*60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 Siz: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'çıkış', 'bye']:
                    print("👋 Görüşürüz!")
                    break
                
                if not user_input:
                    print("⚠️ Lütfen bir soru yazın!")
                    continue
                
                # Generate response
                print("🤖 TelekomAI: ", end="", flush=True)
                response = self.generate_response(user_input)
                print(response)
                
                # Check if it contains tool calls and validate APIs
                if "<tool_code>" in response:
                    print("✅ Model tool çağrısı yaptı!")
                    self.validate_api_calls(response)
                elif "backend_api." in response:
                    print("🟡 API çağrısı var ama format eksik")
                    self.validate_api_calls(response)
                else:
                    print("ℹ️ Normal yanıt (tool çağrısı yok)")
                
            except KeyboardInterrupt:
                print("\n👋 Görüşürüz!")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    def validate_api_calls(self, response):
        """Validate if API calls are correct"""
        # Correct APIs from schema
        correct_apis = [
            "get_customer_package", "get_available_packages", "change_package",
            "get_remaining_quotas", "get_package_details", "enable_roaming",
            "get_current_bill", "get_past_bills", "pay_bill", 
            "get_payment_history", "setup_autopay",
            "check_network_status", "create_fault_ticket", 
            "get_fault_ticket_status", "test_internet_speed",
            "get_customer_profile", "update_customer_contact",
            "suspend_line", "reactivate_line", "check_number_portability"
        ]
        
        found_apis = []
        for api in correct_apis:
            if api in response:
                found_apis.append(api)
        
        if found_apis:
            print(f"📋 Doğru API'ler: {', '.join(found_apis)}")
        else:
            print("⚠️ Tanınmayan API kullanımı tespit edildi")
    
    def cleanup(self):
        """Clean up resources"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

def main():
    """Main function"""
    tester = InteractiveModelTester()
    
    # Load model
    if not tester.load_model():
        return
    
    try:
        # Start chat
        tester.chat_loop()
    finally:
        # Cleanup
        print("🧹 Temizlik yapılıyor...")
        tester.cleanup()

if __name__ == "__main__":
    main() 