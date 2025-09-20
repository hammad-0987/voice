<template>
  <BNavbar toggleable="lg" variant="dark" class="app-navbar">
    <BContainer fluid>
      <!-- Brand -->
      <BNavbarBrand :to="dashboardRoute" class="brand">
        <i class="bi bi-shield-check me-2"></i>
        Student CMS
      </BNavbarBrand>

      <!-- Mobile Toggle -->
      <BNavbarToggle target="navbar-collapse" />

      <BCollapse id="navbar-collapse" is-nav>
        <!-- Search Bar (Desktop) -->
        <BNavbarNav class="me-auto d-none d-lg-flex">
          <BNavItem>
            <div class="search-container">
              <BInputGroup size="sm">
                <BFormInput
                  v-model="searchQuery"
                  placeholder="Search complaints..."
                  @keyup.enter="handleSearch"
                />
                <BInputGroupText>
                  <i class="bi bi-search"></i>
                </BInputGroupText>
              </BInputGroup>
            </div>
          </BNavItem>
        </BNavbarNav>

        <!-- Right Side Items -->
        <BNavbarNav class="ms-auto">
          <!-- Notifications -->
          <BNavItem>
            <BDropdown
              variant="link"
              no-caret
              class="notification-dropdown"
              menu-class="notification-menu"
            >
              <template #button-content>
                <div class="notification-icon">
                  <i class="bi bi-bell"></i>
                  <BBadge
                    v-if="notificationsStore.unreadCount > 0"
                    variant="danger"
                    class="notification-badge"
                  >
                    {{ notificationsStore.unreadCount > 99 ? '99+' : notificationsStore.unreadCount }}
                  </BBadge>
                </div>
              </template>

              <!-- Notification Header -->
              <div class="notification-header">
                <h6 class="mb-0">Notifications</h6>
                <BButton
                  v-if="notificationsStore.unreadCount > 0"
                  variant="link"
                  size="sm"
                  @click="markAllAsRead"
                >
                  Mark all read
                </BButton>
              </div>

              <BDropdownDivider />

              <!-- Notification List -->
              <div class="notification-list">
                <div
                  v-if="notificationsStore.recentNotifications.length === 0"
                  class="no-notifications"
                >
                  <i class="bi bi-bell-slash text-muted"></i>
                  <p class="text-muted mb-0">No notifications</p>
                </div>

                <BDropdownItem
                  v-for="notification in notificationsStore.recentNotifications"
                  :key="notification.id"
                  class="notification-item"
                  :class="{ 'unread': !notification.is_read }"
                  @click="handleNotificationClick(notification)"
                >
                  <div class="notification-content">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-message">{{ notification.message }}</div>
                    <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
                  </div>
                  <div v-if="!notification.is_read" class="unread-indicator"></div>
                </BDropdownItem>
              </div>

              <BDropdownDivider />

              <!-- View All Link -->
              <BDropdownItem :to="`/${authStore.userRole}/notifications`">
                <i class="bi bi-list-ul me-2"></i>
                View all notifications
              </BDropdownItem>
            </BDropdown>
          </BNavItem>

          <!-- User Menu -->
          <BNavItem>
            <BDropdown variant="link" no-caret class="user-dropdown">
              <template #button-content>
                <div class="user-info">
                  <div class="user-avatar">
                    {{ authStore.userInitials }}
                  </div>
                  <div class="user-details d-none d-md-block">
                    <div class="user-name">{{ authStore.userName }}</div>
                    <div class="user-role">{{ formatRole(authStore.userRole) }}</div>
                  </div>
                  <i class="bi bi-chevron-down ms-2"></i>
                </div>
              </template>

              <!-- User Menu Items -->
              <BDropdownItem :to="`/${authStore.userRole}/profile`">
                <i class="bi bi-person me-2"></i>
                Profile
              </BDropdownItem>

              <BDropdownItem :to="`/${authStore.userRole}/notifications`">
                <i class="bi bi-bell me-2"></i>
                Notifications
              </BDropdownItem>

              <BDropdownDivider />

              <BDropdownItem @click="handleLogout">
                <i class="bi bi-box-arrow-right me-2"></i>
                Logout
              </BDropdownItem>
            </BDropdown>
          </BNavItem>
        </BNavbarNav>
      </BCollapse>
    </BContainer>
  </BNavbar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'
import { formatDistanceToNow } from 'date-fns'

const router = useRouter()
const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()

const searchQuery = ref('')

// Computed
const dashboardRoute = computed(() => `/${authStore.userRole}/dashboard`)

// Methods
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'search-results',
      query: { q: searchQuery.value.trim() }
    })
  }
}

const handleNotificationClick = async (notification) => {
  // Mark as read
  if (!notification.is_read) {
    await notificationsStore.markAsRead(notification.id)
  }
  
  // Navigate to related page if link exists
  if (notification.link) {
    router.push(notification.link)
  }
}

const markAllAsRead = async () => {
  await notificationsStore.markAllAsRead()
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
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

const formatTime = (timestamp) => {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
}

// Lifecycle
onMounted(() => {
  // Fetch recent notifications
  notificationsStore.fetchNotifications({ page_size: 10 })
})
</script>

<style scoped>
.app-navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 60px;
}

.brand {
  font-weight: 600;
  font-size: 1.25rem;
  color: white !important;
  text-decoration: none;
}

.search-container {
  width: 300px;
  margin-left: 2rem;
}

.notification-dropdown :deep(.btn-link) {
  color: white !important;
  border: none;
  padding: 0.5rem;
}

.notification-icon {
  position: relative;
  font-size: 1.2rem;
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 0.7rem;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
}

.notification-menu {
  width: 350px;
  max-height: 400px;
  overflow-y: auto;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.no-notifications {
  text-align: center;
  padding: 2rem 1rem;
}

.no-notifications i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.notification-item {
  padding: 0.75rem 1rem !important;
  border-bottom: 1px solid #f1f3f4;
  position: relative;
}

.notification-item.unread {
  background-color: #f8f9ff;
}

.notification-content {
  width: 100%;
}

.notification-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #333;
}

.notification-message {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.notification-time {
  font-size: 0.75rem;
  color: #999;
}

.unread-indicator {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background-color: #007bff;
  border-radius: 50%;
}

.user-dropdown :deep(.btn-link) {
  color: white !important;
  border: none;
  padding: 0.5rem;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.8rem;
  color: white;
  margin-right: 0.5rem;
}

.user-details {
  text-align: left;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.2;
}

.user-role {
  font-size: 0.75rem;
  opacity: 0.8;
  line-height: 1.2;
}

@media (max-width: 768px) {
  .search-container {
    width: 100%;
    margin: 0.5rem 0;
  }
  
  .notification-menu {
    width: 300px;
  }
}
</style>

