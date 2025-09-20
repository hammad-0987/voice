<template>
  <div class="head-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="dashboard-title">
            <i class="fas fa-user-tie me-3"></i>
            Department Head Dashboard
          </h1>
          <p class="dashboard-subtitle">
            Welcome back, {{ user?.full_name || user?.username }}
          </p>
        </div>
        <div class="header-actions">
          <b-button variant="primary" @click="refreshData">
            <i class="fas fa-sync-alt me-2"></i>
            Refresh
          </b-button>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-section">
      <div class="row g-4">
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="fas fa-exclamation-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.total_complaints || 0 }}</h3>
              <p class="stat-label">Total Complaints</p>
              <small class="stat-change positive">
                <i class="fas fa-arrow-up"></i>
                +{{ stats.new_complaints_today || 0 }} today
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.pending_complaints || 0 }}</h3>
              <p class="stat-label">Pending Complaints</p>
              <small class="stat-change">
                <i class="fas fa-hourglass-half"></i>
                Requires attention
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.resolved_complaints || 0 }}</h3>
              <p class="stat-label">Resolved This Month</p>
              <small class="stat-change positive">
                <i class="fas fa-arrow-up"></i>
                {{ stats.resolution_rate || 0 }}% rate
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-info">
            <div class="stat-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.department_staff || 0 }}</h3>
              <p class="stat-label">Department Staff</p>
              <small class="stat-change">
                <i class="fas fa-user-check"></i>
                {{ stats.active_staff || 0 }} active
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="row g-4">
        <div class="col-xl-8">
          <div class="chart-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-chart-line me-2"></i>
                Complaint Trends (Last 6 Months)
              </h5>
              <div class="card-actions">
                <b-dropdown size="sm" variant="outline-secondary" text="Period">
                  <b-dropdown-item @click="changePeriod('6months')">Last 6 Months</b-dropdown-item>
                  <b-dropdown-item @click="changePeriod('year')">Last Year</b-dropdown-item>
                  <b-dropdown-item @click="changePeriod('all')">All Time</b-dropdown-item>
                </b-dropdown>
              </div>
            </div>
            <div class="card-body">
              <canvas ref="trendsChart" height="300"></canvas>
            </div>
          </div>
        </div>

        <div class="col-xl-4">
          <div class="chart-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-chart-pie me-2"></i>
                Status Distribution
              </h5>
            </div>
            <div class="card-body">
              <canvas ref="statusChart" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activities & Quick Actions -->
    <div class="content-section">
      <div class="row g-4">
        <!-- Recent Complaints -->
        <div class="col-xl-8">
          <div class="content-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-list me-2"></i>
                Recent Complaints
              </h5>
              <router-link to="/head/complaints" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <b-spinner variant="primary"></b-spinner>
                <p class="mt-2 text-muted">Loading complaints...</p>
              </div>
              <div v-else-if="recentComplaints.length === 0" class="text-center py-4">
                <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                <p class="text-muted">No recent complaints</p>
              </div>
              <div v-else class="complaints-list">
                <div 
                  v-for="complaint in recentComplaints" 
                  :key="complaint.id"
                  class="complaint-item"
                  @click="viewComplaint(complaint.id)"
                >
                  <div class="complaint-info">
                    <div class="complaint-header">
                      <span class="complaint-number">{{ complaint.complaint_number }}</span>
                      <span :class="['status-badge', `status-${complaint.status}`]">
                        {{ formatStatus(complaint.status) }}
                      </span>
                    </div>
                    <h6 class="complaint-title">{{ complaint.title }}</h6>
                    <div class="complaint-meta">
                      <span class="meta-item">
                        <i class="fas fa-user"></i>
                        {{ complaint.created_by?.full_name || complaint.created_by?.username }}
                      </span>
                      <span class="meta-item">
                        <i class="fas fa-clock"></i>
                        {{ formatDate(complaint.created_at) }}
                      </span>
                      <span class="meta-item">
                        <i class="fas fa-flag"></i>
                        {{ formatPriority(complaint.priority) }}
                      </span>
                    </div>
                  </div>
                  <div class="complaint-actions">
                    <b-button size="sm" variant="outline-primary" @click.stop="viewComplaint(complaint.id)">
                      <i class="fas fa-eye"></i>
                    </b-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-xl-4">
          <div class="content-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-bolt me-2"></i>
                Quick Actions
              </h5>
            </div>
            <div class="card-body">
              <div class="quick-actions">
                <router-link to="/head/complaints" class="action-item">
                  <div class="action-icon bg-primary">
                    <i class="fas fa-list"></i>
                  </div>
                  <div class="action-content">
                    <h6>View All Complaints</h6>
                    <p>Manage department complaints</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </router-link>

                <router-link to="/head/staff" class="action-item">
                  <div class="action-icon bg-success">
                    <i class="fas fa-users"></i>
                  </div>
                  <div class="action-content">
                    <h6>Manage Staff</h6>
                    <p>View and assign staff members</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </router-link>

                <router-link to="/head/analytics" class="action-item">
                  <div class="action-icon bg-info">
                    <i class="fas fa-chart-bar"></i>
                  </div>
                  <div class="action-content">
                    <h6>Department Analytics</h6>
                    <p>View detailed reports</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </router-link>

                <router-link to="/head/withdrawals" class="action-item">
                  <div class="action-icon bg-warning">
                    <i class="fas fa-file-alt"></i>
                  </div>
                  <div class="action-content">
                    <h6>Withdrawal Requests</h6>
                    <p>Review pending requests</p>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useComplaintsStore } from '@/stores/complaints'
import Chart from 'chart.js/auto'

export default {
  name: 'HeadDashboard',
  data() {
    return {
      loading: true,
      stats: {
        total_complaints: 0,
        pending_complaints: 0,
        resolved_complaints: 0,
        new_complaints_today: 0,
        resolution_rate: 0,
        department_staff: 0,
        active_staff: 0
      },
      recentComplaints: [],
      trendsChart: null,
      statusChart: null,
      currentPeriod: '6months'
    }
  },
  computed: {
    ...mapState(useAuthStore, ['user'])
  },
  async mounted() {
    await this.loadDashboardData()
    this.initializeCharts()
  },
  beforeUnmount() {
    if (this.trendsChart) {
      this.trendsChart.destroy()
    }
    if (this.statusChart) {
      this.statusChart.destroy()
    }
  },
  methods: {
    ...mapActions(useComplaintsStore, ['fetchComplaints']),
    
    async loadDashboardData() {
      try {
        this.loading = true
        
        // Load dashboard stats
        await this.loadStats()
        
        // Load recent complaints
        await this.loadRecentComplaints()
        
      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$toast.error('Failed to load dashboard data')
      } finally {
        this.loading = false
      }
    },

    async loadStats() {
      // Mock data - replace with actual API call
      this.stats = {
        total_complaints: 156,
        pending_complaints: 23,
        resolved_complaints: 89,
        new_complaints_today: 5,
        resolution_rate: 78,
        department_staff: 12,
        active_staff: 11
      }
    },

    async loadRecentComplaints() {
      // Mock data - replace with actual API call
      this.recentComplaints = [
        {
          id: 1,
          complaint_number: 'CMP-2024-0156',
          title: 'Library access issue during exam period',
          status: 'pending',
          priority: 'high',
          created_by: { full_name: 'John Doe', username: 'johndoe' },
          created_at: new Date().toISOString()
        },
        {
          id: 2,
          complaint_number: 'CMP-2024-0155',
          title: 'Classroom air conditioning not working',
          status: 'in_progress',
          priority: 'medium',
          created_by: { full_name: 'Jane Smith', username: 'janesmith' },
          created_at: new Date(Date.now() - 86400000).toISOString()
        },
        {
          id: 3,
          complaint_number: 'CMP-2024-0154',
          title: 'WiFi connectivity problems in lab',
          status: 'resolved',
          priority: 'low',
          created_by: { full_name: 'Mike Johnson', username: 'mikej' },
          created_at: new Date(Date.now() - 172800000).toISOString()
        }
      ]
    },

    initializeCharts() {
      this.$nextTick(() => {
        this.createTrendsChart()
        this.createStatusChart()
      })
    },

    createTrendsChart() {
      const ctx = this.$refs.trendsChart?.getContext('2d')
      if (!ctx) return

      this.trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [
            {
              label: 'New Complaints',
              data: [12, 19, 15, 25, 22, 18],
              borderColor: '#667eea',
              backgroundColor: 'rgba(102, 126, 234, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: 'Resolved',
              data: [8, 15, 12, 20, 18, 16],
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            },
            x: {
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            }
          }
        }
      })
    },

    createStatusChart() {
      const ctx = this.$refs.statusChart?.getContext('2d')
      if (!ctx) return

      this.statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Pending', 'In Progress', 'Resolved', 'Rejected'],
          datasets: [{
            data: [23, 34, 89, 10],
            backgroundColor: [
              '#f59e0b',
              '#3b82f6',
              '#10b981',
              '#ef4444'
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      })
    },

    async refreshData() {
      await this.loadDashboardData()
      this.updateCharts()
      this.$toast.success('Dashboard data refreshed')
    },

    updateCharts() {
      if (this.trendsChart) {
        this.trendsChart.update()
      }
      if (this.statusChart) {
        this.statusChart.update()
      }
    },

    changePeriod(period) {
      this.currentPeriod = period
      // Update chart data based on period
      this.updateCharts()
    },

    viewComplaint(id) {
      this.$router.push(`/head/complaints/${id}`)
    },

    formatStatus(status) {
      const statusMap = {
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'resolved': 'Resolved',
        'rejected': 'Rejected',
        'not_resolved': 'Not Resolved',
        'closed': 'Closed'
      }
      return statusMap[status] || status
    },

    formatPriority(priority) {
      const priorityMap = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'urgent': 'Urgent'
      }
      return priorityMap[priority] || priority
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays === 1) return 'Today'
      if (diffDays === 2) return 'Yesterday'
      if (diffDays <= 7) return `${diffDays - 1} days ago`
      
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.head-dashboard {
  padding: 0;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* Header Section */
.dashboard-header {
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

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
}

.dashboard-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0.5rem 0 0 0;
}

.header-actions .btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.header-actions .btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
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
.stat-success .stat-icon { background: linear-gradient(135deg, #10b981, #059669); }
.stat-info .stat-icon { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }

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

.stat-change {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change i {
  font-size: 0.7rem;
}

/* Charts Section */
.charts-section {
  max-width: 1200px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
}

.chart-card, .content-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: none;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  display: flex;
  align-items: center;
}

.card-body {
  padding: 1.5rem;
}

/* Content Section */
.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Complaints List */
.complaints-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.complaint-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.complaint-item:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
  transform: translateX(4px);
}

.complaint-info {
  flex: 1;
}

.complaint-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.complaint-number {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #667eea;
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pending { background: #fef3c7; color: #92400e; }
.status-in_progress { background: #dbeafe; color: #1e40af; }
.status-resolved { background: #d1fae5; color: #065f46; }
.status-rejected { background: #fee2e2; color: #991b1b; }

.complaint-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.complaint-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #64748b;
}

.meta-item i {
  font-size: 0.7rem;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.action-item:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
  transform: translateX(4px);
  text-decoration: none;
  color: inherit;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.action-content {
  flex: 1;
}

.action-content h6 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #1a202c;
}

.action-content p {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.action-item i:last-child {
  color: #cbd5e0;
  font-size: 0.8rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .dashboard-title {
    font-size: 2rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .complaint-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .action-item {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 576px) {
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>
