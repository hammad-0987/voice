<template>
  <div class="not-found-page">
    <div class="container">
      <div class="row justify-content-center min-vh-100 align-items-center">
        <div class="col-lg-6 text-center">
          <div class="error-content">
            <div class="error-code">404</div>
            <h1 class="error-title">Page Not Found</h1>
            <p class="error-description">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div class="error-actions">
              <router-link to="/" class="btn btn-primary me-3">
                <i class="bi bi-house me-2"></i>
                Go Home
              </router-link>
              <button @click="$router.go(-1)" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>
                Go Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  opacity: 0.3;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.error-description {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}
</style>

