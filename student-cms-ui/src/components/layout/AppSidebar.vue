<template>
  <aside class="app-sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- Sidebar Toggle -->
    <div class="sidebar-toggle" @click="toggleSidebar">
      <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
    </div>

    <!-- Sidebar Content -->
    <div class="sidebar-content">
      <!-- User Info -->
      <div class="user-section" v-if="!isCollapsed">
        <div class="user-avatar">
          {{ authStore.userInitials }}
        </div>
        <div class="user-info">
          <div class="user-name">{{ authStore.userName }}</div>
          <div class="user-role">{{ formatRole(authStore.userRole) }}</div>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li
            v-for="item in navigationItems"
            :key="item.name"
            class="nav-item"
            :class="{ 'active': isActiveRoute(item.route) }"
          >
            <router-link
              :to="item.route"
              class="nav-link"
              :title="isCollapsed ? item.label : ''"
            >
              <i class="nav-icon" :class="item.icon"></i>
              <span v-if="!isCollapsed" class="nav-label">{{ item.label }}</span>
              <BBadge
                v-if="item.badge && !isCollapsed"
                :variant="item.badgeVariant || 'primary'"
                class="nav-badge"
              >
                {{ item.badge }}
              </BBadge>
            </router-link>
          </li>
        </ul>
      </nav>

      <!-- Quick Actions -->
      <div v-if="!isCollapsed && quickActions.length > 0" class="quick-actions">
        <div class="section-title">Quick Actions</div>
        <div class="action-buttons">
          <BButton
            v-for="action in quickActions"
            :key="action.name"
            :variant="action.variant || 'outline-primary'"
            size="sm"
            class="action-btn"
            @click="handleQuickAction(action)"
          >
            <i :class="action.icon" class="me-1"></i>
            {{ action.label }}
          </BButton>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()

const isCollapsed = ref(false)

// Methods
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const isActiveRoute = (routePath) => {
  return route.path.startsWith(routePath)
}

const formatRole = (role) => {
  const roleMap = {
    student: 'Student',
    staff: 'Staff',
    head: 'Department Head',
    vc: 'Vice Chancellor',
    admin: 'Administrator'
  }
  return roleMap[role] || role
}

const handleQuickAction = (action) => {
  if (action.route) {
    router.push(action.route)
  } else if (action.action) {
    action.action()
  }
}

// Computed navigation items based on user role
const navigationItems = computed(() => {
  const userRole = authStore.userRole
  const baseItems = []

  switch (userRole) {
    case 'student':
      return [
        {
          name: 'dashboard',
          label: 'Dashboard',
          icon: 'bi bi-speedometer2',
          route: '/student/dashboard'
        },
        {
          name: 'file-complaint',
          label: 'File Complaint',
          icon: 'bi bi-plus-circle',
          route: '/student/file-complaint'
        },
        {
          name: 'my-complaints',
          label: 'My Complaints',
          icon: 'bi bi-list-ul',
          route: '/student/complaints'
        },
        {
          name: 'withdrawals',
          label: 'Withdrawal Requests',
          icon: 'bi bi-file-earmark-text',
          route: '/student/withdrawals'
        },
        {
          name: 'notifications',
          label: 'Notifications',
          icon: 'bi bi-bell',
          route: '/student/notifications',
          badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount : null,
          badgeVariant: 'danger'
        },
        {
          name: 'profile',
          label: 'Profile',
          icon: 'bi bi-person',
          route: '/student/profile'
        }
      ]

    case 'staff':
      return [
        {
          name: 'dashboard',
          label: 'Dashboard',
          icon: 'bi bi-speedometer2',
          route: '/staff/dashboard'
        },
        {
          name: 'assigned-complaints',
          label: 'Assigned Complaints',
          icon: 'bi bi-clipboard-check',
          route: '/staff/complaints'
        },
        {
          name: 'review-withdrawals',
          label: 'Review Withdrawals',
          icon: 'bi bi-file-earmark-check',
          route: '/staff/withdrawals'
        },
        {
          name: 'notifications',
          label: 'Notifications',
          icon: 'bi bi-bell',
          route: '/staff/notifications',
          badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount : null,
          badgeVariant: 'danger'
        }
      ]

    case 'head':
      return [
        {
          name: 'dashboard',
          label: 'Dashboard',
          icon: 'bi bi-speedometer2',
          route: '/head/dashboard'
        },
        {
          name: 'department-complaints',
          label: 'Department Complaints',
          icon: 'bi bi-building',
          route: '/head/complaints'
        },
        {
          name: 'analytics',
          label: 'Analytics',
          icon: 'bi bi-graph-up',
          route: '/head/analytics'
        },
        {
          name: 'manage-staff',
          label: 'Manage Staff',
          icon: 'bi bi-people',
          route: '/head/staff'
        },
        {
          name: 'feedback',
          label: 'Feedback',
          icon: 'bi bi-chat-square-text',
          route: '/head/feedback'
        },
        {
          name: 'notifications',
          label: 'Notifications',
          icon: 'bi bi-bell',
          route: '/head/notifications',
          badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount : null,
          badgeVariant: 'danger'
        }
      ]

    case 'vc':
      return [
        {
          name: 'dashboard',
          label: 'Dashboard',
          icon: 'bi bi-speedometer2',
          route: '/vc/dashboard'
        },
        {
          name: 'all-complaints',
          label: 'All Complaints',
          icon: 'bi bi-list-check',
          route: '/vc/complaints'
        },
        {
          name: 'global-analytics',
          label: 'Global Analytics',
          icon: 'bi bi-graph-up-arrow',
          route: '/vc/analytics'
        },
        {
          name: 'system-reports',
          label: 'System Reports',
          icon: 'bi bi-file-earmark-bar-graph',
          route: '/vc/reports'
        },
        {
          name: 'feedback',
          label: 'Feedback',
          icon: 'bi bi-chat-square-text',
          route: '/vc/feedback'
        },
        {
          name: 'notifications',
          label: 'Notifications',
          icon: 'bi bi-bell',
          route: '/vc/notifications',
          badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount : null,
          badgeVariant: 'danger'
        }
      ]

    case 'admin':
      return [
        {
          name: 'dashboard',
          label: 'Dashboard',
          icon: 'bi bi-speedometer2',
          route: '/admin/dashboard'
        },
        {
          name: 'user-management',
          label: 'User Management',
          icon: 'bi bi-people-fill',
          route: '/admin/users'
        },
        {
          name: 'department-management',
          label: 'Departments',
          icon: 'bi bi-building-fill',
          route: '/admin/departments'
        },
        {
          name: 'system-settings',
          label: 'System Settings',
          icon: 'bi bi-gear-fill',
          route: '/admin/settings'
        },
        {
          name: 'activity-logs',
          label: 'Activity Logs',
          icon: 'bi bi-journal-text',
          route: '/admin/logs'
        },
        {
          name: 'feedback',
          label: 'All Feedback',
          icon: 'bi bi-chat-square-text-fill',
          route: '/admin/feedback'
        },
        {
          name: 'notifications',
          label: 'Notifications',
          icon: 'bi bi-bell-fill',
          route: '/admin/notifications',
          badge: notificationsStore.unreadCount > 0 ? notificationsStore.unreadCount : null,
          badgeVariant: 'danger'
        }
      ]

    default:
      return []
  }
})

// Quick actions based on user role
const quickActions = computed(() => {
  const userRole = authStore.userRole

  switch (userRole) {
    case 'student':
      return [
        {
          name: 'file-complaint',
          label: 'File Complaint',
          icon: 'bi bi-plus-circle',
          variant: 'primary',
          route: '/student/file-complaint'
        },
        {
          name: 'track-complaint',
          label: 'Track Complaint',
          icon: 'bi bi-search',
          variant: 'outline-secondary',
          route: '/track'
        }
      ]

    case 'staff':
      return [
        {
          name: 'pending-complaints',
          label: 'Pending Review',
          icon: 'bi bi-clock',
          variant: 'warning',
          route: '/staff/complaints?status=pending'
        }
      ]

    case 'head':
      return [
        {
          name: 'department-overview',
          label: 'Dept. Overview',
          icon: 'bi bi-pie-chart',
          variant: 'info',
          route: '/head/analytics'
        }
      ]

    case 'vc':
      return [
        {
          name: 'system-overview',
          label: 'System Overview',
          icon: 'bi bi-graph-up',
          variant: 'success',
          route: '/vc/analytics'
        }
      ]

    case 'admin':
      return [
        {
          name: 'create-user',
          label: 'Create User',
          icon: 'bi bi-person-plus',
          variant: 'primary',
          route: '/admin/users?action=create'
        }
      ]

    default:
      return []
  }
})

// Responsive behavior
onMounted(() => {
  const handleResize = () => {
    if (window.innerWidth < 768) {
      isCollapsed.value = true
    }
  }

  window.addEventListener('resize', handleResize)
  handleResize() // Check initial size

  return () => {
    window.removeEventListener('resize', handleResize)
  }
})
</script>

<style scoped>
.app-sidebar {
  width: 280px;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  color: white;
  transition: width 0.3s ease;
  position: relative;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.app-sidebar.collapsed {
  width: 70px;
}

.sidebar-toggle {
  position: absolute;
  top: 10px;
  right: -15px;
  width: 30px;
  height: 30px;
  background: #3498db;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: #2980b9;
  transform: scale(1.1);
}

.sidebar-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}

.user-section {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.75rem;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.25rem;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(5px);
}

.nav-item.active .nav-link {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.nav-item.active .nav-link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #ecf0f1;
}

.nav-icon {
  font-size: 1.1rem;
  margin-right: 0.75rem;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.nav-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-badge {
  margin-left: auto;
  font-size: 0.7rem;
}

.quick-actions {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.section-title {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.action-btn {
  justify-content: flex-start;
  text-align: left;
  border-radius: 6px;
  font-size: 0.8rem;
}

/* Collapsed state styles */
.app-sidebar.collapsed .user-section {
  justify-content: center;
  padding: 1rem 0.5rem;
}

.app-sidebar.collapsed .user-info {
  display: none;
}

.app-sidebar.collapsed .nav-link {
  justify-content: center;
  padding: 0.75rem 0.5rem;
}

.app-sidebar.collapsed .nav-label,
.app-sidebar.collapsed .nav-badge {
  display: none;
}

.app-sidebar.collapsed .nav-icon {
  margin-right: 0;
}

.app-sidebar.collapsed .quick-actions {
  display: none;
}

/* Mobile styles */
@media (max-width: 768px) {
  .app-sidebar {
    position: fixed;
    top: 60px;
    left: 0;
    height: calc(100vh - 60px);
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .app-sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .sidebar-toggle {
    display: none;
  }
}

/* Scrollbar styling */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>

