<template>
  <div class="file-complaint">
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">File New Complaint</h1>
      <p class="page-subtitle">Submit your complaint and we'll work to resolve it promptly</p>
    </div>

    <!-- Complaint Form -->
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card complaint-form-card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-plus-circle me-2"></i>
              Complaint Details
            </h5>
          </div>
          
          <div class="card-body">
            <!-- Success Alert -->
            <BAlert 
              v-if="submitSuccess" 
              variant="success" 
              dismissible
              @dismissed="submitSuccess = false"
              class="fade-in"
            >
              <i class="bi bi-check-circle-fill me-2"></i>
              <strong>Complaint submitted successfully!</strong>
              <br>
              Your complaint number is: <strong>{{ newComplaintNumber }}</strong>
              <br>
              <router-link :to="`/student/complaints/${newComplaintId}`" class="alert-link">
                View your complaint →
              </router-link>
            </BAlert>

            <!-- Error Alert -->
            <BAlert 
              v-if="submitError" 
              variant="danger" 
              dismissible
              @dismissed="submitError = ''"
              class="fade-in"
            >
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              {{ submitError }}
            </BAlert>

            <!-- Form -->
            <form @submit.prevent="submitComplaint" class="complaint-form">
              <!-- Title -->
              <div class="mb-3">
                <label for="title" class="form-label">
                  <i class="bi bi-card-text me-2"></i>
                  Complaint Title *
                </label>
                <BFormInput
                  id="title"
                  v-model="form.title"
                  type="text"
                  placeholder="Enter a clear, descriptive title for your complaint"
                  required
                  :disabled="isSubmitting"
                  maxlength="200"
                  class="form-control"
                />
                <div class="form-text">
                  {{ form.title.length }}/200 characters
                </div>
              </div>

              <!-- Department -->
              <div class="mb-3">
                <label for="department" class="form-label">
                  <i class="bi bi-building me-2"></i>
                  Department *
                </label>
                <BFormSelect
                  id="department"
                  v-model="form.department"
                  :options="departmentOptions"
                  required
                  :disabled="isSubmitting"
                  class="form-select"
                >
                  <template #first>
                    <BFormSelectOption value="" disabled>Select the relevant department</BFormSelectOption>
                  </template>
                </BFormSelect>
              </div>

              <!-- Priority -->
              <div class="mb-3">
                <label for="priority" class="form-label">
                  <i class="bi bi-flag me-2"></i>
                  Priority Level *
                </label>
                <BFormSelect
                  id="priority"
                  v-model="form.priority"
                  :options="priorityOptions"
                  required
                  :disabled="isSubmitting"
                  class="form-select"
                />
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label for="description" class="form-label">
                  <i class="bi bi-chat-square-text me-2"></i>
                  Detailed Description *
                </label>
                <BFormTextarea
                  id="description"
                  v-model="form.description"
                  placeholder="Describe your complaint in detail. Include relevant dates, locations, people involved, and any steps you've already taken to resolve the issue."
                  required
                  :disabled="isSubmitting"
                  rows="6"
                  maxlength="2000"
                  class="form-control"
                />
                <div class="form-text">
                  {{ form.description.length }}/2000 characters. Please provide as much detail as possible.
                </div>
              </div>

              <!-- File Attachments -->
              <div class="mb-4">
                <label class="form-label">
                  <i class="bi bi-paperclip me-2"></i>
                  Attachments (Optional)
                </label>
                
                <!-- File Upload Area -->
                <div 
                  class="file-upload-area"
                  :class="{ 'dragover': isDragOver }"
                  @drop="handleFileDrop"
                  @dragover.prevent="isDragOver = true"
                  @dragleave="isDragOver = false"
                  @click="$refs.fileInput.click()"
                >
                  <div class="upload-content">
                    <i class="bi bi-cloud-upload upload-icon"></i>
                    <h6>Drop files here or click to browse</h6>
                    <p class="text-muted mb-0">
                      Supported formats: PDF, DOC, DOCX, JPG, PNG (Max 10MB each)
                    </p>
                  </div>
                  
                  <input
                    ref="fileInput"
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                    @change="handleFileSelect"
                    style="display: none"
                  />
                </div>

                <!-- Selected Files -->
                <div v-if="selectedFiles.length > 0" class="selected-files mt-3">
                  <h6 class="mb-2">Selected Files:</h6>
                  <div class="file-list">
                    <div 
                      v-for="(file, index) in selectedFiles" 
                      :key="index"
                      class="file-item"
                    >
                      <div class="file-info">
                        <i class="bi bi-file-earmark file-icon"></i>
                        <div class="file-details">
                          <div class="file-name">{{ file.name }}</div>
                          <div class="file-size">{{ formatFileSize(file.size) }}</div>
                        </div>
                      </div>
                      <BButton
                        variant="outline-danger"
                        size="sm"
                        @click="removeFile(index)"
                        :disabled="isSubmitting"
                      >
                        <i class="bi bi-x"></i>
                      </BButton>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Anonymous Option -->
              <div class="form-check mb-4">
                <BFormCheckbox
                  id="anonymous"
                  v-model="form.anonymous"
                  :disabled="isSubmitting"
                >
                  <strong>Submit anonymously</strong>
                  <div class="form-text">
                    Your identity will be hidden from staff, but you can still track your complaint.
                  </div>
                </BFormCheckbox>
              </div>

              <!-- Terms Agreement -->
              <div class="form-check mb-4">
                <BFormCheckbox
                  id="terms"
                  v-model="form.agreeToTerms"
                  required
                  :disabled="isSubmitting"
                >
                  I agree to the <a href="#" @click.prevent="showTerms = true">Terms and Conditions</a> 
                  and confirm that the information provided is accurate.
                </BFormCheckbox>
              </div>

              <!-- Submit Buttons -->
              <div class="form-actions">
                <BButton
                  type="submit"
                  variant="primary"
                  size="lg"
                  :disabled="isSubmitting || !form.agreeToTerms"
                  class="submit-btn"
                >
                  <BSpinner v-if="isSubmitting" small class="me-2" />
                  <i v-else class="bi bi-send me-2"></i>
                  {{ isSubmitting ? 'Submitting...' : 'Submit Complaint' }}
                </BButton>
                
                <BButton
                  type="button"
                  variant="outline-secondary"
                  size="lg"
                  @click="resetForm"
                  :disabled="isSubmitting"
                  class="ms-3"
                >
                  <i class="bi bi-arrow-clockwise me-2"></i>
                  Reset Form
                </BButton>
              </div>
            </form>
          </div>
        </div>

        <!-- Help Card -->
        <div class="card mt-4 help-card">
          <div class="card-body">
            <h6 class="card-title">
              <i class="bi bi-info-circle me-2"></i>
              Need Help?
            </h6>
            <p class="card-text mb-2">
              Before submitting a complaint, you might want to:
            </p>
            <ul class="help-list">
              <li>Check if your issue can be resolved through self-service options</li>
              <li>Contact the relevant department directly first</li>
              <li>Review our <a href="#" @click.prevent="showFAQ = true">Frequently Asked Questions</a></li>
            </ul>
            <div class="contact-info">
              <strong>Need immediate assistance?</strong><br>
              <i class="bi bi-telephone me-1"></i> Call: +1 (555) 123-4567<br>
              <i class="bi bi-envelope me-1"></i> Email: support@university.edu
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms Modal -->
    <BModal
      v-model="showTerms"
      title="Terms and Conditions"
      size="lg"
      ok-only
      ok-title="I Understand"
    >
      <div class="terms-content">
        <h6>Complaint Submission Terms</h6>
        <ul>
          <li>All information provided must be accurate and truthful</li>
          <li>False or malicious complaints may result in disciplinary action</li>
          <li>We will investigate your complaint fairly and promptly</li>
          <li>You will be notified of progress and resolution</li>
          <li>Personal information will be handled according to our privacy policy</li>
        </ul>
      </div>
    </BModal>

    <!-- FAQ Modal -->
    <BModal
      v-model="showFAQ"
      title="Frequently Asked Questions"
      size="lg"
      ok-only
      ok-title="Close"
    >
      <div class="faq-content">
        <div class="faq-item">
          <h6>How long does it take to resolve a complaint?</h6>
          <p>Most complaints are resolved within 5-10 business days, depending on complexity.</p>
        </div>
        <div class="faq-item">
          <h6>Can I track my complaint status?</h6>
          <p>Yes! You'll receive a complaint number that you can use to track progress in real-time.</p>
        </div>
        <div class="faq-item">
          <h6>What if I'm not satisfied with the resolution?</h6>
          <p>You can provide feedback and request escalation to higher authorities if needed.</p>
        </div>
      </div>
    </BModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComplaintsStore } from '@/stores/complaints'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const complaintsStore = useComplaintsStore()
const authStore = useAuthStore()

// Form state
const form = reactive({
  title: '',
  department: '',
  priority: 'medium',
  description: '',
  anonymous: false,
  agreeToTerms: false
})

// Component state
const selectedFiles = ref([])
const isDragOver = ref(false)
const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')
const newComplaintNumber = ref('')
const newComplaintId = ref(null)
const showTerms = ref(false)
const showFAQ = ref(false)

// Options
const departmentOptions = ref([
  { value: 'academic', text: 'Academic Affairs' },
  { value: 'student-services', text: 'Student Services' },
  { value: 'housing', text: 'Housing & Accommodation' },
  { value: 'finance', text: 'Finance & Billing' },
  { value: 'it', text: 'IT Services' },
  { value: 'library', text: 'Library Services' },
  { value: 'cafeteria', text: 'Cafeteria & Dining' },
  { value: 'transport', text: 'Transportation' },
  { value: 'security', text: 'Security & Safety' },
  { value: 'other', text: 'Other' }
])

const priorityOptions = ref([
  { value: 'low', text: 'Low - General inquiry or minor issue' },
  { value: 'medium', text: 'Medium - Standard complaint requiring attention' },
  { value: 'high', text: 'High - Urgent issue affecting studies/services' },
  { value: 'urgent', text: 'Urgent - Critical issue requiring immediate action' }
])

// Methods
const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
}

const handleFileDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  const files = Array.from(event.dataTransfer.files)
  addFiles(files)
}

const addFiles = (files) => {
  const maxSize = 10 * 1024 * 1024 // 10MB
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg', 'image/jpg', 'image/png']
  
  files.forEach(file => {
    if (file.size > maxSize) {
      submitError.value = `File "${file.name}" is too large. Maximum size is 10MB.`
      return
    }
    
    if (!allowedTypes.includes(file.type)) {
      submitError.value = `File "${file.name}" is not a supported format.`
      return
    }
    
    if (selectedFiles.value.length >= 5) {
      submitError.value = 'Maximum 5 files allowed.'
      return
    }
    
    selectedFiles.value.push(file)
  })
}

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const submitComplaint = async () => {
  isSubmitting.value = true
  submitError.value = ''
  
  try {
    // Create FormData for file upload
    const formData = new FormData()
    formData.append('title', form.title)
    formData.append('department', form.department)
    formData.append('priority', form.priority)
    formData.append('description', form.description)
    formData.append('anonymous', form.anonymous)
    
    // Add files
    selectedFiles.value.forEach((file, index) => {
      formData.append(`attachments`, file)
    })
    
    const result = await complaintsStore.createComplaint(formData)
    
    if (result.success) {
      submitSuccess.value = true
      newComplaintNumber.value = result.data.complaint_number
      newComplaintId.value = result.data.id
      
      // Reset form after successful submission
      setTimeout(() => {
        resetForm()
        submitSuccess.value = false
      }, 5000)
    } else {
      submitError.value = result.error || 'Failed to submit complaint. Please try again.'
    }
  } catch (error) {
    submitError.value = 'An unexpected error occurred. Please try again.'
    console.error('Complaint submission error:', error)
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    title: '',
    department: '',
    priority: 'medium',
    description: '',
    anonymous: false,
    agreeToTerms: false
  })
  selectedFiles.value = []
  submitError.value = ''
  submitSuccess.value = false
}

// Lifecycle
onMounted(() => {
  // Load departments from API if needed
  // complaintsStore.fetchDepartments()
})
</script>

<style scoped>
.page-header {
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

.complaint-form-card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
}

.complaint-form-card .card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  padding: 1.5rem;
}

/* Form Styling - Fixed */
.complaint-form .mb-3 {
  margin-bottom: 2rem !important;
}

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

.file-upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  background: #f8f9fa;
}

.file-upload-area:hover,
.file-upload-area.dragover {
  border-color: #667eea;
  background: #f0f4ff;
}

.upload-content {
  pointer-events: none;
}

.upload-icon {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 1rem;
}

.selected-files {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.file-info {
  display: flex;
  align-items: center;
}

.file-icon {
  font-size: 1.5rem;
  color: #667eea;
  margin-right: 0.75rem;
}

.file-details {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  color: #2c3e50;
}

.file-size {
  font-size: 0.8rem;
  color: #6c757d;
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2rem;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.help-card {
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  border-left: 4px solid #17a2b8;
}

.help-list {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.help-list li {
  margin-bottom: 0.5rem;
}

.contact-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.terms-content,
.faq-content {
  line-height: 1.6;
}

.faq-item {
  margin-bottom: 1.5rem;
}

.faq-item h6 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-actions .btn {
    width: 100%;
  }
  
  .file-upload-area {
    padding: 2rem 1rem;
  }
}
</style>
