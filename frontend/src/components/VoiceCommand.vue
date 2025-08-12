<template>
  <div class="voice-command-container">
    <!-- Voice Command Button -->
    <button
      type="button"
      @click="toggleVoiceRecording"
      @keydown.enter.prevent="handleEnterKey"
      :disabled="!isSupported"
      class="voice-btn p-4 rounded-xl shadow-xl hover:shadow-2xl transform transition-all duration-300 relative overflow-hidden"
      :class="[
        isRecording ? 'scale-110 animate-pulse' : 'hover:scale-105',
        !isSupported ? 'opacity-50 cursor-not-allowed' : ''
      ]"
      :style="getButtonStyle"
      :title="!isSupported ? 'Tarayıcınız ses tanımayı desteklemiyor' : isRecording ? 'Kayıt durdurun' : 'Sesli mesaj gönderin'"
    >
      <!-- Microphone Icon -->
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6 text-white transition-transform duration-300" 
        :class="isRecording ? 'scale-125' : ''"
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          v-if="!isRecording"
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
        />
        <path 
          v-else
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M21 12a9 9 0 11-6.219-8.56"
        />
      </svg>
      
      <!-- Recording Animation -->
      <div 
        v-if="isRecording" 
        class="absolute inset-0 rounded-xl bg-red-500 opacity-30 animate-ping"
      ></div>
    </button>

    <!-- Status Text -->
    <div 
      v-if="statusText" 
      class="mt-2 text-sm text-center font-medium transition-all duration-300"
      :class="currentTheme === 'monochrome' ? 'text-black' : (darkMode ? 'text-white/80' : 'text-gray-700')"
    >
      {{ statusText }}
    </div>

    <!-- Voice Waveform Animation -->
    <div 
      v-if="isRecording" 
      class="mt-3 flex items-center justify-center gap-1"
    >
      <div 
        v-for="i in 5" 
        :key="i"
        class="voice-wave"
        :style="`animation-delay: ${i * 0.1}s; background-color: ${getWaveColor};`"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VoiceCommand',
  props: {
    darkMode: {
      type: Boolean,
      default: false
    },
    currentTheme: {
      type: String,
      default: 'blue'
    }
  },
  emits: ['voice-result'],
  data() {
    return {
      isSupported: false,
      isRecording: false,
      recognition: null,
      statusText: '',
      lastResult: ''
    }
  },
  computed: {
    getButtonStyle() {
      if (this.isRecording) {
        return 'background: #ef4444; color: white;' // Red when recording
      }
      
      const themeColors = {
        'blue': 'linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%)',
        'burgundy': 'linear-gradient(135deg, #7f1d1d 0%, #991b1b 50%, #b91c1c 100%)',
        'purple': 'linear-gradient(135deg, #5b21b6 0%, #6d28d9 50%, #7c3aed 100%)',
        'emerald': 'linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%)',
        'monochrome': 'linear-gradient(135deg, #000000 0%, #000000 50%, #000000 100%)'
      }
      
      const themeGradient = themeColors[this.currentTheme] || themeColors['blue']
      return `background: ${themeGradient}; color: white;`
    },
    getWaveColor() {
      const themeColors = {
        'blue': '#1d4ed8',
        'burgundy': '#b91c1c',
        'purple': '#7c3aed',
        'emerald': '#059669',
        'monochrome': '#000000'
      }
      
      return themeColors[this.currentTheme] || themeColors['blue']
    }
  },
  mounted() {
    this.initSpeechRecognition()
  },
  beforeUnmount() {
    if (this.recognition) {
      this.recognition.stop()
    }
  },
  methods: {
    initSpeechRecognition() {
      // Check for Web Speech API support
      if ('webkitSpeechRecognition' in window) {
        this.recognition = new webkitSpeechRecognition()
        this.isSupported = true
      } else if ('SpeechRecognition' in window) {
        this.recognition = new SpeechRecognition()
        this.isSupported = true
      } else {
        this.isSupported = false
        this.statusText = 'Tarayıcınız ses tanımayı desteklemiyor'
        return
      }

      // Configure speech recognition
      this.recognition.continuous = false
      this.recognition.interimResults = true
      this.recognition.lang = 'tr-TR' // Turkish language
      this.recognition.maxAlternatives = 1

      // Event listeners
      this.recognition.onstart = () => {
        this.isRecording = true
        this.statusText = 'Dinliyorum... Konuşabilirsiniz'
      }

      this.recognition.onresult = (event) => {
        let finalTranscript = ''
        let interimTranscript = ''

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            finalTranscript += transcript
          } else {
            interimTranscript += transcript
          }
        }

        if (finalTranscript) {
          this.lastResult = finalTranscript.trim()
          this.statusText = `Anladım: "${this.lastResult}"`
          this.$emit('voice-result', this.lastResult)
        } else if (interimTranscript) {
          this.statusText = `Dinliyorum: "${interimTranscript}"`
        }
      }

      this.recognition.onerror = (event) => {
        this.isRecording = false
        console.error('Speech recognition error:', event.error)
        
        switch (event.error) {
          case 'network':
            this.statusText = 'Ağ bağlantısı hatası'
            break
          case 'not-allowed':
            this.statusText = 'Mikrofon izni verilmedi'
            break
          case 'no-speech':
            this.statusText = 'Ses algılanamadı, tekrar deneyin'
            break
          case 'audio-capture':
            this.statusText = 'Mikrofon bulunamadı'
            break
          case 'service-not-allowed':
            this.statusText = 'Ses tanıma servisi kullanılamıyor'
            break
          default:
            this.statusText = 'Ses tanıma hatası'
        }

        setTimeout(() => {
          this.statusText = ''
        }, 3000)
      }

      this.recognition.onend = () => {
        this.isRecording = false
        if (this.lastResult) {
          setTimeout(() => {
            this.statusText = ''
            this.lastResult = ''
          }, 2000)
        } else {
          this.statusText = ''
        }
      }
    },

    toggleVoiceRecording() {
      if (!this.isSupported) return

      if (this.isRecording) {
        this.recognition.stop()
        this.statusText = 'Kayıt durduruluyor...'
      } else {
        // Request microphone permission
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(() => {
            this.recognition.start()
          })
          .catch((error) => {
            console.error('Microphone access denied:', error)
            this.statusText = 'Mikrofon izni gerekli'
            setTimeout(() => {
              this.statusText = ''
            }, 3000)
          })
      }
    },

    handleEnterKey(event) {
      // Prevent default enter behavior and don't trigger voice recording
      event.preventDefault()
      event.stopPropagation()
      event.stopImmediatePropagation()
      
      // Explicitly do nothing - this prevents Enter key from activating the microphone
      // The button type="button" already prevents form submission, 
      // but this adds extra protection against any event bubbling
      return false
    }
  }
}
</script>

<style scoped>
.voice-command-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.voice-btn {
  position: relative;
  border: none;
  cursor: pointer;
  user-select: none;
  will-change: transform;
}

.voice-btn:disabled {
  cursor: not-allowed;
  transform: none !important;
}

.voice-wave {
  width: 3px;
  height: 20px;
  border-radius: 2px;
  animation: voice-wave 1.5s ease-in-out infinite;
}

@keyframes voice-wave {
  0%, 100% {
    height: 8px;
    opacity: 0.4;
  }
  50% {
    height: 24px;
    opacity: 1;
  }
}

/* Pulse animation for recording state */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.voice-btn.animate-pulse {
  animation: pulse 2s infinite;
}
</style>
