from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict, Optional


EVAL_PROMPT = (
    "Aşağıda telekom domain'inde bir soru, beklenen yanıt ve model yanıtı var. "
    "Görevin: (1) Doğruluk ve faydalılık; (2) Telekom operasyonlarına uygunluk; "
    "(3) Güvenlik/uygun olmayan öneriler; (4) Şema uyumu (eğer JSON ise) açısından değerlendir. "
    "0.0 ile 1.0 arasında bir puan ver. JSON olarak dön: {\"score\": float, \"reasons\": str}.\n\n"
    "Soru: {input}\nBeklenen: {expected}\nModel: {prediction}\n"
)


async def llm_grade_openai(
    input_text: str,
    expected: str,
    prediction: str,
    model: str = "gpt-4o-mini",
    api_key_env: str = "OPENAI_API_KEY",
    timeout: int = 60,
    max_retries: int = 3,
) -> Dict[str, Any]:
    from openai import AsyncOpenAI  # OpenAI backend destekli fakat varsayılan değil

    api_key = os.getenv(api_key_env)
    if not api_key:
        return {"score": 0.0, "reasons": f"Missing API key env: {api_key_env}"}

    prompt = EVAL_PROMPT.format(input=input_text, expected=expected, prediction=prediction)
    client = AsyncOpenAI(api_key=api_key)
    last_error: Optional[str] = None
    for attempt in range(max_retries):
        try:
            resp = await asyncio.wait_for(
                client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=256,
                ),
                timeout=timeout,
            )
            text = resp.choices[0].message.content or ""
            try:
                data = json.loads(text)
                score = float(data.get("score", 0.0))
                reasons = str(data.get("reasons", ""))
                score = max(0.0, min(1.0, score))
                return {"score": score, "reasons": reasons}
            except Exception:
                return {"score": 0.0, "reasons": f"Invalid JSON from evaluator: {text[:200]}"}
        except Exception as e:
            last_error = str(e)
            await asyncio.sleep(min(2 ** attempt, 8))
    return {"score": 0.0, "reasons": last_error or "evaluator error"}


async def llm_grade_hf(
    input_text: str,
    expected: str,
    prediction: str,
    model: str = "Qwen/Qwen2-7B-Instruct",
    api_key_env: str = "HF_API_TOKEN",
    timeout: int = 60,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Hugging Face Inference API üzerinden değerlendirme yapar.

    Modelden {"score": float, "reasons": str} formatında JSON beklenir.
    """
    import os
    import requests

    token = os.getenv(api_key_env)
    if not token:
        return {"score": 0.0, "reasons": f"Missing API key env: {api_key_env}"}

    prompt = EVAL_PROMPT.format(input=input_text, expected=expected, prediction=prediction)
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0, "max_new_tokens": 256},
        "options": {"wait_for_model": True},
    }

    last_error: Optional[str] = None
    for attempt in range(max_retries):
        try:
            def _post():
                return requests.post(url, headers=headers, json=payload, timeout=timeout)

            resp = await asyncio.to_thread(_post)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
                    text = data[0]["generated_text"]
                else:
                    text = str(data)
                try:
                    parsed = json.loads(text)
                    score = float(parsed.get("score", 0.0))
                    reasons = str(parsed.get("reasons", ""))
                    score = max(0.0, min(1.0, score))
                    return {"score": score, "reasons": reasons}
                except Exception:
                    return {"score": 0.0, "reasons": f"Invalid JSON from evaluator: {text[:200]}"}
            last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_error = str(e)
        await asyncio.sleep(min(2 ** attempt, 8))
    return {"score": 0.0, "reasons": last_error or "evaluator error"}

async def llm_grade_mock(
    input_text: str, expected: str, prediction: str, **_: Any
) -> Dict[str, Any]:
    # Basit benzerlik heuristiği ile hızlı/ucuz mock skor
    score = 1.0 if expected.strip() == prediction.strip() else 0.5
    return {"score": score, "reasons": "mock-eval"}


