<template>
  <div class="login-page">
    <!-- Background -->
    <div class="login-background">
      <div class="background-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- Content -->
    <div class="login-content">
      <div class="login-container">
        <!-- Header -->
        <div class="login-header" v-motion-fade-visible>
          <router-link to="/" class="back-link">
            <ArrowLeftIcon class="w-5 h-5" />
            Back to Home
          </router-link>
          
          <div class="brand-section">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
              <AcademicCapIcon class="w-10 h-10 text-white" />
            </div>
            <h1 class="text-3xl font-bold gradient-text mb-2">Welcome Back</h1>
            <p class="text-slate-600 dark:text-slate-300">Sign in to your Student Voice account</p>
          </div>
        </div>

        <!-- Login Form -->
        <div class="login-form" v-motion-slide-visible-bottom>
          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- Email Field -->
            <div class="form-group">
              <label for="email" class="form-label">
                <EnvelopeIcon class="w-5 h-5" />
                Email Address
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="input"
                :class="{ 'error': errors.email }"
                placeholder="Enter your email address"
                @blur="validateEmail"
              />
              <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
            </div>

            <!-- Password Field -->
            <div class="form-group">
              <label for="password" class="form-label">
                <LockClosedIcon class="w-5 h-5" />
                Password
              </label>
              <div class="password-input">
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="input pr-12"
                  :class="{ 'error': errors.password }"
                  placeholder="Enter your password"
                  @blur="validatePassword"
                />
                <button
                  type="button"
                  @click="togglePassword"
                  class="password-toggle"
                >
                  <EyeIcon v-if="!showPassword" class="w-5 h-5" />
                  <EyeSlashIcon v-else class="w-5 h-5" />
                </button>
              </div>
              <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="form-options">
              <label class="checkbox-label">
                <input
                  v-model="form.rememberMe"
                  type="checkbox"
                  class="checkbox"
                />
                <span class="checkbox-text">Remember me</span>
              </label>
              
              <router-link to="/forgot-password" class="forgot-link">
                Forgot password?
              </router-link>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="isLoading"
              class="submit-btn"
            >
              <span v-if="!isLoading" class="flex items-center justify-center">
                <ArrowRightOnRectangleIcon class="w-5 h-5 mr-2" />
                Sign In
              </span>
              <span v-else class="flex items-center justify-center">
                <div class="spinner w-5 h-5 mr-2"></div>
                Signing In...
              </span>
            </button>

            <!-- Error Message -->
            <div v-if="errors.general" class="error-alert">
              <ExclamationTriangleIcon class="w-5 h-5" />
              <span>{{ errors.general }}</span>
            </div>
          </form>
        </div>

        <!-- Footer -->
        <div class="login-footer" v-motion-fade-visible>
          <div class="divider">
            <span>New to Student Voice?</span>
          </div>
          
          <router-link to="/register" class="register-link">
            <UserPlusIcon class="w-5 h-5 mr-2" />
            Create Student Account
          </router-link>
          
          <div class="help-links">
            <router-link to="/track" class="help-link">
              <MagnifyingGlassIcon class="w-4 h-4 mr-1" />
              Track Complaint
            </router-link>
            <router-link to="/help" class="help-link">
              <QuestionMarkCircleIcon class="w-4 h-4 mr-1" />
              Need Help?
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import {
  ArrowLeftIcon,
  AcademicCapIcon,
  EnvelopeIcon,
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowRightOnRectangleIcon,
  ExclamationTriangleIcon,
  UserPlusIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const isLoading = ref(false)
const showPassword = ref(false)

const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

const errors = reactive({
  email: '',
  password: '',
  general: ''
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const validateEmail = () => {
  errors.email = ''
  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
  }
}

const validatePassword = () => {
  errors.password = ''
  if (!form.password) {
    errors.password = 'Password is required'
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
  }
}

const validateForm = () => {
  validateEmail()
  validatePassword()
  return !errors.email && !errors.password
}

const handleLogin = async () => {
  errors.general = ''
  
  if (!validateForm()) {
    return
  }

  isLoading.value = true

  try {
    await authStore.login({
      email: form.email,
      password: form.password,
      remember: form.rememberMe
    })

    toast.success('Welcome back! Login successful.')
    
    // Redirect to dashboard or intended route
    const redirectTo = router.currentRoute.value.query.redirect || '/dashboard'
    router.push(redirectTo)
    
  } catch (error) {
    console.error('Login error:', error)
    
    if (error.response?.status === 401) {
      errors.general = 'Invalid email or password. Please try again.'
    } else if (error.response?.status === 429) {
      errors.general = 'Too many login attempts. Please try again later.'
    } else {
      errors.general = 'Login failed. Please check your connection and try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  @apply min-h-screen flex items-center justify-center relative;
  @apply bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100;
  @apply dark:from-slate-900 dark:via-slate-800 dark:to-slate-900;
}

.login-background {
  @apply absolute inset-0 overflow-hidden;
}

.background-shapes {
  @apply absolute inset-0;
}

.shape {
  @apply absolute rounded-full opacity-10;
  animation: float 8s ease-in-out infinite;
}

.shape-1 {
  @apply w-96 h-96 bg-blue-400 -top-20 -left-20;
  animation-delay: 0s;
}

.shape-2 {
  @apply w-64 h-64 bg-indigo-400 top-1/2 -right-10;
  animation-delay: 3s;
}

.shape-3 {
  @apply w-48 h-48 bg-purple-400 -bottom-10 left-1/3;
  animation-delay: 6s;
}

.login-content {
  @apply relative z-10 w-full max-w-md mx-auto px-4;
}

.login-container {
  @apply glass-card p-8 space-y-8;
}

.login-header {
  @apply text-center space-y-4;
}

.back-link {
  @apply inline-flex items-center space-x-2 text-slate-600 dark:text-slate-400;
  @apply hover:text-slate-900 dark:hover:text-slate-100 transition-colors duration-200;
  @apply mb-6;
}

.brand-section {
  @apply space-y-2;
}

.login-form {
  @apply space-y-6;
}

.form-group {
  @apply space-y-2;
}

.form-label {
  @apply flex items-center space-x-2 text-sm font-medium;
  @apply text-slate-700 dark:text-slate-300;
}

.password-input {
  @apply relative;
}

.password-toggle {
  @apply absolute right-3 top-1/2 transform -translate-y-1/2;
  @apply text-slate-400 hover:text-slate-600 dark:hover:text-slate-300;
  @apply transition-colors duration-200;
}

.form-options {
  @apply flex items-center justify-between;
}

.checkbox-label {
  @apply flex items-center space-x-2 cursor-pointer;
}

.checkbox {
  @apply w-4 h-4 text-blue-600 bg-white dark:bg-slate-700;
  @apply border-slate-300 dark:border-slate-600 rounded;
  @apply focus:ring-blue-500 focus:ring-2;
}

.checkbox-text {
  @apply text-sm text-slate-600 dark:text-slate-400;
}

.forgot-link {
  @apply text-sm text-blue-600 dark:text-blue-400;
  @apply hover:text-blue-700 dark:hover:text-blue-300;
  @apply transition-colors duration-200;
}

.submit-btn {
  @apply w-full btn-primary py-3 text-base font-semibold;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
}

.error-message {
  @apply text-sm text-red-600 dark:text-red-400;
}

.error-alert {
  @apply flex items-center space-x-2 p-3 rounded-lg;
  @apply bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400;
  @apply border border-red-200 dark:border-red-800;
}

.input.error {
  @apply border-red-300 dark:border-red-600;
  @apply focus:ring-red-500 focus:border-red-500;
}

.login-footer {
  @apply space-y-4 text-center;
}

.divider {
  @apply relative;
}

.divider span {
  @apply bg-white dark:bg-slate-800 px-4 text-sm text-slate-500 dark:text-slate-400;
}

.divider::before {
  @apply absolute inset-0 flex items-center;
  content: '';
  @apply border-t border-slate-200 dark:border-slate-700;
}

.register-link {
  @apply inline-flex items-center justify-center w-full py-3 px-4;
  @apply bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300;
  @apply hover:bg-slate-200 dark:hover:bg-slate-600;
  @apply rounded-xl font-medium transition-all duration-200;
  @apply border border-slate-200 dark:border-slate-600;
}

.help-links {
  @apply flex items-center justify-center space-x-6;
}

.help-link {
  @apply inline-flex items-center text-sm text-slate-500 dark:text-slate-400;
  @apply hover:text-slate-700 dark:hover:text-slate-300;
  @apply transition-colors duration-200;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}
</style>

