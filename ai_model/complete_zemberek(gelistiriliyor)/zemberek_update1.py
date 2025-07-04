"""
Turkish Text Preprocessing for Synthetic Data + Morphological Test(Geliştirme sürecinde) 
============================================

Bu modül, Türkçe metin verilerinin ön işlenmesi için Zemberek kütüphanesi
entegrasyonunu sağlar, ayrıca yaygın konuşma dilini resmi dile dönüştürme
sistemini içerir. Geliştirmeye devam ediliyordur.

Requirements:
    pip install zemberek-python

Usage:
    from ai_model.scripts.turkish_preprocessing import TurkishPreprocessor

    preprocessor = TurkishPreprocessor()
    normalized = preprocessor.normalize_text("İnternetimin hızını yükseltmek istiyorum.")
"""

import re
from typing import List, Dict

# Zemberek import ve kullanılabilirlik kontrolü
try:
    from zemberek import TurkishMorphology  # type: ignore
    ZEMBEREK_AVAILABLE = True
except ImportError:
    ZEMBEREK_AVAILABLE = False
    print("⚠  Zemberek kütüphanesi yüklü değil. Kurulum için: pip install zemberek-python")

# Emoji ve özel karakter temizleme regex (Bu kısımları öğretebilir miyim?)
_EMOJI_PATTERN = re.compile(
    "[\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
    "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
    "\u2600-\u26FF\u2700-\u27BF]+", flags=re.UNICODE)

# Argo -> formal çeviri sözlüğü(Bu kısımları öğretebilir miyim?)
_INFORMAL_TO_FORMAL = {
    r"abi": "",
    r"ya+": "",
    r"şey ya": "",
    r"bi": "bir",
    r"niye": "neden",
    r"niçin": "neden",
    r"gelmiyoo+r": "gelmiyor"
}

# Stop-words listesi(Bu kısımları öğretebilir miyim?)
_STOP_WORDS = {
    've', 'ile', 'bu', 'şu', 'o', 'bir', 'için', 'ki', 'da', 'de',
    'olan', 'olarak', 'gibi', 'kadar', 'daha', 'en', 'çok',
    'az', 'var', 'yok', 'mı', 'mi', 'mu', 'mü'
}

class TurkishPreprocessor:
    """Türkçe metin ön işleme: normalize etme, kök çıkarma, formalizasyon."""

    def __init__(self):
        """Zemberek morphology analyzer'ı başlatılır; açılamazsa fallback mod."""
        if ZEMBEREK_AVAILABLE:
            try:
                # Zemberek nesnesi oluşturulur
                self.morphology = TurkishMorphology.create_with_defaults()
                self.enabled = True
            except Exception as e:
                print(f"⚠  Zemberek başlatılamadı: {e}")
                self.enabled = False
        else:
            self.enabled = False

    def normalize_text(self, text: str) -> str:
        """
        Metni normalleştir:
        1. Temel temizlik (_basic_cleanup)
        2. Emoji temizleme
        3. Morfolojik kök tabanlı normalize (_zemberek_normalize) veya fallback
        4. Argo düzeltme (_formalize_informal)
        5. Küçük harf ve kırpma
        """
        if not text:
            return ""
        cleaned = self._basic_cleanup(text)
        cleaned = _EMOJI_PATTERN.sub('', cleaned)
        if self.enabled:
            cleaned = self._zemberek_normalize(cleaned)
        else:
            cleaned = self._simple_normalize(cleaned)
        cleaned = self._formalize_informal(cleaned)
        return cleaned.strip().lower()

    def extract_keywords(self, text: str) -> List[str]:
        """
        Metinden anahtar kelimeleri çıkar:
        - Zemberek varsa morfolojik kök
        - Yoksa stop-word filtresi
        """
        if not text:
            return []
        tokens = re.findall(r"\w+", text)
        keywords = []
        if self.enabled:
            for t in tokens:
                try:
                    analyses = self.morphology.analyze_sentence(t)
                    if analyses:
                        root = analyses[0].dictionaryItem.root
                        keywords.append(root)
                    else:
                        keywords.append(t.lower())
                except Exception:
                    keywords.append(t.lower())
        else:
            for t in tokens:
                if t.lower() not in _STOP_WORDS and len(t) > 2:
                    keywords.append(t.lower())
        return list(dict.fromkeys(keywords))

    def _basic_cleanup(self, text: str) -> str:
        """Fazla boşluk ve özel karakter temizliği."""
        text = re.sub(r"\s+", ' ', text)
        text = re.sub(r"[^\w\s\.,;!?'-]", '', text)
        return text

    def _zemberek_normalize(self, text: str) -> str:
        """
        Zemberek yoklamasıyla her kelimenin kökünü alarak normalize eder.
        Hata olursa fallback (_simple_normalize) kullanır.
        """
        tokens = re.findall(r"\w+", text)
        roots = []
        for t in tokens:
            try:
                analyses = self.morphology.analyze_sentence(t)
                if analyses:
                    roots.append(analyses[0].dictionaryItem.root)
                else:
                    roots.append(t)
            except Exception:
                roots.append(t)
        return ' '.join(roots)

    def _simple_normalize(self, text: str) -> str:
        """Türkçe karakterleri düzelt ve metni iade et."""
        replacements = {'İ':'i','I':'ı','Ş':'ş','Ğ':'ğ','Ü':'ü','Ö':'ö','Ç':'ç'}#bu işlemin kısayolu olmalı bknz.-->zemberek_morph
        for old,new in replacements.items():
            text = text.replace(old,new)
        return text

    def _formalize_informal(self, text: str) -> str:
        """Argo ifadeleri resmi dile çevirir."""
        for pat, repl in _INFORMAL_TO_FORMAL.items():
            text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        return re.sub(r"\s+", ' ', text)


def preprocess_synthetic_data_inputs(data_points: List[Dict]) -> List[Dict]:
    """Sentetik input'ları ön işler ve metadata ekler."""
    pre = TurkishPreprocessor()
    processed = []
    for point in data_points:
        if 'input' in point:
            orig = point['input']
            norm = pre.normalize_text(orig)
            keys = pre.extract_keywords(orig)
            new_point = point.copy()
            new_point['input'] = norm
            new_point['_metadata'] = {
                'original_input': orig,
                'keywords': keys,
                'preprocessed': True
            }
            processed.append(new_point)
        else:
            processed.append(point)
    return processed

# Basit testler
if __name__ == '__main__':
    sample_texts = [
        "İnternetimin hızını yükseltmek istiyorum.",
        "abi bu internet niye çekmiyooor ya? 😊",
        "Fatura ödeme durumunu kontrol etmek istiyorum!"
    ]
    pre = TurkishPreprocessor()
    print("🧪 Türkçe Ön İşleme Testi")
    print("="*40)
    for txt in sample_texts:
        print(f"Orijinal : {txt}")
        print(f"Normalize : {pre.normalize_text(txt)}")
        print(f"Keywords : {pre.extract_keywords(txt)}")
        print("-"*40)