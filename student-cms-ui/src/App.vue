<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()
const route = useRoute()

onMounted(() => {
  // Initialize auth state from localStorage
  authStore.initializeAuth()
  
  // Fetch notifications if user is authenticated
  if (authStore.isAuthenticated) {
    notificationsStore.fetchUnreadCount()
  }
})

// Check if current route is public
const isPublicRoute = () => {
  return route.meta?.public || false
}
</script>

<template>
  <div id="app">
    <!-- Public Layout -->
    <div v-if="isPublicRoute() || !authStore.isAuthenticated" class="public-layout">
      <router-view />
    </div>
    
    <!-- Authenticated Layout -->
    <div v-else class="authenticated-layout">
      <AppNavbar />
      <div class="main-content">
        <AppSidebar />
        <main class="content-area">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.public-layout {
  min-height: 100vh;
}

.authenticated-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  flex: 1;
  min-height: calc(100vh - 60px); /* Subtract navbar height */
}

.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .content-area {
    padding: 15px;
  }
}
</style>
