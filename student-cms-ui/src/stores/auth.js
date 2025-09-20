import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const refreshToken = ref(localStorage.getItem('refreshToken'))
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role)
  const userName = computed(() => user.value ? `${user.value.first_name} ${user.value.last_name}` : '')
  const userInitials = computed(() => {
    if (!user.value) return ''
    return `${user.value.first_name?.[0] || ''}${user.value.last_name?.[0] || ''}`.toUpperCase()
  })

  // Actions
  const login = async (credentials) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post('/users/login/', credentials)
      const { access, refresh, user: userData } = response.data
      
      // Store tokens
      token.value = access
      refreshToken.value = refresh
      user.value = userData
      
      // Persist to localStorage
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)
      localStorage.setItem('user', JSON.stringify(userData))
      
      // Set default authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.post('/users/register/', userData)
      
      // Auto-login after successful registration
      if (response.data.success) {
        const loginResult = await login({
          username: userData.username,
          password: userData.password
        })
        return loginResult
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      // Call logout endpoint if token exists
      if (token.value) {
        await api.post('/users/logout/', { refresh: refreshToken.value })
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear state and localStorage
      user.value = null
      token.value = null
      refreshToken.value = null
      error.value = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      
      // Remove authorization header
      delete api.defaults.headers.common['Authorization']
    }
  }

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available')
      }
      
      const response = await api.post('/users/token/refresh/', {
        refresh: refreshToken.value
      })
      
      const { access } = response.data
      token.value = access
      localStorage.setItem('token', access)
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      return access
    } catch (err) {
      // Refresh failed, logout user
      await logout()
      throw err
    }
  }

  const fetchUserProfile = async () => {
    try {
      const response = await api.get('/users/profile/')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return response.data
    } catch (err) {
      console.error('Failed to fetch user profile:', err)
      throw err
    }
  }

  const updateProfile = async (profileData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await api.put('/users/profile/', profileData)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Profile update failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    try {
      isLoading.value = true
      error.value = null
      
      await api.post('/users/change-password/', passwordData)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Password change failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Initialize auth state from localStorage
  const initializeAuth = () => {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    
    if (storedUser && storedToken) {
      try {
        user.value = JSON.parse(storedUser)
        token.value = storedToken
        api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
      } catch (err) {
        console.error('Failed to parse stored user data:', err)
        logout()
      }
    }
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    token,
    refreshToken,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    userRole,
    userName,
    userInitials,
    
    // Actions
    login,
    register,
    logout,
    refreshAccessToken,
    fetchUserProfile,
    updateProfile,
    changePassword,
    initializeAuth,
    clearError
  }
})

