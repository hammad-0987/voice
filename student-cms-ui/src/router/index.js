import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Public Views
import LandingPage from '@/views/public/LandingPage.vue'
import LoginPage from '@/views/public/LoginPage.vue'
import RegisterPage from '@/views/public/RegisterPage.vue'
import TrackComplaint from '@/views/public/TrackComplaint.vue'

// Student Views
import StudentDashboard from '@/views/student/StudentDashboard.vue'
import FileComplaint from '@/views/student/FileComplaint.vue'
import MyComplaints from '@/views/student/MyComplaints.vue'
import ComplaintDetail from '@/views/student/ComplaintDetail.vue'
import WithdrawalRequests from '@/views/student/WithdrawalRequests.vue'
import StudentProfile from '@/views/student/StudentProfile.vue'
import StudentNotifications from '@/views/student/StudentNotifications.vue'

// Staff Views
import StaffDashboard from '@/views/staff/StaffDashboard.vue'
import AssignedComplaints from '@/views/staff/AssignedComplaints.vue'
import StaffComplaintDetail from '@/views/staff/StaffComplaintDetail.vue'
import ReviewWithdrawals from '@/views/staff/ReviewWithdrawals.vue'
import StaffNotifications from '@/views/staff/StaffNotifications.vue'

// Head Views
import HeadDashboard from '@/views/head/HeadDashboard.vue'
import DepartmentComplaints from '@/views/head/DepartmentComplaints.vue'
import DepartmentAnalytics from '@/views/head/DepartmentAnalytics.vue'
import ManageStaff from '@/views/head/ManageStaff.vue'
import HeadNotifications from '@/views/head/HeadNotifications.vue'

// VC Views
import VCDashboard from '@/views/vc/VCDashboard.vue'
import AllComplaints from '@/views/vc/AllComplaints.vue'
import GlobalAnalytics from '@/views/vc/GlobalAnalytics.vue'
import SystemReports from '@/views/vc/SystemReports.vue'
import VCNotifications from '@/views/vc/VCNotifications.vue'

// Admin Views
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import DepartmentManagement from '@/views/admin/DepartmentManagement.vue'
import SystemSettings from '@/views/admin/SystemSettings.vue'
import ActivityLogs from '@/views/admin/ActivityLogs.vue'
import AdminNotifications from '@/views/admin/AdminNotifications.vue'

// Shared Views
import FeedbackViewer from '@/views/shared/FeedbackViewer.vue'
import NotFound from '@/views/shared/NotFound.vue'

const routes = [
  // Public Routes
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
    meta: { public: true }
  },
  {
    path: '/track',
    name: 'track-complaint',
    component: TrackComplaint,
    meta: { public: true }
  },

  // Student Routes
  {
    path: '/student',
    meta: { requiresAuth: true, roles: ['student'] },
    children: [
      {
        path: 'dashboard',
        name: 'student-dashboard',
        component: StudentDashboard
      },
      {
        path: 'file-complaint',
        name: 'file-complaint',
        component: FileComplaint
      },
      {
        path: 'complaints',
        name: 'my-complaints',
        component: MyComplaints
      },
      {
        path: 'complaints/:id',
        name: 'student-complaint-detail',
        component: ComplaintDetail,
        props: true
      },
      {
        path: 'withdrawals',
        name: 'withdrawal-requests',
        component: WithdrawalRequests
      },
      {
        path: 'profile',
        name: 'student-profile',
        component: StudentProfile
      },
      {
        path: 'notifications',
        name: 'student-notifications',
        component: StudentNotifications
      }
    ]
  },

  // Staff Routes
  {
    path: '/staff',
    meta: { requiresAuth: true, roles: ['staff'] },
    children: [
      {
        path: 'dashboard',
        name: 'staff-dashboard',
        component: StaffDashboard
      },
      {
        path: 'complaints',
        name: 'staff-complaints',
        component: () => import('@/views/staff/StaffComplaints.vue')
      },
      {
        path: 'complaints/:id',
        name: 'staff-complaint-detail',
        component: StaffComplaintDetail,
        props: true
      },
      {
        path: 'withdrawals',
        name: 'review-withdrawals',
        component: ReviewWithdrawals
      },
      {
        path: 'notifications',
        name: 'staff-notifications',
        component: StaffNotifications
      }
    ]
  },

  // Head Routes
  {
    path: '/head',
    meta: { requiresAuth: true, roles: ['head'] },
    children: [
      {
        path: 'dashboard',
        name: 'head-dashboard',
        component: HeadDashboard
      },
      {
        path: 'complaints',
        name: 'department-complaints',
        component: DepartmentComplaints
      },
      {
        path: 'analytics',
        name: 'department-analytics',
        component: DepartmentAnalytics
      },
      {
        path: 'staff',
        name: 'manage-staff',
        component: ManageStaff
      },
      {
        path: 'feedback',
        name: 'head-feedback',
        component: FeedbackViewer
      },
      {
        path: 'notifications',
        name: 'head-notifications',
        component: HeadNotifications
      }
    ]
  },

  // VC Routes
  {
    path: '/vc',
    meta: { requiresAuth: true, roles: ['vc'] },
    children: [
      {
        path: 'dashboard',
        name: 'vc-dashboard',
        component: VCDashboard
      },
      {
        path: 'complaints',
        name: 'all-complaints',
        component: AllComplaints
      },
      {
        path: 'analytics',
        name: 'global-analytics',
        component: GlobalAnalytics
      },
      {
        path: 'reports',
        name: 'system-reports',
        component: SystemReports
      },
      {
        path: 'feedback',
        name: 'vc-feedback',
        component: FeedbackViewer
      },
      {
        path: 'notifications',
        name: 'vc-notifications',
        component: VCNotifications
      }
    ]
  },

  // Admin Routes
  {
    path: '/admin',
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: AdminDashboard
      },
      {
        path: 'users',
        name: 'user-management',
        component: UserManagement
      },
      {
        path: 'departments',
        name: 'department-management',
        component: DepartmentManagement
      },
      {
        path: 'settings',
        name: 'system-settings',
        component: SystemSettings
      },
      {
        path: 'logs',
        name: 'activity-logs',
        component: ActivityLogs
      },
      {
        path: 'feedback',
        name: 'admin-feedback',
        component: FeedbackViewer
      },
      {
        path: 'notifications',
        name: 'admin-notifications',
        component: AdminNotifications
      }
    ]
  },

  // Catch all 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      // Redirect to login if not authenticated
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // Check role-based access
    if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
      // Redirect to appropriate dashboard if role doesn't match
      next(`/${authStore.userRole}/dashboard`)
      return
    }
  }
  
  // Redirect authenticated users away from public auth pages
  if (to.meta.public && ['login', 'register'].includes(to.name) && authStore.isAuthenticated) {
    next(`/${authStore.userRole}/dashboard`)
    return
  }
  
  next()
})

export default router
