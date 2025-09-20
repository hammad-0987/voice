<template>
  <div class="dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header" v-motion-fade-visible>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-100">
            Welcome back, {{ authStore.user?.first_name }}!
          </h1>
          <p class="text-slate-600 dark:text-slate-400 mt-1">
            Here's what's happening with your {{ userRoleText }} account today.
          </p>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Quick Actions -->
          <div class="hidden md:flex items-center space-x-2">
            <button
              v-for="action in quickActions"
              :key="action.name"
              @click="action.handler"
              class="btn-secondary px-4 py-2 text-sm"
            >
              <component :is="action.icon" class="w-4 h-4 mr-2" />
              {{ action.label }}
            </button>
          </div>
          
          <!-- Refresh Button -->
          <button
            @click="refreshDashboard"
            :disabled="isRefreshing"
            class="p-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
            title="Refresh Dashboard"
          >
            <ArrowPathIcon class="w-5 h-5" :class="{ 'animate-spin': isRefreshing }" />
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="dashboard-grid" v-motion-slide-visible-bottom>
      <div
        v-for="(stat, index) in dashboardStats"
        :key="stat.title"
        class="stat-card"
        :style="{ '--delay': `${index * 100}ms` }"
      >
        <div class="stat-icon" :class="stat.iconColor">
          <component :is="stat.icon" class="w-6 h-6" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-change" :class="stat.changeType">
            <component :is="stat.changeIcon" class="w-4 h-4" />
            <span>{{ stat.change }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Recent Activity -->
      <div class="activity-section" v-motion-slide-visible-left>
        <div class="section-header">
          <h2 class="section-title">Recent Activity</h2>
          <router-link to="/activity" class="section-link">
            View All
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>
        </div>
        
        <div class="activity-list">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon" :class="activity.iconColor">
              <component :is="activity.icon" class="w-4 h-4" />
            </div>
            <div class="activity-content">
              <p class="activity-text">{{ activity.text }}</p>
              <p class="activity-time">{{ formatTime(activity.timestamp) }}</p>
            </div>
          </div>
          
          <div v-if="recentActivities.length === 0" class="empty-state">
            <ClockIcon class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <p class="text-slate-500 dark:text-slate-400">No recent activity</p>
          </div>
        </div>
      </div>

      <!-- Quick Stats Chart -->
      <div class="chart-section" v-motion-slide-visible-right>
        <div class="section-header">
          <h2 class="section-title">Performance Overview</h2>
          <div class="chart-controls">
            <select v-model="chartPeriod" class="chart-select">
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
            </select>
          </div>
        </div>
        
        <div class="chart-container">
          <canvas ref="chartCanvas" class="w-full h-64"></canvas>
        </div>
      </div>

      <!-- Notifications Panel -->
      <div class="notifications-section" v-motion-slide-visible-bottom>
        <div class="section-header">
          <h2 class="section-title">Notifications</h2>
          <router-link to="/notifications" class="section-link">
            View All
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>
        </div>
        
        <div class="notifications-list">
          <div
            v-for="notification in recentNotifications"
            :key="notification.id"
            class="notification-item"
            :class="{ 'unread': !notification.is_read }"
          >
            <div class="notification-content">
              <p class="notification-text">{{ notification.message }}</p>
              <p class="notification-time">{{ formatTime(notification.created_at) }}</p>
            </div>
            <button
              v-if="!notification.is_read"
              @click="markAsRead(notification.id)"
              class="mark-read-btn"
            >
              <CheckIcon class="w-4 h-4" />
            </button>
          </div>
          
          <div v-if="recentNotifications.length === 0" class="empty-state">
            <BellIcon class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <p class="text-slate-500 dark:text-slate-400">No new notifications</p>
          </div>
        </div>
      </div>

      <!-- Role-specific Panel -->
      <div class="role-panel" v-motion-slide-visible-bottom>
        <component :is="roleSpecificComponent" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowPathIcon,
  ArrowRightIcon,
  ClockIcon,
  BellIcon,
  CheckIcon,
  PlusCircleIcon,
  DocumentTextIcon,
  ChartBarIcon,
  UserGroupIcon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/vue/24/outline'
import { formatDistanceToNow } from 'date-fns'
import { Chart, registerables } from 'chart.js'
import { useAuthStore } from '../stores/auth'
import { useNotificationsStore } from '../stores/notifications'

// Register Chart.js components
Chart.register(...registerables)

const router = useRouter()
const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()

const isRefreshing = ref(false)
const chartPeriod = ref('7d')
const chartCanvas = ref(null)
const chart = ref(null)

const recentActivities = ref([])
const recentNotifications = ref([])

const userRoleText = computed(() => {
  const roleMap = {
    student: 'student',
    staff: 'staff',
    head: 'department head',
    vc: 'vice chancellor',
    admin: 'administrator'
  }
  return roleMap[authStore.user?.role] || 'user'
})

const quickActions = computed(() => {
  const role = authStore.user?.role
  const actions = []

  if (role === 'student') {
    actions.push({
      name: 'file-complaint',
      label: 'File Complaint',
      icon: PlusCircleIcon,
      handler: () => router.push('/complaints/create')
    })
  } else if (['staff', 'head', 'vc', 'admin'].includes(role)) {
    actions.push({
      name: 'view-complaints',
      label: 'View Complaints',
      icon: DocumentTextIcon,
      handler: () => router.push('/complaints')
    })
  }

  return actions
})

const dashboardStats = computed(() => {
  const role = authStore.user?.role
  const stats = []

  if (role === 'student') {
    stats.push(
      {
        title: 'My Complaints',
        value: '12',
        change: '+2 this month',
        changeType: 'positive',
        changeIcon: ArrowTrendingUpIcon,
        icon: DocumentTextIcon,
        iconColor: 'bg-blue-500'
      },
      {
        title: 'Resolved',
        value: '8',
        change: '+3 this week',
        changeType: 'positive',
        changeIcon: ArrowTrendingUpIcon,
        icon: CheckIcon,
        iconColor: 'bg-green-500'
      },
      {
        title: 'Pending',
        value: '3',
        change: '-1 this week',
        changeType: 'negative',
        changeIcon: ArrowTrendingDownIcon,
        icon: ClockIcon,
        iconColor: 'bg-yellow-500'
      },
      {
        title: 'Avg Response',
        value: '2.5 days',
        change: 'Improved',
        changeType: 'positive',
        changeIcon: ArrowTrendingUpIcon,
        icon: ChartBarIcon,
        iconColor: 'bg-indigo-500'
      }
    )
  } else if (role === 'admin') {
    stats.push(
      {
        title: 'Total Users',
        value: '1,234',
        change: '+45 this month',
        changeType: 'positive',
        changeIcon: ArrowTrendingUpIcon,
        icon: UserGroupIcon,
        iconColor: 'bg-blue-500'
      },
      {
        title: 'Active Complaints',
        value: '156',
        change: '+12 today',
        changeType: 'neutral',
        changeIcon: ArrowTrendingUpIcon,
        icon: DocumentTextIcon,
        iconColor: 'bg-yellow-500'
      },
      {
        title: 'Resolution Rate',
        value: '94.2%',
        change: '+2.1% this month',
        changeType: 'positive',
        changeIcon: ArrowTrendingUpIcon,
        icon: ChartBarIcon,
        iconColor: 'bg-green-500'
      },
      {
        title: 'Urgent Issues',
        value: '8',
        change: '-3 today',
        changeType: 'positive',
        changeIcon: ArrowTrendingDownIcon,
        icon: ExclamationTriangleIcon,
        iconColor: 'bg-red-500'
      }
    )
  }

  return stats
})

const roleSpecificComponent = computed(() => {
  // Return different components based on user role
  return 'div' // Placeholder for now
})

const refreshDashboard = async () => {
  isRefreshing.value = true
  
  try {
    // Simulate API calls
    await Promise.all([
      fetchRecentActivities(),
      fetchRecentNotifications(),
      updateChart()
    ])
  } catch (error) {
    console.error('Error refreshing dashboard:', error)
  } finally {
    setTimeout(() => {
      isRefreshing.value = false
    }, 1000)
  }
}

const fetchRecentActivities = async () => {
  // Mock data - replace with actual API call
  recentActivities.value = [
    {
      id: 1,
      text: 'Complaint #CMP-2024-0123 was updated',
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
      icon: DocumentTextIcon,
      iconColor: 'bg-blue-500'
    },
    {
      id: 2,
      text: 'New notification received',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
      icon: BellIcon,
      iconColor: 'bg-green-500'
    }
  ]
}

const fetchRecentNotifications = async () => {
  try {
    const notifications = await notificationsStore.fetchNotifications()
    recentNotifications.value = notifications.slice(0, 5)
  } catch (error) {
    console.error('Error fetching notifications:', error)
  }
}

const markAsRead = async (notificationId) => {
  try {
    await notificationsStore.markAsRead(notificationId)
    const notification = recentNotifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.is_read = true
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

const formatTime = (timestamp) => {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
}

const initChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  
  chart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Complaints',
        data: [12, 19, 3, 5, 2, 3, 9],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(148, 163, 184, 0.1)'
          }
        },
        x: {
          grid: {
            color: 'rgba(148, 163, 184, 0.1)'
          }
        }
      }
    }
  })
}

const updateChart = async () => {
  if (chart.value) {
    // Update chart data based on chartPeriod
    // This would typically fetch new data from API
    chart.value.update()
  }
}

onMounted(async () => {
  await refreshDashboard()
  
  nextTick(() => {
    initChart()
  })
})
</script>

<style scoped>
.dashboard {
  @apply space-y-8;
}

.dashboard-header {
  @apply mb-8;
}

.dashboard-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6;
}

.stat-card {
  @apply card p-6 hover:scale-105 transition-all duration-300;
  @apply flex items-center space-x-4;
  animation-delay: var(--delay);
}

.stat-icon {
  @apply w-12 h-12 rounded-xl flex items-center justify-center text-white;
}

.stat-content {
  @apply flex-1;
}

.stat-value {
  @apply text-2xl font-bold text-slate-900 dark:text-slate-100;
}

.stat-title {
  @apply text-sm text-slate-600 dark:text-slate-400 mb-1;
}

.stat-change {
  @apply flex items-center space-x-1 text-xs font-medium;
}

.stat-change.positive {
  @apply text-green-600 dark:text-green-400;
}

.stat-change.negative {
  @apply text-red-600 dark:text-red-400;
}

.stat-change.neutral {
  @apply text-slate-600 dark:text-slate-400;
}

.content-grid {
  @apply grid grid-cols-1 lg:grid-cols-2 gap-8;
}

.activity-section,
.chart-section,
.notifications-section,
.role-panel {
  @apply card p-6;
}

.section-header {
  @apply flex items-center justify-between mb-6;
}

.section-title {
  @apply text-lg font-semibold text-slate-900 dark:text-slate-100;
}

.section-link {
  @apply flex items-center space-x-1 text-sm text-blue-600 dark:text-blue-400;
  @apply hover:text-blue-700 dark:hover:text-blue-300 transition-colors duration-200;
}

.activity-list,
.notifications-list {
  @apply space-y-4;
}

.activity-item {
  @apply flex items-start space-x-3 p-3 rounded-lg;
  @apply hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors duration-200;
}

.activity-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center text-white flex-shrink-0;
}

.activity-content {
  @apply flex-1 min-w-0;
}

.activity-text {
  @apply text-sm text-slate-900 dark:text-slate-100 mb-1;
}

.activity-time {
  @apply text-xs text-slate-500 dark:text-slate-400;
}

.notification-item {
  @apply flex items-start justify-between p-3 rounded-lg;
  @apply hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors duration-200;
}

.notification-item.unread {
  @apply bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500;
}

.notification-content {
  @apply flex-1 min-w-0;
}

.notification-text {
  @apply text-sm text-slate-900 dark:text-slate-100 mb-1;
}

.notification-time {
  @apply text-xs text-slate-500 dark:text-slate-400;
}

.mark-read-btn {
  @apply p-1 rounded text-slate-400 hover:text-slate-600 dark:hover:text-slate-300;
  @apply transition-colors duration-200;
}

.chart-controls {
  @apply flex items-center space-x-2;
}

.chart-select {
  @apply text-sm bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600;
  @apply rounded-lg px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.empty-state {
  @apply text-center py-8;
}
</style>

