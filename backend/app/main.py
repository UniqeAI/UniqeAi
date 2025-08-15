from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import asyncio
import logging
from pathlib import Path

app = FastAPI(
    title="UniqueAi Backend",
    description="UniqueAi projesi için API'leri ve AI modelini sunan servis.",
    version="1.0.0",
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health", tags=["Monitoring"])
def health_check():
    """
    Servisin ayakta olup olmadığını kontrol eden endpoint.
    """
    return {
        "status": "ok",
        "ai_model_type": settings.AI_MODEL_TYPE,
        "backend_version": "1.0.0"
    }

@app.get("/", tags=["Monitoring"])
def root():
    return {"status":"ok"}

# favicon.ico isteğini sessizce yut (dosya olmadan)
@app.get("/favicon.ico")
def ignore_favicon():
    return Response(status_code=204)  # No Content

# Chat router'ını dahil et
from app.api.v1 import chat
app.include_router(chat.router, prefix="/api/v1")

# Mock test router'ı kaldırıldı - artık gerekli değil

# Telekom API router'ını dahil et
from app.api.v1 import telekom
app.include_router(telekom.router, prefix="/api/v1")

# User router'ını dahil et
from app.api.v1 import user
app.include_router(user.router, prefix="/api/v1")

# Feedback router'ını dahil et
from app.api.v1 import feedback
app.include_router(feedback.router, prefix="/api/v1")

# AI Model bilgisi endpoint'i
@app.get("/api/v1/ai/model-info", tags=["AI"])
def get_ai_model_info():
    """
    AI model bilgilerini döndür
    """
    return {
        "model_type": settings.AI_MODEL_TYPE,
        "model_name": settings.HUGGING_FACE_MODEL_NAME if settings.is_real_ai_mode() else "Mock AI Model",
        "is_mock_mode": settings.is_mock_mode(),
        "is_real_ai_mode": settings.is_real_ai_mode()
    }

# Gelecekte eklenecek diğer endpoint'ler için router'lar buraya dahil edilecek. 

# Startup event - v6 model kontrolü
@app.on_event("startup")
async def startup_event():
    """
    Uygulama başlatıldığında v6 modelini kontrol et ve gerekirse indir
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Backend başlatılıyor...")
        logger.info("🔍 v6 model kontrol ediliyor...")
        
        # Yerel model dosyasını kontrol et
        local_model_path = Path("models/ChoyrensAi-8b-q8_0.gguf")
        
        if not local_model_path.exists():
            # Alternatif olarak models klasöründeki GGUF dosyalarını ara
            models_dir = Path("models")
            if models_dir.exists():
                gguf_files = list(models_dir.glob("*.gguf"))
                if gguf_files:
                    local_model_path = gguf_files[0]
                    logger.info(f"✅ Model bulundu: {local_model_path.name}")
                else:
                    logger.warning("⚠️  GGUF model bulunamadı!")
                    logger.info("💡 Model dosyasını models/ klasörüne koyun")
                    return
            else:
                logger.warning("⚠️  models/ klasörü bulunamadı!")
                return
        
        if local_model_path.exists():
            model_size = local_model_path.stat().st_size / (1024**3)
            logger.info(f"✅ Yerel model mevcut: {local_model_path.name} ({model_size:.2f} GB)")
            logger.info("🎯 Yerel model kullanıma hazır!")
            
    except Exception as e:
        logger.error(f"❌ Startup hatası: {e}")

def download_v6_model_normal():
    """
    v6 modelini normal şekilde indir (blocking)
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("📥 v6 model normal şekilde indiriliyor...")
        
        # Hugging Face'den modeli indir
        from huggingface_hub import hf_hub_download
        
        repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
        filename = "ChoyrensAi-8b-q5_k_m.gguf"
        
        # İndirme dizini
        download_dir = Path("models/v6_model")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 İndirme dizini: {download_dir.absolute()}")
        
        # Modeli indir (normal blocking)
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=download_dir
        )
        
        model_size = Path(model_path).stat().st_size / (1024**3)
        logger.info(f"✅ v6 model başarıyla indirildi! ({model_size:.2f} GB)")
        logger.info(f"📍 Konum: {model_path}")
        logger.info("🎯 v6 model hazır! Backend kullanıma hazır.")
        
    except Exception as e:
        logger.error(f"❌ Model indirme hatası: {e}")
        logger.warning("⚠️  v5 model ile devam ediliyor...")

def download_v6_model_background():
    """
    v6 modelini arka planda indir (blocking olmayan) - artık kullanılmıyor
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("📥 v6 model arka planda indiriliyor...")
        
        # Hugging Face'den modeli indir
        from huggingface_hub import hf_hub_download
        
        repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
        filename = "ChoyrensAi-8b-q5_k_m.gguf"
        
        # İndirme dizini
        download_dir = Path("models/v6_model")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 İndirme dizini: {download_dir.absolute()}")
        
        # Modeli indir
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=download_dir
        )
        
        model_size = Path(model_path).stat().st_size / (1024**3)
        logger.info(f"✅ v6 model başarıyla indirildi! ({model_size:.2f} GB)")
        logger.info(f"📍 Konum: {model_path}")
        logger.info("🔄 Backend'i yeniden başlatmanız önerilir!")
        
    except Exception as e:
        logger.error(f"❌ Model indirme hatası: {e}")
        logger.warning("⚠️  v5 model ile devam ediliyor...")

async def download_v6_model_async():
    """
    v6 modelini asenkron olarak indir (eski fonksiyon - artık kullanılmıyor)
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("📥 v6 model indiriliyor...")
        
        # Hugging Face'den modeli indir
        from huggingface_hub import hf_hub_download
        
        repo_id = "Choyrens/ChoyrensAI-Telekom-Agent-v6-gguf"
        filename = "ChoyrensAi-8b-q5_k_m.gguf"
        
        # İndirme dizini
        download_dir = Path("models/v6_model")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 İndirme dizini: {download_dir.absolute()}")
        
        # Modeli indir (asenkron olmayan işlemi thread pool'da çalıştır)
        import concurrent.futures
        
        def download_model():
            return hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                local_dir=download_dir
            )
        
        # Thread pool'da indirme işlemini çalıştır
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(download_model)
            model_path = future.result()
        
        model_size = Path(model_path).stat().st_size / (1024**3)
        logger.info(f"✅ v6 model başarıyla indirildi! ({model_size:.2f} GB)")
        logger.info(f"📍 Konum: {model_path}")
        
    except Exception as e:
        logger.error(f"❌ Model indirme hatası: {e}")
        logger.warning("⚠️  v5 model ile devam ediliyor...") 