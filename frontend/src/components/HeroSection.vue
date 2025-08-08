<template>
  <section class="flex flex-col justify-center items-center min-h-screen text-center bg-secondary">
    <h1 class="text-4xl font-bold text-primary mb-4">Choyrens AI</h1>
    <p class="text-gray-600 max-w-xl mx-auto mb-8">Akıllı Telekom Müşteri Hizmetleri Asistanı</p>
    <div class="flex justify-center gap-4">
      <router-link 
        to="/chat"
        class="bg-primary text-white px-6 py-2 rounded hover:bg-purple-700 transition-colors"
      >
        Hemen Başla
      </router-link>
      <button 
        @click="login"
        class="border border-primary text-primary px-6 py-2 rounded hover:bg-primary hover:text-white transition-colors"
      >
        Giriş Yap
      </button>
    </div>
  </section>
</template>

<script setup>
const login = () => {
  // Navigate to login page
  console.log('Going to login...')
  // You can implement actual navigation here
}
</script> 