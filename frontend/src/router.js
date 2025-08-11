import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Chat from './pages/Chat.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import LogoDemo from './pages/LogoDemo.vue'
import TelekomServices from './pages/TelekomServices.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/logo-demo',
    name: 'LogoDemo',
    component: LogoDemo
  },
  {
    path: '/telekom-services',
    name: 'TelekomServices',
    component: TelekomServices
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 