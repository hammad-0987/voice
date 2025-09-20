<template>
  <div class="complaint-detail">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-spinner">
      <BSpinner class="spinner-border-custom" />
      <p class="mt-3 text-muted">Loading complaint details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">
        <i class="bi bi-exclamation-triangle"></i>
      </div>
      <h4>Error Loading Complaint</h4>
      <p>{{ error }}</p>
      <BButton variant="primary" @click="fetchComplaint">
        <i class="bi bi-arrow-clockwise me-2"></i>
        Try Again
      </BButton>
    </div>

    <!-- Complaint Content -->
    <div v-else-if="complaint" class="complaint-content">
      <!-- Header -->
      <div class="complaint-header">
        <div class="header-info">
          <h1 class="complaint-title">{{ complaint.title }}</h1>
          <div class="complaint-meta">
            <span class="complaint-number">{{ complaint.complaint_number }}</span>
            <span class="separator">•</span>
            <span class="complaint-date">Filed {{ formatDate(complaint.created_at) }}</span>
            <span class="separator">•</span>
            <span class="complaint-department">{{ complaint.department_name }}</span>
          </div>
        </div>
        <div class="header-badges">
          <BBadge :variant="getStatusVariant(complaint.status)" class="status-badge">
            {{ formatStatus(complaint.status) }}
          </BBadge>
          <BBadge :variant="getPriorityVariant(complaint.priority)" class="priority-badge">
            {{ formatPriority(complaint.priority) }}
          </BBadge>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row">
        <!-- Left Column - Details -->
        <div class="col-lg-8">
          <!-- Description -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-chat-square-text me-2"></i>
                Description
              </h5>
            </div>
            <div class="card-body">
              <p class="complaint-description">{{ complaint.description }}</p>
            </div>
          </div>

          <!-- Attachments -->
          <div v-if="complaint.attachments?.length > 0" class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-paperclip me-2"></i>
                Attachments ({{ complaint.attachments.length }})
              </h5>
            </div>
            <div class="card-body">
              <div class="attachments-list">
                <div 
                  v-for="attachment in complaint.attachments" 
                  :key="attachment.id"
                  class="attachment-item"
                >
                  <div class="attachment-info">
                    <i class="bi bi-file-earmark attachment-icon"></i>
                    <div class="attachment-details">
                      <div class="attachment-name">{{ attachment.filename }}</div>
                      <div class="attachment-size">{{ formatFileSize(attachment.size) }}</div>
                    </div>
                  </div>
                  <BButton
                    variant="outline-primary"
                    size="sm"
                    @click="downloadAttachment(attachment)"
                  >
                    <i class="bi bi-download"></i>
                  </BButton>
                </div>
              </div>
            </div>
          </div>

          <!-- Comments Timeline -->
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-chat-dots me-2"></i>
                Activity Timeline
              </h5>
            </div>
            <div class="card-body">
              <div class="timeline">
                <!-- Initial Complaint -->
                <div class="timeline-item">
                  <div class="timeline-content">
                    <div class="timeline-header">
                      <strong>{{ complaint.created_by_name }}</strong>
                      <span class="timeline-action">filed this complaint</span>
                      <span class="timeline-date">{{ formatRelativeTime(complaint.created_at) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Comments -->
                <div 
                  v-for="comment in comments" 
                  :key="comment.id"
                  class="timeline-item"
                  :class="`comment-type-${comment.comment_type}`"
                >
                  <div class="timeline-content">
                    <div class="timeline-header">
                      <strong>{{ comment.user_name }}</strong>
                      <span class="timeline-action">{{ getCommentAction(comment.comment_type) }}</span>
                      <span class="timeline-date">{{ formatRelativeTime(comment.created_at) }}</span>
                    </div>
                    <div class="timeline-body">
                      <p>{{ comment.text }}</p>
                      
                      <!-- Student Reply -->
                      <div v-if="comment.reply" class="student-reply">
                        <div class="reply-header">
                          <strong>{{ complaint.created_by_name }}</strong> replied:
                        </div>
                        <p>{{ comment.reply }}</p>
                      </div>
                      
                      <!-- Reply Form -->
                      <div 
                        v-if="canReplyToComment(comment) && !comment.reply"
                        class="reply-form"
                      >
                        <label class="form-label">
                          <i class="bi bi-reply me-2"></i>
                          Your Reply
                        </label>
                        <BFormTextarea
                          v-model="replyText[comment.id]"
                          placeholder="Type your reply to this request..."
                          rows="3"
                          class="form-control mb-2"
                        />
                        <div class="reply-actions">
                          <BButton
                            variant="primary"
                            size="sm"
                            @click="submitReply(comment.id)"
                            :disabled="!replyText[comment.id]?.trim()"
                          >
                            <i class="bi bi-reply me-1"></i>
                            Reply
                          </BButton>
                          <BButton
                            variant="outline-secondary"
                            size="sm"
                            @click="cancelReply(comment.id)"
                            class="ms-2"
                          >
                            Cancel
                          </BButton>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Feedback Section -->
          <div 
            v-if="canSubmitFeedback" 
            class="card mt-4 feedback-card"
          >
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="bi bi-star me-2"></i>
                Submit Feedback
              </h5>
            </div>
            <div class="card-body">
              <p class="text-muted mb-3">
                How satisfied are you with the resolution of your complaint?
              </p>
              
              <form @submit.prevent="submitFeedback">
                <!-- Rating -->
                <div class="mb-3">
                  <label class="form-label">
                    <i class="bi bi-star me-2"></i>
                    Rating *
                  </label>
                  <div class="rating-stars">
                    <i 
                      v-for="star in 5" 
                      :key="star"
                      class="bi star-icon"
                      :class="star <= feedbackForm.rating ? 'bi-star-fill' : 'bi-star'"
                      @click="feedbackForm.rating = star"
                    ></i>
                  </div>
                  <div class="form-text">Click to rate your satisfaction (1-5 stars)</div>
                </div>

                <!-- Feedback Text -->
                <div class="mb-3">
                  <label class="form-label">
                    <i class="bi bi-chat-square-text me-2"></i>
                    Comments (Optional)
                  </label>
                  <BFormTextarea
                    v-model="feedbackForm.feedback_text"
                    placeholder="Share your experience and suggestions for improvement..."
                    rows="4"
                    class="form-control"
                  />
                </div>

                <BButton
                  type="submit"
                  variant="primary"
                  :disabled="feedbackForm.rating === 0 || isSubmittingFeedback"
                >
                  <BSpinner v-if="isSubmittingFeedback" small class="me-2" />
                  <i v-else class="bi bi-send me-2"></i>
                  Submit Feedback
                </BButton>
              </form>
            </div>
          </div>
        </div>

        <!-- Right Column - Info -->
        <div class="col-lg-4">
          <!-- Status Card -->
          <div class="card mb-4 info-card">
            <div class="card-header">
              <h6 class="card-title mb-0">Complaint Information</h6>
            </div>
            <div class="card-body">
              <div class="info-item">
                <label>Status</label>
                <BBadge :variant="getStatusVariant(complaint.status)">
                  {{ formatStatus(complaint.status) }}
                </BBadge>
              </div>
              <div class="info-item">
                <label>Priority</label>
                <BBadge :variant="getPriorityVariant(complaint.priority)">
                  {{ formatPriority(complaint.priority) }}
                </BBadge>
              </div>
              <div class="info-item">
                <label>Department</label>
                <span>{{ complaint.department_name }}</span>
              </div>
              <div class="info-item">
                <label>Assigned To</label>
                <span>{{ complaint.assigned_to_name || 'Not assigned' }}</span>
              </div>
              <div class="info-item">
                <label>Created</label>
                <span>{{ formatDate(complaint.created_at) }}</span>
              </div>
              <div class="info-item">
                <label>Last Updated</label>
                <span>{{ formatRelativeTime(complaint.updated_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Actions Card -->
          <div class="card actions-card">
            <div class="card-header">
              <h6 class="card-title mb-0">Actions</h6>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <BButton
                  variant="outline-primary"
                  @click="refreshComplaint"
                  :disabled="isLoading"
                >
                  <i class="bi bi-arrow-clockwise me-2"></i>
                  Refresh
                </BButton>
                <BButton
                  variant="outline-secondary"
                  @click="printComplaint"
                >
                  <i class="bi bi-printer me-2"></i>
                  Print
                </BButton>
                <router-link 
                  to="/student/complaints" 
                  class="btn btn-outline-secondary"
                >
                  <i class="bi bi-arrow-left me-2"></i>
                  Back to List
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useComplaintsStore } from '@/stores/complaints'
import { formatDistanceToNow, format } from 'date-fns'

const route = useRoute()
const complaintsStore = useComplaintsStore()

// Component state
const complaint = ref(null)
const comments = ref([])
const isLoading = ref(false)
const error = ref('')
const replyText = reactive({})
const isSubmittingFeedback = ref(false)

// Feedback form
const feedbackForm = reactive({
  rating: 0,
  feedback_text: ''
})

// Computed
const canSubmitFeedback = computed(() => {
  return complaint.value && 
         ['resolved', 'rejected', 'closed'].includes(complaint.value.status) &&
         !complaint.value.feedback_submitted
})

// Methods
const fetchComplaint = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const result = await complaintsStore.fetchComplaint(route.params.id)
    if (result.success) {
      complaint.value = result.data
      comments.value = result.data.comments || []
    } else {
      error.value = result.error || 'Failed to load complaint'
    }
  } catch (err) {
    error.value = 'An unexpected error occurred'
    console.error('Error fetching complaint:', err)
  } finally {
    isLoading.value = false
  }
}

const canReplyToComment = (comment) => {
  return ['require_info', 'ask_question'].includes(comment.comment_type)
}

const submitReply = async (commentId) => {
  const reply = replyText[commentId]?.trim()
  if (!reply) return
  
  try {
    const result = await complaintsStore.replyToComment(commentId, reply)
    if (result.success) {
      // Update the comment with the reply
      const comment = comments.value.find(c => c.id === commentId)
      if (comment) {
        comment.reply = reply
        comment.replied_at = new Date().toISOString()
      }
      delete replyText[commentId]
    }
  } catch (error) {
    console.error('Error submitting reply:', error)
  }
}

const cancelReply = (commentId) => {
  delete replyText[commentId]
}

const submitFeedback = async () => {
  if (feedbackForm.rating === 0) return
  
  isSubmittingFeedback.value = true
  
  try {
    const result = await complaintsStore.submitFeedback(complaint.value.id, feedbackForm)
    if (result.success) {
      complaint.value.feedback_submitted = true
      // Reset form
      Object.assign(feedbackForm, { rating: 0, feedback_text: '' })
    }
  } catch (error) {
    console.error('Error submitting feedback:', error)
  } finally {
    isSubmittingFeedback.value = false
  }
}

const refreshComplaint = () => {
  fetchComplaint()
}

const printComplaint = () => {
  window.print()
}

const downloadAttachment = async (attachment) => {
  try {
    const result = await complaintsStore.downloadAttachment(attachment.id)
    if (result.success) {
      // Create download link
      const url = window.URL.createObjectURL(new Blob([result.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = attachment.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }
  } catch (error) {
    console.error('Error downloading attachment:', error)
  }
}

// Formatting methods
const formatDate = (date) => format(new Date(date), 'MMM dd, yyyy')
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

const getCommentAction = (type) => {
  const actionMap = {
    comment: 'added a comment',
    require_info: 'requested additional information',
    ask_question: 'asked a question'
  }
  return actionMap[type] || 'commented'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Lifecycle
onMounted(() => {
  fetchComplaint()
})
</script>

<style scoped>
.complaint-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
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

.form-text {
  font-size: 0.875rem !important;
  color: #6c757d !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0 !important;
}

.complaint-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.complaint-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.separator {
  color: #dee2e6;
}

.header-badges {
  display: flex;
  gap: 0.5rem;
}

.complaint-description {
  line-height: 1.6;
  color: #495057;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.attachment-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.attachment-info {
  display: flex;
  align-items: center;
}

.attachment-icon {
  font-size: 1.5rem;
  color: #667eea;
  margin-right: 0.75rem;
}

.attachment-name {
  font-weight: 500;
  color: #2c3e50;
}

.attachment-size {
  font-size: 0.8rem;
  color: #6c757d;
}

.timeline-item {
  position: relative;
  padding-left: 2rem;
  margin-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0.5rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #667eea;
  border: 3px solid white;
  box-shadow: 0 0 0 2px #667eea;
}

.timeline-content {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-left: 1rem;
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.timeline-action {
  color: #6c757d;
}

.timeline-date {
  color: #999;
  margin-left: auto;
}

.student-reply {
  background: #f0f4ff;
  border-left: 4px solid #667eea;
  padding: 0.75rem;
  margin-top: 1rem;
  border-radius: 0 6px 6px 0;
}

.reply-header {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #667eea;
}

.reply-form {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.info-card .info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f3f4;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item label {
  font-weight: 500;
  color: #6c757d;
  margin-bottom: 0;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.star-icon {
  font-size: 1.5rem;
  color: #ffc107;
  cursor: pointer;
  transition: all 0.2s ease;
}

.star-icon:hover {
  transform: scale(1.1);
}

.feedback-card {
  border-left: 4px solid #28a745;
}

@media (max-width: 768px) {
  .complaint-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .timeline-item {
    padding-left: 1rem;
  }
  
  .timeline-content {
    margin-left: 0.5rem;
  }
}
</style>
