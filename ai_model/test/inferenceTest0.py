# Gerekirse pip ile şu paketleri kur
# pip install -U transformers accelerate bitsandbytes huggingface_hub

from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

# Hugging Face erişim token'ını buraya gir
token = ""  # <-- Buraya kendi token'ını yazmalısın

# LLaMA 3.1 Instruct model ID'si (düzgün yazımıyla)
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # 3.1 henüz resmi adlandırmada geçmiyor

# Hugging Face hesabına giriş
login(token)

# Tokenizer'ı indir
tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)

# Modeli indir ve doğru ayarlarla yükle
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",  # Otomatik olarak GPU'ya veya CPU'ya yerleştirir
    token=token
)

# Prompt
prompt = "Türkiye'nin başkenti neresidir?"

# Giriş tokenlarını hazırla
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Modelden çıktı al
output = model.generate(**inputs, max_new_tokens=50)

# Yanıtı yazdır
print(tokenizer.decode(output[0], skip_special_tokens=True))
