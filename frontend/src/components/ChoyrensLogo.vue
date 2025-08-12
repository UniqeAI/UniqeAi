<template>
  <div class="logo-container" :class="{ 'dark-mode': darkMode }">
    <div class="logo-size">
      <div class="main-logo">
        <div class="logo-icon">
          <div class="rotating-c-container">
            <div class="rotating-c">
              <div class="c-letter-main"></div>
            </div>
            <div class="orbital-ring"></div>
            <div class="particle"></div>
          </div>
          
          <div class="network-nodes">
            <div class="network-node"></div>
            <div class="network-node"></div>
            <div class="network-node"></div>
            <div class="network-connection"></div>
            <div class="network-connection"></div>
          </div>
        </div>
        
        <div class="logo-text">
          Cayros<span class="ai-part">AI</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChoyrensLogo',
  props: {
    darkMode: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium'
    }
  }
}
</script>

<style scoped>
.logo-container {
  display: inline-block;
  font-family: 'Inter', sans-serif;
}

.logo-size {
  width: 120px;
  height: 60px;
}

.main-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 100%;
}

.logo-icon {
  position: relative;
  width: 48px;
  height: 48px;
}

.rotating-c-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rotating-c {
  width: 40px;
  height: 40px;
  position: relative;
  animation: rotate 8s linear infinite;
}

.c-letter-main {
  width: 40px;
  height: 40px;
  border: 3px solid transparent;
  border-left: 3px solid var(--primary-purple);
  border-top: 3px solid var(--primary-purple);
  border-bottom: 3px solid var(--primary-purple);
  border-radius: 50%;
  position: relative;
  background: rgba(147, 51, 234, 0.1);
}

.c-letter-main::before {
  content: 'C';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--primary-purple);
  font-size: 18px;
  font-weight: 800;
  font-family: 'Inter', sans-serif;
}

.orbital-ring {
  position: absolute;
  width: 48px;
  height: 48px;
  border: 1px solid rgba(147, 51, 234, 0.3);
  border-radius: 50%;
  animation: rotate-reverse 12s linear infinite;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--primary-purple);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: particle-float 3s ease-in-out infinite;
}

.network-nodes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.network-node {
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--primary-purple);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.network-node:nth-child(1) {
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 0s;
}

.network-node:nth-child(2) {
  top: 50%;
  right: -8px;
  transform: translateY(-50%);
  animation-delay: 0.5s;
}

.network-node:nth-child(3) {
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 1s;
}

.network-connection {
  position: absolute;
  width: 2px;
  height: 20px;
  background: linear-gradient(to bottom, var(--primary-purple), transparent);
  border-radius: 1px;
  animation: pulse 3s ease-in-out infinite;
}

.network-connection:nth-child(4) {
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 0.25s;
}

.network-connection:nth-child(5) {
  top: 50%;
  right: -4px;
  transform: translateY(-50%) rotate(90deg);
  animation-delay: 0.75s;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  color: var(--dark-purple);
  text-shadow: 0 0 10px rgba(147, 51, 234, 0.3);
  animation: text-glow 3s ease-in-out infinite;
}

.ai-part {
  background: linear-gradient(135deg, var(--primary-purple) 0%, var(--light-purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Dark mode styles */
.dark-mode .logo-text {
  color: var(--white);
  text-shadow: 0 0 10px rgba(147, 51, 234, 0.5);
}

.dark-mode .c-letter-main {
  background: rgba(147, 51, 234, 0.2);
}

.dark-mode .orbital-ring {
  border-color: rgba(147, 51, 234, 0.5);
}

.dark-mode .network-node {
  background: var(--light-purple);
}

.dark-mode .network-connection {
  background: linear-gradient(to bottom, var(--light-purple), transparent);
}

/* Animations */
@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes rotate-reverse {
  0% { transform: rotate(360deg); }
  100% { transform: rotate(0deg); }
}

@keyframes pulse {
  0%, 100% { 
    opacity: 0.6;
    transform: scale(1); 
  }
  50% { 
    opacity: 1;
    transform: scale(1.3); 
  }
}

@keyframes text-glow {
  0%, 100% {
    text-shadow: 0 0 10px rgba(147, 51, 234, 0.3);
  }
  50% {
    text-shadow: 0 0 20px rgba(147, 51, 234, 0.6);
  }
}

@keyframes particle-float {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 1;
  }
}

/* Hover effects */
.logo-container:hover .rotating-c {
  animation-duration: 4s;
}

.logo-container:hover .network-node {
  animation-duration: 1s;
  transform: scale(1.5);
}

.logo-container:hover .network-connection {
  animation-duration: 1.5s;
}

.logo-container:hover .rotating-c-container {
  transform: scale(1.05);
}

.logo-container:hover .c-letter-main::before {
  color: var(--light-purple);
}

.logo-container:hover .logo-text {
  animation-duration: 1.5s;
}

.logo-container:hover .particle {
  animation-duration: 1.5s;
  transform: translate(-50%, -50%) scale(1.5);
}
</style> 