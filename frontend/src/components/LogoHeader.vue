<template>
  <div class="header-logo" :class="{ 'dark-mode': darkMode }">
          <div class="logo-container">
        <div class="main-logo">
          <div class="logo-text" :class="currentTheme === 'monochrome' ? 'monochrome' : ''">
            Choyrens<span class="ai-part"> AI</span>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'LogoHeader',
  props: {
    darkMode: {
      type: Boolean,
      default: false
    },
    currentTheme: {
      type: String,
      default: 'blue'
    }
  }
}
</script>

<style scoped>
.header-logo {
  display: inline-block;
  font-family: 'Inter', sans-serif;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-family: 'Inter', sans-serif;
  font-size: 24px;
  font-weight: 800;
  color: var(--dark-purple);
}

.logo-text .ai-part {
  color: var(--primary-purple);
}

.dark-mode .logo-text {
  color: var(--white);
}

/* Monokrom tema için özel stil */
.logo-text.monochrome {
  color: #000000;
}

.logo-text.monochrome .ai-part {
  color: #000000;
}


</style> 