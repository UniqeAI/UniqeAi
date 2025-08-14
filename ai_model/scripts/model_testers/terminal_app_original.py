# -*- coding: utf-8 -*-
"""
🚀 Telekom AI Agent Terminal Uygulaması - Arkadaş Paylaşım Versiyonu
================================================================

Bu uygulama, eğitilmiş Telekom müşteri hizmetleri AI modelini
terminal üzerinden kolayca test etmenizi sağlar.

Özellikler:
- 🔄 Otomatik model indirme (Hugging Face Hub'dan)
- 🎯 Gerçek zamanlı yanıt akışı
- 🛠️ Tool-calling desteği
- 💡 Dinamik bağlam yönetimi
- 🔍 Hata ayıklama modu

Gereksinimler:
- NVIDIA GPU (CUDA desteği)
- Python 3.8+
- Yeterli RAM (8GB+ önerilir)
"""

import os
import sys
import json
import re
import uuid
import torch
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import argparse

# UI ve etkileşim için
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("❌ Rich kütüphanesi bulunamadı. Lütfen 'pip install rich' çalıştırın.")
    sys.exit(1)

# AI model kütüphaneleri
try:
    from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer,
        BitsAndBytesConfig,
        TextStreamer
    )
    from huggingface_hub import snapshot_download, HfApi
except ImportError:
    print("❌ Transformers veya huggingface_hub bulunamadı. Lütfen requirements.txt'i kurun.")
    sys.exit(1)

# Tool tanımları için yerel import
try:
    from tool_definitions import get_tool_definitions, get_tool_response
except ImportError:
    print("⚠️ tool_definitions.py bulunamadı. Araç işlevselliği devre dışı olacak.")
    get_tool_definitions = lambda: []
    get_tool_response = lambda name, args: f"Araç '{name}' bulunamadı."

console = Console()

@dataclass
class AppConfig:
    """Uygulama yapılandırması"""
    model_name: str = "Choyrens/ChoyrensAI-Telekom-Agent-v1-merged"
    local_model_dir: str = "./models/telekom-agent"
    max_conversation_length: int = 6  # Son N diyalog çiftini tutar
    max_new_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    debug_mode: bool = False
    streaming: bool = True

class ModelManager:
    """Model indirme ve yönetim sınıfı"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.model_path = Path(config.local_model_dir)
        
    def ensure_model_available(self) -> bool:
        """Model varsa True, yoksa indir ve True döndür"""
        if self.model_path.exists() and any(self.model_path.iterdir()):
            console.print(f"✅ Model zaten mevcut: {self.model_path}")
            return True
            
        return self._download_model()
    
    def _download_model(self) -> bool:
        """Modeli Hugging Face Hub'dan indir"""
        try:
            console.print(f"📥 Model indiriliyor: {self.config.model_name}")
            console.print("   Bu işlem internet hızınıza bağlı olarak birkaç dakika sürebilir...")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Model indiriliyor...", total=None)
                
                # Model dosyalarını indir
                snapshot_download(
                    repo_id=self.config.model_name,
                    local_dir=self.model_path,
                    local_dir_use_symlinks=False  # Windows uyumluluğu için
                )
                
                progress.update(task, description="✅ İndirme tamamlandı!")
            
            console.print(f"✅ Model başarıyla indirildi: {self.model_path}")
            return True
            
        except Exception as e:
            console.print(f"❌ Model indirme hatası: {e}")
            if "authentication" in str(e).lower():
                console.print("💡 İpucu: Hugging Face token'ınızı kontrol edin.")
            return False

class ChatSession:
    """Sohbet oturumu yönetimi"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.conversation_history: List[Dict[str, str]] = []
        self.tools = get_tool_definitions()
        
    def add_message(self, role: str, content: str):
        """Konuşma geçmişine mesaj ekle"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Uzun konuşmaları kısalt
        if len(self.conversation_history) > self.config.max_conversation_length * 2:
            # İlk sistem mesajını koru, ortadakileri sil
            self.conversation_history = (
                self.conversation_history[:1] + 
                self.conversation_history[-(self.config.max_conversation_length * 2 - 1):]
            )
    
    def get_chat_context(self) -> List[Dict[str, str]]:
        """Mevcut sohbet bağlamını döndür"""
        # Sistem mesajıyla başla
        context = [{
            "role": "system",
            "content": (
                "Sen Türk Telekom müşteri hizmetleri asistanısın. "
                "Müşterilere yardım etmek için çeşitli araçları kullanabilirsin. "
                "Her zaman kibar, yardımsever ve çözüm odaklı ol. "
                "Eğer bir araç kullanman gerekiyorsa, uygun aracı çağır ve sonucunu müşteriye açıkla."
            )
        }]
        
        # Konuşma geçmişini ekle
        for msg in self.conversation_history:
            if msg["role"] in ["user", "assistant"]:
                context.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        return context

class ToolCallParser:
    """Araç çağrılarını ayrıştırma sınıfı"""
    
    @staticmethod
    def extract_tool_calls(text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Model çıktısından araç çağrılarını çıkart
        Format: <|begin_of_tool_code|>print(function_name(param="value"))<|end_of_tool_code|>
        """
        pattern = r"<\|begin_of_tool_code\|>(.*?)<\|end_of_tool_code\|>"
        matches = re.findall(pattern, text, re.DOTALL)
        
        if not matches:
            return None
        
        tool_calls = []
        for match in matches:
            tool_code = match.strip()
            
            # print(function_name(args)) formatını yakala
            func_pattern = r"print\((\w+)\((.*)\)\)"
            func_match = re.search(func_pattern, tool_code)
            
            if func_match:
                function_name = func_match.group(1)
                args_str = func_match.group(2)
                
                # Parametreleri ayrıştır
                params = ToolCallParser._parse_arguments(args_str)
                
                tool_calls.append({
                    "id": f"call_{uuid.uuid4().hex[:8]}",
                    "function": function_name,
                    "arguments": params
                })
        
        return tool_calls if tool_calls else None
    
    @staticmethod
    def _parse_arguments(args_str: str) -> Dict[str, Any]:
        """Fonksiyon argümanlarını ayrıştır"""
        if not args_str.strip():
            return {}
        
        params = {}
        
        # key="value" veya key=value formatını yakala
        arg_pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\"|([^,\)]+))'
        matches = re.findall(arg_pattern, args_str)
        
        for match in matches:
            key = match[0]
            value = match[1] or match[2] or match[3]
            
            # Tip dönüşümü
            if value.lower() in ['true', 'false']:
                params[key] = value.lower() == 'true'
            elif value.isdigit():
                params[key] = int(value)
            elif value.replace('.', '').isdigit():
                params[key] = float(value)
            else:
                params[key] = value
        
        return params

class TelekomAITerminal:
    """Ana terminal uygulaması"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.model_manager = ModelManager(config)
        self.chat_session = ChatSession(config)
        self.model = None
        self.tokenizer = None
        
    def initialize(self) -> bool:
        """Uygulamayı başlat"""
        console.print("🤖 Telekom AI Agent Terminal'e Hoş Geldiniz!")
        console.print("=" * 60)
        
        # Model varlığını kontrol et
        if not self.model_manager.ensure_model_available():
            return False
        
        # Modeli yükle
        return self._load_model()
    
    def _load_model(self) -> bool:
        """AI modelini belleğe yükle"""
        try:
            console.print("🔄 Model yükleniyor...")
            
            # GPU kontrolü
            if not torch.cuda.is_available():
                console.print("⚠️ CUDA bulunamadı. CPU modu kullanılacak (yavaş olabilir).")
                device_map = "cpu"
                quantization_config = None
            else:
                console.print(f"✅ GPU tespit edildi: {torch.cuda.get_device_name()}")
                device_map = "auto"
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_use_double_quant=True,
                )
            
            # Tokenizer yükle
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_manager.model_path,
                trust_remote_code=True
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Model yükle
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_manager.model_path,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                trust_remote_code=True
            )
            
            console.print("✅ Model başarıyla yüklendi!")
            return True
            
        except Exception as e:
            console.print(f"❌ Model yükleme hatası: {e}")
            return False
    
    def _generate_response(self, user_input: str) -> str:
        """Kullanıcı girdisi için yanıt üret"""
        # Bağlamı hazırla
        self.chat_session.add_message("user", user_input)
        context = self.chat_session.get_chat_context()
        
        if self.config.debug_mode:
            console.print("🔍 Debug - Gönderilen bağlam:")
            for msg in context:
                console.print(f"  {msg['role']}: {msg['content'][:100]}...")
        
        # Tokenize et
        chat_template = self.tokenizer.apply_chat_template(
            context,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(
            chat_template,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.model.device)
        
        # Terminasyon tokenları
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        
        # Yanıt üret
        if self.config.streaming:
            streamer = TextStreamer(
                self.tokenizer,
                skip_prompt=True,
                skip_special_tokens=True
            )
        else:
            streamer = None
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                eos_token_id=terminators,
                do_sample=True,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                pad_token_id=self.tokenizer.eos_token_id,
                streamer=streamer
            )
        
        # Yanıtı decode et
        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1]:],
            skip_special_tokens=True
        )
        
        return response.strip()
    
    def _handle_tool_calls(self, response: str) -> str:
        """Araç çağrılarını işle ve nihai yanıtı döndür"""
        tool_calls = ToolCallParser.extract_tool_calls(response)
        
        if not tool_calls:
            return response
        
        console.print("\n🛠️ Araç çağrıları tespit edildi:")
        
        # Her araç çağrısını işle
        tool_results = []
        for call in tool_calls:
            func_name = call["function"]
            args = call["arguments"]
            
            console.print(f"  📞 {func_name}({', '.join(f'{k}={v}' for k, v in args.items())})")
            
            # Aracı çalıştır
            result = get_tool_response(func_name, args)
            tool_results.append(f"🔧 {func_name}: {result}")
            
            console.print(f"    ✅ Sonuç: {result}")
        
        # Araç sonuçlarını bağlama ekle ve özet iste
        tool_summary = "\n".join(tool_results)
        summary_prompt = f"""
Yukarıdaki araç çağrılarının sonuçlarına dayanarak, müşteriye net ve anlaşılır bir yanıt ver:

Araç Sonuçları:
{tool_summary}

Lütfen bu bilgileri kullanarak müşterinin sorusunu yanıtla:
"""
        
        return self._generate_response(summary_prompt)
    
    def run(self):
        """Ana uygulama döngüsü"""
        if not self.initialize():
            console.print("❌ Uygulama başlatılamadı.")
            return
        
        # Kullanım talimatları
        console.print("\n📋 Kullanım Talimatları:")
        console.print("  • Herhangi bir soru sorun")
        console.print("  • 'debug' yazarak hata ayıklama modunu açın/kapatın")
        console.print("  • 'clear' yazarak konuşma geçmişini temizleyin")
        console.print("  • 'quit' veya Ctrl+C ile çıkın")
        console.print("=" * 60)
        
        try:
            while True:
                # Kullanıcı girdisi al
                user_input = Prompt.ask("\n[bold blue]Siz")
                
                if not user_input.strip():
                    continue
                
                # Özel komutlar
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'debug':
                    self.config.debug_mode = not self.config.debug_mode
                    console.print(f"🔍 Debug modu: {'AÇIK' if self.config.debug_mode else 'KAPALI'}")
                    continue
                elif user_input.lower() == 'clear':
                    self.chat_session.conversation_history.clear()
                    console.print("🗑️ Konuşma geçmişi temizlendi.")
                    continue
                
                # AI yanıtı üret
                console.print("\n[bold green]🤖 Asistan:[/bold green]", end=" ")
                
                if not self.config.streaming:
                    console.print("Düşünüyor...")
                
                try:
                    response = self._generate_response(user_input)
                    
                    # Araç çağrıları varsa işle
                    if "<|begin_of_tool_code|>" in response:
                        final_response = self._handle_tool_calls(response)
                        
                        if not self.config.streaming:
                            console.print(final_response)
                        
                        self.chat_session.add_message("assistant", final_response)
                    else:
                        if not self.config.streaming:
                            console.print(response)
                        
                        self.chat_session.add_message("assistant", response)
                
                except KeyboardInterrupt:
                    console.print("\n⏹️ Yanıt oluşturma durduruldu.")
                except Exception as e:
                    console.print(f"\n❌ Hata: {e}")
                    if self.config.debug_mode:
                        import traceback
                        console.print(traceback.format_exc())
        
        except KeyboardInterrupt:
            pass
        
        console.print("\n👋 Görüşmek üzere!")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description="Telekom AI Agent Terminal")
    parser.add_argument("--model", default="Choyrens/ChoyrensAI-Telekom-Agent-v1-merged", 
                       help="Model repository adı")
    parser.add_argument("--debug", action="store_true", help="Debug modunda başlat")
    parser.add_argument("--no-streaming", action="store_true", help="Streaming'i devre dışı bırak")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Maksimum token sayısı")
    
    args = parser.parse_args()
    
    # Konfigürasyon oluştur
    config = AppConfig(
        model_name=args.model,
        debug_mode=args.debug,
        streaming=not args.no_streaming,
        max_new_tokens=args.max_tokens
    )
    
    # Terminal uygulamasını başlat
    app = TelekomAITerminal(config)
    app.run()

if __name__ == "__main__":
    main() 