<template>
  <div class="my-complaints">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">My Complaints</h1>
        <p class="page-subtitle">Track and manage all your submitted complaints</p>
      </div>
      <div class="header-actions">
        <router-link to="/student/file-complaint" class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i>
          File New Complaint
        </router-link>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="card mb-4 filters-card">
      <div class="card-body">
        <div class="row align-items-end">
          <!-- Search -->
          <div class="col-md-4 mb-3">
            <label class="form-label">
              <i class="bi bi-search me-2"></i>
              Search Complaints
            </label>
            <div class="input-group">
              <BFormInput
                v-model="filters.search"
                placeholder="Search by title or complaint number..."
                @input="debouncedSearch"
                class="form-control"
              />
              <BInputGroupText>
                <i class="bi bi-search"></i>
              </BInputGroupText>
            </div>
          </div>

          <!-- Status Filter -->
          <div class="col-md-3 mb-3">
            <label class="form-label">
              <i class="bi bi-flag me-2"></i>
              Status
            </label>
            <BFormSelect
              v-model="filters.status"
              :options="statusOptions"
              @change="applyFilters"
              class="form-select"
            />
          </div>

          <!-- Priority Filter -->
          <div class="col-md-3 mb-3">
            <label class="form-label">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Priority
            </label>
            <BFormSelect
              v-model="filters.priority"
              :options="priorityOptions"
              @change="applyFilters"
              class="form-select"
            />
          </div>

          <!-- Clear Filters -->
          <div class="col-md-2 mb-3">
            <BButton
              variant="outline-secondary"
              @click="clearFilters"
              class="w-100"
            >
              <i class="bi bi-x-circle me-1"></i>
              Clear
            </BButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card primary">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stats-number">{{ statistics.total }}</div>
            <div class="stats-label">Total Complaints</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card warning">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-clock"></i>
            </div>
            <div class="stats-number">{{ statistics.pending }}</div>
            <div class="stats-label">Pending</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card info">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-gear"></i>
            </div>
            <div class="stats-number">{{ statistics.inProgress }}</div>
            <div class="stats-label">In Progress</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card success">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stats-number">{{ statistics.resolved }}</div>
            <div class="stats-label">Resolved</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Complaints List -->
    <div class="card complaints-card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">
            <i class="bi bi-list-ul me-2"></i>
            Complaints List
          </h5>
          <div class="view-options">
            <BButtonGroup size="sm">
              <BButton
                :variant="viewMode === 'list' ? 'primary' : 'outline-primary'"
                @click="viewMode = 'list'"
              >
                <i class="bi bi-list"></i>
              </BButton>
              <BButton
                :variant="viewMode === 'grid' ? 'primary' : 'outline-primary'"
                @click="viewMode = 'grid'"
              >
                <i class="bi bi-grid"></i>
              </BButton>
            </BButtonGroup>
          </div>
        </div>
      </div>
      
      <div class="card-body">
        <!-- Loading State -->
        <div v-if="isLoading" class="loading-spinner">
          <BSpinner class="spinner-border-custom" />
          <p class="mt-3 text-muted">Loading your complaints...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="complaints.length === 0" class="empty-state">
          <div class="empty-state-icon">
            <i class="bi bi-inbox"></i>
          </div>
          <div class="empty-state-title">No complaints found</div>
          <div class="empty-state-description">
            {{ hasActiveFilters ? 'No complaints match your current filters.' : 'You haven\'t filed any complaints yet.' }}
          </div>
          <router-link 
            v-if="!hasActiveFilters" 
            to="/student/file-complaint" 
            class="btn btn-primary"
          >
            <i class="bi bi-plus-circle me-2"></i>
            File Your First Complaint
          </router-link>
          <BButton 
            v-else 
            variant="outline-secondary" 
            @click="clearFilters"
          >
            <i class="bi bi-x-circle me-2"></i>
            Clear Filters
          </BButton>
        </div>

        <!-- List View -->
        <div v-else-if="viewMode === 'list'" class="complaints-list">
          <div 
            v-for="complaint in complaints" 
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
                  <span class="complaint-date">{{ formatDate(complaint.created_at) }}</span>
                  <span class="separator">•</span>
                  <span class="complaint-department">{{ complaint.department_name }}</span>
                </div>
              </div>
              <div class="complaint-badges">
                <BBadge 
                  :variant="getStatusVariant(complaint.status)"
                  class="status-badge"
                >
                  {{ formatStatus(complaint.status) }}
                </BBadge>
                <BBadge 
                  :variant="getPriorityVariant(complaint.priority)"
                  class="priority-badge"
                >
                  {{ formatPriority(complaint.priority) }}
                </BBadge>
              </div>
            </div>
            
            <div class="complaint-description">
              {{ truncateText(complaint.description, 150) }}
            </div>
            
            <div class="complaint-footer">
              <div class="complaint-stats">
                <span v-if="complaint.comments_count > 0" class="stat-item">
                  <i class="bi bi-chat-dots me-1"></i>
                  {{ complaint.comments_count }} comments
                </span>
                <span v-if="complaint.attachments_count > 0" class="stat-item">
                  <i class="bi bi-paperclip me-1"></i>
                  {{ complaint.attachments_count }} files
                </span>
                <span class="stat-item">
                  <i class="bi bi-clock me-1"></i>
                  Updated {{ formatRelativeTime(complaint.updated_at) }}
                </span>
              </div>
              <div class="complaint-actions">
                <BButton
                  variant="outline-primary"
                  size="sm"
                  @click.stop="viewComplaint(complaint.id)"
                >
                  <i class="bi bi-eye me-1"></i>
                  View Details
                </BButton>
              </div>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-else class="complaints-grid">
          <div class="row">
            <div 
              v-for="complaint in complaints" 
              :key="complaint.id"
              class="col-lg-4 col-md-6 mb-4"
            >
              <div class="complaint-card card-hover" @click="viewComplaint(complaint.id)">
                <div class="card-header">
                  <div class="d-flex justify-content-between align-items-start">
                    <h6 class="card-title mb-0">{{ truncateText(complaint.title, 50) }}</h6>
                    <BBadge 
                      :variant="getStatusVariant(complaint.status)"
                      class="status-badge"
                    >
                      {{ formatStatus(complaint.status) }}
                    </BBadge>
                  </div>
                  <div class="complaint-number">{{ complaint.complaint_number }}</div>
                </div>
                
                <div class="card-body">
                  <p class="complaint-description">
                    {{ truncateText(complaint.description, 100) }}
                  </p>
                  
                  <div class="complaint-meta">
                    <div class="meta-item">
                      <i class="bi bi-building me-1"></i>
                      {{ complaint.department_name }}
                    </div>
                    <div class="meta-item">
                      <i class="bi bi-flag me-1"></i>
                      {{ formatPriority(complaint.priority) }}
                    </div>
                    <div class="meta-item">
                      <i class="bi bi-calendar me-1"></i>
                      {{ formatDate(complaint.created_at) }}
                    </div>
                  </div>
                </div>
                
                <div class="card-footer">
                  <div class="complaint-stats">
                    <span v-if="complaint.comments_count > 0" class="stat-item">
                      <i class="bi bi-chat-dots me-1"></i>
                      {{ complaint.comments_count }}
                    </span>
                    <span v-if="complaint.attachments_count > 0" class="stat-item">
                      <i class="bi bi-paperclip me-1"></i>
                      {{ complaint.attachments_count }}
                    </span>
                  </div>
                  <BButton
                    variant="outline-primary"
                    size="sm"
                    @click.stop="viewComplaint(complaint.id)"
                  >
                    View
                  </BButton>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-wrapper">
          <BPagination
            v-model="currentPage"
            :total-rows="totalComplaints"
            :per-page="perPage"
            @page-click="handlePageChange"
            align="center"
            size="sm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useComplaintsStore } from '@/stores/complaints'
import { formatDistanceToNow, format } from 'date-fns'

const router = useRouter()
const complaintsStore = useComplaintsStore()

// Component state
const complaints = ref([])
const isLoading = ref(false)
const viewMode = ref('list')
const currentPage = ref(1)
const perPage = ref(10)
const totalComplaints = ref(0)
const totalPages = ref(0)

// Filters
const filters = reactive({
  search: '',
  status: '',
  priority: ''
})

// Statistics
const statistics = reactive({
  total: 0,
  pending: 0,
  inProgress: 0,
  resolved: 0
})

// Filter options
const statusOptions = ref([
  { value: '', text: 'All Statuses' },
  { value: 'pending', text: 'Pending' },
  { value: 'in_progress', text: 'In Progress' },
  { value: 'resolved', text: 'Resolved' },
  { value: 'rejected', text: 'Rejected' },
  { value: 'closed', text: 'Closed' }
])

const priorityOptions = ref([
  { value: '', text: 'All Priorities' },
  { value: 'low', text: 'Low' },
  { value: 'medium', text: 'Medium' },
  { value: 'high', text: 'High' },
  { value: 'urgent', text: 'Urgent' }
])

// Computed
const hasActiveFilters = computed(() => {
  return filters.search || filters.status || filters.priority
})

// Methods
const fetchComplaints = async () => {
  isLoading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: perPage.value,
      search: filters.search || undefined,
      status: filters.status || undefined,
      priority: filters.priority || undefined
    }
    
    const result = await complaintsStore.fetchMyComplaints(params)
    
    if (result.success) {
      complaints.value = result.data.results
      totalComplaints.value = result.data.count
      totalPages.value = Math.ceil(totalComplaints.value / perPage.value)
    }
  } catch (error) {
    console.error('Error fetching complaints:', error)
  } finally {
    isLoading.value = false
  }
}

const fetchStatistics = async () => {
  try {
    const result = await complaintsStore.fetchComplaintStatistics()
    if (result.success) {
      Object.assign(statistics, result.data)
    }
  } catch (error) {
    console.error('Error fetching statistics:', error)
  }
}

const applyFilters = () => {
  currentPage.value = 1
  fetchComplaints()
}

const clearFilters = () => {
  Object.assign(filters, {
    search: '',
    status: '',
    priority: ''
  })
  currentPage.value = 1
  fetchComplaints()
}

// Debounced search
let searchTimeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchComplaints()
}

const viewComplaint = (id) => {
  router.push(`/student/complaints/${id}`)
}

// Formatting methods
const formatDate = (date) => {
  return format(new Date(date), 'MMM dd, yyyy')
}

const formatRelativeTime = (date) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

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
  fetchComplaints()
  fetchStatistics()
})

// Watch for view mode changes
watch(viewMode, () => {
  // Save preference to localStorage
  localStorage.setItem('complaintsViewMode', viewMode.value)
})

// Load saved view mode
onMounted(() => {
  const savedViewMode = localStorage.getItem('complaintsViewMode')
  if (savedViewMode) {
    viewMode.value = savedViewMode
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
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

.filters-card {
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.complaints-card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
}

.complaints-card .card-header {
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 1.5rem;
}

.view-options .btn {
  padding: 0.375rem 0.75rem;
}

/* List View Styles */
.complaints-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.complaint-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
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
  margin-bottom: 1rem;
}

.complaint-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
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
  margin-bottom: 1rem;
}

.complaint-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
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

/* Grid View Styles */
.complaints-grid .complaint-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
}

.complaints-grid .complaint-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.complaints-grid .card-header {
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 1rem;
}

.complaints-grid .card-body {
  padding: 1rem;
  flex: 1;
}

.complaints-grid .card-footer {
  background: transparent;
  border-top: 1px solid #f1f3f4;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.complaint-number {
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 500;
  margin-top: 0.25rem;
}

.complaint-meta .meta-item {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

/* Responsive Design */
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
    gap: 1rem;
  }
  
  .complaint-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .complaint-stats {
    flex-wrap: wrap;
  }
}
</style>
