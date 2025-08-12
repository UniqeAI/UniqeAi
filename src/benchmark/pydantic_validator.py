from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, Field
import importlib.util
from pathlib import Path


def _load_telekom_schema_funcs():
    """telekom_api_schema'nın validate_response_data ve get_response_model fonksiyonlarını yükler.

    Paket __init__ yan etkilerinden kaçınmak için doğrudan dosya yolundan yüklemeyi dener.
    """
    # 1) Normal import denemesi (eğer paket düzgünse)
    try:
        from ai_model.modular_generator import telekom_api_schema as tmod  # type: ignore

        return tmod.validate_response_data, tmod.get_response_model
    except Exception:
        pass

    # 2) Dosya yolundan yükleme (yan etkileri minimize etmek için)
    repo_root = Path(__file__).resolve().parents[2]
    candidate = repo_root / "ai_model/modular_generator/telekom_api_schema.py"
    if candidate.exists():
        spec = importlib.util.spec_from_file_location("telekom_api_schema_local", str(candidate))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)  # type: ignore[attr-defined]
                return module.validate_response_data, module.get_response_model
            except Exception:
                return None
    return None


class GenericTelecomResponse(BaseModel):
    status: str = Field(..., description="success | error")
    message: str
    recommendations: list[str] = []
    priority_level: Optional[int] = None


def _extract_first_json(text: str) -> Optional[Dict[str, Any]]:
    # Basit ve sağlam bir JSON çıkarımı: ilk { ... } aralığını yakalamaya çalış
    if not isinstance(text, str):
        return None
    try:
        return json.loads(text)
    except Exception:
        pass

    # Heuristic: first balanced braces
    start_idxs = [m.start() for m in re.finditer(r"\{", text)]
    for s in start_idxs:
        depth = 0
        for i in range(s, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    chunk = text[s : i + 1]
                    try:
                        return json.loads(chunk)
                    except Exception:
                        break
    return None


def validate_against_schema(
    model_output_text: str | Dict[str, Any],
    function_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Model çıktısını telekom şeması (varsa function_name ile) ya da generik şema ile doğrula.

    Returns: { valid: bool, errors: list[str], normalized: dict | None }
    """
    errors: list[str] = []
    data: Optional[Dict[str, Any]] = None

    if isinstance(model_output_text, dict):
        data = model_output_text
    else:
        parsed = _extract_first_json(model_output_text)
        if parsed is None:
            errors.append("Çıktıdan JSON parse edilemedi")
            return {"valid": False, "errors": errors, "normalized": None}
        data = parsed

    # Telekom fonksiyonuna göre doğrulama
    if function_name:
        funcs = _load_telekom_schema_funcs()
        if funcs is not None:
            telekom_validate_response_data, _ = funcs
            try:
                telekom_validate_response_data(function_name, data)
                return {"valid": True, "errors": [], "normalized": data}
            except Exception as e:
                errors.append(f"Telekom şema hatası: {e}")
                return {"valid": False, "errors": errors, "normalized": None}

    # Generik doğrulama
    try:
        norm = GenericTelecomResponse(**data)
        return {"valid": True, "errors": [], "normalized": json.loads(norm.model_dump_json())}
    except Exception as e:
        errors.append(f"Generik şema hatası: {e}")
        return {"valid": False, "errors": errors, "normalized": None}


