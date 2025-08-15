<template>
  <div class="bot-message-actions">
    <div class="action-buttons">
      <button 
        @click="copyMessage"
        class="action-btn"
        title="Mesajı kopyala"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
      
      <button 
        @click="likeMessage"
        :class="['action-btn', { 'liked': isLiked }]"
        title="Beğen"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
        </svg>
      </button>
      
      <button 
        @click="dislikeMessage"
        :class="['action-btn', { 'disliked': isDisliked }]"
        title="Beğenme"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" style="transform: scaleY(-1)">
          <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
        </svg>
      </button>
      
      <button 
        @click="speakMessage"
        :class="['action-btn', { 'speaking': isSpeaking }]"
        title="Mesajı seslendir"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
        </svg>
      </button>
    </div>
    
    <div v-if="showCopySuccess" class="copy-success">
      Kopyalandı!
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  messageId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['like', 'dislike', 'speak'])

const isLiked = ref(false)
const isDisliked = ref(false)
const showCopySuccess = ref(false)
const isSpeaking = ref(false)

const copyMessage = async () => {
  try {
    await navigator.clipboard.writeText(props.message)
    showCopySuccess.value = true
    setTimeout(() => {
      showCopySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Kopyalama hatası:', err)
    // Fallback: Text selection method
    const textArea = document.createElement('textarea')
    textArea.value = props.message
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    
    showCopySuccess.value = true
    setTimeout(() => {
      showCopySuccess.value = false
    }, 2000)
  }
}

const likeMessage = () => {
  if (isDisliked.value) {
    isDisliked.value = false
  }
  isLiked.value = !isLiked.value
  
  emit('like', {
    messageId: props.messageId,
    isLiked: isLiked.value
  })
}

const dislikeMessage = () => {
  if (isLiked.value) {
    isLiked.value = false
  }
  isDisliked.value = !isDisliked.value
  
  emit('dislike', {
    messageId: props.messageId,
    isDisliked: isDisliked.value
  })
}

const speakMessage = () => {
  if (isSpeaking.value) {
    // Eğer konuşma devam ediyorsa durdur
    speechSynthesis.cancel()
    isSpeaking.value = false
    return
  }

  // Web Speech API kullanarak mesajı seslendir
  if ('speechSynthesis' in window) {
    // Sesler yüklü değilse bekle
    if (speechSynthesis.getVoices().length === 0) {
      speechSynthesis.addEventListener('voiceschanged', speakMessage, { once: true })
      return
    }
    const utterance = new SpeechSynthesisUtterance(props.message)
    
    // Tüm mevcut sesleri al
    const voices = speechSynthesis.getVoices()
    console.log('Tüm mevcut sesler:', voices.map(v => `${v.name} (${v.lang}) - ${v.localService ? 'Yerel' : 'Uzak'}`))
    
    // Türkçe sesleri çok geniş kriterlerde ara
    const turkishVoices = voices.filter(voice => {
      const name = voice.name.toLowerCase()
      const lang = voice.lang.toLowerCase()
      return (
        lang.startsWith('tr') || 
        lang.includes('tr-') ||
        lang === 'tr' ||
        name.includes('turk') || 
        name.includes('türk') || 
        name.includes('yelda') ||
        name.includes('emel') ||
        name.includes('turkish') ||
        name.includes('fatma') ||
        name.includes('kemal') ||
        name.includes('espeak') && name.includes('tr') ||
        name.includes('festival') && name.includes('tr')
      )
    })
    
    // Eğer hiç Türkçe ses yoksa, en azından tr içeren herhangi bir ses ara
    if (turkishVoices.length === 0) {
      const possibleTurkish = voices.filter(voice => {
        const combined = (voice.name + ' ' + voice.lang).toLowerCase()
        return combined.includes('tr') || combined.includes('turk')
      })
      if (possibleTurkish.length > 0) {
        turkishVoices.push(...possibleTurkish)
        console.log('🔍 Alternatif Türkçe sesler bulundu:', possibleTurkish.map(v => v.name))
      }
    }
    
    console.log('Bulunan Türkçe sesler:', turkishVoices.map(v => `${v.name} (${v.lang})`))
    
    // En iyi Türk aksanına sahip ses seç (öncelik sırası)
    let selectedVoice = null
    if (turkishVoices.length > 0) {
      // 1. Öncelik: Türk kadın sesleri (daha doğal aksan)
      selectedVoice = turkishVoices.find(voice => {
        const name = voice.name.toLowerCase()
        return (name.includes('yelda') || name.includes('emel') || name.includes('fatma')) && 
               voice.lang.toLowerCase().startsWith('tr')
      })
      
      // 2. Öncelik: Microsoft Türkçe (genellikle daha iyi aksan)
      if (!selectedVoice) {
        selectedVoice = turkishVoices.find(voice => 
          voice.name.toLowerCase().includes('microsoft') && voice.lang.toLowerCase().startsWith('tr')
        )
      }
      
      // 3. Öncelik: Yerel Türkçe sesler (sistem sesleri)
      if (!selectedVoice) {
        selectedVoice = turkishVoices.find(voice => 
          voice.localService && voice.lang.toLowerCase().startsWith('tr')
        )
      }
      
      // 4. Öncelik: Google Türkçe
      if (!selectedVoice) {
        selectedVoice = turkishVoices.find(voice => 
          voice.name.toLowerCase().includes('google') && voice.lang.toLowerCase().startsWith('tr')
        )
      }
      
      // 5. Öncelik: Espeak Türkçe (Linux'ta yaygın)
      if (!selectedVoice) {
        selectedVoice = turkishVoices.find(voice => 
          voice.name.toLowerCase().includes('espeak') && voice.lang.toLowerCase().includes('tr')
        )
      }
      
      // 6. Son çare: Herhangi bir Türkçe ses
      if (!selectedVoice) {
        selectedVoice = turkishVoices[0]
      }
    }
    
    if (selectedVoice) {
      utterance.voice = selectedVoice
      console.log('✅ Seçilen Türkçe ses:', selectedVoice.name, selectedVoice.lang, selectedVoice.localService ? '(Yerel)' : '(Uzak)')
    } else {
      console.warn('❌ Türkçe ses bulunamadı! Sistem varsayılan sesini kullanacak.')
      console.log('💡 Türkçe ses yüklemek için tarayıcı ayarlarınızı kontrol edin.')
      
      // Manuel test - tüm sesleri dene
      console.log('🧪 Manuel test için tüm sesleri Türkçe test et:')
      voices.forEach((voice, index) => {
        console.log(`${index}: ${voice.name} (${voice.lang}) - Test: speechSynthesis.getVoices()[${index}]`)
      })
      console.log('💻 Test komutu: ')
      console.log(`const testUtterance = new SpeechSynthesisUtterance("Merhaba test")`)
      console.log(`testUtterance.voice = speechSynthesis.getVoices()[INDEX_NUMARASI]`)
      console.log(`testUtterance.lang = "tr-TR"`)
      console.log(`speechSynthesis.speak(testUtterance)`)
    }
    
    // Çok agresif Türkçe zorlaması
    if (selectedVoice && selectedVoice.lang.toLowerCase().startsWith('tr')) {
      utterance.lang = selectedVoice.lang
      console.log('🎯 Türkçe ses dili kullanılıyor:', selectedVoice.lang)
    } else {
      // Birden fazla Türkçe format dene
      const turkishFormats = ['tr-TR', 'tr', 'tr-tr', 'TR-TR', 'TR']
      utterance.lang = turkishFormats[0] // tr-TR başla
      console.log('🔄 Varsayılan Türkçe dil zorlanıyor:', utterance.lang)
    }
    
    // Ek Türkçe zorlaması - utterance properties
    Object.defineProperty(utterance, 'lang', {
      get() { return this._lang || 'tr-TR' },
      set(value) { 
        this._lang = value.toLowerCase().includes('tr') ? value : 'tr-TR'
        console.log('📝 Dil ayarı güncellendi:', this._lang)
      }
    })
    utterance.lang = utterance.lang // Trigger setter
    
    // Türk aksanı için optimize edilmiş parametreler
    utterance.rate = 0.8 // Türkçe için ideal konuşma hızı
    utterance.pitch = 1.0 // Doğal Türk sesi tonu
    utterance.volume = 0.95 // Net ses seviyesi
    
    // Ses tipine göre ince ayar
    if (selectedVoice) {
      const voiceName = selectedVoice.name.toLowerCase()
      
      if (voiceName.includes('yelda') || voiceName.includes('fatma')) {
        // Türk kadın sesleri için
        utterance.rate = 0.75
        utterance.pitch = 1.05
        console.log('👩 Türk kadın sesi için optimize edildi')
      } else if (voiceName.includes('kemal') || voiceName.includes('erkek')) {
        // Türk erkek sesleri için
        utterance.rate = 0.8
        utterance.pitch = 0.95
        console.log('👨 Türk erkek sesi için optimize edildi')
      } else if (voiceName.includes('espeak')) {
        // Espeak için özel ayar
        utterance.rate = 0.7
        utterance.pitch = 1.1
        console.log('🔧 Espeak Türkçe için optimize edildi')
      }
    }
    
    console.log('🎤 Seslendirme ayarları:', {
      voice: selectedVoice?.name || 'Varsayılan',
      lang: utterance.lang,
      rate: utterance.rate,
      pitch: utterance.pitch,
      platform: navigator.platform || 'Bilinmiyor'
    })
    
    // Linux platformu tespiti ve özel ayarlar
    if (navigator.platform.toLowerCase().includes('linux')) {
      console.log('🐧 Linux platformu tespit edildi')
      // Linux'ta daha düşük hız daha iyi çalışabilir
      utterance.rate = Math.max(0.7, utterance.rate - 0.1)
      console.log('⚙️ Linux için konuşma hızı ayarlandı:', utterance.rate)
    }
    
    utterance.onstart = () => {
      isSpeaking.value = true
      console.log('🎙️ Türkçe seslendirme başladı')
      console.log('🇹🇷 Aksan kontrolü:', {
        voice: selectedVoice?.name || 'Varsayılan',
        language: utterance.lang,
        isturkish: utterance.lang.toLowerCase().includes('tr')
      })
    }
    
    utterance.onend = () => {
      isSpeaking.value = false
    }
    
    utterance.onerror = (event) => {
      isSpeaking.value = false
      console.error('Metin seslendirilirken hata oluştu:', event.error)
      
      // Linux'ta TTS hatası için özel mesaj
      if (event.error === 'synthesis-failed' || event.error === 'audio-hardware') {
        console.log('🐧 Linux TTS hatası tespit edildi')
        console.log('💡 Çözüm önerileri:')
        console.log('1. PulseAudio servisini kontrol edin: systemctl --user status pulseaudio')
        console.log('2. ALSA ses ayarlarını kontrol edin: alsamixer')
        console.log('3. Speech Dispatcher servisini başlatın: sudo systemctl start speech-dispatcher')
        console.log('4. Tarayıcı izinlerini kontrol edin (mikrofon/hoparlör erişimi)')
      }
    }
    
    speechSynthesis.speak(utterance)
    
    emit('speak', {
      messageId: props.messageId,
      message: props.message
    })
  } else {
    alert('Tarayıcınız metin seslendirme özelliğini desteklemiyor.')
  }
  
  // Eğer Türkçe ses yoksa kullanıcıyı bilgilendir
  const voices = speechSynthesis.getVoices()
  const hasTurkishVoice = voices.some(voice => 
    voice.lang.toLowerCase().startsWith('tr') || 
    voice.name.toLowerCase().includes('turk')
  )
  
  if (!hasTurkishVoice && voices.length > 0) {
    console.warn('⚠️ Türkçe ses bulunamadı. Sistem İngilizce seslendirebilir.')
    console.log('🔧 Linux için Türkçe TTS kurulum rehberi:')
    console.log('')
    console.log('📦 Ubuntu/Debian için:')
    console.log('sudo apt update')
    console.log('sudo apt install espeak espeak-data-tr')
    console.log('sudo apt install festival festvox-tr-kal')
    console.log('sudo apt install speech-dispatcher speech-dispatcher-tr')
    console.log('')
    console.log('📦 Fedora/RHEL için:')
    console.log('sudo dnf install espeak espeak-tr')
    console.log('sudo dnf install festival festvox-tr-kal')
    console.log('')
    console.log('📦 Arch Linux için:')
    console.log('sudo pacman -S espeak espeak-tr')
    console.log('sudo pacman -S festival festival-tr')
    console.log('')
    console.log('🌐 Tarayıcı ayarları:')
    console.log('• Chrome: chrome://settings/languages > Türkçe ekleyin')
    console.log('• Firefox: about:config > intl.locale.requested = "tr"')
    console.log('')
    console.log('🔄 Kurulum sonrası tarayıcıyı yeniden başlatın')
  }
}
</script>

<style scoped>
.bot-message-actions {
  position: relative;
  margin-top: 8px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.action-btn {
  @apply p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200;
  border: none;
  cursor: pointer;
  color: #6b7280;
}

.action-btn:hover {
  color: #374151;
}

.action-btn.liked {
  @apply bg-green-100 text-green-600;
}

.action-btn.disliked {
  @apply bg-red-100 text-red-600;
}

.action-btn.speaking {
  @apply bg-blue-100 text-blue-600;
  animation: pulse 1.5s ease-in-out infinite;
}

.copy-success {
  @apply absolute top-0 left-0 bg-green-500 text-white px-2 py-1 rounded text-xs;
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-10px); }
  20% { opacity: 1; transform: translateY(0); }
  80% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-10px); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
</style>
