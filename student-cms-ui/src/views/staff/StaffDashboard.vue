<template>
  <div class="staff-dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Staff Dashboard</h1>
        <p class="page-subtitle">Manage assigned complaints and support students</p>
      </div>
      <div class="header-actions">
        <BButton variant="outline-primary" @click="refreshDashboard" :disabled="isLoading">
          <i class="bi bi-arrow-clockwise me-2"></i>
          Refresh
        </BButton>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card primary">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-person-check"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.assigned }}</div>
              <div class="stats-label">Assigned to Me</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card warning">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.pending }}</div>
              <div class="stats-label">Pending Action</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card info">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-chat-dots"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.awaitingReply }}</div>
              <div class="stats-label">Awaiting Reply</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card success">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.resolved }}</div>
              <div class="stats-label">Resolved Today</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card quick-actions-card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-lightning me-2"></i>
              Quick Actions
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 mb-3">
                <router-link to="/staff/complaints" class="quick-action-btn">
                  <div class="quick-action-icon">
                    <i class="bi bi-list-task"></i>
                  </div>
                  <div class="quick-action-text">
                    <div class="action-title">View All Complaints</div>
                    <div class="action-subtitle">Manage assigned complaints</div>
                  </div>
                </router-link>
              </div>
              
              <div class="col-md-3 mb-3">
                <router-link to="/staff/withdrawals" class="quick-action-btn">
                  <div class="quick-action-icon">
                    <i class="bi bi-file-earmark-x"></i>
                  </div>
                  <div class="quick-action-text">
                    <div class="action-title">Withdrawal Requests</div>
                    <div class="action-subtitle">Review pending requests</div>
                  </div>
                </router-link>
              </div>
              
              <div class="col-md-3 mb-3">
                <BButton variant="outline-primary" class="quick-action-btn" @click="showForwardModal = true">
                  <div class="quick-action-icon">
                    <i class="bi bi-arrow-right-circle"></i>
                  </div>
                  <div class="quick-action-text">
                    <div class="action-title">Forward Complaint</div>
                    <div class="action-subtitle">Transfer to another staff</div>
                  </div>
                </BButton>
              </div>
              
              <div class="col-md-3 mb-3">
                <router-link to="/staff/notifications" class="quick-action-btn">
                  <div class="quick-action-icon">
                    <i class="bi bi-bell"></i>
                  </div>
                  <div class="quick-action-text">
                    <div class="action-title">Notifications</div>
                    <div class="action-subtitle">{{ unreadNotifications }} unread</div>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Complaints -->
    <div class="row">
      <div class="col-lg-8">
        <div class="card recent-complaints-card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock me-2"></i>
                Recent Complaints
              </h5>
              <router-link to="/staff/complaints" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <!-- Loading State -->
            <div v-if="isLoading" class="loading-spinner">
              <BSpinner class="spinner-border-custom" />
              <p class="mt-3 text-muted">Loading complaints...</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="recentComplaints.length === 0" class="empty-state">
              <div class="empty-state-icon">
                <i class="bi bi-inbox"></i>
              </div>
              <div class="empty-state-title">No recent complaints</div>
              <div class="empty-state-description">
                You don't have any complaints assigned to you yet.
              </div>
            </div>

            <!-- Complaints List -->
            <div v-else class="complaints-list">
              <div 
                v-for="complaint in recentComplaints" 
                :key="complaint.id"
                class="complaint-item"
                @click="viewComplaint(complaint.id)"
              >
                <div class="complaint-header">
                  <div class="complaint-info">
                    <h6 class="complaint-title">{{ complaint.title }}</h6>
                    <div class="complaint-meta">
                      <span class="complaint-number">{{ complaint.complaint_number }}</span>
                      <span class="separator">•</span>
                      <span class="complaint-date">{{ formatRelativeTime(complaint.created_at) }}</span>
                      <span class="separator">•</span>
                      <span class="complaint-student">{{ complaint.created_by_name }}</span>
                    </div>
                  </div>
                  <div class="complaint-badges">
                    <BBadge :variant="getStatusVariant(complaint.status)" class="status-badge">
                      {{ formatStatus(complaint.status) }}
                    </BBadge>
                    <BBadge :variant="getPriorityVariant(complaint.priority)" class="priority-badge">
                      {{ formatPriority(complaint.priority) }}
                    </BBadge>
                  </div>
                </div>
                
                <div class="complaint-description">
                  {{ truncateText(complaint.description, 120) }}
                </div>
                
                <div class="complaint-footer">
                  <div class="complaint-stats">
                    <span v-if="complaint.comments_count > 0" class="stat-item">
                      <i class="bi bi-chat-dots me-1"></i>
                      {{ complaint.comments_count }} comments
                    </span>
                    <span v-if="complaint.requires_reply" class="stat-item urgent">
                      <i class="bi bi-exclamation-circle me-1"></i>
                      Requires reply
                    </span>
                  </div>
                  <div class="complaint-actions">
                    <BButton
                      variant="outline-primary"
                      size="sm"
                      @click.stop="viewComplaint(complaint.id)"
                    >
                      <i class="bi bi-eye me-1"></i>
                      View
                    </BButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="col-lg-4">
        <!-- Priority Complaints -->
        <div class="card mb-4 priority-card">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="bi bi-exclamation-triangle me-2"></i>
              High Priority
            </h6>
          </div>
          <div class="card-body">
            <div v-if="priorityComplaints.length === 0" class="text-muted text-center py-3">
              No high priority complaints
            </div>
            <div v-else>
              <div 
                v-for="complaint in priorityComplaints" 
                :key="complaint.id"
                class="priority-item"
                @click="viewComplaint(complaint.id)"
              >
                <div class="priority-info">
                  <div class="priority-title">{{ truncateText(complaint.title, 40) }}</div>
                  <div class="priority-meta">
                    <span class="priority-number">{{ complaint.complaint_number }}</span>
                    <BBadge variant="danger" class="ms-2">{{ formatPriority(complaint.priority) }}</BBadge>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Summary -->
        <div class="card performance-card">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="bi bi-graph-up me-2"></i>
              This Week's Performance
            </h6>
          </div>
          <div class="card-body">
            <div class="performance-metrics">
              <div class="metric-item">
                <div class="metric-label">Complaints Resolved</div>
                <div class="metric-value">{{ weeklyStats.resolved }}</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Average Response Time</div>
                <div class="metric-value">{{ weeklyStats.avgResponseTime }}</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Student Satisfaction</div>
                <div class="metric-value">{{ weeklyStats.satisfaction }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Forward Complaint Modal -->
    <BModal
      v-model="showForwardModal"
      title="Forward Complaint"
      size="md"
      @ok="handleForward"
      ok-title="Forward"
      :ok-disabled="!forwardForm.complaint_id || !forwardForm.to_user"
    >
      <form>
        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-file-earmark me-2"></i>
            Select Complaint
          </label>
          <BFormSelect
            v-model="forwardForm.complaint_id"
            :options="forwardableComplaints"
            class="form-select"
          >
            <template #first>
              <BFormSelectOption value="" disabled>Choose a complaint to forward</BFormSelectOption>
            </template>
          </BFormSelect>
        </div>

        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-person me-2"></i>
            Forward To
          </label>
          <BFormSelect
            v-model="forwardForm.to_user"
            :options="staffOptions"
            class="form-select"
          >
            <template #first>
              <BFormSelectOption value="" disabled>Select staff member</BFormSelectOption>
            </template>
          </BFormSelect>
        </div>

        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-chat-square-text me-2"></i>
            Remarks (Optional)
          </label>
          <BFormTextarea
            v-model="forwardForm.remarks"
            placeholder="Add any notes or context for the receiving staff member..."
            rows="3"
            class="form-control"
          />
        </div>
      </form>
    </BModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComplaintsStore } from '@/stores/complaints'
import { useAuthStore } from '@/stores/auth'
import { formatDistanceToNow } from 'date-fns'

const router = useRouter()
const complaintsStore = useComplaintsStore()
const authStore = useAuthStore()

// Component state
const isLoading = ref(false)
const recentComplaints = ref([])
const priorityComplaints = ref([])
const showForwardModal = ref(false)
const unreadNotifications = ref(0)

// Statistics
const statistics = reactive({
  assigned: 0,
  pending: 0,
  awaitingReply: 0,
  resolved: 0
})

// Weekly stats
const weeklyStats = reactive({
  resolved: 0,
  avgResponseTime: '0h',
  satisfaction: 0
})

// Forward form
const forwardForm = reactive({
  complaint_id: '',
  to_user: '',
  remarks: ''
})

const forwardableComplaints = ref([])
const staffOptions = ref([])

// Methods
const fetchDashboardData = async () => {
  isLoading.value = true
  
  try {
    // Fetch recent complaints
    const complaintsResult = await complaintsStore.fetchStaffComplaints({ 
      page_size: 5,
      ordering: '-created_at'
    })
    
    if (complaintsResult.success) {
      recentComplaints.value = complaintsResult.data.results || []
    }

    // Fetch priority complaints
    const priorityResult = await complaintsStore.fetchStaffComplaints({ 
      priority: 'high,urgent',
      page_size: 5
    })
    
    if (priorityResult.success) {
      priorityComplaints.value = priorityResult.data.results || []
    }

    // Fetch statistics
    const statsResult = await complaintsStore.fetchStaffStatistics()
    if (statsResult.success) {
      Object.assign(statistics, statsResult.data)
    }

    // Fetch weekly performance
    const weeklyResult = await complaintsStore.fetchWeeklyStats()
    if (weeklyResult.success) {
      Object.assign(weeklyStats, weeklyResult.data)
    }

    // Fetch forwardable complaints for modal
    const forwardableResult = await complaintsStore.fetchStaffComplaints({ 
      status: 'pending,in_progress',
      page_size: 50
    })
    
    if (forwardableResult.success) {
      forwardableComplaints.value = forwardableResult.data.results.map(c => ({
        value: c.id,
        text: `${c.complaint_number} - ${c.title}`
      }))
    }

    // Fetch staff options
    const staffResult = await complaintsStore.fetchStaffList()
    if (staffResult.success) {
      staffOptions.value = staffResult.data.map(s => ({
        value: s.id,
        text: `${s.name} (${s.department})`
      }))
    }

  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

const refreshDashboard = () => {
  fetchDashboardData()
}

const viewComplaint = (id) => {
  router.push(`/staff/complaints/${id}`)
}

const handleForward = async () => {
  try {
    const result = await complaintsStore.forwardComplaint(forwardForm.complaint_id, {
      to_user: forwardForm.to_user,
      remarks: forwardForm.remarks
    })
    
    if (result.success) {
      // Reset form
      Object.assign(forwardForm, {
        complaint_id: '',
        to_user: '',
        remarks: ''
      })
      
      // Refresh data
      fetchDashboardData()
    }
  } catch (error) {
    console.error('Error forwarding complaint:', error)
  }
}

// Formatting methods
const formatRelativeTime = (date) => formatDistanceToNow(new Date(date), { addSuffix: true })

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    in_progress: 'In Progress',
    resolved: 'Resolved',
    rejected: 'Rejected',
    closed: 'Closed'
  }
  return statusMap[status] || status
}

const formatPriority = (priority) => {
  const priorityMap = {
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    urgent: 'Urgent'
  }
  return priorityMap[priority] || priority
}

const getStatusVariant = (status) => {
  const variantMap = {
    pending: 'warning',
    in_progress: 'info',
    resolved: 'success',
    rejected: 'danger',
    closed: 'secondary'
  }
  return variantMap[status] || 'secondary'
}

const getPriorityVariant = (priority) => {
  const variantMap = {
    low: 'success',
    medium: 'info',
    high: 'warning',
    urgent: 'danger'
  }
  return variantMap[priority] || 'secondary'
}

const truncateText = (text, length) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
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

.quick-actions-card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
}

.quick-action-btn {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  background: white;
  width: 100%;
}

.quick-action-btn:hover {
  border-color: #667eea;
  background: #f8f9ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.1);
}

.quick-action-icon {
  font-size: 1.5rem;
  color: #667eea;
  margin-right: 1rem;
}

.action-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.action-subtitle {
  font-size: 0.875rem;
  color: #6c757d;
}

.recent-complaints-card,
.priority-card,
.performance-card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
}

.complaint-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  background: white;
}

.complaint-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
}

.complaint-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.complaint-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.complaint-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.separator {
  color: #dee2e6;
}

.complaint-badges {
  display: flex;
  gap: 0.5rem;
}

.complaint-description {
  color: #495057;
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.complaint-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f3f4;
}

.complaint-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  font-size: 0.875rem;
  color: #6c757d;
  display: flex;
  align-items: center;
}

.stat-item.urgent {
  color: #dc3545;
  font-weight: 600;
}

.priority-item {
  padding: 0.75rem;
  border: 1px solid #f1f3f4;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.priority-item:hover {
  border-color: #dc3545;
  background: #fff5f5;
}

.priority-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.priority-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.priority-number {
  font-size: 0.8rem;
  color: #6c757d;
}

.performance-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f3f4;
}

.metric-item:last-child {
  border-bottom: none;
}

.metric-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.metric-value {
  font-weight: 600;
  color: #2c3e50;
}

/* Form Styling - Fixed */
.form-label {
  color: #495057 !important;
  font-weight: 600 !important;
  margin-bottom: 0.75rem !important;
  display: flex !important;
  align-items: center !important;
  font-size: 0.95rem !important;
}

.form-label i {
  color: #667eea !important;
  margin-right: 0.5rem !important;
}

.form-control,
.form-select {
  border: 1px solid #dee2e6 !important;
  border-radius: 8px !important;
  padding: 0.875rem 1rem !important;
  font-size: 1rem !important;
  line-height: 1.5 !important;
  transition: all 0.3s ease !important;
  margin-bottom: 0 !important;
  background-color: #fff !important;
  width: 100% !important;
}

.form-control:focus,
.form-select:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
  outline: none !important;
}

.form-control:hover,
.form-select:hover {
  border-color: #adb5bd !important;
}

.form-control::placeholder {
  color: #6c757d !important;
  opacity: 0.7 !important;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .btn {
    width: 100%;
  }
  
  .complaint-header {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .complaint-footer {
    flex-direction: column;
    gap: 0.75rem;
    align-items: flex-start;
  }
}
</style>
