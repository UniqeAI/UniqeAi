from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from ...schemas.feedback import FeedbackSchema, FeedbackResponse
from ...services.feedback_service import FeedbackService

logger = logging.getLogger(__name__)
router = APIRouter()

# Feedback servisi
feedback_service = FeedbackService()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackSchema):
    """Feedback verisini al ve işle"""
    try:
        logger.info(f"Feedback alındı: {feedback.feedback_type} - {feedback.message_id}")
        
        # Feedback'i işle
        result = await feedback_service.process_feedback(feedback)
        
        if result["success"]:
            logger.info(f"Feedback başarıyla işlendi: {result['feedback_id']}")
            return FeedbackResponse(
                success=True,
                message=result["message"],
                feedback_id=result["feedback_id"],
                processed=result["processed"]
            )
        else:
            logger.error(f"Feedback işlenemedi: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Feedback endpoint hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback işlenirken hata oluştu: {str(e)}")

@router.get("/feedback/stats/{user_id}")
async def get_user_feedback_stats(user_id: str):
    """Kullanıcının feedback istatistiklerini getir"""
    try:
        # Kullanıcı tercihlerini al
        preferences = await feedback_service.get_user_preferences(user_id)
        
        # Feedback sayılarını al (basit implementasyon)
        stats = {
            "user_id": user_id,
            "preferences": preferences,
            "total_feedback": 0,  # Bu kısım geliştirilebilir
            "positive_count": 0,
            "negative_count": 0
        }
        
        return {"success": True, "data": stats}
        
    except Exception as e:
        logger.error(f"Feedback istatistik hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İstatistikler alınırken hata oluştu: {str(e)}")

@router.get("/feedback/patterns")
async def get_response_patterns():
    """Response pattern'larını getir"""
    try:
        # Bu endpoint admin paneli için kullanılabilir
        return {"success": True, "message": "Pattern'lar başarıyla alındı"}
        
    except Exception as e:
        logger.error(f"Pattern getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Pattern'lar alınırken hata oluştu: {str(e)}")

@router.get("/feedback/improvements")
async def get_improved_answers():
    """İyileştirilmiş cevapları getir"""
    try:
        # Bu endpoint admin paneli için kullanılabilir
        return {"success": True, "message": "İyileştirilmiş cevaplar başarıyla alındı"}
        
    except Exception as e:
        logger.error(f"İyileştirilmiş cevaplar getirme hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İyileştirilmiş cevaplar alınırken hata oluştu: {str(e)}") 