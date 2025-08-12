#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telekom AI Backend Başlatma Scripti
======================================
4-bit quantization ile Hugging Face modeli kullanır
"""

import os
import sys
import logging
from pathlib import Path

# Project root'u ekle
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Backend'i 4-bit quantization ile başlat"""
    try:
        logger.info("🚀 Telekom AI Backend başlatılıyor...")
        logger.info("🧠 4-bit quantization ile Hugging Face modeli yüklenecek")
        
        # Environment variables
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        reload = os.getenv("RELOAD", "true").lower() == "true"
        
        logger.info(f"📡 Server: http://{host}:{port}")
        logger.info(f"🔄 Hot Reload: {reload}")
        logger.info(f"🎯 Swagger UI: http://{host}:{port}/docs")
        logger.info(f"🩺 Health Check: http://{host}:{port}/api/v1/health")
        logger.info(f"🤖 Chat API: http://{host}:{port}/api/v1/chat/")
        
        # Model bilgileri
        logger.info("📋 Model Konfigürasyonu:")
        logger.info("   - Model: Choyrens/ChoyrensAI-Telekom-Agent-v1-merged")
        logger.info("   - Quantization: 4-bit BitsAndBytesConfig")
        logger.info("   - Compute Type: bfloat16")
        logger.info("   - Tool Calling: Enabled")
        
        # Uvicorn ile başlat
        uvicorn.run(
            "backend.app.main:app",
            host=host,
            port=port,
            reload=reload,
            reload_dirs=[str(PROJECT_ROOT / "backend")],
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Backend kullanıcı tarafından durduruldu.")
    except Exception as e:
        logger.error(f"❌ Backend başlatma hatası: {e}")
        logger.error("💡 Sorun giderme için README_HUGGINGFACE_INTEGRATION.md dosyasını kontrol edin")
        sys.exit(1)

if __name__ == "__main__":
    main() 