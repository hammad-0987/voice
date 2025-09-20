# 🚀 Installation Guide - Student Voice CMS

This guide will help you set up the Student Voice CMS system on your local machine or server.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (recommended: Python 3.11)
- **Node.js 16+** (recommended: Node.js 18 LTS)
- **MySQL 8.0+**
- **Git**
- **npm** or **yarn**

## 🔧 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Windows 10, macOS 10.15, Ubuntu 18.04+

### Recommended Requirements
- **RAM**: 8GB+
- **Storage**: 5GB+ free space
- **OS**: Latest versions of Windows, macOS, or Linux

## 🗄️ Database Setup

### MySQL Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS (using Homebrew)
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Windows
Download and install MySQL from [official website](https://dev.mysql.com/downloads/mysql/)

### Database Configuration

1. **Login to MySQL**
   ```bash
   mysql -u root -p
   ```

2. **Create Database and User**
   ```sql
   CREATE DATABASE student_voice_cms;
   CREATE USER 'cms_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON student_voice_cms.* TO 'cms_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

## 🐍 Backend Setup (Django)

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd student-voice-cms
```

### 2. Navigate to Backend Directory
```bash
cd student_cms_api
```

### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the `student_cms_api` directory:

```env
# Database Configuration
DB_NAME=student_voice_cms
DB_USER=cms_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Django Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# File Upload Configuration
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=pdf,doc,docx,jpg,jpeg,png
```

### 6. Update Django Settings
Update `student_cms/settings.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

### 7. Database Migration
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 8. Load Sample Data (Optional)
```bash
# Load sample departments
python manage.py loaddata fixtures/departments.json

# Load sample users
python manage.py loaddata fixtures/sample_users.json
```

### 9. Start Development Server
```bash
python manage.py runserver
```

The backend will be available at: `http://localhost:8000`

## 🎨 Frontend Setup (Vue.js)

### 1. Navigate to Frontend Directory
```bash
cd ../student-cms-ui
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration
Create a `.env` file in the `student-cms-ui` directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000

# App Configuration
VITE_APP_NAME=Student Voice CMS
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=Complete Complaint Management System

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_DARK_MODE=true

# File Upload Configuration
VITE_MAX_FILE_SIZE=10485760
VITE_ALLOWED_FILE_TYPES=pdf,doc,docx,jpg,jpeg,png
```

### 4. Update API Configuration
Update `src/services/api.js`:

```javascript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
```

### 5. Start Development Server
```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

The frontend will be available at: `http://localhost:5173`

## 🔐 Security Setup

### 1. Generate Secret Keys
```bash
# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Configure CORS
Update `student_cms_api/student_cms/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
```

### 3. Set Up HTTPS (Production)
For production deployment, ensure you:
- Use HTTPS certificates
- Set `SECURE_SSL_REDIRECT = True`
- Configure proper CORS origins
- Use environment variables for secrets

## 📊 Verification

### Backend Verification
1. Visit `http://localhost:8000/admin` - Django admin should load
2. Visit `http://localhost:8000/api/` - API root should display
3. Check `http://localhost:8000/api/auth/` - Auth endpoints should be available

### Frontend Verification
1. Visit `http://localhost:5173` - Landing page should load
2. Try registering a new student account
3. Login with the created account
4. Navigate through different sections

### Database Verification
```bash
mysql -u cms_user -p student_voice_cms
```

```sql
SHOW TABLES;
SELECT COUNT(*) FROM users_user;
SELECT COUNT(*) FROM users_department;
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution**: Check MySQL service is running and credentials are correct.

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'module_name'
```
**Solution**: Ensure virtual environment is activated and dependencies are installed.

#### 3. CORS Error in Frontend
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**: Check CORS configuration in Django settings.

#### 4. Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::5173
```
**Solution**: Kill the process using the port or use a different port.

### Debug Commands

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check MySQL status
sudo systemctl status mysql

# Check Django configuration
python manage.py check

# Check for migration issues
python manage.py showmigrations

# Test database connection
python manage.py dbshell
```

## 🚀 Next Steps

After successful installation:

1. **Explore the Admin Panel**: Create departments and users
2. **Test User Registration**: Register as a student
3. **Submit Test Complaints**: Test the complaint workflow
4. **Configure Email**: Set up email notifications
5. **Customize Settings**: Adjust system settings as needed

## 📞 Support

If you encounter issues during installation:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check the GitHub issues for similar problems
4. Create a new issue with detailed error information

**Happy coding! 🎉**

