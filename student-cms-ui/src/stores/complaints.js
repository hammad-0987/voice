import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useComplaintsStore = defineStore('complaints', () => {
  // State
  const complaints = ref([])
  const currentComplaint = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    totalPages: 1,
    totalCount: 0,
    pageSize: 20
  })

  // Getters
  const pendingComplaints = computed(() => 
    complaints.value.filter(c => c.status === 'pending')
  )
  
  const inProgressComplaints = computed(() => 
    complaints.value.filter(c => c.status === 'in_progress')
  )
  
  const resolvedComplaints = computed(() => 
    complaints.value.filter(c => c.status === 'resolved')
  )
  
  const complaintsByStatus = computed(() => {
    const statusCounts = {}
    complaints.value.forEach(complaint => {
      statusCounts[complaint.status] = (statusCounts[complaint.status] || 0) + 1
    })
    return statusCounts
  })

  // Actions
  const fetchComplaints = async (params = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get('/complaints/', { params })
      
      complaints.value = response.data.results || response.data
      
      if (response.data.count !== undefined) {
        pagination.value = {
          page: params.page || 1,
          totalPages: Math.ceil(response.data.count / (params.page_size || 20)),
          totalCount: response.data.count,
          pageSize: params.page_size || 20
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch complaints'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchComplaintById = async (id) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get(`/complaints/${id}/`)
      currentComplaint.value = response.data
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch complaint'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createComplaint = async (complaintData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const formData = new FormData()
      Object.keys(complaintData).forEach(key => {
        if (complaintData[key] !== null && complaintData[key] !== undefined) {
          formData.append(key, complaintData[key])
        }
      })
      
      const response = await api.post('/complaints/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Add to local state
      complaints.value.unshift(response.data)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create complaint'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateComplaint = async (id, updateData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.put(`/complaints/${id}/`, updateData)
      
      // Update local state
      const index = complaints.value.findIndex(c => c.id === id)
      if (index !== -1) {
        complaints.value[index] = response.data
      }
      
      if (currentComplaint.value?.id === id) {
        currentComplaint.value = response.data
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update complaint'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const forwardComplaint = async (id, forwardData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post(`/complaints/${id}/forward/`, forwardData)
      
      // Refresh complaint data
      await fetchComplaintById(id)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to forward complaint'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchComplaintComments = async (id) => {
    try {
      const response = await api.get(`/complaints/${id}/comments/`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch comments:', err)
      throw err
    }
  }

  const addComplaintComment = async (id, commentData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post(`/complaints/${id}/comments/`, commentData)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to add comment'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const replyToComment = async (complaintId, commentId, replyData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post(`/complaints/${complaintId}/comments/${commentId}/reply/`, replyData)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to reply to comment'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const trackComplaint = async (complaintNumber) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get(`/complaints/track/${complaintNumber}/`)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Complaint not found'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const searchComplaints = async (searchParams) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get('/complaints/search/', { params: searchParams })
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Search failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchMyComplaints = async (params = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get('/complaints/my/', { params })
      
      complaints.value = response.data.results || response.data
      
      if (response.data.count !== undefined) {
        pagination.value = {
          page: params.page || 1,
          totalPages: Math.ceil(response.data.count / (params.page_size || 20)),
          totalCount: response.data.count,
          pageSize: params.page_size || 20
        }
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch complaints'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchComplaint = async (id) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.get(`/complaints/${id}/`)
      currentComplaint.value = response.data
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch complaint'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchComplaintStatistics = async () => {
    try {
      const response = await api.get('/complaints/statistics/')
      
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to fetch statistics' }
    }
  }

  const submitFeedback = async (complaintId, feedbackData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post(`/complaints/${complaintId}/feedback/`, feedbackData)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to submit feedback'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const downloadAttachment = async (attachmentId) => {
    try {
      const response = await api.get(`/complaints/attachments/${attachmentId}/download/`, {
        responseType: 'blob'
      })
      
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to download attachment' }
    }
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  // Clear current complaint
  const clearCurrentComplaint = () => {
    currentComplaint.value = null
  }

  // Staff-specific methods
  const fetchStaffComplaints = async (params = {}) => {
    try {
      isLoading.value = true
      const response = await api.get('/staff/complaints/', { params })
      
      if (response.data) {
        return { 
          success: true, 
          data: response.data 
        }
      }
      
      return { success: false, error: 'No data received' }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch staff complaints'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchStaffStatistics = async () => {
    try {
      const response = await api.get('/staff/statistics/')
      
      if (response.data) {
        return { 
          success: true, 
          data: response.data 
        }
      }
      
      return { success: false, error: 'No data received' }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch staff statistics'
      return { success: false, error: error.value }
    }
  }

  const fetchWeeklyStats = async () => {
    try {
      const response = await api.get('/staff/weekly-stats/')
      
      if (response.data) {
        return { 
          success: true, 
          data: response.data 
        }
      }
      
      return { success: false, error: 'No data received' }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch weekly stats'
      return { success: false, error: error.value }
    }
  }

  const fetchStaffList = async () => {
    try {
      const response = await api.get('/staff/list/')
      
      if (response.data) {
        return { 
          success: true, 
          data: response.data 
        }
      }
      
      return { success: false, error: 'No data received' }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch staff list'
      return { success: false, error: error.value }
    }
  }

  return {
    // State
    complaints,
    currentComplaint,
    isLoading,
    error,
    pagination,
    
    // Getters
    pendingComplaints,
    inProgressComplaints,
    resolvedComplaints,
    complaintsByStatus,
    
    // Actions
    fetchComplaints,
    fetchComplaintById,
    fetchComplaint,
    fetchMyComplaints,
    fetchComplaintStatistics,
    createComplaint,
    updateComplaint,
    forwardComplaint,
    fetchComplaintComments,
    addComplaintComment,
    replyToComment,
    submitFeedback,
    downloadAttachment,
    trackComplaint,
    searchComplaints,
    clearError,
    clearCurrentComplaint,
    
    // Staff methods
    fetchStaffComplaints,
    fetchStaffStatistics,
    fetchWeeklyStats,
    fetchStaffList
  }
})
