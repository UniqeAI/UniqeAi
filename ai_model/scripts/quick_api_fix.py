#!/usr/bin/env python3
"""
🚀 Quick API Fix - Model'in yanlış öğrendiği API'leri düzeltmek için
================================================================

Bu script eksik senaryoları dataset'e ekleyip kısa bir re-training yapar.
"""

import json
import os

def create_fix_dataset():
    """Create additional training data for confused APIs"""
    
    fix_data = [
        # Hat değiştirme senaryoları -> update_customer_contact
        {
            "instruction": "Update Customer Contact",
            "input": "hattımı değiştirmek istiyorum",
            "output": "<tool_code>print(backend_api.update_customer_contact(user_id=1001, contact_type='phone', new_value='05551234567'))</tool_code>"
        },
        {
            "instruction": "Update Customer Contact", 
            "input": "telefon numaramı değiştirmek istiyorum",
            "output": "<tool_code>print(backend_api.update_customer_contact(user_id=1002, contact_type='phone', new_value='05559876543'))</tool_code>"
        },
        {
            "instruction": "Update Customer Contact",
            "input": "numaramı 5050505050 olarak değiştir",
            "output": "<tool_code>print(backend_api.update_customer_contact(user_id=1003, contact_type='phone', new_value='5050505050'))</tool_code>"
        },
        {
            "instruction": "Update Customer Contact",
            "input": "yeni telefon numaram 5050505050",
            "output": "<tool_code>print(backend_api.update_customer_contact(user_id=1004, contact_type='phone', new_value='5050505050'))</tool_code>"
        },
        
        # Arıza kaydı senaryoları -> create_fault_ticket  
        {
            "instruction": "Create Fault Ticket",
            "input": "arıza kaydı oluşturmak istiyorum",
            "output": "<tool_code>print(backend_api.create_fault_ticket(user_id=2001, issue_description='Arıza kaydı oluşturma talebi'))</tool_code>"
        },
        {
            "instruction": "Create Fault Ticket",
            "input": "teknik arıza bildirmek istiyorum", 
            "output": "<tool_code>print(backend_api.create_fault_ticket(user_id=2002, issue_description='Teknik arıza bildirimi'))</tool_code>"
        },
        {
            "instruction": "Create Fault Ticket",
            "input": "sorun kaydı açmak istiyorum",
            "output": "<tool_code>print(backend_api.create_fault_ticket(user_id=2003, issue_description='Sorun kaydı açma talebi'))</tool_code>"
        },
        
        # Fatura görme senaryoları -> get_current_bill (bu doğru)
        {
            "instruction": "Get Current Bill",
            "input": "faturamı görmek istiyorum",
            "output": "<tool_code>print(backend_api.get_current_bill(user_id=3001))</tool_code>"
        },
        {
            "instruction": "Get Current Bill", 
            "input": "güncel fatura borcumu öğrenmek istiyorum",
            "output": "<tool_code>print(backend_api.get_current_bill(user_id=3002))</tool_code>"
        },
        
        # İnternet hızı testi -> test_internet_speed (bu doğru)
        {
            "instruction": "Test Internet Speed",
            "input": "internetim çok yavaş",
            "output": "<tool_code>print(backend_api.test_internet_speed(user_id=4001))</tool_code>"
        },
        {
            "instruction": "Test Internet Speed",
            "input": "internet hızımı test etmek istiyorum", 
            "output": "<tool_code>print(backend_api.test_internet_speed(user_id=4002))</tool_code>"
        }
    ]
    
    return fix_data

def quick_retrain():
    """Quick retraining with fix data"""
    print("🚀 Quick API Fix başlatılıyor...")
    
    # Load original dataset
    with open("../data/telekom_training_dataset_enhanced.json", 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # Add fix data
    fix_data = create_fix_dataset()
    combined_data = original_data + fix_data
    
    # Save combined dataset
    fix_file = "../data/telekom_training_dataset_fix.json"
    with open(fix_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fix dataset oluşturuldu: {len(fix_data)} yeni örnek eklendi")
    print(f"📁 Dosya: {fix_file}")
    print(f"📊 Toplam: {len(combined_data)} örnek")
    
    # Quick retrain script
    retrain_code = f'''
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import PeftModel, get_peft_model, LoraConfig, TaskType
from datasets import Dataset
import json

# Load model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    device_map="auto",
    torch_dtype=torch.float16
)

# Load existing fine-tuned model
model = PeftModel.from_pretrained(base_model, "./qlora_fine_tuned_model")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
tokenizer.pad_token = tokenizer.eos_token

# Load fix dataset ONLY
with open("{fix_file}", 'r', encoding='utf-8') as f:
    fix_data = json.load(f)[-{len(fix_data)}:]  # Only new examples

# Format data
formatted_data = []
for item in fix_data:
    text = f"### Instruction:\\n{{item['instruction']}}\\n\\n### Input:\\n{{item['input']}}\\n\\n### Response:\\n{{item['output']}}<|endoftext|>"
    formatted_data.append({{"text": text}})

dataset = Dataset.from_list(formatted_data)

# Quick training args
training_args = TrainingArguments(
    output_dir="./qlora_fix_model",
    num_train_epochs=1,  # Sadece 1 epoch
    per_device_train_batch_size=1,
    learning_rate=1e-5,  # Düşük learning rate
    save_steps=999999,   # Don't save intermediate
    logging_steps=5
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)

print("🔥 Quick retraining başlatılıyor...")
trainer.train()
trainer.save_model()
print("✅ Quick fix tamamlandı!")
'''
    
    with open("quick_retrain.py", 'w', encoding='utf-8') as f:
        f.write(retrain_code)
    
    print("📝 Quick retrain script hazırlandı: quick_retrain.py")
    print("\n🎯 Çalıştırmak için:")
    print("   python quick_retrain.py")

if __name__ == "__main__":
    quick_retrain() 