<template>
  <div class="bot-message-actions mt-3 flex items-center justify-between">
    <!-- Left Side: Like/Dislike Buttons -->
    <div class="flex items-center gap-2">
      <!-- Like Button -->
      <button
        @click="toggleLike"
        class="action-btn p-2 rounded-lg transition-all duration-300 hover:scale-110"
        :class="[
          feedback.liked ? 'bg-green-100 text-green-600' : 'hover:bg-gray-100',
          currentTheme === 'monochrome' ? 'hover:bg-gray-200' : ''
        ]"
        title="Beğen"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-5 w-5 transition-transform duration-300" 
          :class="feedback.liked ? 'scale-110' : ''"
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
        </svg>
      </button>

      <!-- Dislike Button -->
      <button
        @click="toggleDislike"
        class="action-btn p-2 rounded-lg transition-all duration-300 hover:scale-110"
        :class="[
          feedback.disliked ? 'bg-red-100 text-red-600' : 'hover:bg-gray-100',
          currentTheme === 'monochrome' ? 'hover:bg-gray-200' : ''
        ]"
        title="Beğenme"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-5 w-5 transition-transform duration-300" 
          :class="feedback.disliked ? 'scale-110 rotate-180' : ''"
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.106-1.79l-.05-.025A4 4 0 0011.057 2H5.641a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
        </svg>
      </button>

      <!-- Emotion Selection -->
      <div class="relative ml-2">
        <button
          @click="toggleEmotionMenu"
          class="action-btn p-2 rounded-lg transition-all duration-300 hover:scale-110"
          :class="[
            feedback.emotion ? getEmotionButtonStyle : 'hover:bg-gray-100',
            currentTheme === 'monochrome' ? 'hover:bg-gray-200' : ''
          ]"
          title="Duygu durumu seç"
        >
          <span class="text-lg">{{ feedback.emotion || '😊' }}</span>
        </button>

        <!-- Emotion Dropdown -->
        <div
          v-if="showEmotionMenu"
          class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 p-3"
          :class="darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'"
        >
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="emotion in emotions"
              :key="emotion.emoji"
              @click="selectEmotion(emotion)"
              class="emotion-btn p-2 rounded-lg hover:bg-gray-100 transition-all duration-200 hover:scale-110"
              :class="[
                feedback.emotion === emotion.emoji ? 'bg-blue-100 ring-2 ring-blue-500' : '',
                darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
              ]"
              :title="emotion.name"
            >
              <span class="text-2xl">{{ emotion.emoji }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side: Voice Playback Button -->
    <div class="flex items-center gap-2">
      <button
        @click="toggleSpeech"
        class="action-btn p-2 rounded-lg transition-all duration-300 hover:scale-110"
        :class="[
          isPlaying ? 'bg-blue-100 text-blue-600 animate-pulse' : 'hover:bg-gray-100',
          currentTheme === 'monochrome' ? 'hover:bg-gray-200' : ''
        ]"
        :title="isPlaying ? 'Durak' : 'Sesli oku'"
        :disabled="!isSpeechSupported"
      >
        <svg 
          v-if="!isPlaying"
          xmlns="http://www.w3.org/2000/svg" 
          class="h-5 w-5" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 14.142M9 9a3 3 0 000 6H12l3 3V6l-3 3H9z" />
        </svg>
        <svg 
          v-else
          xmlns="http://www.w3.org/2000/svg" 
          class="h-5 w-5" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BotMessageActions',
  props: {
    messageId: {
      type: String,
      required: true
    },
    messageText: {
      type: String,
      required: true
    },
    darkMode: {
      type: Boolean,
      default: false
    },
    currentTheme: {
      type: String,
      default: 'blue'
    }
  },
  emits: ['feedback-changed'],
  data() {
    return {
      feedback: {
        liked: false,
        disliked: false,
        emotion: null
      },
      showEmotionMenu: false,
      isPlaying: false,
      speechSynthesis: null,
      isSpeechSupported: false,
      emotions: [
        { emoji: '😊', name: 'Mutlu' },
        { emoji: '😍', name: 'Harika' },
        { emoji: '😂', name: 'Komik' },
        { emoji: '😐', name: 'Normal' },
        { emoji: '😕', name: 'Üzgün' },
        { emoji: '😠', name: 'Kızgın' }
      ]
    }
  },
  computed: {
    getEmotionButtonStyle() {
      const themeColors = {
        'blue': 'bg-blue-100 text-blue-600',
        'burgundy': 'bg-red-100 text-red-600',
        'purple': 'bg-purple-100 text-purple-600',
        'emerald': 'bg-emerald-100 text-emerald-600',
        'monochrome': 'bg-gray-100 text-gray-600'
      }
      
      return themeColors[this.currentTheme] || themeColors['blue']
    }
  },
  mounted() {
    // Check for Speech Synthesis support
    this.isSpeechSupported = 'speechSynthesis' in window
    if (this.isSpeechSupported) {
      this.speechSynthesis = window.speechSynthesis
    }

    // Load saved feedback from localStorage
    this.loadFeedback()

    // Add click outside listener for emotion menu
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    // Stop any ongoing speech
    if (this.speechSynthesis) {
      this.speechSynthesis.cancel()
    }
    
    // Remove event listener
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    toggleLike() {
      this.feedback.liked = !this.feedback.liked
      if (this.feedback.liked) {
        this.feedback.disliked = false
      }
      this.saveFeedback()
      this.emitFeedback()
    },
    
    toggleDislike() {
      this.feedback.disliked = !this.feedback.disliked
      if (this.feedback.disliked) {
        this.feedback.liked = false
      }
      this.saveFeedback()
      this.emitFeedback()
    },
    
    toggleEmotionMenu() {
      this.showEmotionMenu = !this.showEmotionMenu
    },
    
    selectEmotion(emotion) {
      this.feedback.emotion = emotion.emoji
      this.showEmotionMenu = false
      this.saveFeedback()
      this.emitFeedback()
    },
    
    toggleSpeech() {
      if (!this.isSpeechSupported) return
      
      if (this.isPlaying) {
        this.speechSynthesis.cancel()
        this.isPlaying = false
      } else {
        this.speakText()
      }
    },
    
    speakText() {
      if (!this.isSpeechSupported || !this.messageText) return
      
      const utterance = new SpeechSynthesisUtterance(this.messageText)
      utterance.lang = 'tr-TR' // Turkish language
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 0.8
      
      utterance.onstart = () => {
        this.isPlaying = true
      }
      
      utterance.onend = () => {
        this.isPlaying = false
      }
      
      utterance.onerror = () => {
        this.isPlaying = false
        console.error('Speech synthesis error')
      }
      
      this.speechSynthesis.speak(utterance)
    },
    
    handleClickOutside(event) {
      if (this.showEmotionMenu && !event.target.closest('.relative')) {
        this.showEmotionMenu = false
      }
    },
    
    saveFeedback() {
      const feedbackData = JSON.parse(localStorage.getItem('botMessageFeedback') || '{}')
      feedbackData[this.messageId] = this.feedback
      localStorage.setItem('botMessageFeedback', JSON.stringify(feedbackData))
    },
    
    loadFeedback() {
      const feedbackData = JSON.parse(localStorage.getItem('botMessageFeedback') || '{}')
      if (feedbackData[this.messageId]) {
        this.feedback = { ...feedbackData[this.messageId] }
      }
    },
    
    emitFeedback() {
      this.$emit('feedback-changed', {
        messageId: this.messageId,
        feedback: this.feedback
      })
    }
  }
}
</script>

<style scoped>
.bot-message-actions {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 8px;
  margin-top: 8px;
}

.action-btn {
  border: none;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  min-height: 36px;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.emotion-btn {
  border: none;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 44px;
}

.dark-mode .action-btn:hover {
  background-color: rgba(55, 65, 81, 0.5) !important;
}

.dark-mode .emotion-btn:hover {
  background-color: rgba(55, 65, 81, 0.5) !important;
}

/* Animation for selected states */
.action-btn.bg-green-100 {
  animation: likePressed 0.3s ease-out;
}

.action-btn.bg-red-100 {
  animation: dislikePressed 0.3s ease-out;
}

@keyframes likePressed {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1.1); }
}

@keyframes dislikePressed {
  0% { transform: scale(1); }
  50% { transform: scale(1.2) rotate(180deg); }
  100% { transform: scale(1.1) rotate(180deg); }
}
</style>
