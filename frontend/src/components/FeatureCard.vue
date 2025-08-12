<template>
  <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 text-center border border-gray-200/50 dark:border-gray-700/50 hover:border-purple-300/50 dark:hover:border-purple-400/50 transform hover:-translate-y-0.5 hover:scale-105">
    <div class="w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center text-white text-lg mx-auto mb-3 shadow-md">
      {{ icon || '✨' }}
    </div>
    <h3 class="font-semibold text-gray-800 dark:text-gray-100 text-base mb-2 font-sans">{{ title }}</h3>
    <p class="text-gray-600 dark:text-gray-300 text-xs leading-relaxed font-sans">{{ description }}</p>
    <div class="mt-3">
      <button class="text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 text-xs font-medium transition-colors">
        Detaylı Bilgi →
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '7/24 Hizmet'
  },
  description: {
    type: String,
    default: 'Her zaman yanınızda destek.'
  },
  icon: {
    type: String,
    default: '✨'
  }
})
</script> 