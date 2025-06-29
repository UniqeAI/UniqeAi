# Paketlerin kurulumu (Gerekirse çalıştır)
#!pip uninstall -y transformers bitsandbytes accelerate xformers -q
#!pip install -U transformers bitsandbytes accelerate -q

from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

token = "hf_...."  # <--- DEĞİŞTİR

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

login(token)

tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=token)


model = AutoModelForCausalLM.from_pretrained(
    model_id,
    use_auth_token=token
)

device = next(model.parameters()).device
print(f"Model cihazı: {device}")

prompt = "Türkiye'nin başkenti neresidir?"
inputs = tokenizer(prompt, return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}

output = model.generate(**inputs, max_new_tokens=50)

print(tokenizer.decode(output[0], skip_special_tokens=True))