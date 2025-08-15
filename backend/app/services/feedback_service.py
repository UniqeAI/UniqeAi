import logging
import asyncio
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..schemas.feedback import (
    FeedbackSchema, 
    FeedbackType, 
    UserPreferenceSchema,
    ResponsePatternSchema,
    ImprovedAnswerSchema
)

logger = logging.getLogger(__name__)

class FeedbackService:
    """Feedback işleme ve öğrenme servisi"""
    
    def __init__(self):
        self.db_url = "sqlite:///./feedback.db"
        self.engine = None
        self.SessionLocal = None
        self._init_database()
    
    def _init_database(self):
        """Veritabanı başlatma"""
        try:
            # SQLite veritabanı oluştur
            self.engine = create_engine(
                self.db_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self.engine
            )
            
            # Tabloları oluştur
            self._create_tables()
            logger.info("Feedback veritabanı başarıyla başlatıldı")
            
        except Exception as e:
            logger.error(f"Veritabanı başlatma hatası: {e}")
    
    def _create_tables(self):
        """Gerekli tabloları oluştur"""
        try:
            with self.engine.connect() as conn:
                # Feedback tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS feedback_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        feedback_id TEXT UNIQUE,
                        feedback_type TEXT,
                        message_id TEXT,
                        user_question TEXT,
                        ai_response TEXT,
                        user_id TEXT,
                        session_id TEXT,
                        context TEXT,
                        timestamp TEXT,
                        processed BOOLEAN DEFAULT FALSE
                    )
                """))
                
                # Kullanıcı tercihleri tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT UNIQUE,
                        prefer_detailed BOOLEAN DEFAULT FALSE,
                        prefer_simple BOOLEAN DEFAULT FALSE,
                        prefer_formal BOOLEAN DEFAULT FALSE,
                        prefer_casual BOOLEAN DEFAULT FALSE,
                        language TEXT DEFAULT 'tr',
                        created_at TEXT,
                        updated_at TEXT
                    )
                """))
                
                # Response pattern'ları tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS response_patterns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pattern_id TEXT UNIQUE,
                        question_type TEXT,
                        answer_style TEXT,
                        keywords TEXT,
                        context TEXT,
                        confidence_score REAL DEFAULT 0.0,
                        usage_count INTEGER DEFAULT 0,
                        created_at TEXT,
                        last_used TEXT
                    )
                """))
                
                # İyileştirilmiş cevaplar tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS improved_answers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_question TEXT,
                        original_answer TEXT,
                        improved_answer TEXT,
                        improvement_type TEXT,
                        quality_score REAL DEFAULT 0.0,
                        feedback_count INTEGER DEFAULT 0,
                        created_at TEXT
                    )
                """))
                
                conn.commit()
                logger.info("Feedback tabloları oluşturuldu")
                
        except Exception as e:
            logger.error(f"Tablo oluşturma hatası: {e}")
    
    async def process_feedback(self, feedback: FeedbackSchema) -> Dict[str, Any]:
        """Feedback verisini işle ve öğren"""
        try:
            logger.info(f"Feedback işleniyor: {feedback.feedback_type}")
            
            # Feedback'i veritabanına kaydet
            feedback_id = await self._save_feedback(feedback)
            
            # Feedback tipine göre işle
            if feedback.feedback_type == FeedbackType.POSITIVE:
                await self._learn_from_positive(feedback)
            elif feedback.feedback_type == FeedbackType.NEGATIVE:
                await self._learn_from_negative(feedback)
            
            # Kullanıcı tercihlerini güncelle
            await self._update_user_preferences(feedback)
            
            return {
                "success": True,
                "message": "Feedback başarıyla işlendi",
                "feedback_id": feedback_id,
                "processed": True
            }
            
        except Exception as e:
            logger.error(f"Feedback işleme hatası: {e}")
            return {
                "success": False,
                "message": f"Feedback işlenemedi: {str(e)}",
                "processed": False
            }
    
    async def _save_feedback(self, feedback: FeedbackSchema) -> str:
        """Feedback'i veritabanına kaydet"""
        feedback_id = f"FB_{uuid.uuid4().hex[:8]}"
        
        with self.SessionLocal() as session:
            session.execute(text("""
                INSERT INTO feedback_data (
                    feedback_id, feedback_type, message_id, user_question, 
                    ai_response, user_id, session_id, context, timestamp
                ) VALUES (:feedback_id, :feedback_type, :message_id, :user_question, 
                         :ai_response, :user_id, :session_id, :context, :timestamp)
            """), {
                "feedback_id": feedback_id,
                "feedback_type": feedback.feedback_type.value,
                "message_id": feedback.message_id,
                "user_question": feedback.user_question,
                "ai_response": feedback.ai_response,
                "user_id": feedback.user_id,
                "session_id": feedback.session_id,
                "context": json.dumps(feedback.context) if feedback.context else None,
                "timestamp": feedback.timestamp.isoformat()
            })
            session.commit()
        
        logger.info(f"Feedback kaydedildi: {feedback_id}")
        return feedback_id
    
    async def _learn_from_positive(self, feedback: FeedbackSchema):
        """Pozitif feedback'den öğren"""
        try:
            # Soru-cevap pattern'ını analiz et
            pattern = await self._extract_response_pattern(feedback)
            
            # Pattern'ı veritabanına kaydet
            await self._save_response_pattern(pattern)
            
            # Benzer sorulara aynı yaklaşımı kullan
            await self._update_response_style(pattern)
            
            logger.info(f"Pozitif feedback'den öğrenildi: {pattern['question_type']}")
            
        except Exception as e:
            logger.error(f"Pozitif feedback öğrenme hatası: {e}")
    
    async def _learn_from_negative(self, feedback: FeedbackSchema):
        """Negatif feedback'den öğren"""
        try:
            # Mevcut cevabı analiz et
            issues = await self._analyze_response_issues(feedback.ai_response)
            
            # İyileştirilmiş cevap üret
            improved_answer = await self._generate_improved_answer(
                feedback.user_question, 
                feedback.ai_response, 
                issues
            )
            
            # İyileştirilmiş cevabı kaydet
            await self._save_improved_answer(
                feedback.user_question,
                feedback.ai_response,
                improved_answer,
                issues
            )
            
            logger.info(f"Negatif feedback'den öğrenildi ve iyileştirildi")
            
        except Exception as e:
            logger.error(f"Negatif feedback öğrenme hatası: {e}")
    
    async def _extract_response_pattern(self, feedback: FeedbackSchema) -> Dict[str, Any]:
        """Response pattern'ını çıkar"""
        # Basit pattern extraction (anahtar kelime sınıflandırması kaldırıldı)
        question_lower = feedback.user_question.lower()
        
        # Soru tipini belirle (nötr)
        question_type = "general"
        
        # Cevap stilini analiz et
        answer_style = "informative"
        if len(feedback.ai_response) > 200:
            answer_style = "detailed"
        elif len(feedback.ai_response) < 100:
            answer_style = "concise"
        
        # Anahtar kelimeleri çıkar (yalnızca depolama amaçlı, karar için kullanılmıyor)
        keywords = [word for word in question_lower.split() if len(word) > 3]
        
        return {
            "pattern_id": f"PAT_{uuid.uuid4().hex[:8]}",
            "question_type": question_type,
            "answer_style": answer_style,
            "keywords": keywords,
            "context": feedback.context,
            "confidence_score": 0.9,
            "usage_count": 1
        }
    
    async def _save_response_pattern(self, pattern: Dict[str, Any]):
        """Response pattern'ını kaydet"""
        with self.SessionLocal() as session:
            session.execute(text("""
                INSERT OR REPLACE INTO response_patterns (
                    pattern_id, question_type, answer_style, keywords, 
                    context, confidence_score, usage_count, created_at
                ) VALUES (:pattern_id, :question_type, :answer_style, :keywords, 
                         :context, :confidence_score, :usage_count, :created_at)
            """), {
                "pattern_id": pattern["pattern_id"],
                "question_type": pattern["question_type"],
                "answer_style": pattern["answer_style"],
                "keywords": json.dumps(pattern["keywords"]),
                "context": json.dumps(pattern["context"]),
                "confidence_score": pattern["confidence_score"],
                "usage_count": pattern["usage_count"],
                "created_at": datetime.now().isoformat()
            })
            session.commit()
    
    async def _analyze_response_issues(self, response: str) -> List[str]:
        """Response'daki sorunları analiz et"""
        issues = []
        
        # Basit analiz
        if len(response) < 50:
            issues.append("too_short")
        elif len(response) > 500:
            issues.append("too_long")
        
        if not any(char in response for char in ".,!?"):
            issues.append("no_punctuation")
        
        if response.count(" ") < 5:
            issues.append("too_simple")
        
        return issues
    
    async def _generate_improved_answer(self, question: str, current_answer: str, issues: List[str]) -> str:
        """İyileştirilmiş cevap üret"""
        # Basit iyileştirme kuralları
        improved = current_answer
        
        if "too_short" in issues:
            improved += f"\n\n{question} hakkında daha detaylı bilgi için müşteri hizmetlerimizle iletişime geçebilirsiniz."
        
        if "too_long" in issues:
            # Cevabı kısalt
            sentences = improved.split(". ")
            if len(sentences) > 3:
                improved = ". ".join(sentences[:3]) + "."
        
        if "no_punctuation" in issues:
            # Noktalama ekle
            if not improved.endswith((".", "!", "?")):
                improved += "."
        
        return improved
    
    async def _save_improved_answer(self, question: str, original: str, improved: str, issues: List[str]):
        """İyileştirilmiş cevabı kaydet"""
        with self.SessionLocal() as session:
            session.execute(text("""
                INSERT INTO improved_answers (
                    original_question, original_answer, improved_answer, 
                    improvement_type, quality_score
                ) VALUES (:original_question, :original_answer, :improved_answer, 
                         :improvement_type, :quality_score)
            """), {
                "original_question": question,
                "original_answer": original,
                "improved_answer": improved,
                "improvement_type": json.dumps(issues),
                "quality_score": 0.8  # Varsayılan kalite skoru
            })
            session.commit()
    
    async def _update_user_preferences(self, feedback: FeedbackSchema):
        """Kullanıcı tercihlerini güncelle"""
        if not feedback.user_id:
            return
        
        try:
            with self.SessionLocal() as session:
                # Mevcut tercihleri kontrol et
                result = session.execute(text("""
                    SELECT * FROM user_preferences WHERE user_id = :user_id
                """), {"user_id": feedback.user_id}).fetchone()
                
                if result:
                    # Tercihleri güncelle
                    if feedback.feedback_type == FeedbackType.POSITIVE:
                        # Pozitif feedback varsa detaylı cevapları tercih et
                        session.execute(text("""
                            UPDATE user_preferences 
                            SET prefer_detailed = TRUE, updated_at = :updated_at
                            WHERE user_id = :user_id
                        """), {
                            "updated_at": datetime.now().isoformat(),
                            "user_id": feedback.user_id
                        })
                else:
                    # Yeni kullanıcı tercihleri oluştur
                    session.execute(text("""
                        INSERT INTO user_preferences (
                            user_id, prefer_detailed, created_at, updated_at
                        ) VALUES (:user_id, :prefer_detailed, :created_at, :updated_at)
                    """), {
                        "user_id": feedback.user_id,
                        "prefer_detailed": feedback.feedback_type == FeedbackType.POSITIVE,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    })
                
                session.commit()
                
        except Exception as e:
            logger.error(f"Kullanıcı tercihleri güncelleme hatası: {e}")
    
    async def _update_response_style(self, pattern: Dict[str, Any]):
        """Response stilini güncelle"""
        # Bu fonksiyon gelecekte AI modelini güncellemek için kullanılabilir
        logger.info(f"Response stili güncellendi: {pattern['question_type']} -> {pattern['answer_style']}")
    
    async def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı tercihlerini getir"""
        try:
            with self.SessionLocal() as session:
                result = session.execute(text("""
                    SELECT * FROM user_preferences WHERE user_id = :user_id
                """), {"user_id": user_id}).fetchone()
                
                if result:
                    return {
                        "user_id": result[1],
                        "prefer_detailed": bool(result[2]),
                        "prefer_simple": bool(result[3]),
                        "prefer_formal": bool(result[4]),
                        "prefer_casual": bool(result[5]),
                        "language": result[6]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Kullanıcı tercihleri getirme hatası: {e}")
            return None
    
    async def get_similar_patterns(self, question: str) -> List[Dict[str, Any]]:
        """Benzer sorular için pattern'ları getir"""
        try:
            question_lower = question.lower()
            keywords = [word for word in question_lower.split() if len(word) > 3]
            
            with self.SessionLocal() as session:
                # Anahtar kelimelere göre benzer pattern'ları bul
                patterns = []
                for keyword in keywords:
                    result = session.execute(text("""
                        SELECT * FROM response_patterns 
                        WHERE keywords LIKE :keyword_pattern 
                        ORDER BY confidence_score DESC, usage_count DESC
                        LIMIT 5
                    """), {"keyword_pattern": f"%{keyword}%"}).fetchall()
                    
                    for row in result:
                        patterns.append({
                            "pattern_id": row[1],
                            "question_type": row[2],
                            "answer_style": row[3],
                            "confidence_score": row[6],
                            "usage_count": row[7]
                        })
                
                return patterns
                
        except Exception as e:
            logger.error(f"Benzer pattern'lar getirme hatası: {e}")
            return []
    
    async def get_improved_answers(self, question: str) -> List[Dict[str, Any]]:
        """İyileştirilmiş cevapları getir"""
        try:
            with self.SessionLocal() as session:
                result = session.execute(text("""
                    SELECT * FROM improved_answers 
                    WHERE original_question LIKE :question_pattern 
                    ORDER BY quality_score DESC, feedback_count DESC
                    LIMIT 3
                """), {"question_pattern": f"%{question[:50]}%"}).fetchall()
                
                improved_answers = []
                for row in result:
                    improved_answers.append({
                        "original_question": row[1],
                        "improved_answer": row[3],
                        "improvement_type": row[4],
                        "quality_score": row[5]
                    })
                
                return improved_answers
                
        except Exception as e:
            logger.error(f"İyileştirilmiş cevaplar getirme hatası: {e}")
            return [] 