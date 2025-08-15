
# ==============================================================================
# 🔧 DATA AUGMENTATION SNIPPETS FOR expert_trainer-stable.py
# ==============================================================================

def apply_token_masking(text: str, mask_probability: float = 0.1) -> str:
    """
    Metindeki kelimelerin %10'unu [MASK] ile değiştirir
    """
    words = text.split()
    if len(words) <= 3:
        return text
    
    masked_words = []
    for word in words:
        if random.random() < mask_probability:
            masked_words.append("[MASK]")
        else:
            masked_words.append(word)
    
    return " ".join(masked_words)

def inject_noise_words(text: str, noise_probability: float = 0.1) -> str:
    """
    Metne gürültü kelimeleri ekler
    """
    noise_words = ["efendim", "şey", "yani", "işte", "bakın", "anlıyorsunuz"]
    
    if random.random() < noise_probability:
        noise_word = random.choice(noise_words)
        return f"{noise_word}, {text}"
    
    return text

def apply_punctuation_variations(text: str, variation_probability: float = 0.15) -> str:
    """
    Noktalama işaretlerini çeşitlendirir
    """
    variations = [".", "!", "?", "...", "!!", "??"]
    
    if random.random() < variation_probability:
        return text.replace(".", random.choice(variations))
    
    return text

def add_filler_phrases(text: str, filler_probability: float = 0.1) -> str:
    """
    Filler phrases ekler
    """
    fillers = ["bir dakika", "bir saniye", "hemen", "şimdi", "az önce"]
    
    if random.random() < filler_probability:
        filler = random.choice(fillers)
        return f"{filler}, {text}"
    
    return text

class AugmentedDataLoader:
    """
    expert_trainer-stable.py için augmented data loader
    """
    
    def __init__(self, augmentation_enabled: bool = True):
        self.augmentation_enabled = augmentation_enabled
    
    def augment_text(self, text: str) -> str:
        """
        Metne tüm augmentation tekniklerini uygular
        """
        if not self.augmentation_enabled:
            return text
        
        augmented_text = text
        augmented_text = apply_token_masking(augmented_text)
        augmented_text = inject_noise_words(augmented_text)
        augmented_text = apply_punctuation_variations(augmented_text)
        augmented_text = add_filler_phrases(augmented_text)
        
        return augmented_text
    
    def augment_dialogue(self, dialogue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diyalog yapısına augmentation uygular
        """
        if not self.augmentation_enabled:
            return dialogue
        
        augmented_dialogue = dialogue.copy()
        
        for turn in augmented_dialogue.get("donguler", []):
            if "icerik" in turn:
                turn["icerik"] = self.augment_text(turn["icerik"])
        
        return augmented_dialogue

# ==============================================================================
# 📝 INTEGRATION WITH expert_trainer-stable.py
# ==============================================================================

# ExpertTrainer sınıfına eklenecek metodlar:

def _load_and_prepare_dataset_with_augmentation(self, tokenizer: AutoTokenizer) -> Dataset:
    """
    Augmentation ile veri seti yükleme ve hazırlama
    """
    # Mevcut _load_and_prepare_dataset metodunun başına ekle:
    
    # Augmentation loader'ı başlat
    augmentation_loader = AugmentedDataLoader(augmentation_enabled=True)
    
    # ... mevcut kod ...
    
    for i, item in enumerate(all_data):
        # Normalize et
        normalized_item = self._normalize_dialogue_item(item)
        
        if not normalized_item:
            continue
        
        # Augmentation uygula
        normalized_item = augmentation_loader.augment_dialogue(normalized_item)
        
        # ... geri kalan mevcut kod ...

# ==============================================================================
# 🎯 USAGE EXAMPLE
# ==============================================================================

# expert_trainer-stable.py'de kullanım:
# 
# 1. Augmentation kodlarını dosyanın başına ekle
# 2. _load_and_prepare_dataset metodunu güncelle
# 3. Augmentation parametrelerini config'e ekle:
#
# @dataclass
# class ModelAndDataConfig:
#     # ... mevcut alanlar ...
#     enable_augmentation: bool = field(default=True, metadata={"help": "Data augmentation aktif mi?"})
#     augmentation_probability: float = field(default=0.1, metadata={"help": "Augmentation olasılığı"})
#
