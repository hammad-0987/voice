<template>
  <aside class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- Sidebar Header -->
    <div class="sidebar-header">
      <div class="flex items-center justify-between">
        <div v-if="!isCollapsed" class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
            <AcademicCapIcon class="w-5 h-5 text-white" />
          </div>
          <span class="text-lg font-bold gradient-text">Student Voice</span>
        </div>
        
        <button
          @click="toggleSidebar"
          class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
        >
          <ChevronLeftIcon v-if="!isCollapsed" class="w-5 h-5 text-slate-600 dark:text-slate-400" />
          <ChevronRightIcon v-else class="w-5 h-5 text-slate-600 dark:text-slate-400" />
        </button>
      </div>
    </div>

    <!-- User Profile Section -->
    <div v-if="!isCollapsed" class="user-profile">
      <div class="flex items-center space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl">
        <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full flex items-center justify-center">
          <span class="text-white text-sm font-medium">
            {{ authStore.user?.first_name?.charAt(0) }}{{ authStore.user?.last_name?.charAt(0) }}
          </span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">
            {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
          </p>
          <p class="text-xs text-slate-500 dark:text-slate-400 capitalize">
            {{ authStore.user?.role }}
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="sidebar-nav">
      <div class="space-y-2">
        <!-- Main Navigation -->
        <div v-for="section in navigationSections" :key="section.title" class="nav-section">
          <h3 v-if="!isCollapsed && section.title" class="nav-section-title">
            {{ section.title }}
          </h3>
          
          <ul class="space-y-1">
            <li v-for="item in section.items" :key="item.name">
              <!-- Regular nav item -->
              <router-link
                v-if="!item.children"
                :to="item.route"
                class="nav-link"
                :class="{ 'active': isActiveRoute(item.route) }"
                :title="isCollapsed ? item.label : ''"
              >
                <component :is="item.icon" class="nav-icon" />
                <span v-if="!isCollapsed" class="nav-label">{{ item.label }}</span>
                <span
                  v-if="item.badge && !isCollapsed"
                  class="nav-badge"
                  :class="getBadgeClass(item.badgeType)"
                >
                  {{ item.badge }}
                </span>
              </router-link>

              <!-- Expandable nav item -->
              <div v-else>
                <button
                  @click="toggleSubmenu(item.name)"
                  class="nav-link w-full"
                  :class="{ 'active': hasActiveChild(item.children) }"
                >
                  <component :is="item.icon" class="nav-icon" />
                  <span v-if="!isCollapsed" class="nav-label flex-1 text-left">{{ item.label }}</span>
                  <ChevronDownIcon
                    v-if="!isCollapsed"
                    class="w-4 h-4 transition-transform duration-200"
                    :class="{ 'rotate-180': expandedMenus.includes(item.name) }"
                  />
                </button>
                
                <!-- Submenu -->
                <transition name="submenu">
                  <ul
                    v-if="!isCollapsed && expandedMenus.includes(item.name)"
                    class="submenu"
                  >
                    <li v-for="child in item.children" :key="child.name">
                      <router-link
                        :to="child.route"
                        class="submenu-link"
                        :class="{ 'active': isActiveRoute(child.route) }"
                      >
                        <component :is="child.icon" class="submenu-icon" />
                        <span class="submenu-label">{{ child.label }}</span>
                        <span
                          v-if="child.badge"
                          class="nav-badge"
                          :class="getBadgeClass(child.badgeType)"
                        >
                          {{ child.badge }}
                        </span>
                      </router-link>
                    </li>
                  </ul>
                </transition>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Quick Actions -->
    <div v-if="!isCollapsed && quickActions.length > 0" class="quick-actions">
      <h3 class="nav-section-title">Quick Actions</h3>
      <div class="space-y-2">
        <button
          v-for="action in quickActions"
          :key="action.name"
          @click="action.handler"
          class="quick-action-btn"
        >
          <component :is="action.icon" class="w-4 h-4" />
          <span class="text-sm font-medium">{{ action.label }}</span>
        </button>
      </div>
    </div>

    <!-- Sidebar Footer -->
    <div class="sidebar-footer">
      <div v-if="!isCollapsed" class="text-center">
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Student Voice CMS v2.0
        </p>
        <p class="text-xs text-slate-400 dark:text-slate-500">
          © 2024 All rights reserved
        </p>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  AcademicCapIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  HomeIcon,
  DocumentTextIcon,
  PlusCircleIcon,
  UserGroupIcon,
  BuildingOfficeIcon,
  ChartBarIcon,
  DocumentChartBarIcon,
  BellIcon,
  UserIcon,
  CogIcon,
  ExclamationTriangleIcon,
  ClipboardDocumentListIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '../../stores/auth'
import { useNotificationsStore } from '../../stores/notifications'

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()
const route = useRoute()

const isCollapsed = ref(false)
const expandedMenus = ref([])

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  // Save preference to localStorage
  localStorage.setItem('sidebarCollapsed', isCollapsed.value.toString())
}

const toggleSubmenu = (menuName) => {
  const index = expandedMenus.value.indexOf(menuName)
  if (index > -1) {
    expandedMenus.value.splice(index, 1)
  } else {
    expandedMenus.value.push(menuName)
  }
}

const isActiveRoute = (routePath) => {
  return route.path === routePath || route.path.startsWith(routePath + '/')
}

const hasActiveChild = (children) => {
  return children.some(child => isActiveRoute(child.route))
}

const getBadgeClass = (type) => {
  const classes = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    default: 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300'
  }
  return classes[type] || classes.default
}

// Navigation configuration based on user role
const navigationSections = computed(() => {
  const userRole = authStore.user?.role
  const sections = []

  // Main section - always present
  const mainSection = {
    title: 'Main',
    items: [
      {
        name: 'dashboard',
        label: 'Dashboard',
        route: '/dashboard',
        icon: HomeIcon
      }
    ]
  }

  // Role-specific sections
  if (userRole === 'student') {
    sections.push(mainSection)
    sections.push({
      title: 'Complaints',
      items: [
        {
          name: 'my-complaints',
          label: 'My Complaints',
          route: '/complaints',
          icon: DocumentTextIcon,
          badge: '3',
          badgeType: 'info'
        },
        {
          name: 'file-complaint',
          label: 'File Complaint',
          route: '/complaints/create',
          icon: PlusCircleIcon
        }
      ]
    })
    sections.push({
      title: 'Requests',
      items: [
        {
          name: 'withdrawals',
          label: 'Withdrawal Requests',
          route: '/withdrawals',
          icon: ArrowRightOnRectangleIcon
        }
      ]
    })
  } else if (userRole === 'staff') {
    sections.push(mainSection)
    sections.push({
      title: 'Management',
      items: [
        {
          name: 'complaints',
          label: 'Complaints',
          route: '/complaints',
          icon: DocumentTextIcon,
          badge: '12',
          badgeType: 'warning'
        },
        {
          name: 'withdrawals',
          label: 'Withdrawal Requests',
          route: '/withdrawals',
          icon: ArrowRightOnRectangleIcon,
          badge: '5',
          badgeType: 'info'
        }
      ]
    })
  } else if (userRole === 'head') {
    sections.push(mainSection)
    sections.push({
      title: 'Department',
      items: [
        {
          name: 'complaints',
          label: 'Complaints',
          route: '/complaints',
          icon: DocumentTextIcon,
          badge: '25',
          badgeType: 'warning'
        },
        {
          name: 'analytics',
          label: 'Analytics',
          route: '/analytics',
          icon: ChartBarIcon
        },
        {
          name: 'withdrawals',
          label: 'Withdrawal Requests',
          route: '/withdrawals',
          icon: ArrowRightOnRectangleIcon,
          badge: '8',
          badgeType: 'info'
        }
      ]
    })
  } else if (userRole === 'vc') {
    sections.push(mainSection)
    sections.push({
      title: 'System Overview',
      items: [
        {
          name: 'complaints',
          label: 'All Complaints',
          route: '/complaints',
          icon: DocumentTextIcon,
          badge: '156',
          badgeType: 'warning'
        },
        {
          name: 'analytics',
          label: 'Analytics',
          route: '/analytics',
          icon: ChartBarIcon
        },
        {
          name: 'reports',
          label: 'Reports',
          route: '/reports',
          icon: DocumentChartBarIcon
        }
      ]
    })
  } else if (userRole === 'admin') {
    sections.push(mainSection)
    sections.push({
      title: 'Administration',
      items: [
        {
          name: 'users',
          label: 'User Management',
          route: '/users',
          icon: UserGroupIcon
        },
        {
          name: 'departments',
          label: 'Departments',
          route: '/departments',
          icon: BuildingOfficeIcon
        },
        {
          name: 'complaints',
          label: 'All Complaints',
          route: '/complaints',
          icon: DocumentTextIcon,
          badge: '156',
          badgeType: 'warning'
        }
      ]
    })
    sections.push({
      title: 'Analytics',
      items: [
        {
          name: 'analytics',
          label: 'System Analytics',
          route: '/analytics',
          icon: ChartBarIcon
        },
        {
          name: 'reports',
          label: 'Reports',
          route: '/reports',
          icon: DocumentChartBarIcon
        }
      ]
    })
  }

  // Settings section - always present
  sections.push({
    title: 'Account',
    items: [
      {
        name: 'notifications',
        label: 'Notifications',
        route: '/notifications',
        icon: BellIcon,
        badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount.toString() : null,
        badgeType: 'danger'
      },
      {
        name: 'profile',
        label: 'Profile',
        route: '/profile',
        icon: UserIcon
      },
      {
        name: 'settings',
        label: 'Settings',
        route: '/settings',
        icon: CogIcon
      }
    ]
  })

  return sections
})

// Quick actions based on user role
const quickActions = computed(() => {
  const userRole = authStore.user?.role
  const actions = []

  if (userRole === 'student') {
    actions.push({
      name: 'file-complaint',
      label: 'File Complaint',
      icon: PlusCircleIcon,
      handler: () => {
        // Navigate to file complaint
        console.log('Navigate to file complaint')
      }
    })
  } else if (['staff', 'head', 'vc', 'admin'].includes(userRole)) {
    actions.push({
      name: 'urgent-complaints',
      label: 'Urgent Complaints',
      icon: ExclamationTriangleIcon,
      handler: () => {
        // Navigate to urgent complaints
        console.log('Navigate to urgent complaints')
      }
    })
  }

  return actions
})

onMounted(() => {
  // Restore sidebar state from localStorage
  const savedState = localStorage.getItem('sidebarCollapsed')
  if (savedState !== null) {
    isCollapsed.value = savedState === 'true'
  }
})
</script>

<style scoped>
.sidebar {
  @apply fixed left-0 top-16 h-[calc(100vh-4rem)] w-64;
  @apply bg-white/80 dark:bg-slate-900/80;
  @apply backdrop-blur-xl backdrop-saturate-150;
  @apply border-r border-slate-200 dark:border-slate-700;
  @apply shadow-soft;
  @apply transition-all duration-300 ease-in-out;
  @apply flex flex-col;
  @apply z-30;
}

.sidebar.collapsed {
  @apply w-16;
}

.sidebar-header {
  @apply p-4 border-b border-slate-200 dark:border-slate-700;
  @apply flex-shrink-0;
}

.user-profile {
  @apply p-4 flex-shrink-0;
}

.sidebar-nav {
  @apply flex-1 overflow-y-auto p-4;
  @apply scrollbar-hide;
}

.nav-section {
  @apply mb-6;
}

.nav-section-title {
  @apply text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider;
  @apply mb-3 px-3;
}

.nav-link {
  @apply flex items-center px-3 py-2.5 rounded-xl;
  @apply text-slate-600 dark:text-slate-400;
  @apply hover:text-slate-900 dark:hover:text-slate-100;
  @apply hover:bg-slate-100 dark:hover:bg-slate-700/50;
  @apply transition-all duration-200;
  @apply group;
}

.nav-link.active {
  @apply bg-gradient-to-r from-blue-500/10 to-indigo-500/10;
  @apply text-blue-600 dark:text-blue-400;
  @apply border-r-2 border-blue-500;
  @apply font-medium;
}

.nav-icon {
  @apply w-5 h-5 flex-shrink-0;
  @apply transition-colors duration-200;
}

.nav-label {
  @apply ml-3 text-sm font-medium;
  @apply transition-all duration-200;
}

.nav-badge {
  @apply ml-auto px-2 py-1 text-xs font-medium rounded-full;
  @apply transition-all duration-200;
}

.submenu {
  @apply mt-2 ml-8 space-y-1;
}

.submenu-link {
  @apply flex items-center px-3 py-2 rounded-lg;
  @apply text-slate-500 dark:text-slate-500;
  @apply hover:text-slate-700 dark:hover:text-slate-300;
  @apply hover:bg-slate-50 dark:hover:bg-slate-700/30;
  @apply transition-all duration-200;
  @apply text-sm;
}

.submenu-link.active {
  @apply bg-blue-50 dark:bg-blue-900/20;
  @apply text-blue-600 dark:text-blue-400;
  @apply font-medium;
}

.submenu-icon {
  @apply w-4 h-4 flex-shrink-0;
}

.submenu-label {
  @apply ml-3;
}

.quick-actions {
  @apply p-4 border-t border-slate-200 dark:border-slate-700;
  @apply flex-shrink-0;
}

.quick-action-btn {
  @apply w-full flex items-center space-x-3 px-3 py-2 rounded-lg;
  @apply bg-gradient-to-r from-blue-500 to-indigo-500;
  @apply text-white hover:from-blue-600 hover:to-indigo-600;
  @apply transition-all duration-200;
  @apply transform hover:scale-105 active:scale-95;
}

.sidebar-footer {
  @apply p-4 border-t border-slate-200 dark:border-slate-700;
  @apply flex-shrink-0;
}

/* Submenu animation */
.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.submenu-enter-from,
.submenu-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-10px);
}

.submenu-enter-to,
.submenu-leave-from {
  opacity: 1;
  max-height: 200px;
  transform: translateY(0);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .sidebar {
    @apply transform -translate-x-full;
  }
  
  .sidebar.show {
    @apply translate-x-0;
  }
}
</style>

