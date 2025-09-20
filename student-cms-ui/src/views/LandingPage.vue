<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-background">
        <!-- Animated background elements -->
        <div class="floating-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
          <div class="shape shape-4"></div>
        </div>
      </div>

      <div class="hero-content">
        <div class="max-w-4xl mx-auto text-center">
          <!-- Logo and Brand -->
          <div class="brand-section" v-motion-fade-visible>
            <div class="w-20 h-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl">
              <AcademicCapIcon class="w-12 h-12 text-white" />
            </div>
            <h1 class="text-5xl md:text-7xl font-bold gradient-text mb-6">
              Student Voice
            </h1>
            <p class="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto">
              Modern complaint management system designed for educational institutions
            </p>
          </div>

          <!-- CTA Buttons -->
          <div class="cta-section" v-motion-slide-visible-bottom>
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <router-link
                to="/login"
                class="btn-primary px-8 py-4 text-lg font-semibold rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300"
              >
                <ArrowRightOnRectangleIcon class="w-6 h-6 mr-2" />
                Sign In
              </router-link>
              <router-link
                to="/register"
                class="btn-secondary px-8 py-4 text-lg font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              >
                <UserPlusIcon class="w-6 h-6 mr-2" />
                Register as Student
              </router-link>
            </div>
            
            <div class="mt-8">
              <router-link
                to="/track"
                class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium transition-colors duration-200"
              >
                <MagnifyingGlassIcon class="w-5 h-5 mr-2" />
                Track Your Complaint
                <ArrowRightIcon class="w-4 h-4 ml-1" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16" v-motion-fade-visible>
          <h2 class="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-4">
            Powerful Features for Everyone
          </h2>
          <p class="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Streamlined complaint management with role-based access and real-time tracking
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Feature cards -->
          <div
            v-for="(feature, index) in features"
            :key="feature.title"
            class="feature-card"
            v-motion-slide-visible-bottom
            :style="{ '--delay': `${index * 100}ms` }"
          >
            <div class="feature-icon">
              <component :is="feature.icon" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-3">
              {{ feature.title }}
            </h3>
            <p class="text-slate-600 dark:text-slate-300">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div
            v-for="(stat, index) in stats"
            :key="stat.label"
            class="stat-card"
            v-motion-fade-visible
            :style="{ '--delay': `${index * 150}ms` }"
          >
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16" v-motion-fade-visible>
          <h2 class="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-4">
            How It Works
          </h2>
          <p class="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Simple steps to submit and track your complaints
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div
            v-for="(step, index) in steps"
            :key="step.title"
            class="step-card"
            v-motion-slide-visible-bottom
            :style="{ '--delay': `${index * 200}ms` }"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-icon">
              <component :is="step.icon" class="w-12 h-12" />
            </div>
            <h3 class="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-3">
              {{ step.title }}
            </h3>
            <p class="text-slate-600 dark:text-slate-300">
              {{ step.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <div class="flex items-center justify-center space-x-3 mb-4">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <AcademicCapIcon class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-bold gradient-text">Student Voice</span>
          </div>
          <p class="text-slate-600 dark:text-slate-300 mb-4">
            Empowering students with a modern complaint management system
          </p>
          <p class="text-sm text-slate-500 dark:text-slate-400">
            © 2024 Student Voice CMS. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import {
  AcademicCapIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  MagnifyingGlassIcon,
  ArrowRightIcon,
  DocumentTextIcon,
  BellIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  ClockIcon,
  UserGroupIcon,
  PencilSquareIcon,
  EyeIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

// Features data
const features = [
  {
    title: 'Easy Complaint Filing',
    description: 'Submit complaints with a simple, intuitive interface. Attach files and track progress in real-time.',
    icon: DocumentTextIcon
  },
  {
    title: 'Real-time Notifications',
    description: 'Get instant updates on your complaint status via email and in-app notifications.',
    icon: BellIcon
  },
  {
    title: 'Advanced Analytics',
    description: 'Comprehensive dashboards and reports for administrators to track performance.',
    icon: ChartBarIcon
  },
  {
    title: 'Secure & Private',
    description: 'Your data is protected with enterprise-grade security and privacy controls.',
    icon: ShieldCheckIcon
  },
  {
    title: '24/7 Availability',
    description: 'Access the system anytime, anywhere. Submit and track complaints around the clock.',
    icon: ClockIcon
  },
  {
    title: 'Role-based Access',
    description: 'Different interfaces for students, staff, department heads, and administrators.',
    icon: UserGroupIcon
  }
]

// Stats data
const stats = [
  { value: '10K+', label: 'Students' },
  { value: '500+', label: 'Staff Members' },
  { value: '95%', label: 'Resolution Rate' },
  { value: '24h', label: 'Avg Response Time' }
]

// Steps data
const steps = [
  {
    title: 'Submit Complaint',
    description: 'Fill out the complaint form with all necessary details and attachments.',
    icon: PencilSquareIcon
  },
  {
    title: 'Track Progress',
    description: 'Monitor your complaint status and receive updates throughout the process.',
    icon: EyeIcon
  },
  {
    title: 'Get Resolution',
    description: 'Receive notification when your complaint is resolved and provide feedback.',
    icon: CheckCircleIcon
  }
]
</script>

<style scoped>
.landing-page {
  @apply min-h-screen;
}

.hero-section {
  @apply relative min-h-screen flex items-center justify-center;
  @apply bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100;
  @apply dark:from-slate-900 dark:via-slate-800 dark:to-slate-900;
  @apply overflow-hidden;
}

.hero-background {
  @apply absolute inset-0;
}

.floating-shapes {
  @apply absolute inset-0;
}

.shape {
  @apply absolute rounded-full opacity-20;
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  @apply w-64 h-64 bg-blue-400 top-10 left-10;
  animation-delay: 0s;
}

.shape-2 {
  @apply w-48 h-48 bg-indigo-400 top-1/2 right-10;
  animation-delay: 2s;
}

.shape-3 {
  @apply w-32 h-32 bg-purple-400 bottom-20 left-1/4;
  animation-delay: 4s;
}

.shape-4 {
  @apply w-40 h-40 bg-pink-400 bottom-10 right-1/3;
  animation-delay: 1s;
}

.hero-content {
  @apply relative z-10 px-4 sm:px-6 lg:px-8;
}

.brand-section {
  animation-delay: 0.2s;
}

.cta-section {
  animation-delay: 0.4s;
}

.features-section {
  @apply py-24 bg-white dark:bg-slate-800;
}

.feature-card {
  @apply glass-card text-center hover:scale-105 transition-all duration-300;
  animation-delay: var(--delay);
}

.feature-icon {
  @apply w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl;
  @apply flex items-center justify-center mx-auto mb-6 text-white;
}

.stats-section {
  @apply py-16 bg-gradient-to-r from-blue-600 to-indigo-600;
}

.stat-card {
  @apply text-center text-white;
  animation-delay: var(--delay);
}

.stat-number {
  @apply text-4xl md:text-5xl font-bold mb-2;
}

.stat-label {
  @apply text-blue-100 text-lg;
}

.how-it-works-section {
  @apply py-24 bg-slate-50 dark:bg-slate-900;
}

.step-card {
  @apply text-center relative;
  animation-delay: var(--delay);
}

.step-number {
  @apply absolute -top-4 left-1/2 transform -translate-x-1/2;
  @apply w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full;
  @apply flex items-center justify-center text-white font-bold text-sm;
}

.step-icon {
  @apply w-20 h-20 bg-white dark:bg-slate-800 rounded-2xl shadow-lg;
  @apply flex items-center justify-center mx-auto mb-6 mt-8;
  @apply text-blue-600 dark:text-blue-400;
}

.footer-section {
  @apply py-12 bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Motion directives styling */
[v-motion-fade-visible] {
  opacity: 0;
  transition: opacity 0.6s ease;
}

[v-motion-slide-visible-bottom] {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.motion-visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}
</style>

