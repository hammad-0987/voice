<template>
  <div class="student-notifications">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">
            <i class="fas fa-bell me-3"></i>
            Notifications
          </h1>
          <p class="page-subtitle">
            Stay updated with your complaint status and system updates
          </p>
        </div>
        <div class="header-actions">
          <b-button variant="outline-primary" @click="markAllAsRead" :disabled="unreadCount === 0">
            <i class="fas fa-check-double me-2"></i>
            Mark All Read
          </b-button>
          <b-button variant="outline-secondary" @click="refreshNotifications">
            <i class="fas fa-sync-alt me-2"></i>
            Refresh
          </b-button>
        </div>
      </div>
    </div>

    <!-- Notification Stats -->
    <div class="stats-section">
      <div class="row g-4">
        <div class="col-md-3">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="fas fa-bell"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ totalNotifications }}</h3>
              <p class="stat-label">Total Notifications</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="fas fa-bell-slash"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ unreadCount }}</h3>
              <p class="stat-label">Unread</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-info">
            <div class="stat-icon">
              <i class="fas fa-exclamation-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ complaintNotifications }}</h3>
              <p class="stat-label">Complaint Updates</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="fas fa-info-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ systemNotifications }}</h3>
              <p class="stat-label">System Updates</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="row g-3">
        <div class="col-md-3">
          <select class="form-select" v-model="selectedType" @change="applyFilters">
            <option value="">All Types</option>
            <option value="complaint_update">Complaint Updates</option>
            <option value="complaint_comment">Comments</option>
            <option value="complaint_forward">Forwarded</option>
            <option value="system">System</option>
          </select>
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="selectedStatus" @change="applyFilters">
            <option value="">All Status</option>
            <option value="unread">Unread</option>
            <option value="read">Read</option>
          </select>
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="selectedPeriod" @change="applyFilters">
            <option value="">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
        <div class="col-md-3">
          <b-button variant="outline-secondary" @click="clearFilters" class="w-100">
            <i class="fas fa-times me-2"></i>
            Clear Filters
          </b-button>
        </div>
      </div>
    </div>

    <!-- Notifications List -->
    <div class="notifications-section">
      <div class="notifications-card">
        <div class="card-header">
          <h5 class="card-title">
            <i class="fas fa-list me-2"></i>
            Notifications ({{ filteredNotifications.length }})
          </h5>
        </div>
        
        <div class="notifications-list">
          <div v-if="loading" class="text-center py-5">
            <b-spinner variant="primary" class="mb-3"></b-spinner>
            <p class="text-muted">Loading notifications...</p>
          </div>
          
          <div v-else-if="filteredNotifications.length === 0" class="empty-state">
            <i class="fas fa-bell-slash fa-4x text-muted mb-3"></i>
            <h5 class="text-muted">No notifications found</h5>
            <p class="text-muted">You're all caught up! Check back later for updates.</p>
          </div>
          
          <div v-else>
            <div 
              v-for="notification in paginatedNotifications" 
              :key="notification.id"
              :class="['notification-item', { 'unread': !notification.is_read }]"
              @click="handleNotificationClick(notification)"
            >
              <div class="notification-icon">
                <i :class="getNotificationIcon(notification.type)" :style="{ color: getNotificationColor(notification.type) }"></i>
              </div>
              
              <div class="notification-content">
                <div class="notification-header">
                  <h6 class="notification-title">{{ notification.title }}</h6>
                  <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                </div>
                
                <p class="notification-message">{{ notification.message }}</p>
                
                <div class="notification-meta">
                  <span :class="['notification-type', `type-${notification.type}`]">
                    {{ formatType(notification.type) }}
                  </span>
                  <span v-if="notification.complaint_number" class="complaint-ref">
                    <i class="fas fa-hashtag"></i>
                    {{ notification.complaint_number }}
                  </span>
                </div>
              </div>
              
              <div class="notification-actions">
                <b-button 
                  size="sm" 
                  variant="outline-primary" 
                  v-if="!notification.is_read"
                  @click.stop="markAsRead(notification)"
                >
                  <i class="fas fa-check"></i>
                </b-button>
                <b-button 
                  size="sm" 
                  variant="outline-danger" 
                  @click.stop="deleteNotification(notification)"
                >
                  <i class="fas fa-trash"></i>
                </b-button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="card-footer" v-if="filteredNotifications.length > itemsPerPage">
          <b-pagination
            v-model="currentPage"
            :total-rows="filteredNotifications.length"
            :per-page="itemsPerPage"
            size="sm"
            class="mb-0 justify-content-center"
          ></b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentNotifications',
  data() {
    return {
      loading: true,
      notifications: [],
      selectedType: '',
      selectedStatus: '',
      selectedPeriod: '',
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    totalNotifications() {
      return this.notifications.length
    },
    
    unreadCount() {
      return this.notifications.filter(n => !n.is_read).length
    },
    
    complaintNotifications() {
      return this.notifications.filter(n => 
        ['complaint_update', 'complaint_comment', 'complaint_forward'].includes(n.type)
      ).length
    },
    
    systemNotifications() {
      return this.notifications.filter(n => n.type === 'system').length
    },
    
    filteredNotifications() {
      let filtered = [...this.notifications]
      
      // Type filter
      if (this.selectedType) {
        filtered = filtered.filter(n => n.type === this.selectedType)
      }
      
      // Status filter
      if (this.selectedStatus) {
        const isRead = this.selectedStatus === 'read'
        filtered = filtered.filter(n => n.is_read === isRead)
      }
      
      // Period filter
      if (this.selectedPeriod) {
        const now = new Date()
        const filterDate = new Date()
        
        switch (this.selectedPeriod) {
          case 'today':
            filterDate.setHours(0, 0, 0, 0)
            break
          case 'week':
            filterDate.setDate(now.getDate() - 7)
            break
          case 'month':
            filterDate.setMonth(now.getMonth() - 1)
            break
        }
        
        filtered = filtered.filter(n => new Date(n.created_at) >= filterDate)
      }
      
      // Sort by date (newest first)
      filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      
      return filtered
    },
    
    paginatedNotifications() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredNotifications.slice(start, end)
    }
  },
  async mounted() {
    await this.loadNotifications()
  },
  methods: {
    async loadNotifications() {
      try {
        this.loading = true
        
        // Mock data - replace with actual API call
        this.notifications = [
          {
            id: 1,
            type: 'complaint_update',
            title: 'Complaint Status Updated',
            message: 'Your complaint CMP-2024-0156 has been updated to "In Progress"',
            complaint_number: 'CMP-2024-0156',
            is_read: false,
            created_at: new Date().toISOString(),
            link: '/student/complaints/156'
          },
          {
            id: 2,
            type: 'complaint_comment',
            title: 'New Comment on Your Complaint',
            message: 'Staff has added a comment to your complaint about library access',
            complaint_number: 'CMP-2024-0155',
            is_read: false,
            created_at: new Date(Date.now() - 3600000).toISOString(),
            link: '/student/complaints/155'
          },
          {
            id: 3,
            type: 'complaint_forward',
            title: 'Complaint Forwarded',
            message: 'Your complaint has been forwarded to the IT Department for resolution',
            complaint_number: 'CMP-2024-0154',
            is_read: true,
            created_at: new Date(Date.now() - 86400000).toISOString(),
            link: '/student/complaints/154'
          },
          {
            id: 4,
            type: 'system',
            title: 'System Maintenance Notice',
            message: 'The complaint system will undergo maintenance on Sunday from 2 AM to 4 AM',
            is_read: true,
            created_at: new Date(Date.now() - 172800000).toISOString()
          },
          {
            id: 5,
            type: 'complaint_update',
            title: 'Complaint Resolved',
            message: 'Your complaint CMP-2024-0153 has been marked as resolved',
            complaint_number: 'CMP-2024-0153',
            is_read: true,
            created_at: new Date(Date.now() - 259200000).toISOString(),
            link: '/student/complaints/153'
          }
        ]
        
      } catch (error) {
        console.error('Error loading notifications:', error)
        this.$toast.error('Failed to load notifications')
      } finally {
        this.loading = false
      }
    },
    
    async markAsRead(notification) {
      try {
        // Mock API call - replace with actual implementation
        notification.is_read = true
        this.$toast.success('Notification marked as read')
      } catch (error) {
        console.error('Error marking notification as read:', error)
        this.$toast.error('Failed to mark notification as read')
      }
    },
    
    async markAllAsRead() {
      try {
        // Mock API call - replace with actual implementation
        this.notifications.forEach(n => n.is_read = true)
        this.$toast.success('All notifications marked as read')
      } catch (error) {
        console.error('Error marking all notifications as read:', error)
        this.$toast.error('Failed to mark all notifications as read')
      }
    },
    
    async deleteNotification(notification) {
      if (!confirm('Are you sure you want to delete this notification?')) {
        return
      }
      
      try {
        // Mock API call - replace with actual implementation
        const index = this.notifications.findIndex(n => n.id === notification.id)
        if (index !== -1) {
          this.notifications.splice(index, 1)
        }
        this.$toast.success('Notification deleted')
      } catch (error) {
        console.error('Error deleting notification:', error)
        this.$toast.error('Failed to delete notification')
      }
    },
    
    handleNotificationClick(notification) {
      // Mark as read when clicked
      if (!notification.is_read) {
        this.markAsRead(notification)
      }
      
      // Navigate to linked page if available
      if (notification.link) {
        this.$router.push(notification.link)
      }
    },
    
    async refreshNotifications() {
      await this.loadNotifications()
      this.$toast.success('Notifications refreshed')
    },
    
    applyFilters() {
      this.currentPage = 1
    },
    
    clearFilters() {
      this.selectedType = ''
      this.selectedStatus = ''
      this.selectedPeriod = ''
      this.currentPage = 1
    },
    
    getNotificationIcon(type) {
      const icons = {
        'complaint_update': 'fas fa-sync-alt',
        'complaint_comment': 'fas fa-comment',
        'complaint_forward': 'fas fa-share',
        'system': 'fas fa-cog'
      }
      return icons[type] || 'fas fa-bell'
    },
    
    getNotificationColor(type) {
      const colors = {
        'complaint_update': '#3b82f6',
        'complaint_comment': '#10b981',
        'complaint_forward': '#f59e0b',
        'system': '#6b7280'
      }
      return colors[type] || '#667eea'
    },
    
    formatType(type) {
      const types = {
        'complaint_update': 'Complaint Update',
        'complaint_comment': 'Comment',
        'complaint_forward': 'Forwarded',
        'system': 'System'
      }
      return types[type] || type
    },
    
    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffMinutes = Math.ceil(diffTime / (1000 * 60))
      const diffHours = Math.ceil(diffTime / (1000 * 60 * 60))
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffMinutes < 60) {
        return `${diffMinutes}m ago`
      } else if (diffHours < 24) {
        return `${diffHours}h ago`
      } else if (diffDays < 7) {
        return `${diffDays}d ago`
      } else {
        return date.toLocaleDateString()
      }
    }
  }
}
</script>

<style scoped>
.student-notifications {
  padding: 0;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* Header Section */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0.5rem 0 0 0;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.header-actions .btn {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  color: white;
}

/* Stats Section */
.stats-section {
  max-width: 1200px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-primary .stat-icon { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-warning .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.stat-info .stat-icon { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
.stat-success .stat-icon { background: linear-gradient(135deg, #10b981, #059669); }

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  color: #1a202c;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0.25rem 0;
  font-weight: 500;
}

/* Filters Section */
.filters-section {
  max-width: 1200px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
}

.form-select {
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Notifications Section */
.notifications-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.notifications-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  display: flex;
  align-items: center;
}

.notifications-list {
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-item:hover {
  background-color: #f8fafc;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: #fef7ff;
  border-left: 4px solid #667eea;
}

.notification-item.unread:hover {
  background-color: #f3f4f6;
}

.notification-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
  border: 1px solid #e2e8f0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.notification-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  line-height: 1.4;
}

.notification-time {
  font-size: 0.8rem;
  color: #6b7280;
  white-space: nowrap;
  margin-left: 1rem;
}

.notification-message {
  font-size: 0.9rem;
  color: #4b5563;
  margin: 0 0 0.75rem 0;
  line-height: 1.5;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.notification-type {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.type-complaint_update { background: #dbeafe; color: #1e40af; }
.type-complaint_comment { background: #d1fae5; color: #065f46; }
.type-complaint_forward { background: #fef3c7; color: #92400e; }
.type-system { background: #f3f4f6; color: #374151; }

.complaint-ref {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.notification-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-shrink: 0;
}

.notification-actions .btn {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .notification-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .notification-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .notification-time {
    margin-left: 0;
  }
  
  .notification-actions {
    flex-direction: row;
    align-self: stretch;
  }
  
  .notification-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .notification-item {
    padding: 1rem;
  }
  
  .notification-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .filters-section .row > div {
    margin-bottom: 0.5rem;
  }
}

/* Loading Animation */
.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Smooth Transitions */
.notification-item {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

/* Focus States */
.form-select:focus,
.btn:focus {
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Notification Badge Animation */
.notification-item.unread .notification-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
  }
}
</style>
