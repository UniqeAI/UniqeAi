import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig
)
from peft import LoraConfig
from trl import SFTTrainer

def main():
    # 1. Model ve Tokenizer'ı Yükleme
    model_name = "meta-llama/Llama-3.1-8B-Instruct"
    print(f"Loading model: {model_name}")
    
    # Not: Eğer GPU belleği kısıtlıysa 4-bit kuantizasyon kullanılabilir.
    # bnb_config = BitsAndBytesConfig(...)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Llama 3'ün pad token'ı yok, genellikle eos_token kullanılır.
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        # quantization_config=bnb_config, # Kuantizasyon gerekirse aktif et
        device_map="auto", # Modeli uygun cihaza (GPU/CPU) otomatik yükler
    )
    print("Model and tokenizer loaded.")

    # 2. Veri Setini Yükleme
    # `ai_model/data/synthetic_data.jsonl` dosyasını yükleyeceğiz.
    print("Loading dataset...")
    # dataset = load_dataset("json", data_files="path/to/your/synthetic_data.jsonl", split="train")
    # print(f"Dataset loaded with {len(dataset)} examples.")

    # 3. LoRA/PEFT Konfigürasyonu
    # Sadece belirli katmanları eğiterek fine-tuning'i hızlandırır ve bellek kullanımını azaltır.
    lora_config = LoraConfig(
        r=8,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    print("LoRA config created.")

    # 4. Eğitim Argümanları
    # Fine-tuning sürecini kontrol eden hiper-parametreler.
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        # Diğer önemli parametreler buraya eklenebilir.
    )
    print("Training arguments set.")

    # 5. SFTTrainer'ı (Supervised Fine-tuning Trainer) Oluşturma
    # trainer = SFTTrainer(
    #     model=model,
    #     train_dataset=dataset,
    #     peft_config=lora_config,
    #     dataset_text_field="text", # Veri setinizdeki metin sütununun adı
    #     tokenizer=tokenizer,
    #     args=training_args,
    #     max_seq_length=1024, # Modelin işleyebileceği maksimum token sayısı
    # )

    # 6. Eğitimi Başlatma
    # print("Starting training...")
    # trainer.train()
    # print("Training finished.")

    # 7. Modeli Kaydetme
    # print("Saving model...")
    # trainer.save_model("./fine-tuned-model")
    # print("Model saved.")

if __name__ == "__main__":
    # main() # Gerçek eğitim için bu satırın yorumunu kaldırın.
    print("AI fine-tuning script scaffold is ready.")
    print("Fill in the dataset path and uncomment the calls to run.") 