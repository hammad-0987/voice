import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { MotionPlugin } from '@vueuse/motion'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import App from './App.vue'
import router from './router'
import './assets/css/main.css'

// Create pinia store
const pinia = createPinia()

// Toast configuration
const toastOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  transition: 'Vue-Toastification__bounce',
  maxToasts: 20,
  newestOnTop: true
}

// Create app
const app = createApp(App)

// Use plugins
app.use(pinia)
app.use(router)
app.use(MotionPlugin)
app.use(Toast, toastOptions)

// Global properties
app.config.globalProperties.$filters = {
  currency(value) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value)
  },
  date(value) {
    return new Date(value).toLocaleDateString()
  },
  datetime(value) {
    return new Date(value).toLocaleString()
  }
}

// Mount app
app.mount('#app')
