<template>
  <div class="student-dashboard">
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <p class="page-subtitle">Welcome back, {{ authStore.userName }}!</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card primary">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stats-number">5</div>
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
            <div class="stats-number">2</div>
            <div class="stats-label">Pending</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card success">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stats-number">3</div>
            <div class="stats-label">Resolved</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card info">
          <div class="card-body">
            <div class="stats-icon">
              <i class="bi bi-star"></i>
            </div>
            <div class="stats-number">4.5</div>
            <div class="stats-label">Avg Rating</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3">
                <router-link to="/student/file-complaint" class="action-card">
                  <i class="bi bi-plus-circle"></i>
                  <span>File New Complaint</span>
                </router-link>
              </div>
              <div class="col-md-4 mb-3">
                <router-link to="/student/complaints" class="action-card">
                  <i class="bi bi-list-ul"></i>
                  <span>View My Complaints</span>
                </router-link>
              </div>
              <div class="col-md-4 mb-3">
                <router-link to="/student/withdrawals" class="action-card">
                  <i class="bi bi-file-earmark-text"></i>
                  <span>Withdrawal Requests</span>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Complaints -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Recent Complaints</h5>
          </div>
          <div class="card-body">
            <div class="empty-state">
              <div class="empty-state-icon">
                <i class="bi bi-inbox"></i>
              </div>
              <div class="empty-state-title">No complaints yet</div>
              <div class="empty-state-description">
                Start by filing your first complaint to track issues and get them resolved.
              </div>
              <router-link to="/student/file-complaint" class="btn btn-primary">
                File Your First Complaint
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
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

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-decoration: none;
  color: #495057;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.action-card:hover {
  background: #e9ecef;
  color: #495057;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-card i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #667eea;
}

.action-card span {
  font-weight: 500;
  text-align: center;
}
</style>

