<script setup>
import { ref, onMounted, provide, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'
import { useNotificationsStore } from './stores/notifications'
import ThemeToggle from './components/common/ThemeToggle.vue'
import LoadingOverlay from './components/common/LoadingOverlay.vue'
import AppNavbar from './components/layout/AppNavbar.vue'
import AppSidebar from './components/layout/AppSidebar.vue'

// Stores
const authStore = useAuthStore()
const themeStore = useThemeStore()
const notificationsStore = useNotificationsStore()
const router = useRouter()
const route = useRoute()

// Global loading state
const isLoading = ref(false)

// Provide global loading state
provide('isLoading', isLoading)

// Computed properties
const isPublicRoute = computed(() => {
  return route.meta?.public || false
})

const isAuthenticated = computed(() => {
  return authStore.isAuthenticated
})

// Initialize app
onMounted(async () => {
  // Initialize theme
  themeStore.initializeTheme()
  
  // Initialize auth state from localStorage
  await authStore.initializeAuth()
  
  // Fetch notifications if user is authenticated
  if (authStore.isAuthenticated) {
    notificationsStore.fetchUnreadCount()
  }
})

// Router loading states
router.beforeEach((to, from, next) => {
  isLoading.value = true
  next()
})

router.afterEach(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 300)
})
</script>

<template>
  <div id="app" class="min-h-screen">
    <!-- Background Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <!-- Animated background shapes -->
      <div class="absolute top-10 left-10 w-72 h-72 bg-blue-400/10 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-1/2 right-10 w-96 h-96 bg-indigo-400/10 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-10 left-1/3 w-80 h-80 bg-purple-400/10 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <!-- Theme Toggle (always visible) -->
    <ThemeToggle />

    <!-- Main Content -->
    <div class="relative z-10">
      <!-- Public Layout -->
      <div v-if="isPublicRoute || !isAuthenticated" class="public-layout">
        <router-view v-slot="{ Component, route }">
          <transition
            :name="route.meta.transition || 'fade'"
            mode="out-in"
            appear
          >
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </div>
      
      <!-- Authenticated Layout -->
      <div v-else class="authenticated-layout">
        <AppNavbar />
        <div class="main-content">
          <AppSidebar />
          <main class="content-area">
            <router-view v-slot="{ Component, route }">
              <transition
                :name="route.meta.transition || 'slide-left'"
                mode="out-in"
                appear
              >
                <component :is="Component" :key="route.path" />
              </transition>
            </router-view>
          </main>
        </div>
      </div>
    </div>

    <!-- Global Loading Overlay -->
    <LoadingOverlay v-if="isLoading" />

    <!-- Notification Container -->
    <div id="toast-container"></div>
  </div>
</template>

<style scoped>
#app {
  @apply min-h-screen;
}

.public-layout {
  @apply min-h-screen;
}

.authenticated-layout {
  @apply min-h-screen flex flex-col;
}

.main-content {
  @apply flex flex-1;
  min-height: calc(100vh - 4rem); /* Subtract navbar height */
}

.content-area {
  @apply flex-1 p-6 overflow-y-auto;
  @apply bg-gradient-to-br from-slate-50/50 via-blue-50/30 to-indigo-50/50;
  @apply dark:from-slate-900/50 dark:via-slate-800/30 dark:to-slate-900/50;
}

@media (max-width: 768px) {
  .main-content {
    @apply flex-col;
  }
  
  .content-area {
    @apply p-4;
  }
}

/* Page transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.3s ease;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
