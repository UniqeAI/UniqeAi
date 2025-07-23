"""
Turkish Text Preprocessing for Synthetic Data
============================================

Bu modül, Türkçe metin verilerinin ön işlenmesi için Zemberek kütüphanesi
entegrasyonunu hazırlar. Gün 4 görevleri kapsamında detaylandırılacaktır.

Requirements:
    pip install zemberek-python

Usage:
    from ai_model.scripts.turkish_preprocessing import TurkishPreprocessor
    
    preprocessor = TurkishPreprocessor()
    normalized = preprocessor.normalize_text("İnternetimin hızını yükseltmek istiyorum.")
"""

try:
    from zemberek import TurkishMorphology  # type: ignore
    ZEMBEREK_AVAILABLE = True
except ImportError:
    ZEMBEREK_AVAILABLE = False
    print("⚠️  Zemberek kütüphanesi yüklü değil. Kurulum için: pip install zemberek-python")

import re
from typing import List, Dict, Optional


class TurkishPreprocessor:
    """Türkçe metin ön işleme sınıfı"""
    
    def __init__(self):
        """Zemberek morphology analyzer'ı başlat"""
        if ZEMBEREK_AVAILABLE:
            try:
                self.morphology = TurkishMorphology.createWithDefaults()
                self.enabled = True
            except Exception as e:
                print(f"⚠️  Zemberek başlatılamadı: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def normalize_text(self, text: str) -> str:
        """
        Türkçe metni normalize et
        
        Args:
            text: İşlenecek Türkçe metin
            
        Returns:
            Normalize edilmiş metin
        """
        if not text:
            return ""
        
        # Temel temizlik
        normalized = self._basic_cleanup(text)
        
        # Zemberek ile normalize etme (mevcut ise)
        if self.enabled:
            normalized = self._zemberek_normalize(normalized)
        else:
            # Fallback: Basit normalize etme
            normalized = self._simple_normalize(normalized)
        
        return normalized.strip()
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Metinden anahtar kelimeleri çıkar
        
        Args:
            text: Analiz edilecek metin
            
        Returns:
            Anahtar kelimeler listesi
        """
        if not self.enabled:
            return self._simple_keyword_extraction(text)
        
        keywords = []
        words = text.split()
        
        for word in words:
            # Zemberek ile kök bulma
            analysis = self.morphology.analyzeSentence(word)
            if analysis:
                # İlk analiz sonucunun kökünü al
                root = analysis[0].getDictionaryItem().root
                keywords.append(root)
            else:
                keywords.append(word.lower())
        
        return list(set(keywords))  # Tekrarları kaldır
    
    def _basic_cleanup(self, text: str) -> str:
        """Temel metin temizliği"""
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        
        # Özel karakterleri temizle (sadece gerekli olanları)
        text = re.sub(r'[^\w\s\.\,\!\?\;]', '', text)
        
        return text
    
    def _zemberek_normalize(self, text: str) -> str:
        """Zemberek ile normalize etme"""
        try:
            # Zemberek normalization API kullan
            normalized = self.morphology.normalizeText(text)
            return normalized
        except Exception as e:
            print(f"⚠️  Zemberek normalization hatası: {e}")
            return self._simple_normalize(text)
    
    def _simple_normalize(self, text: str) -> str:
        """Basit normalize etme (Zemberek olmadan)"""
        # Türkçe karakter dönüşümleri
        replacements = {
            'İ': 'i', 'I': 'ı', 'Ş': 'ş', 'Ğ': 'ğ', 
            'Ü': 'ü', 'Ö': 'ö', 'Ç': 'ç'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text.lower()
    
    def _simple_keyword_extraction(self, text: str) -> List[str]:
        """Basit anahtar kelime çıkarma"""
        # Türkçe stop words (basit liste)
        stop_words = {
            've', 'ile', 'bu', 'şu', 'o', 'bir', 'için', 'ki', 'da', 'de',
            'olan', 'olan', 'olarak', 'gibi', 'kadar', 'daha', 'en', 'çok',
            'az', 'var', 'yok', 'mı', 'mi', 'mu', 'mü'
        }
        
        words = text.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return list(set(keywords))


def preprocess_synthetic_data_inputs(data_points: List[Dict]) -> List[Dict]:
    """
    Sentetik veri setindeki input'ları Türkçe ön işleme tabi tut
    
    Args:
        data_points: Sentetik veri noktaları listesi
        
    Returns:
        Ön işleme tabi tutulmuş veri noktaları
    """
    preprocessor = TurkishPreprocessor()
    
    processed_data = []
    
    for point in data_points:
        if 'input' in point:
            # Input metnini normalize et
            original_input = point['input']
            normalized_input = preprocessor.normalize_text(original_input)
            
            # Anahtar kelimeleri çıkar (opsiyonel metadata olarak)
            keywords = preprocessor.extract_keywords(original_input)
            
            # Yeni veri noktası oluştur
            processed_point = point.copy()
            processed_point['input'] = normalized_input
            processed_point['_metadata'] = {
                'original_input': original_input,
                'keywords': keywords,
                'preprocessed': True
            }
            
            processed_data.append(processed_point)
        else:
            processed_data.append(point)
    
    return processed_data


# Test fonksiyonu
if __name__ == "__main__":
    # Basit test
    preprocessor = TurkishPreprocessor()
    
    test_texts = [
        "İnternetimin hızını yükseltmek istiyorum.",
        "Fatura ödeme durumunu kontrol etmek istiyorum.",
        "Şu anda hangi pakette olduğumu öğrenmek istiyorum."
    ]
    
    print("🧪 Türkçe Ön İşleme Testi")
    print("=" * 40)
    
    for text in test_texts:
        normalized = preprocessor.normalize_text(text)
        keywords = preprocessor.extract_keywords(text)
        
        print(f"📝 Orijinal: {text}")
        print(f"✨ Normalize: {normalized}")
        print(f"🔑 Anahtar Kelimeler: {keywords}")
        print("-" * 40) 