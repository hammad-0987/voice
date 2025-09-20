<template>
  <div class="user-management">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">
            <i class="fas fa-users-cog me-3"></i>
            User Management
          </h1>
          <p class="page-subtitle">
            Manage system users, roles, and permissions
          </p>
        </div>
        <div class="header-actions">
          <b-button variant="success" @click="showCreateUserModal" class="me-2">
            <i class="fas fa-plus me-2"></i>
            Add New User
          </b-button>
          <b-button variant="outline-primary" @click="exportUsers">
            <i class="fas fa-download me-2"></i>
            Export
          </b-button>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="row g-3">
        <div class="col-md-4">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              type="text" 
              class="form-control" 
              placeholder="Search users by name, email, or ID..."
              v-model="searchQuery"
              @input="handleSearch"
            >
          </div>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="selectedRole" @change="applyFilters">
            <option value="">All Roles</option>
            <option value="student">Student</option>
            <option value="staff">Staff</option>
            <option value="head">Department Head</option>
            <option value="vc">Vice Chancellor</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="selectedDepartment" @change="applyFilters">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">
              {{ dept.name }}
            </option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="selectedStatus" @change="applyFilters">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
        <div class="col-md-2">
          <b-button variant="outline-secondary" @click="clearFilters" class="w-100">
            <i class="fas fa-times me-2"></i>
            Clear
          </b-button>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="table-section">
      <div class="table-card">
        <div class="table-header">
          <h5 class="table-title">
            <i class="fas fa-list me-2"></i>
            Users ({{ filteredUsers.length }})
          </h5>
          <div class="table-actions">
            <b-dropdown size="sm" variant="outline-secondary" text="Bulk Actions" :disabled="selectedUsers.length === 0">
              <b-dropdown-item @click="bulkActivate">
                <i class="fas fa-check-circle me-2"></i>
                Activate Selected
              </b-dropdown-item>
              <b-dropdown-item @click="bulkDeactivate">
                <i class="fas fa-ban me-2"></i>
                Deactivate Selected
              </b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item @click="bulkDelete" variant="danger">
                <i class="fas fa-trash me-2"></i>
                Delete Selected
              </b-dropdown-item>
            </b-dropdown>
          </div>
        </div>
        
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>
                  <input 
                    type="checkbox" 
                    class="form-check-input"
                    :checked="allSelected"
                    @change="toggleSelectAll"
                  >
                </th>
                <th @click="sortBy('username')" class="sortable">
                  Username
                  <i :class="getSortIcon('username')"></i>
                </th>
                <th @click="sortBy('full_name')" class="sortable">
                  Full Name
                  <i :class="getSortIcon('full_name')"></i>
                </th>
                <th>Email</th>
                <th>Role</th>
                <th>Department</th>
                <th>Status</th>
                <th @click="sortBy('date_joined')" class="sortable">
                  Joined
                  <i :class="getSortIcon('date_joined')"></i>
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="9" class="text-center py-4">
                  <b-spinner variant="primary"></b-spinner>
                  <p class="mt-2 text-muted">Loading users...</p>
                </td>
              </tr>
              <tr v-else-if="filteredUsers.length === 0">
                <td colspan="9" class="text-center py-4">
                  <i class="fas fa-users fa-3x text-muted mb-3"></i>
                  <p class="text-muted">No users found</p>
                </td>
              </tr>
              <tr v-else v-for="user in paginatedUsers" :key="user.id" :class="{ 'table-row-inactive': !user.is_active }">
                <td>
                  <input 
                    type="checkbox" 
                    class="form-check-input"
                    :value="user.id"
                    v-model="selectedUsers"
                  >
                </td>
                <td>
                  <div class="user-info">
                    <div class="user-avatar">
                      <img v-if="user.profile_picture" :src="user.profile_picture" :alt="user.username">
                      <div v-else class="avatar-placeholder">
                        {{ getInitials(user.first_name, user.last_name) }}
                      </div>
                    </div>
                    <div class="user-details">
                      <span class="username">{{ user.username }}</span>
                      <small class="user-id">{{ user.student_id || user.employee_id || 'N/A' }}</small>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="full-name">{{ user.first_name }} {{ user.last_name }}</span>
                </td>
                <td>
                  <span class="email">{{ user.email }}</span>
                </td>
                <td>
                  <span :class="['role-badge', `role-${user.role}`]">
                    {{ formatRole(user.role) }}
                  </span>
                </td>
                <td>
                  <span class="department">{{ user.department?.name || 'N/A' }}</span>
                </td>
                <td>
                  <span :class="['status-badge', user.is_active ? 'status-active' : 'status-inactive']">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <span class="join-date">{{ formatDate(user.date_joined) }}</span>
                </td>
                <td>
                  <div class="action-buttons">
                    <b-button size="sm" variant="outline-primary" @click="viewUser(user)" class="me-1">
                      <i class="fas fa-eye"></i>
                    </b-button>
                    <b-button size="sm" variant="outline-success" @click="editUser(user)" class="me-1">
                      <i class="fas fa-edit"></i>
                    </b-button>
                    <b-button 
                      size="sm" 
                      :variant="user.is_active ? 'outline-warning' : 'outline-info'" 
                      @click="toggleUserStatus(user)"
                      class="me-1"
                    >
                      <i :class="user.is_active ? 'fas fa-ban' : 'fas fa-check'"></i>
                    </b-button>
                    <b-button size="sm" variant="outline-danger" @click="deleteUser(user)">
                      <i class="fas fa-trash"></i>
                    </b-button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="table-footer" v-if="filteredUsers.length > 0">
          <div class="pagination-info">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} of {{ filteredUsers.length }} users
          </div>
          <b-pagination
            v-model="currentPage"
            :total-rows="filteredUsers.length"
            :per-page="itemsPerPage"
            size="sm"
            class="mb-0"
          ></b-pagination>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <b-modal
      v-model="showUserModal"
      :title="editingUser ? 'Edit User' : 'Create New User'"
      size="lg"
      @hidden="resetUserForm"
    >
      <form @submit.prevent="saveUser">
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Username *</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="userForm.username" 
              required
              :disabled="editingUser"
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">Email *</label>
            <input 
              type="email" 
              class="form-control" 
              v-model="userForm.email" 
              required
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">First Name *</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="userForm.first_name" 
              required
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">Last Name *</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="userForm.last_name" 
              required
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">Role *</label>
            <select class="form-select" v-model="userForm.role" required>
              <option value="">Select Role</option>
              <option value="student">Student</option>
              <option value="staff">Staff</option>
              <option value="head">Department Head</option>
              <option value="vc">Vice Chancellor</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label">Department</label>
            <select class="form-select" v-model="userForm.department">
              <option value="">Select Department</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>
          <div class="col-md-6" v-if="userForm.role === 'student'">
            <label class="form-label">Student ID</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="userForm.student_id"
            >
          </div>
          <div class="col-md-6" v-if="userForm.role !== 'student'">
            <label class="form-label">Employee ID</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="userForm.employee_id"
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">Phone</label>
            <input 
              type="tel" 
              class="form-control" 
              v-model="userForm.phone"
            >
          </div>
          <div class="col-md-6" v-if="!editingUser">
            <label class="form-label">Password *</label>
            <input 
              type="password" 
              class="form-control" 
              v-model="userForm.password" 
              required
            >
          </div>
          <div class="col-12">
            <div class="form-check">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="isActive"
                v-model="userForm.is_active"
              >
              <label class="form-check-label" for="isActive">
                Active User
              </label>
            </div>
          </div>
        </div>
      </form>

      <template #modal-footer>
        <b-button variant="secondary" @click="showUserModal = false">
          Cancel
        </b-button>
        <b-button variant="primary" @click="saveUser" :disabled="saving">
          <b-spinner small v-if="saving"></b-spinner>
          {{ saving ? 'Saving...' : (editingUser ? 'Update User' : 'Create User') }}
        </b-button>
      </template>
    </b-modal>

    <!-- User Details Modal -->
    <b-modal
      v-model="showDetailsModal"
      title="User Details"
      size="lg"
      ok-only
      ok-title="Close"
    >
      <div v-if="selectedUser" class="user-details-modal">
        <div class="row g-4">
          <div class="col-md-4 text-center">
            <div class="user-avatar-large">
              <img v-if="selectedUser.profile_picture" :src="selectedUser.profile_picture" :alt="selectedUser.username">
              <div v-else class="avatar-placeholder-large">
                {{ getInitials(selectedUser.first_name, selectedUser.last_name) }}
              </div>
            </div>
            <h5 class="mt-3">{{ selectedUser.first_name }} {{ selectedUser.last_name }}</h5>
            <span :class="['role-badge', `role-${selectedUser.role}`]">
              {{ formatRole(selectedUser.role) }}
            </span>
          </div>
          <div class="col-md-8">
            <div class="detail-group">
              <label>Username:</label>
              <span>{{ selectedUser.username }}</span>
            </div>
            <div class="detail-group">
              <label>Email:</label>
              <span>{{ selectedUser.email }}</span>
            </div>
            <div class="detail-group">
              <label>Phone:</label>
              <span>{{ selectedUser.phone || 'N/A' }}</span>
            </div>
            <div class="detail-group">
              <label>Department:</label>
              <span>{{ selectedUser.department?.name || 'N/A' }}</span>
            </div>
            <div class="detail-group" v-if="selectedUser.student_id">
              <label>Student ID:</label>
              <span>{{ selectedUser.student_id }}</span>
            </div>
            <div class="detail-group" v-if="selectedUser.employee_id">
              <label>Employee ID:</label>
              <span>{{ selectedUser.employee_id }}</span>
            </div>
            <div class="detail-group">
              <label>Status:</label>
              <span :class="['status-badge', selectedUser.is_active ? 'status-active' : 'status-inactive']">
                {{ selectedUser.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
            <div class="detail-group">
              <label>Joined:</label>
              <span>{{ formatDate(selectedUser.date_joined) }}</span>
            </div>
            <div class="detail-group">
              <label>Last Updated:</label>
              <span>{{ formatDate(selectedUser.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'UserManagement',
  data() {
    return {
      loading: true,
      saving: false,
      users: [],
      departments: [],
      searchQuery: '',
      selectedRole: '',
      selectedDepartment: '',
      selectedStatus: '',
      selectedUsers: [],
      currentPage: 1,
      itemsPerPage: 10,
      sortField: 'date_joined',
      sortDirection: 'desc',
      
      // Modals
      showUserModal: false,
      showDetailsModal: false,
      editingUser: null,
      selectedUser: null,
      
      // Form
      userForm: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: '',
        department: '',
        student_id: '',
        employee_id: '',
        phone: '',
        password: '',
        is_active: true
      }
    }
  },
  computed: {
    filteredUsers() {
      let filtered = this.users

      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(user => 
          user.username.toLowerCase().includes(query) ||
          user.first_name.toLowerCase().includes(query) ||
          user.last_name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query) ||
          (user.student_id && user.student_id.toLowerCase().includes(query)) ||
          (user.employee_id && user.employee_id.toLowerCase().includes(query))
        )
      }

      // Role filter
      if (this.selectedRole) {
        filtered = filtered.filter(user => user.role === this.selectedRole)
      }

      // Department filter
      if (this.selectedDepartment) {
        filtered = filtered.filter(user => user.department?.id === this.selectedDepartment)
      }

      // Status filter
      if (this.selectedStatus) {
        const isActive = this.selectedStatus === 'active'
        filtered = filtered.filter(user => user.is_active === isActive)
      }

      // Sort
      filtered.sort((a, b) => {
        let aVal = a[this.sortField]
        let bVal = b[this.sortField]
        
        if (this.sortField === 'full_name') {
          aVal = `${a.first_name} ${a.last_name}`
          bVal = `${b.first_name} ${b.last_name}`
        }
        
        if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase()
          bVal = bVal.toLowerCase()
        }
        
        if (this.sortDirection === 'asc') {
          return aVal > bVal ? 1 : -1
        } else {
          return aVal < bVal ? 1 : -1
        }
      })

      return filtered
    },

    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredUsers.slice(start, end)
    },

    allSelected() {
      return this.selectedUsers.length === this.paginatedUsers.length && this.paginatedUsers.length > 0
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        await Promise.all([
          this.loadUsers(),
          this.loadDepartments()
        ])
      } catch (error) {
        console.error('Error loading data:', error)
        this.$toast.error('Failed to load data')
      } finally {
        this.loading = false
      }
    },

    async loadUsers() {
      // Mock data - replace with actual API call
      this.users = [
        {
          id: 1,
          username: 'johndoe',
          email: 'john.doe@university.edu',
          first_name: 'John',
          last_name: 'Doe',
          role: 'student',
          department: { id: 1, name: 'Computer Science' },
          student_id: 'CS2024001',
          phone: '+1234567890',
          is_active: true,
          date_joined: '2024-01-15T10:30:00Z',
          updated_at: '2024-09-15T14:20:00Z'
        },
        {
          id: 2,
          username: 'janesmith',
          email: 'jane.smith@university.edu',
          first_name: 'Jane',
          last_name: 'Smith',
          role: 'staff',
          department: { id: 1, name: 'Computer Science' },
          employee_id: 'EMP001',
          phone: '+1234567891',
          is_active: true,
          date_joined: '2023-08-20T09:15:00Z',
          updated_at: '2024-09-10T11:45:00Z'
        },
        {
          id: 3,
          username: 'drbrown',
          email: 'dr.brown@university.edu',
          first_name: 'Robert',
          last_name: 'Brown',
          role: 'head',
          department: { id: 2, name: 'Engineering' },
          employee_id: 'HEAD002',
          phone: '+1234567892',
          is_active: true,
          date_joined: '2022-03-10T08:00:00Z',
          updated_at: '2024-09-12T16:30:00Z'
        }
      ]
    },

    async loadDepartments() {
      // Mock data - replace with actual API call
      this.departments = [
        { id: 1, name: 'Computer Science' },
        { id: 2, name: 'Engineering' },
        { id: 3, name: 'Business Administration' },
        { id: 4, name: 'Arts & Sciences' }
      ]
    },

    handleSearch() {
      this.currentPage = 1
    },

    applyFilters() {
      this.currentPage = 1
    },

    clearFilters() {
      this.searchQuery = ''
      this.selectedRole = ''
      this.selectedDepartment = ''
      this.selectedStatus = ''
      this.currentPage = 1
    },

    sortBy(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
    },

    getSortIcon(field) {
      if (this.sortField !== field) {
        return 'fas fa-sort text-muted'
      }
      return this.sortDirection === 'asc' ? 'fas fa-sort-up text-primary' : 'fas fa-sort-down text-primary'
    },

    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedUsers = []
      } else {
        this.selectedUsers = this.paginatedUsers.map(user => user.id)
      }
    },

    showCreateUserModal() {
      this.editingUser = null
      this.resetUserForm()
      this.showUserModal = true
    },

    editUser(user) {
      this.editingUser = user
      this.userForm = {
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        role: user.role,
        department: user.department?.id || '',
        student_id: user.student_id || '',
        employee_id: user.employee_id || '',
        phone: user.phone || '',
        password: '',
        is_active: user.is_active
      }
      this.showUserModal = true
    },

    viewUser(user) {
      this.selectedUser = user
      this.showDetailsModal = true
    },

    async saveUser() {
      try {
        this.saving = true
        
        // Mock API call - replace with actual implementation
        if (this.editingUser) {
          // Update user
          const index = this.users.findIndex(u => u.id === this.editingUser.id)
          if (index !== -1) {
            this.users[index] = { ...this.users[index], ...this.userForm }
          }
          this.$toast.success('User updated successfully')
        } else {
          // Create user
          const newUser = {
            id: Date.now(),
            ...this.userForm,
            date_joined: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            department: this.departments.find(d => d.id === this.userForm.department) || null
          }
          this.users.unshift(newUser)
          this.$toast.success('User created successfully')
        }
        
        this.showUserModal = false
        this.resetUserForm()
        
      } catch (error) {
        console.error('Error saving user:', error)
        this.$toast.error('Failed to save user')
      } finally {
        this.saving = false
      }
    },

    async toggleUserStatus(user) {
      try {
        // Mock API call - replace with actual implementation
        user.is_active = !user.is_active
        this.$toast.success(`User ${user.is_active ? 'activated' : 'deactivated'} successfully`)
      } catch (error) {
        console.error('Error toggling user status:', error)
        this.$toast.error('Failed to update user status')
      }
    },

    async deleteUser(user) {
      if (!confirm(`Are you sure you want to delete user "${user.username}"?`)) {
        return
      }

      try {
        // Mock API call - replace with actual implementation
        const index = this.users.findIndex(u => u.id === user.id)
        if (index !== -1) {
          this.users.splice(index, 1)
        }
        this.$toast.success('User deleted successfully')
      } catch (error) {
        console.error('Error deleting user:', error)
        this.$toast.error('Failed to delete user')
      }
    },

    async bulkActivate() {
      try {
        // Mock API call - replace with actual implementation
        this.users.forEach(user => {
          if (this.selectedUsers.includes(user.id)) {
            user.is_active = true
          }
        })
        this.selectedUsers = []
        this.$toast.success('Selected users activated successfully')
      } catch (error) {
        console.error('Error activating users:', error)
        this.$toast.error('Failed to activate users')
      }
    },

    async bulkDeactivate() {
      try {
        // Mock API call - replace with actual implementation
        this.users.forEach(user => {
          if (this.selectedUsers.includes(user.id)) {
            user.is_active = false
          }
        })
        this.selectedUsers = []
        this.$toast.success('Selected users deactivated successfully')
      } catch (error) {
        console.error('Error deactivating users:', error)
        this.$toast.error('Failed to deactivate users')
      }
    },

    async bulkDelete() {
      if (!confirm(`Are you sure you want to delete ${this.selectedUsers.length} selected users?`)) {
        return
      }

      try {
        // Mock API call - replace with actual implementation
        this.users = this.users.filter(user => !this.selectedUsers.includes(user.id))
        this.selectedUsers = []
        this.$toast.success('Selected users deleted successfully')
      } catch (error) {
        console.error('Error deleting users:', error)
        this.$toast.error('Failed to delete users')
      }
    },

    exportUsers() {
      // Mock export functionality
      this.$toast.info('Exporting users...')
    },

    resetUserForm() {
      this.userForm = {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: '',
        department: '',
        student_id: '',
        employee_id: '',
        phone: '',
        password: '',
        is_active: true
      }
    },

    getInitials(firstName, lastName) {
      return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
    },

    formatRole(role) {
      const roleMap = {
        'student': 'Student',
        'staff': 'Staff',
        'head': 'Department Head',
        'vc': 'Vice Chancellor',
        'admin': 'Admin'
      }
      return roleMap[role] || role
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 0;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* Header Section */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0.5rem 0 0 0;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.header-actions .btn {
  backdrop-filter: blur(10px);
}

.header-actions .btn-success {
  background: rgba(16, 185, 129, 0.9);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.header-actions .btn-success:hover {
  background: rgba(16, 185, 129, 1);
  border-color: rgba(16, 185, 129, 0.4);
}

.header-actions .btn-outline-primary {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .btn-outline-primary:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  color: white;
}

/* Filters Section */
.filters-section {
  max-width: 1400px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  z-index: 2;
}

.search-box .form-control {
  padding-left: 2.5rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.search-box .form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-select {
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Table Section */
.table-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.table-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.table-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  display: flex;
  align-items: center;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  margin: 0;
}

.table th {
  background-color: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
  color: #374151;
  padding: 1rem 0.75rem;
  white-space: nowrap;
}

.table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.table th.sortable:hover {
  background-color: #f1f5f9;
}

.table td {
  padding: 1rem 0.75rem;
  vertical-align: middle;
  border-bottom: 1px solid #f1f5f9;
}

.table-row-inactive {
  opacity: 0.6;
  background-color: #fafafa;
}

/* User Info */
.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 600;
  color: #1a202c;
  font-size: 0.9rem;
}

.user-id {
  color: #6b7280;
  font-size: 0.75rem;
}

.full-name {
  font-weight: 500;
  color: #374151;
}

.email {
  color: #6b7280;
  font-size: 0.9rem;
}

/* Badges */
.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-student { background: #dbeafe; color: #1e40af; }
.role-staff { background: #d1fae5; color: #065f46; }
.role-head { background: #fef3c7; color: #92400e; }
.role-vc { background: #e0e7ff; color: #3730a3; }
.role-admin { background: #fee2e2; color: #991b1b; }

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active { background: #d1fae5; color: #065f46; }
.status-inactive { background: #fee2e2; color: #991b1b; }

.department {
  color: #6b7280;
  font-size: 0.9rem;
}

.join-date {
  color: #6b7280;
  font-size: 0.85rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.action-buttons .btn {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

/* Table Footer */
.table-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8fafc;
}

.pagination-info {
  font-size: 0.85rem;
  color: #6b7280;
}

/* User Details Modal */
.user-details-modal {
  padding: 1rem 0;
}

.user-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto;
  border: 4px solid #e2e8f0;
}

.user-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder-large {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 2rem;
}

.detail-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-group:last-child {
  border-bottom: none;
}

.detail-group label {
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.detail-group span {
  color: #6b7280;
}

/* Form Styling */
.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.75rem;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}

.form-check-input:focus {
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .table-responsive {
    font-size: 0.85rem;
  }
  
  .user-info {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .table-footer {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .filters-section .row > div {
    margin-bottom: 0.5rem;
  }
  
  .table th, .table td {
    padding: 0.5rem 0.25rem;
    font-size: 0.8rem;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
  }
  
  .avatar-placeholder {
    font-size: 0.75rem;
  }
}

/* Loading and Empty States */
.table tbody tr td {
  text-align: center;
}

.table tbody tr:not(.text-center) td {
  text-align: left;
}

/* Hover Effects */
.table tbody tr:hover {
  background-color: #f8fafc;
}

.btn:hover {
  transform: translateY(-1px);
  transition: all 0.2s ease;
}

/* Animation for modals */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter, .modal-leave-to {
  opacity: 0;
}
</style>
