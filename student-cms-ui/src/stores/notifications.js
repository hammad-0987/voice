import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useNotificationsStore = defineStore('notifications', () => {
  // State
  const notifications = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const unreadCount = ref(0)

  // Getters
  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.is_read)
  )
  
  const recentNotifications = computed(() => 
    notifications.value.slice(0, 10)
  )

  // Actions
  const fetchNotifications = async (params = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get('/notifications/', { params })
      
      notifications.value = response.data.results || response.data
      unreadCount.value = unreadNotifications.value.length
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch notifications'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const markAsRead = async (notificationId) => {
    try {
      await api.patch(`/notifications/${notificationId}/`, { is_read: true })
      
      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.is_read = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to mark notification as read'
      return { success: false, error: error.value }
    }
  }

  const markAllAsRead = async () => {
    try {
      await api.post('/notifications/mark-all-read/')
      
      // Update local state
      notifications.value.forEach(n => {
        n.is_read = true
      })
      unreadCount.value = 0
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to mark all notifications as read'
      return { success: false, error: error.value }
    }
  }

  const deleteNotification = async (notificationId) => {
    try {
      await api.delete(`/notifications/${notificationId}/`)
      
      // Remove from local state
      const index = notifications.value.findIndex(n => n.id === notificationId)
      if (index !== -1) {
        const notification = notifications.value[index]
        if (!notification.is_read) {
          unreadCount.value = Math.max(0, unreadCount.value - 1)
        }
        notifications.value.splice(index, 1)
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete notification'
      return { success: false, error: error.value }
    }
  }

  const fetchUnreadCount = async () => {
    try {
      const response = await api.get('/notifications/unread-count/')
      unreadCount.value = response.data.count
      return response.data.count
    } catch (err) {
      console.error('Failed to fetch unread count:', err)
      return 0
    }
  }

  // Add new notification (for real-time updates)
  const addNotification = (notification) => {
    notifications.value.unshift(notification)
    if (!notification.is_read) {
      unreadCount.value += 1
    }
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    notifications,
    isLoading,
    error,
    unreadCount,
    
    // Getters
    unreadNotifications,
    recentNotifications,
    
    // Actions
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    fetchUnreadCount,
    addNotification,
    clearError
  }
})

