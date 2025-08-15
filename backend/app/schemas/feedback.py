from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class FeedbackSchema(BaseModel):
    """Feedback verisi için schema"""
    feedback_type: FeedbackType
    message_id: str
    user_question: str
    ai_response: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
class FeedbackResponse(BaseModel):
    """Feedback response schema"""
    success: bool
    message: str
    feedback_id: Optional[str] = None
    processed: bool = False

class UserPreferenceSchema(BaseModel):
    """Kullanıcı tercihleri schema"""
    user_id: str
    prefer_detailed: bool = False
    prefer_simple: bool = False
    prefer_formal: bool = False
    prefer_casual: bool = False
    language: str = "tr"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ResponsePatternSchema(BaseModel):
    """Response pattern schema"""
    pattern_id: str
    question_type: str
    answer_style: str
    keywords: list[str]
    context: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.0
    usage_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    last_used: Optional[datetime] = None

class ImprovedAnswerSchema(BaseModel):
    """İyileştirilmiş cevap schema"""
    original_question: str
    original_answer: str
    improved_answer: str
    improvement_type: str
    quality_score: float
    feedback_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now) 