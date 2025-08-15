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
        @click="reportMessage"
        class="action-btn text-red-500"
        title="Şikayet et"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
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

const emit = defineEmits(['like', 'dislike', 'report'])

const isLiked = ref(false)
const isDisliked = ref(false)
const showCopySuccess = ref(false)

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

const reportMessage = () => {
  if (confirm('Bu mesajı şikayet etmek istediğinizden emin misiniz?')) {
    emit('report', {
      messageId: props.messageId,
      message: props.message
    })
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
</style>
