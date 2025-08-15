<template>
  <div class="voice-command">
    <button 
      @click="toggleVoiceRecording"
      :class="['voice-btn', { 'recording': isRecording }]"
      :title="isRecording ? 'Kayıt durduruluyor...' : 'Sesli komut başlat'"
    >
      <svg v-if="!isRecording" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
      </svg>
      <svg v-else class="w-6 h-6 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" />
        <path d="M19 10v2a7 7 0 01-14 0v-2" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>
    
    <div v-if="isListening" class="listening-indicator">
      <span class="text-sm text-blue-600">Dinleniyor...</span>
      <div class="audio-waves">
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
      </div>
    </div>
    
    <div v-if="transcript" class="transcript">
      <p class="text-sm text-gray-700">{{ transcript }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isRecording = ref(false)
const isListening = ref(false)
const transcript = ref('')
const recognition = ref(null)

const emit = defineEmits(['voice-result'])

onMounted(() => {
  // Web Speech API desteği kontrolü
  if ('webkitSpeechRecognition' in window) {
    recognition.value = new webkitSpeechRecognition()
  } else if ('SpeechRecognition' in window) {
    recognition.value = new SpeechRecognition()
  }
  
  if (recognition.value) {
    recognition.value.continuous = false
    recognition.value.interimResults = true
    recognition.value.lang = 'tr-TR'
    
    recognition.value.onstart = () => {
      isListening.value = true
    }
    
    recognition.value.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        } else {
          interimTranscript += event.results[i][0].transcript
        }
      }
      
      // Show interim results as user speaks
      transcript.value = finalTranscript || interimTranscript
      
      if (finalTranscript) {
        emit('voice-result', finalTranscript)
        // Clear transcript after sending
        setTimeout(() => {
          transcript.value = ''
        }, 500)
      }
    }
    
    recognition.value.onend = () => {
      isRecording.value = false
      isListening.value = false
    }
    
    recognition.value.onerror = (event) => {
      console.error('Ses tanıma hatası:', event.error)
      isRecording.value = false
      isListening.value = false
    }
  }
})

onUnmounted(() => {
  if (recognition.value && isRecording.value) {
    recognition.value.stop()
  }
})

const toggleVoiceRecording = () => {
  if (!recognition.value) {
    alert('Tarayıcınız ses tanımayı desteklemiyor.')
    return
  }
  
  if (isRecording.value) {
    recognition.value.stop()
  } else {
    transcript.value = ''
    isRecording.value = true
    recognition.value.start()
  }
}
</script>

<style scoped>
.voice-command {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.voice-btn {
  @apply p-3 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-200;
  border: none;
  cursor: pointer;
}

.voice-btn.recording {
  @apply bg-red-500 hover:bg-red-600;
}

.listening-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.audio-waves {
  display: flex;
  gap: 2px;
}

.wave {
  width: 3px;
  height: 10px;
  background: #3b82f6;
  animation: wave 1s infinite ease-in-out;
}

.wave:nth-child(2) {
  animation-delay: 0.1s;
}

.wave:nth-child(3) {
  animation-delay: 0.2s;
}

@keyframes wave {
  0%, 40%, 100% {
    transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
  }
}

.transcript {
  @apply p-2 bg-gray-100 rounded max-w-xs text-center;
}
</style>
