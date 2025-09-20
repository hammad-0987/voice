<template>
  <div class="vc-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="dashboard-title">
            <i class="fas fa-crown me-3"></i>
            Vice Chancellor Dashboard
          </h1>
          <p class="dashboard-subtitle">
            System-wide overview and management
          </p>
        </div>
        <div class="header-actions">
          <b-button variant="light" @click="exportReport" class="me-2">
            <i class="fas fa-download me-2"></i>
            Export Report
          </b-button>
          <b-button variant="primary" @click="refreshData">
            <i class="fas fa-sync-alt me-2"></i>
            Refresh
          </b-button>
        </div>
      </div>
    </div>

    <!-- System Overview Stats -->
    <div class="stats-section">
      <div class="row g-4">
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="fas fa-university"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.total_departments || 0 }}</h3>
              <p class="stat-label">Total Departments</p>
              <small class="stat-change">
                <i class="fas fa-building"></i>
                {{ stats.active_departments || 0 }} active
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-info">
            <div class="stat-icon">
              <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.total_complaints || 0 }}</h3>
              <p class="stat-label">Total Complaints</p>
              <small class="stat-change positive">
                <i class="fas fa-arrow-up"></i>
                +{{ stats.new_complaints_week || 0 }} this week
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="fas fa-hourglass-half"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.pending_complaints || 0 }}</h3>
              <p class="stat-label">Pending Resolution</p>
              <small class="stat-change">
                <i class="fas fa-clock"></i>
                Needs attention
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="fas fa-chart-line"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.resolution_rate || 0 }}%</h3>
              <p class="stat-label">Resolution Rate</p>
              <small class="stat-change positive">
                <i class="fas fa-arrow-up"></i>
                +{{ stats.rate_improvement || 0 }}% vs last month
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts and Analytics -->
    <div class="analytics-section">
      <div class="row g-4">
        <!-- Department Performance Chart -->
        <div class="col-xl-8">
          <div class="chart-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-chart-bar me-2"></i>
                Department Performance Overview
              </h5>
              <div class="card-actions">
                <b-dropdown size="sm" variant="outline-secondary" text="View">
                  <b-dropdown-item @click="changeView('complaints')">By Complaints</b-dropdown-item>
                  <b-dropdown-item @click="changeView('resolution')">By Resolution Rate</b-dropdown-item>
                  <b-dropdown-item @click="changeView('satisfaction')">By Satisfaction</b-dropdown-item>
                </b-dropdown>
              </div>
            </div>
            <div class="card-body">
              <canvas ref="departmentChart" height="350"></canvas>
            </div>
          </div>
        </div>

        <!-- System Health -->
        <div class="col-xl-4">
          <div class="chart-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-heartbeat me-2"></i>
                System Health
              </h5>
            </div>
            <div class="card-body">
              <div class="health-metrics">
                <div class="health-item">
                  <div class="health-label">
                    <i class="fas fa-tachometer-alt"></i>
                    Response Time
                  </div>
                  <div class="health-value excellent">
                    <span class="value">2.3s</span>
                    <span class="status">Excellent</span>
                  </div>
                </div>

                <div class="health-item">
                  <div class="health-label">
                    <i class="fas fa-users"></i>
                    Active Users
                  </div>
                  <div class="health-value good">
                    <span class="value">{{ stats.active_users || 0 }}</span>
                    <span class="status">Good</span>
                  </div>
                </div>

                <div class="health-item">
                  <div class="health-label">
                    <i class="fas fa-database"></i>
                    System Load
                  </div>
                  <div class="health-value good">
                    <span class="value">67%</span>
                    <span class="status">Normal</span>
                  </div>
                </div>

                <div class="health-item">
                  <div class="health-label">
                    <i class="fas fa-shield-alt"></i>
                    Security Status
                  </div>
                  <div class="health-value excellent">
                    <span class="value">100%</span>
                    <span class="status">Secure</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trends Chart -->
      <div class="row g-4 mt-0">
        <div class="col-12">
          <div class="chart-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-chart-line me-2"></i>
                System-wide Trends (Last 12 Months)
              </h5>
              <div class="card-actions">
                <b-button-group size="sm">
                  <b-button 
                    :variant="trendsView === 'complaints' ? 'primary' : 'outline-secondary'"
                    @click="trendsView = 'complaints'"
                  >
                    Complaints
                  </b-button>
                  <b-button 
                    :variant="trendsView === 'satisfaction' ? 'primary' : 'outline-secondary'"
                    @click="trendsView = 'satisfaction'"
                  >
                    Satisfaction
                  </b-button>
                  <b-button 
                    :variant="trendsView === 'resolution' ? 'primary' : 'outline-secondary'"
                    @click="trendsView = 'resolution'"
                  >
                    Resolution
                  </b-button>
                </b-button-group>
              </div>
            </div>
            <div class="card-body">
              <canvas ref="trendsChart" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Management Overview -->
    <div class="management-section">
      <div class="row g-4">
        <!-- Critical Issues -->
        <div class="col-xl-6">
          <div class="content-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-exclamation-triangle me-2 text-danger"></i>
                Critical Issues Requiring Attention
              </h5>
              <router-link to="/vc/complaints?filter=critical" class="btn btn-sm btn-outline-danger">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <b-spinner variant="primary"></b-spinner>
                <p class="mt-2 text-muted">Loading critical issues...</p>
              </div>
              <div v-else-if="criticalIssues.length === 0" class="text-center py-4">
                <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
                <p class="text-muted">No critical issues at the moment</p>
              </div>
              <div v-else class="issues-list">
                <div 
                  v-for="issue in criticalIssues" 
                  :key="issue.id"
                  class="issue-item"
                  @click="viewIssue(issue.id)"
                >
                  <div class="issue-priority critical">
                    <i class="fas fa-exclamation-triangle"></i>
                  </div>
                  <div class="issue-content">
                    <h6 class="issue-title">{{ issue.title }}</h6>
                    <p class="issue-department">{{ issue.department }}</p>
                    <small class="issue-time">{{ formatDate(issue.created_at) }}</small>
                  </div>
                  <div class="issue-status">
                    <span :class="['status-badge', `status-${issue.status}`]">
                      {{ formatStatus(issue.status) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Department Rankings -->
        <div class="col-xl-6">
          <div class="content-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-trophy me-2 text-warning"></i>
                Department Performance Rankings
              </h5>
              <b-dropdown size="sm" variant="outline-secondary" text="This Month">
                <b-dropdown-item @click="changeRankingPeriod('month')">This Month</b-dropdown-item>
                <b-dropdown-item @click="changeRankingPeriod('quarter')">This Quarter</b-dropdown-item>
                <b-dropdown-item @click="changeRankingPeriod('year')">This Year</b-dropdown-item>
              </b-dropdown>
            </div>
            <div class="card-body">
              <div class="rankings-list">
                <div 
                  v-for="(dept, index) in departmentRankings" 
                  :key="dept.id"
                  class="ranking-item"
                >
                  <div class="ranking-position">
                    <span :class="['position-badge', getRankingClass(index)]">
                      {{ index + 1 }}
                    </span>
                  </div>
                  <div class="ranking-content">
                    <h6 class="dept-name">{{ dept.name }}</h6>
                    <div class="dept-metrics">
                      <span class="metric">
                        <i class="fas fa-check-circle text-success"></i>
                        {{ dept.resolution_rate }}% resolved
                      </span>
                      <span class="metric">
                        <i class="fas fa-star text-warning"></i>
                        {{ dept.satisfaction_score }}/5.0
                      </span>
                    </div>
                  </div>
                  <div class="ranking-score">
                    <span class="score">{{ dept.overall_score }}</span>
                    <small>Overall</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="actions-section">
      <div class="row g-4">
        <div class="col-12">
          <div class="content-card">
            <div class="card-header">
              <h5 class="card-title">
                <i class="fas fa-bolt me-2"></i>
                Executive Actions
              </h5>
            </div>
            <div class="card-body">
              <div class="executive-actions">
                <router-link to="/vc/complaints" class="exec-action">
                  <div class="action-icon bg-primary">
                    <i class="fas fa-list-alt"></i>
                  </div>
                  <div class="action-details">
                    <h6>All Complaints</h6>
                    <p>Review and manage system-wide complaints</p>
                  </div>
                </router-link>

                <router-link to="/vc/analytics" class="exec-action">
                  <div class="action-icon bg-info">
                    <i class="fas fa-chart-pie"></i>
                  </div>
                  <div class="action-details">
                    <h6>Global Analytics</h6>
                    <p>Comprehensive system analytics and insights</p>
                  </div>
                </router-link>

                <router-link to="/vc/reports" class="exec-action">
                  <div class="action-icon bg-success">
                    <i class="fas fa-file-chart-line"></i>
                  </div>
                  <div class="action-details">
                    <h6>System Reports</h6>
                    <p>Generate detailed performance reports</p>
                  </div>
                </router-link>

                <router-link to="/admin/users" class="exec-action">
                  <div class="action-icon bg-warning">
                    <i class="fas fa-users-cog"></i>
                  </div>
                  <div class="action-details">
                    <h6>User Management</h6>
                    <p>Manage system users and permissions</p>
                  </div>
                </router-link>

                <router-link to="/vc/withdrawals" class="exec-action">
                  <div class="action-icon bg-danger">
                    <i class="fas fa-file-signature"></i>
                  </div>
                  <div class="action-details">
                    <h6>Withdrawal Approvals</h6>
                    <p>Review and approve withdrawal requests</p>
                  </div>
                </router-link>

                <router-link to="/admin/settings" class="exec-action">
                  <div class="action-icon bg-secondary">
                    <i class="fas fa-cogs"></i>
                  </div>
                  <div class="action-details">
                    <h6>System Settings</h6>
                    <p>Configure system-wide settings</p>
                  </div>
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
import { mapState } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import Chart from 'chart.js/auto'

export default {
  name: 'VCDashboard',
  data() {
    return {
      loading: true,
      stats: {
        total_departments: 8,
        active_departments: 8,
        total_complaints: 1247,
        new_complaints_week: 23,
        pending_complaints: 45,
        resolution_rate: 87,
        rate_improvement: 5,
        active_users: 342
      },
      criticalIssues: [],
      departmentRankings: [],
      departmentChart: null,
      trendsChart: null,
      currentView: 'complaints',
      trendsView: 'complaints',
      rankingPeriod: 'month'
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
    if (this.departmentChart) {
      this.departmentChart.destroy()
    }
    if (this.trendsChart) {
      this.trendsChart.destroy()
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true
        
        await Promise.all([
          this.loadCriticalIssues(),
          this.loadDepartmentRankings()
        ])
        
      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$toast.error('Failed to load dashboard data')
      } finally {
        this.loading = false
      }
    },

    async loadCriticalIssues() {
      // Mock data - replace with actual API call
      this.criticalIssues = [
        {
          id: 1,
          title: 'Server downtime affecting multiple departments',
          department: 'IT Services',
          status: 'pending',
          created_at: new Date().toISOString()
        },
        {
          id: 2,
          title: 'Library access system failure',
          department: 'Library Services',
          status: 'in_progress',
          created_at: new Date(Date.now() - 3600000).toISOString()
        }
      ]
    },

    async loadDepartmentRankings() {
      // Mock data - replace with actual API call
      this.departmentRankings = [
        {
          id: 1,
          name: 'Computer Science',
          resolution_rate: 95,
          satisfaction_score: 4.8,
          overall_score: 94
        },
        {
          id: 2,
          name: 'Engineering',
          resolution_rate: 89,
          satisfaction_score: 4.5,
          overall_score: 87
        },
        {
          id: 3,
          name: 'Business Administration',
          resolution_rate: 85,
          satisfaction_score: 4.3,
          overall_score: 84
        },
        {
          id: 4,
          name: 'Arts & Sciences',
          resolution_rate: 82,
          satisfaction_score: 4.1,
          overall_score: 81
        }
      ]
    },

    initializeCharts() {
      this.$nextTick(() => {
        this.createDepartmentChart()
        this.createTrendsChart()
      })
    },

    createDepartmentChart() {
      const ctx = this.$refs.departmentChart?.getContext('2d')
      if (!ctx) return

      this.departmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Computer Science', 'Engineering', 'Business', 'Arts & Sciences', 'Medicine', 'Law', 'Education', 'Architecture'],
          datasets: [
            {
              label: 'Total Complaints',
              data: [45, 67, 23, 34, 56, 12, 28, 19],
              backgroundColor: 'rgba(102, 126, 234, 0.8)',
              borderColor: '#667eea',
              borderWidth: 1
            },
            {
              label: 'Resolved',
              data: [42, 59, 20, 28, 48, 11, 25, 17],
              backgroundColor: 'rgba(16, 185, 129, 0.8)',
              borderColor: '#10b981',
              borderWidth: 1
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

    createTrendsChart() {
      const ctx = this.$refs.trendsChart?.getContext('2d')
      if (!ctx) return

      this.trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
              label: 'New Complaints',
              data: [65, 78, 66, 89, 95, 87, 92, 78, 85, 90, 88, 82],
              borderColor: '#667eea',
              backgroundColor: 'rgba(102, 126, 234, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: 'Resolved',
              data: [58, 72, 61, 82, 88, 81, 87, 74, 79, 85, 83, 78],
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: 'Satisfaction Score',
              data: [4.2, 4.3, 4.1, 4.4, 4.5, 4.3, 4.6, 4.4, 4.5, 4.7, 4.6, 4.8],
              borderColor: '#f59e0b',
              backgroundColor: 'rgba(245, 158, 11, 0.1)',
              tension: 0.4,
              yAxisID: 'y1'
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
              type: 'linear',
              display: true,
              position: 'left',
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              min: 0,
              max: 5,
              grid: {
                drawOnChartArea: false,
              },
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

    async refreshData() {
      await this.loadDashboardData()
      this.updateCharts()
      this.$toast.success('Dashboard data refreshed')
    },

    updateCharts() {
      if (this.departmentChart) {
        this.departmentChart.update()
      }
      if (this.trendsChart) {
        this.trendsChart.update()
      }
    },

    changeView(view) {
      this.currentView = view
      // Update department chart based on view
      this.updateCharts()
    },

    changeRankingPeriod(period) {
      this.rankingPeriod = period
      this.loadDepartmentRankings()
    },

    exportReport() {
      // Implement report export functionality
      this.$toast.info('Generating report...')
    },

    viewIssue(id) {
      this.$router.push(`/vc/complaints/${id}`)
    },

    getRankingClass(index) {
      if (index === 0) return 'gold'
      if (index === 1) return 'silver'
      if (index === 2) return 'bronze'
      return 'default'
    },

    formatStatus(status) {
      const statusMap = {
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'resolved': 'Resolved',
        'rejected': 'Rejected'
      }
      return statusMap[status] || status
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffHours = Math.ceil(diffTime / (1000 * 60 * 60))
      
      if (diffHours < 1) return 'Just now'
      if (diffHours < 24) return `${diffHours}h ago`
      
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      if (diffDays === 1) return 'Yesterday'
      if (diffDays <= 7) return `${diffDays} days ago`
      
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.vc-dashboard {
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
  max-width: 1400px;
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

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.header-actions .btn {
  backdrop-filter: blur(10px);
}

.header-actions .btn-light {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .btn-light:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  color: white;
}

.header-actions .btn-primary {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .btn-primary:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

/* Stats Section */
.stats-section {
  max-width: 1400px;
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
.stat-info .stat-icon { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
.stat-warning .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
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

.stat-change {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #64748b;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change i {
  font-size: 0.7rem;
}

/* Analytics Section */
.analytics-section {
  max-width: 1400px;
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

/* System Health */
.health-metrics {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.health-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.health-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.health-label i {
  color: #6b7280;
}

.health-value {
  text-align: right;
}

.health-value .value {
  font-size: 1.1rem;
  font-weight: 600;
  display: block;
}

.health-value .status {
  font-size: 0.8rem;
  text-transform: uppercase;
  font-weight: 500;
}

.health-value.excellent .value { color: #10b981; }
.health-value.excellent .status { color: #10b981; }
.health-value.good .value { color: #3b82f6; }
.health-value.good .status { color: #3b82f6; }
.health-value.warning .value { color: #f59e0b; }
.health-value.warning .status { color: #f59e0b; }

/* Management Section */
.management-section {
  max-width: 1400px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
}

/* Critical Issues */
.issues-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.issue-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.issue-item:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
  transform: translateX(4px);
}

.issue-priority {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.issue-priority.critical {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.issue-content {
  flex: 1;
}

.issue-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
}

.issue-department {
  font-size: 0.85rem;
  color: #6b7280;
  margin: 0 0 0.25rem 0;
}

.issue-time {
  font-size: 0.75rem;
  color: #9ca3af;
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

/* Department Rankings */
.rankings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.ranking-item:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
}

.ranking-position {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.position-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: white;
}

.position-badge.gold { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
.position-badge.silver { background: linear-gradient(135deg, #e5e7eb, #d1d5db); color: #374151; }
.position-badge.bronze { background: linear-gradient(135deg, #d97706, #b45309); }
.position-badge.default { background: linear-gradient(135deg, #6b7280, #4b5563); }

.ranking-content {
  flex: 1;
}

.dept-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.dept-metrics {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.metric {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.ranking-score {
  text-align: center;
}

.ranking-score .score {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  display: block;
}

.ranking-score small {
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
}

/* Executive Actions */
.actions-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.executive-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.exec-action {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.exec-action:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.3rem;
}

.action-details h6 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #1a202c;
}

.action-details p {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
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
  
  .health-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .issue-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .ranking-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .executive-actions {
    grid-template-columns: 1fr;
  }
  
  .exec-action {
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
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
}
</style>
