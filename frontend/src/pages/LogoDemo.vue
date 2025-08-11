<template>
  <div class="min-h-screen relative overflow-hidden">
    <!-- Static Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-black via-dark-gray to-dark-purple"></div>

    <div class="container mx-auto px-4 py-8 relative z-10">
      <!-- Dark Mode Toggle -->
      <div class="text-center mb-6">
        <button @click="toggleDarkMode" class="btn p-3 rounded-full backdrop-blur-sm shadow-lg hover:shadow-xl transform hover:scale-105">
          <span class="text-white text-lg">{{ darkMode ? '☀️' : '🌙' }}</span>
        </button>
      </div>
      
      <h1 class="title text-4xl mb-8">Choyrens AI Logo Koleksiyonu</h1>
      
      <!-- Logo Showcase -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <!-- Ana Logo -->
        <div class="card">
          <h3 class="text-xl font-bold text-white mb-4">✨ Ana Logo</h3>
          <div class="flex justify-center">
            <ChoyrensLogo :darkMode="true" />
          </div>
        </div>
        
        <!-- Light Mode Logo -->
        <div class="card">
          <h3 class="text-xl font-bold text-white mb-4">☀️ Light Mode</h3>
          <div class="flex justify-center">
            <ChoyrensLogo :darkMode="false" />
          </div>
        </div>
        
        <!-- Büyük Logo -->
        <div class="card">
          <h3 class="text-xl font-bold text-white mb-4">🔍 Büyük Boyut</h3>
          <div class="flex justify-center">
            <ChoyrensLogo :darkMode="true" size="large" />
          </div>
        </div>
      </div>
      
      <!-- Renk Paleti -->
      <div class="card mb-8">
        <h2 class="title text-2xl mb-6">Renk Paleti</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-2 rounded-lg bg-primary-purple"></div>
            <p class="text-white text-sm">Primary Purple</p>
            <p class="text-white/60 text-xs">#9333ea</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-2 rounded-lg bg-secondary-purple"></div>
            <p class="text-white text-sm">Secondary Purple</p>
            <p class="text-white/60 text-xs">#8e44ad</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-2 rounded-lg bg-light-purple"></div>
            <p class="text-white text-sm">Light Purple</p>
            <p class="text-white/60 text-xs">#a855f7</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-2 rounded-lg bg-lavender"></div>
            <p class="text-white text-sm">Lavender</p>
            <p class="text-white/60 text-xs">#e9d5ff</p>
          </div>
        </div>
      </div>
      
      <!-- Animasyon Örnekleri -->
      <div class="card">
        <h2 class="title text-2xl mb-6">Animasyon Efektleri</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary-purple glow-effect"></div>
            <p class="text-white">Glow Effect</p>
          </div>
          <div class="text-center">
            <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-secondary-purple float-animation"></div>
            <p class="text-white">Float Animation</p>
          </div>
          <div class="text-center">
            <div class="w-20 h-20 mx-auto mb-4 rounded-lg gradient-animation"></div>
            <p class="text-white">Gradient Shift</p>
          </div>
        </div>
      </div>
      
      <!-- Geri Dön Butonu -->
      <div class="text-center mt-8">
        <router-link to="/" class="btn px-6 py-3">
          ← Ana Sayfaya Dön
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChoyrensLogo from '../components/ChoyrensLogo.vue'

const darkMode = ref(false)

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

onMounted(() => {
  // Check for saved dark mode preference
  const savedDarkMode = localStorage.getItem('darkMode')
  if (savedDarkMode === 'true') {
    darkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    darkMode.value = false
    document.documentElement.classList.remove('dark')
  }
})
</script>

<style scoped>
.bg-primary-purple { background-color: var(--primary-purple); }
.bg-secondary-purple { background-color: var(--secondary-purple); }
.bg-light-purple { background-color: var(--light-purple); }
.bg-lavender { background-color: var(--lavender); }
</style> 