<template>
  <div class="staff-complaints">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">My Assigned Complaints</h1>
        <p class="page-subtitle">Manage and respond to complaints assigned to you</p>
      </div>
      <div class="header-actions">
        <BButton variant="outline-primary" @click="refreshComplaints" :disabled="isLoading">
          <i class="bi bi-arrow-clockwise me-2"></i>
          Refresh
        </BButton>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="card mb-4">
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
                placeholder="Search by title, number, or student name..."
                @input="debouncedSearch"
                class="form-control"
              />
              <BInputGroupText>
                <i class="bi bi-search"></i>
              </BInputGroupText>
            </div>
          </div>

          <!-- Status Filter -->
          <div class="col-md-2 mb-3">
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
          <div class="col-md-2 mb-3">
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

          <!-- Sort -->
          <div class="col-md-2 mb-3">
            <label class="form-label">
              <i class="bi bi-sort-down me-2"></i>
              Sort By
            </label>
            <BFormSelect
              v-model="filters.ordering"
              :options="sortOptions"
              @change="applyFilters"
              class="form-select"
            />
          </div>

          <!-- Actions -->
          <div class="col-md-2 mb-3">
            <BButton
              variant="outline-secondary"
              @click="clearFilters"
              class="w-100"
            >
              <i class="bi bi-x-circle me-2"></i>
              Clear
            </BButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Summary -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="stats-card primary">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-list-task"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ filteredStats.total }}</div>
              <div class="stats-label">Total Assigned</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="stats-card warning">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ filteredStats.pending }}</div>
              <div class="stats-label">Pending</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="stats-card info">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-arrow-repeat"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ filteredStats.inProgress }}</div>
              <div class="stats-label">In Progress</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="stats-card success">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ filteredStats.resolved }}</div>
              <div class="stats-label">Resolved</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Complaints List -->
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">
            <i class="bi bi-list me-2"></i>
            Complaints ({{ pagination.count || 0 }})
          </h5>
          <div class="d-flex align-items-center gap-2">
            <span class="text-muted">Show:</span>
            <BFormSelect
              v-model="pagination.page_size"
              :options="pageSizeOptions"
              @change="applyFilters"
              size="sm"
              style="width: auto;"
            />
          </div>
        </div>
      </div>
      
      <div class="card-body">
        <!-- Loading State -->
        <div v-if="isLoading" class="loading-spinner">
          <BSpinner class="spinner-border-custom" />
          <p class="mt-3 text-muted">Loading complaints...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="complaints.length === 0" class="empty-state">
          <div class="empty-state-icon">
            <i class="bi bi-inbox"></i>
          </div>
          <div class="empty-state-title">No complaints found</div>
          <div class="empty-state-description">
            {{ filters.search || filters.status !== '' || filters.priority !== '' 
               ? 'No complaints match your current filters.' 
               : 'You don\'t have any complaints assigned to you yet.' }}
          </div>
          <BButton 
            v-if="filters.search || filters.status !== '' || filters.priority !== ''"
            variant="outline-primary" 
            @click="clearFilters"
            class="mt-3"
          >
            Clear Filters
          </BButton>
        </div>

        <!-- Complaints Table -->
        <div v-else class="complaints-table">
          <div 
            v-for="complaint in complaints" 
            :key="complaint.id"
            class="complaint-row"
            @click="viewComplaint(complaint.id)"
          >
            <div class="complaint-main">
              <div class="complaint-header">
                <div class="complaint-info">
                  <h6 class="complaint-title">{{ complaint.title }}</h6>
                  <div class="complaint-meta">
                    <span class="complaint-number">{{ complaint.complaint_number }}</span>
                    <span class="separator">•</span>
                    <span class="complaint-date">{{ formatRelativeTime(complaint.created_at) }}</span>
                    <span class="separator">•</span>
                    <span class="complaint-student">{{ complaint.created_by_name }}</span>
                    <span class="separator">•</span>
                    <span class="complaint-department">{{ complaint.department_name }}</span>
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
                {{ truncateText(complaint.description, 150) }}
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
                  <span v-if="complaint.has_attachment" class="stat-item">
                    <i class="bi bi-paperclip me-1"></i>
                    Has attachment
                  </span>
                  <span class="stat-item">
                    <i class="bi bi-clock me-1"></i>
                    {{ formatRelativeTime(complaint.updated_at) }}
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
                  <BDropdown
                    variant="outline-secondary"
                    size="sm"
                    no-caret
                    @click.stop
                  >
                    <template #button-content>
                      <i class="bi bi-three-dots"></i>
                    </template>
                    <BDropdownItem @click="addComment(complaint.id)">
                      <i class="bi bi-chat-plus me-2"></i>
                      Add Comment
                    </BDropdownItem>
                    <BDropdownItem @click="forwardComplaint(complaint.id)">
                      <i class="bi bi-arrow-right me-2"></i>
                      Forward
                    </BDropdownItem>
                    <BDropdownItem @click="updateStatus(complaint.id)">
                      <i class="bi bi-flag me-2"></i>
                      Update Status
                    </BDropdownItem>
                  </BDropdown>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.count > pagination.page_size" class="d-flex justify-content-between align-items-center mt-4">
          <div class="pagination-info">
            Showing {{ ((pagination.current_page - 1) * pagination.page_size) + 1 }} to 
            {{ Math.min(pagination.current_page * pagination.page_size, pagination.count) }} 
            of {{ pagination.count }} complaints
          </div>
          <BPagination
            v-model="pagination.current_page"
            :total-rows="pagination.count"
            :per-page="pagination.page_size"
            @page-click="handlePageChange"
            size="sm"
            class="mb-0"
          />
        </div>
      </div>
    </div>

    <!-- Quick Comment Modal -->
    <BModal
      v-model="showCommentModal"
      title="Add Comment"
      size="md"
      @ok="handleAddComment"
      ok-title="Add Comment"
      :ok-disabled="!commentForm.text.trim()"
    >
      <form>
        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-chat-square-text me-2"></i>
            Comment Type
          </label>
          <BFormSelect
            v-model="commentForm.comment_type"
            :options="commentTypeOptions"
            class="form-select"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-pencil me-2"></i>
            Comment Text
          </label>
          <BFormTextarea
            v-model="commentForm.text"
            placeholder="Enter your comment, question, or information request..."
            rows="4"
            class="form-control"
          />
        </div>
      </form>
    </BModal>

    <!-- Forward Modal -->
    <BModal
      v-model="showForwardModal"
      title="Forward Complaint"
      size="md"
      @ok="handleForward"
      ok-title="Forward"
      :ok-disabled="!forwardForm.to_user"
    >
      <form>
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

    <!-- Status Update Modal -->
    <BModal
      v-model="showStatusModal"
      title="Update Status"
      size="md"
      @ok="handleStatusUpdate"
      ok-title="Update"
      :ok-disabled="!statusForm.status"
    >
      <form>
        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-flag me-2"></i>
            New Status
          </label>
          <BFormSelect
            v-model="statusForm.status"
            :options="statusUpdateOptions"
            class="form-select"
          >
            <template #first>
              <BFormSelectOption value="" disabled>Select new status</BFormSelectOption>
            </template>
          </BFormSelect>
        </div>

        <div class="mb-3">
          <label class="form-label">
            <i class="bi bi-chat-square-text me-2"></i>
            Notes (Optional)
          </label>
          <BFormTextarea
            v-model="statusForm.notes"
            placeholder="Add any notes about this status change..."
            rows="3"
            class="form-control"
          />
        </div>
      </form>
    </BModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComplaintsStore } from '@/stores/complaints'
import { formatDistanceToNow } from 'date-fns'
import { debounce } from 'lodash-es'

const router = useRouter()
const complaintsStore = useComplaintsStore()

// Component state
const isLoading = ref(false)
const complaints = ref([])
const showCommentModal = ref(false)
const showForwardModal = ref(false)
const showStatusModal = ref(false)
const selectedComplaintId = ref(null)

// Filters
const filters = reactive({
  search: '',
  status: '',
  priority: '',
  ordering: '-created_at'
})

// Pagination
const pagination = reactive({
  current_page: 1,
  page_size: 10,
  count: 0
})

// Forms
const commentForm = reactive({
  comment_type: 'comment',
  text: ''
})

const forwardForm = reactive({
  to_user: '',
  remarks: ''
})

const statusForm = reactive({
  status: '',
  notes: ''
})

// Options
const statusOptions = [
  { value: '', text: 'All Statuses' },
  { value: 'pending', text: 'Pending' },
  { value: 'in_progress', text: 'In Progress' },
  { value: 'resolved', text: 'Resolved' },
  { value: 'rejected', text: 'Rejected' }
]

const priorityOptions = [
  { value: '', text: 'All Priorities' },
  { value: 'low', text: 'Low' },
  { value: 'medium', text: 'Medium' },
  { value: 'high', text: 'High' },
  { value: 'urgent', text: 'Urgent' }
]

const sortOptions = [
  { value: '-created_at', text: 'Newest First' },
  { value: 'created_at', text: 'Oldest First' },
  { value: '-updated_at', text: 'Recently Updated' },
  { value: 'priority', text: 'Priority' },
  { value: 'status', text: 'Status' }
]

const pageSizeOptions = [
  { value: 5, text: '5' },
  { value: 10, text: '10' },
  { value: 25, text: '25' },
  { value: 50, text: '50' }
]

const commentTypeOptions = [
  { value: 'comment', text: 'Comment' },
  { value: 'require_info', text: 'Require Information' },
  { value: 'ask_question', text: 'Ask Question' }
]

const statusUpdateOptions = [
  { value: 'in_progress', text: 'In Progress' },
  { value: 'resolved', text: 'Resolved' },
  { value: 'rejected', text: 'Rejected' }
]

const staffOptions = ref([])

// Computed
const filteredStats = computed(() => {
  return {
    total: complaints.value.length,
    pending: complaints.value.filter(c => c.status === 'pending').length,
    inProgress: complaints.value.filter(c => c.status === 'in_progress').length,
    resolved: complaints.value.filter(c => c.status === 'resolved').length
  }
})

// Methods
const fetchComplaints = async () => {
  isLoading.value = true
  
  try {
    const params = {
      page: pagination.current_page,
      page_size: pagination.page_size,
      ordering: filters.ordering
    }
    
    if (filters.search) params.search = filters.search
    if (filters.status) params.status = filters.status
    if (filters.priority) params.priority = filters.priority
    
    const result = await complaintsStore.fetchStaffComplaints(params)
    
    if (result.success) {
      complaints.value = result.data.results || []
      pagination.count = result.data.count || 0
    }
  } catch (error) {
    console.error('Error fetching complaints:', error)
  } finally {
    isLoading.value = false
  }
}

const refreshComplaints = () => {
  fetchComplaints()
}

const applyFilters = () => {
  pagination.current_page = 1
  fetchComplaints()
}

const clearFilters = () => {
  Object.assign(filters, {
    search: '',
    status: '',
    priority: '',
    ordering: '-created_at'
  })
  pagination.current_page = 1
  fetchComplaints()
}

const debouncedSearch = debounce(() => {
  applyFilters()
}, 500)

const handlePageChange = (page) => {
  pagination.current_page = page
  fetchComplaints()
}

const viewComplaint = (id) => {
  router.push(`/staff/complaints/${id}`)
}

const addComment = (complaintId) => {
  selectedComplaintId.value = complaintId
  showCommentModal.value = true
}

const forwardComplaint = (complaintId) => {
  selectedComplaintId.value = complaintId
  showForwardModal.value = true
}

const updateStatus = (complaintId) => {
  selectedComplaintId.value = complaintId
  showStatusModal.value = true
}

const handleAddComment = async () => {
  try {
    const result = await complaintsStore.addComplaintComment(selectedComplaintId.value, {
      comment_type: commentForm.comment_type,
      text: commentForm.text
    })
    
    if (result.success) {
      // Reset form
      Object.assign(commentForm, {
        comment_type: 'comment',
        text: ''
      })
      
      // Refresh complaints
      fetchComplaints()
    }
  } catch (error) {
    console.error('Error adding comment:', error)
  }
}

const handleForward = async () => {
  try {
    const result = await complaintsStore.forwardComplaint(selectedComplaintId.value, {
      to_user: forwardForm.to_user,
      remarks: forwardForm.remarks
    })
    
    if (result.success) {
      // Reset form
      Object.assign(forwardForm, {
        to_user: '',
        remarks: ''
      })
      
      // Refresh complaints
      fetchComplaints()
    }
  } catch (error) {
    console.error('Error forwarding complaint:', error)
  }
}

const handleStatusUpdate = async () => {
  try {
    const result = await complaintsStore.updateComplaint(selectedComplaintId.value, {
      status: statusForm.status,
      notes: statusForm.notes
    })
    
    if (result.success) {
      // Reset form
      Object.assign(statusForm, {
        status: '',
        notes: ''
      })
      
      // Refresh complaints
      fetchComplaints()
    }
  } catch (error) {
    console.error('Error updating status:', error)
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

// Fetch staff options
const fetchStaffOptions = async () => {
  try {
    const result = await complaintsStore.fetchStaffList()
    if (result.success) {
      staffOptions.value = result.data.map(s => ({
        value: s.id,
        text: `${s.name} (${s.department})`
      }))
    }
  } catch (error) {
    console.error('Error fetching staff options:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchComplaints()
  fetchStaffOptions()
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
  font-size: 2rem;
  opacity: 0.8;
}

.stats-content {
  text-align: right;
}

.stats-number {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stats-label {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 500;
}

.complaint-row {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  background: white;
}

.complaint-row:hover {
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
  flex-wrap: wrap;
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

.complaint-actions {
  display: flex;
  gap: 0.5rem;
}

.pagination-info {
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
  
  .complaint-actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
