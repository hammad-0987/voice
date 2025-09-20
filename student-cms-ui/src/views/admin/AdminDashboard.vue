<template>
  <div class="admin-dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Administrator Dashboard</h1>
        <p class="page-subtitle">System overview and management center</p>
      </div>
      <div class="header-actions">
        <BButton variant="outline-primary" @click="refreshDashboard" :disabled="isLoading">
          <i class="bi bi-arrow-clockwise me-2"></i>
          Refresh
        </BButton>
        <BButton variant="primary" @click="showQuickActionsModal = true">
          <i class="bi bi-lightning me-2"></i>
          Quick Actions
        </BButton>
      </div>
    </div>

    <!-- System Statistics -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card primary">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ systemStats.totalComplaints }}</div>
              <div class="stats-label">Total Complaints</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card success">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ systemStats.totalUsers }}</div>
              <div class="stats-label">Total Users</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card warning">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-building"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ systemStats.totalDepartments }}</div>
              <div class="stats-label">Departments</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card info">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-graph-up"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ systemStats.resolutionRate }}%</div>
              <div class="stats-label">Resolution Rate</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="row">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Recent Activity -->
        <div class="card mb-4">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-activity me-2"></i>
                Recent System Activity
              </h5>
              <router-link to="/admin/activity-logs" class="btn btn-sm btn-outline-primary">
                View All Logs
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="loading-spinner">
              <BSpinner class="spinner-border-custom" />
              <p class="mt-3 text-muted">Loading activity...</p>
            </div>
            
            <div v-else-if="recentActivity.length === 0" class="empty-state">
              <div class="empty-state-icon">
                <i class="bi bi-clock-history"></i>
              </div>
              <div class="empty-state-title">No recent activity</div>
            </div>
            
            <div v-else class="activity-timeline">
              <div 
                v-for="activity in recentActivity" 
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.action)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-header">
                    <span class="activity-user">{{ activity.user_name }}</span>
                    <span class="activity-action">{{ formatActivityAction(activity.action) }}</span>
                    <span class="activity-target">{{ activity.target }}</span>
                  </div>
                  <div class="activity-time">{{ formatRelativeTime(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Performance -->
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-speedometer2 me-2"></i>
              System Performance
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3">
                <div class="performance-metric">
                  <div class="metric-label">Average Response Time</div>
                  <div class="metric-value">{{ systemPerformance.avgResponseTime }}</div>
                  <div class="metric-trend" :class="systemPerformance.responseTimeTrend">
                    <i :class="getTrendIcon(systemPerformance.responseTimeTrend)"></i>
                    {{ systemPerformance.responseTimeChange }}
                  </div>
                </div>
              </div>
              
              <div class="col-md-4 mb-3">
                <div class="performance-metric">
                  <div class="metric-label">System Uptime</div>
                  <div class="metric-value">{{ systemPerformance.uptime }}</div>
                  <div class="metric-trend positive">
                    <i class="bi bi-arrow-up"></i>
                    Stable
                  </div>
                </div>
              </div>
              
              <div class="col-md-4 mb-3">
                <div class="performance-metric">
                  <div class="metric-label">Active Sessions</div>
                  <div class="metric-value">{{ systemPerformance.activeSessions }}</div>
                  <div class="metric-trend" :class="systemPerformance.sessionsTrend">
                    <i :class="getTrendIcon(systemPerformance.sessionsTrend)"></i>
                    {{ systemPerformance.sessionsChange }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Quick Stats -->
        <div class="card mb-4">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="bi bi-pie-chart me-2"></i>
              Today's Overview
            </h6>
          </div>
          <div class="card-body">
            <div class="quick-stats">
              <div class="quick-stat-item">
                <div class="stat-icon primary">
                  <i class="bi bi-plus-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ todayStats.newComplaints }}</div>
                  <div class="stat-label">New Complaints</div>
                </div>
              </div>
              
              <div class="quick-stat-item">
                <div class="stat-icon success">
                  <i class="bi bi-check-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ todayStats.resolvedComplaints }}</div>
                  <div class="stat-label">Resolved</div>
                </div>
              </div>
              
              <div class="quick-stat-item">
                <div class="stat-icon warning">
                  <i class="bi bi-person-plus"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ todayStats.newUsers }}</div>
                  <div class="stat-label">New Users</div>
                </div>
              </div>
              
              <div class="quick-stat-item">
                <div class="stat-icon info">
                  <i class="bi bi-bell"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ todayStats.notifications }}</div>
                  <div class="stat-label">Notifications</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Department Status -->
        <div class="card mb-4">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="bi bi-building me-2"></i>
              Department Status
            </h6>
          </div>
          <div class="card-body">
            <div v-if="departmentStatus.length === 0" class="text-muted text-center py-3">
              No departments configured
            </div>
            <div v-else>
              <div 
                v-for="dept in departmentStatus" 
                :key="dept.id"
                class="department-item"
              >
                <div class="department-info">
                  <div class="department-name">{{ dept.name }}</div>
                  <div class="department-stats">
                    <span class="stat-badge pending">{{ dept.pending }} pending</span>
                    <span class="stat-badge resolved">{{ dept.resolved }} resolved</span>
                  </div>
                </div>
                <div class="department-status">
                  <div class="status-indicator" :class="dept.status"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Alerts -->
        <div class="card">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="bi bi-exclamation-triangle me-2"></i>
              System Alerts
            </h6>
          </div>
          <div class="card-body">
            <div v-if="systemAlerts.length === 0" class="text-muted text-center py-3">
              <i class="bi bi-check-circle text-success me-2"></i>
              All systems operational
            </div>
            <div v-else>
              <div 
                v-for="alert in systemAlerts" 
                :key="alert.id"
                class="alert-item"
                :class="alert.severity"
              >
                <div class="alert-icon">
                  <i :class="getAlertIcon(alert.severity)"></i>
                </div>
                <div class="alert-content">
                  <div class="alert-title">{{ alert.title }}</div>
                  <div class="alert-message">{{ alert.message }}</div>
                  <div class="alert-time">{{ formatRelativeTime(alert.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions Modal -->
    <BModal
      v-model="showQuickActionsModal"
      title="Quick Actions"
      size="lg"
      hide-footer
    >
      <div class="quick-actions-grid">
        <router-link to="/admin/users" class="quick-action-card">
          <div class="action-icon">
            <i class="bi bi-people"></i>
          </div>
          <div class="action-content">
            <div class="action-title">Manage Users</div>
            <div class="action-description">Add, edit, or remove users</div>
          </div>
        </router-link>
        
        <router-link to="/admin/departments" class="quick-action-card">
          <div class="action-icon">
            <i class="bi bi-building"></i>
          </div>
          <div class="action-content">
            <div class="action-title">Manage Departments</div>
            <div class="action-description">Configure departments and heads</div>
          </div>
        </router-link>
        
        <router-link to="/admin/settings" class="quick-action-card">
          <div class="action-icon">
            <i class="bi bi-gear"></i>
          </div>
          <div class="action-content">
            <div class="action-title">System Settings</div>
            <div class="action-description">Configure system preferences</div>
          </div>
        </router-link>
        
        <router-link to="/admin/activity-logs" class="quick-action-card">
          <div class="action-icon">
            <i class="bi bi-list-ul"></i>
          </div>
          <div class="action-content">
            <div class="action-title">Activity Logs</div>
            <div class="action-description">View system activity and audit trail</div>
          </div>
        </router-link>
      </div>
    </BModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'

// Component state
const isLoading = ref(false)
const showQuickActionsModal = ref(false)
const recentActivity = ref([])

// Statistics
const systemStats = reactive({
  totalComplaints: 0,
  totalUsers: 0,
  totalDepartments: 0,
  resolutionRate: 0
})

const todayStats = reactive({
  newComplaints: 0,
  resolvedComplaints: 0,
  newUsers: 0,
  notifications: 0
})

const systemPerformance = reactive({
  avgResponseTime: '0ms',
  responseTimeTrend: 'positive',
  responseTimeChange: '+5%',
  uptime: '99.9%',
  activeSessions: 0,
  sessionsTrend: 'positive',
  sessionsChange: '+12%'
})

const departmentStatus = ref([])
const systemAlerts = ref([])

// Methods
const fetchDashboardData = async () => {
  isLoading.value = true
  
  try {
    // Simulate API calls - replace with actual API integration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock data - replace with actual API responses
    Object.assign(systemStats, {
      totalComplaints: 1247,
      totalUsers: 89,
      totalDepartments: 12,
      resolutionRate: 87
    })
    
    Object.assign(todayStats, {
      newComplaints: 23,
      resolvedComplaints: 18,
      newUsers: 5,
      notifications: 42
    })
    
    Object.assign(systemPerformance, {
      avgResponseTime: '245ms',
      responseTimeTrend: 'positive',
      responseTimeChange: '+5%',
      uptime: '99.9%',
      activeSessions: 156,
      sessionsTrend: 'positive',
      sessionsChange: '+12%'
    })
    
    recentActivity.value = [
      {
        id: 1,
        user_name: 'John Doe',
        action: 'complaint_created',
        target: 'CMP-2024-0123',
        timestamp: new Date(Date.now() - 5 * 60 * 1000)
      },
      {
        id: 2,
        user_name: 'Jane Smith',
        action: 'user_created',
        target: 'student@example.com',
        timestamp: new Date(Date.now() - 15 * 60 * 1000)
      },
      {
        id: 3,
        user_name: 'Admin User',
        action: 'department_updated',
        target: 'Computer Science',
        timestamp: new Date(Date.now() - 30 * 60 * 1000)
      }
    ]
    
    departmentStatus.value = [
      { id: 1, name: 'Computer Science', pending: 12, resolved: 45, status: 'active' },
      { id: 2, name: 'Mathematics', pending: 8, resolved: 32, status: 'active' },
      { id: 3, name: 'Physics', pending: 15, resolved: 28, status: 'warning' },
      { id: 4, name: 'Chemistry', pending: 6, resolved: 38, status: 'active' }
    ]
    
    systemAlerts.value = [
      {
        id: 1,
        severity: 'warning',
        title: 'High Complaint Volume',
        message: 'Physics department has 15 pending complaints',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      }
    ]
    
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

const refreshDashboard = () => {
  fetchDashboardData()
}

// Formatting methods
const formatRelativeTime = (date) => formatDistanceToNow(new Date(date), { addSuffix: true })

const formatActivityAction = (action) => {
  const actionMap = {
    complaint_created: 'created complaint',
    complaint_updated: 'updated complaint',
    user_created: 'created user',
    user_updated: 'updated user',
    department_created: 'created department',
    department_updated: 'updated department'
  }
  return actionMap[action] || action
}

const getActivityIcon = (action) => {
  const iconMap = {
    complaint_created: 'bi bi-file-earmark-plus text-primary',
    complaint_updated: 'bi bi-file-earmark-check text-info',
    user_created: 'bi bi-person-plus text-success',
    user_updated: 'bi bi-person-check text-info',
    department_created: 'bi bi-building text-success',
    department_updated: 'bi bi-building text-info'
  }
  return iconMap[action] || 'bi bi-circle text-secondary'
}

const getTrendIcon = (trend) => {
  return trend === 'positive' ? 'bi bi-arrow-up' : 'bi bi-arrow-down'
}

const getAlertIcon = (severity) => {
  const iconMap = {
    info: 'bi bi-info-circle',
    warning: 'bi bi-exclamation-triangle',
    error: 'bi bi-x-circle',
    success: 'bi bi-check-circle'
  }
  return iconMap[severity] || 'bi bi-info-circle'
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6c757d;
  margin-bottom: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.stats-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  overflow: hidden;
  cursor: pointer;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.stats-card.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stats-card.success {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
  color: white;
}

.stats-card.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stats-card.info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stats-card .card-body {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stats-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.stats-content {
  text-align: right;
}

.stats-number {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stats-label {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 500;
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: #f8f9fa;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-header {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.activity-user {
  color: #667eea;
  font-weight: 600;
}

.activity-time {
  font-size: 0.875rem;
  color: #6c757d;
}

.performance-metric {
  text-align: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.performance-metric:hover {
  border-color: #667eea;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
}

.metric-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.metric-trend {
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.metric-trend.positive {
  color: #28a745;
}

.metric-trend.negative {
  color: #dc3545;
}

.quick-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quick-stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.quick-stat-item:hover {
  background: #f8f9fa;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.stat-icon.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.success {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.department-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  border: 1px solid #f1f3f4;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.department-item:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.department-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.department-stats {
  display: flex;
  gap: 0.5rem;
}

.stat-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
}

.stat-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.stat-badge.resolved {
  background: #d4edda;
  color: #155724;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-indicator.active {
  background: #28a745;
}

.status-indicator.warning {
  background: #ffc107;
}

.status-indicator.error {
  background: #dc3545;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.alert-item.warning {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
}

.alert-item.error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
}

.alert-item.info {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
}

.alert-icon {
  font-size: 1.2rem;
}

.alert-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.alert-message {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.alert-time {
  font-size: 0.75rem;
  color: #6c757d;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.quick-action-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.quick-action-card:hover {
  border-color: #667eea;
  background: #f8f9ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.1);
  color: inherit;
  text-decoration: none;
}

.action-icon {
  font-size: 2rem;
  color: #667eea;
}

.action-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.action-description {
  font-size: 0.875rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: stretch;
  }
  
  .header-actions .btn {
    flex: 1;
  }
  
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
