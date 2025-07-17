# -*- coding: utf-8 -*-
"""
🚀 İnteraktif Çıkarım (Sohbet) Script'i (Interactive Inference Script)
=====================================================================

Bu script, birleştirilmiş (merged) model ile interaktif bir sohbet oturumu
başlatmak için kullanılır. Bu, modelin niteliksel (qualitative) olarak
değerlendirilmesi, davranışlarının anlaşılması ve zayıf noktalarının
tespit edilmesi için kritik bir araçtır.

"eval_loss" gibi metrikler matematiksel performansı gösterirken, bu script
modelin "ruhunu" ve gerçek dünyadaki muhakeme yeteneğini anlamamızı sağlar.

Nasıl Çalışır?
- Birleştirilmiş modeli ve tokenizer'ı yükler.
- Terminalde bir sohbet döngüsü başlatır.
- Llama-3'ün sohbet formatına uygun şekilde geçmişi yönetir.
- Modelin metin ve araç çağırma (tool call) yanıtlarını ayrıştırıp
  anlaşılır bir şekilde gösterir.
"""

import os
import torch
import logging
import json
from pathlib import Path
from dataclasses import dataclass, field
from transformers import AutoModelForCausalLM, AutoTokenizer, HfArgumentParser, BitsAndBytesConfig

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Proje Kök Dizini Tanımlaması ---
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# --- Yapılandırma ---
@dataclass
class ChatConfig:
    """
    Sohbet arayüzü için yapılandırma parametreleri.
    """
    model_path: str = field(
        default="UniqeAi/ai_model/merged_model_v3",
        metadata={"help": "Kullanılacak birleştirilmiş modelin proje kökünden göreli yolu."}
    )
    # Çıkarım sırasında daha iyi performans için quantize edebiliriz
    load_in_4bit: bool = field(default=True, metadata={"help": "Modeli 4-bit olarak yükle (VRAM'i azaltır)."})
    max_new_tokens: int = field(default=1024, metadata={"help": "Modelin tek seferde üreteceği maksimum token sayısı."})
    temperature: float = field(default=0.6, metadata={"help": "Üretimdeki rastgelelik. Daha düşük değerler daha deterministik sonuçlar verir."})
    top_p: float = field(default=0.9, metadata={"help": "Nucleus sampling. Olasılıkları kümülatif olarak %p'yi aşan token'ları filtreler."})


class Chatbot:
    """
    Modeli yükleyen ve interaktif sohbet oturumunu yöneten ana sınıf.
    """
    def __init__(self, config: ChatConfig):
        self.config = config
        self.model_full_path = str(PROJECT_ROOT / self.config.model_path)
        logger.info(f"Sohbet botu başlatılıyor. Model yolu: {self.model_full_path}")

        quantization_config = None
        if self.config.load_in_4bit:
            logger.info("4-bit quantization etkinleştirildi.")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
        
        # 1. Tokenizer ve Birleştirilmiş Modeli Yükle
        logger.info("Tokenizer yükleniyor...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_full_path)
        
        logger.info("Model yükleniyor... Bu işlem VRAM'inize bağlı olarak zaman alabilir.")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_full_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            quantization_config=quantization_config,
        )
        self.model.eval() # Modeli değerlendirme moduna al

        self.history = []
        logger.info("✅ Model ve tokenizer başarıyla yüklendi. Sohbet başlayabilir.")

    def _parse_assistant_response(self, response_text: str) -> dict:
        """
        Modelin ham metin çıktısını, içerik (content) ve araç çağrıları (tool_calls)
        içeren yapısal bir sözlüğe dönüştürür.
        """
        # Llama 3'ün özel token'larını kullanarak yanıtı parçalara ayır
        content_part_raw = response_text
        tool_calls_part_raw = None

        if "<|start_header_id|>tool_calls<|end_header_id|>" in response_text:
            parts = response_text.split("<|start_header_id|>tool_calls<|end_header_id|>", 1)
            content_part_raw = parts[0]
            tool_calls_part_raw = parts[1]

        # İçerik kısmını temizle
        content = content_part_raw.strip()
        if content.endswith("<|eot_id|>"):
            content = content[:-len("<|eot_id|>")].strip()
        
        # Araç çağırma kısmını temizle ve JSON olarak ayrıştır
        tool_calls = None
        if tool_calls_part_raw:
            tool_calls_str = tool_calls_part_raw.strip()
            if tool_calls_str.endswith("<|eot_id|>"):
                tool_calls_str = tool_calls_str[:-len("<|eot_id|>")].strip()
            
            try:
                # Modelin ürettiği string bir JSON listesi olmalı
                tool_calls = json.loads(tool_calls_str)
            except json.JSONDecodeError:
                logger.error("Modelin araç çağırma çıktısı JSON formatında değil: %s", tool_calls_str)
                content += f"\n\n[HATA: Geçersiz araç çağrısı formatı: {tool_calls_str}]"
        
        return {
            "role": "assistant",
            "content": content if content else None,
            "tool_calls": tool_calls
        }

    def run(self):
        """
        Ana sohbet döngüsünü başlatır.
        """
        print("\n--- Uzman Model Sohbet Arayüzü ---")
        print("Model ile sohbete başlayın.")
        print("Geçmişi temizlemek için 'temizle', çıkmak için 'çıkış' yazın.")
        print("-" * 35)

        while True:
            try:
                user_input = input("👤 Siz: ")
                if user_input.lower() in ["çıkış", "cikis", "exit", "quit"]:
                    print("Görüşmek üzere!")
                    break
                if user_input.lower() in ["temizle", "clear"]:
                    self.history = []
                    print("\n✨ Sohbet geçmişi temizlendi.\n")
                    continue

                # 1. Kullanıcı mesajını geçmişe ekle
                self.history.append({"role": "user", "content": user_input})

                # 2. Sohbet geçmişini modele uygun formata çevir ve token'laştır
                input_ids = self.tokenizer.apply_chat_template(
                    self.history,
                    add_generation_prompt=True,
                    return_tensors="pt"
                ).to(self.model.device)

                # 3. Modelden yanıt üret
                print("🤖 Model düşünüyor...", end="\r")
                with torch.no_grad():
                    outputs = self.model.generate(
                        input_ids,
                        max_new_tokens=self.config.max_new_tokens,
                        eos_token_id=self.tokenizer.eos_token_id,
                        do_sample=True,
                        temperature=self.config.temperature,
                        top_p=self.config.top_p,
                    )
                
                # Sadece üretilen yeni token'ları al
                response_ids = outputs[0][input_ids.shape[-1]:]
                assistant_response_raw = self.tokenizer.decode(response_ids, skip_special_tokens=False)
                
                # 4. Model yanıtını ayrıştır ve geçmişe ekle
                assistant_message = self._parse_assistant_response(assistant_response_raw)
                self.history.append(assistant_message)
                
                # 5. Yanıtı kullanıcıya göster
                print("🤖 Model: ", end="", flush=True)
                if assistant_message["content"]:
                    print(assistant_message["content"])

                if assistant_message["tool_calls"]:
                    print("\n--- 🛠️ Araç Çağrısı Algılandı ---")
                    for tool_call in assistant_message["tool_calls"]:
                        func_name = tool_call.get("function", {}).get("name")
                        func_args = tool_call.get("function", {}).get("arguments")
                        print(f"  📞 Fonksiyon: {func_name}")
                        # Argümanları daha okunaklı göstermek için JSON olarak formatla
                        try:
                            args_dict = json.loads(func_args)
                            pretty_args = json.dumps(args_dict, indent=2, ensure_ascii=False)
                            print(f"  📋 Parametreler:\n{pretty_args}")
                        except:
                             print(f"  📋 Parametreler (raw): {func_args}")
                    print("---------------------------------")
                print()


            except KeyboardInterrupt:
                print("\nÇıkış yapılıyor...")
                break
            except Exception as e:
                logger.error(f"Sohbet sırasında bir hata oluştu: {e}", exc_info=True)
                break

def main():
    parser = HfArgumentParser((ChatConfig,))
    config, = parser.parse_args_into_dataclasses()

    try:
        chatbot = Chatbot(config)
        chatbot.run()
    except Exception as e:
        logger.error(f"Sohbet botu başlatılırken bir hata oluştu: {e}", exc_info=True)

if __name__ == "__main__":
    main() 