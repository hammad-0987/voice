<template>
  <nav class="header sticky top-0 z-40">
    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Left side - Brand and mobile menu -->
        <div class="flex items-center">
          <!-- Mobile menu button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
          >
            <Bars3Icon v-if="!showMobileMenu" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>

          <!-- Brand -->
          <router-link
            to="/dashboard"
            class="flex items-center space-x-3 ml-2 md:ml-0"
          >
            <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <AcademicCapIcon class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-bold gradient-text hidden sm:block">
              Student Voice
            </span>
          </router-link>
        </div>

        <!-- Center - Search (hidden on mobile) -->
        <div class="hidden md:flex flex-1 max-w-md mx-8">
          <div class="relative w-full">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search complaints, users..."
              class="w-full pl-10 pr-4 py-2 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
          </div>
        </div>

        <!-- Right side - Actions and user menu -->
        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <div class="relative">
            <button
              @click="toggleNotifications"
              class="p-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200 relative"
            >
              <BellIcon class="w-6 h-6" />
              <span
                v-if="notificationsStore.unreadCount > 0"
                class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-medium"
              >
                {{ notificationsStore.unreadCount > 9 ? '9+' : notificationsStore.unreadCount }}
              </span>
            </button>

            <!-- Notifications dropdown -->
            <transition name="dropdown">
              <div
                v-if="showNotifications"
                class="absolute right-0 mt-2 w-80 bg-white dark:bg-slate-800 rounded-xl shadow-hard border border-slate-200 dark:border-slate-700 z-50"
              >
                <div class="p-4 border-b border-slate-200 dark:border-slate-700">
                  <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100">
                      Notifications
                    </h3>
                    <span class="text-sm text-slate-500 dark:text-slate-400">
                      {{ notificationsStore.unreadCount }} unread
                    </span>
                  </div>
                </div>
                
                <div class="max-h-96 overflow-y-auto">
                  <div v-if="notifications.length === 0" class="p-8 text-center">
                    <BellIcon class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
                    <p class="text-slate-500 dark:text-slate-400">No notifications</p>
                  </div>
                  
                  <div v-else>
                    <div
                      v-for="notification in notifications.slice(0, 5)"
                      :key="notification.id"
                      @click="markAsRead(notification)"
                      class="p-4 hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer transition-colors duration-200 border-l-4"
                      :class="notification.is_read ? 'border-transparent' : 'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20'"
                    >
                      <p class="text-sm text-slate-900 dark:text-slate-100 mb-1">
                        {{ notification.message }}
                      </p>
                      <p class="text-xs text-slate-500 dark:text-slate-400">
                        {{ formatDate(notification.created_at) }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div v-if="notifications.length > 5" class="p-4 border-t border-slate-200 dark:border-slate-700">
                  <router-link
                    to="/notifications"
                    class="block text-center text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium"
                  >
                    View all notifications
                  </router-link>
                </div>
              </div>
            </transition>
          </div>

          <!-- User menu -->
          <div class="relative">
            <button
              @click="toggleUserMenu"
              class="flex items-center space-x-3 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
            >
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">
                  {{ authStore.user?.first_name?.charAt(0) }}{{ authStore.user?.last_name?.charAt(0) }}
                </span>
              </div>
              <div class="hidden md:block text-left">
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
                </p>
                <p class="text-xs text-slate-500 dark:text-slate-400 capitalize">
                  {{ authStore.user?.role }}
                </p>
              </div>
              <ChevronDownIcon class="w-4 h-4 text-slate-400" />
            </button>

            <!-- User dropdown -->
            <transition name="dropdown">
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-56 bg-white dark:bg-slate-800 rounded-xl shadow-hard border border-slate-200 dark:border-slate-700 z-50"
              >
                <div class="p-4 border-b border-slate-200 dark:border-slate-700">
                  <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                    {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
                  </p>
                  <p class="text-xs text-slate-500 dark:text-slate-400">
                    {{ authStore.user?.email }}
                  </p>
                  <span class="inline-block mt-1 px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 rounded-full capitalize">
                    {{ authStore.user?.role }}
                  </span>
                </div>
                
                <div class="py-2">
                  <router-link
                    to="/profile"
                    class="flex items-center px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
                  >
                    <UserIcon class="w-4 h-4 mr-3" />
                    Profile
                  </router-link>
                  <router-link
                    to="/settings"
                    class="flex items-center px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
                  >
                    <CogIcon class="w-4 h-4 mr-3" />
                    Settings
                  </router-link>
                </div>
                
                <div class="py-2 border-t border-slate-200 dark:border-slate-700">
                  <button
                    @click="logout"
                    class="flex items-center w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200"
                  >
                    <ArrowRightOnRectangleIcon class="w-4 h-4 mr-3" />
                    Logout
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <transition name="mobile-menu">
      <div
        v-if="showMobileMenu"
        class="md:hidden bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl border-t border-slate-200 dark:border-slate-700"
      >
        <div class="px-4 py-4 space-y-2">
          <!-- Mobile search -->
          <div class="relative mb-4">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search..."
              class="w-full pl-10 pr-4 py-2 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <!-- Mobile navigation links would go here -->
          <router-link
            to="/dashboard"
            class="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
          >
            Dashboard
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Bars3Icon,
  XMarkIcon,
  BellIcon,
  MagnifyingGlassIcon,
  UserIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
  ChevronDownIcon,
  AcademicCapIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '../../stores/auth'
import { useNotificationsStore } from '../../stores/notifications'
import { formatDistanceToNow } from 'date-fns'

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()

const showMobileMenu = ref(false)
const showNotifications = ref(false)
const showUserMenu = ref(false)
const notifications = ref([])

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  showNotifications.value = false
  showUserMenu.value = false
}

const toggleNotifications = async () => {
  showNotifications.value = !showNotifications.value
  showUserMenu.value = false
  showMobileMenu.value = false
  
  if (showNotifications.value && notifications.value.length === 0) {
    await fetchNotifications()
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
  showMobileMenu.value = false
}

const fetchNotifications = async () => {
  try {
    const response = await notificationsStore.fetchNotifications()
    notifications.value = response
  } catch (error) {
    console.error('Error fetching notifications:', error)
  }
}

const markAsRead = async (notification) => {
  try {
    await notificationsStore.markAsRead(notification.id)
    notification.is_read = true
    
    if (notification.link) {
      // Handle navigation
      console.log('Navigate to:', notification.link)
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

const formatDate = (date) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

const logout = async () => {
  try {
    await authStore.logout()
  } catch (error) {
    console.error('Logout error:', error)
  }
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showNotifications.value = false
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  notificationsStore.fetchUnreadCount()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

