# Student CMS (Complaint Management System) - Backend API

A comprehensive Django REST API for managing student complaints, withdrawal requests, and feedback in educational institutions.

## 🚀 Features

### Core Functionality
- **User Management**: Role-based access control (Student, Staff, Department Head, VC, Admin)
- **Complaint Management**: Full lifecycle management with auto-generated complaint numbers
- **Withdrawal Requests**: Private withdrawal request system with approval workflow
- **Feedback System**: Post-closure feedback with ratings and management responses
- **Notifications**: Real-time notifications with email support
- **Analytics**: Comprehensive analytics and reporting
- **Activity Logging**: Detailed audit trail of all system activities

### Key Highlights
- **Auto-generated Numbers**: Complaints (CMP-YYYY-XXXX) and Withdrawals (WRQ-YYYY-XXXX)
- **Smart Forwarding**: Role-based complaint forwarding with restrictions
- **Comment System**: Three types of interactions (Comment, Require Info, Ask Question)
- **Feedback Auto-forwarding**: Automatic forwarding to Head, VC, and Admin
- **Role-based Permissions**: Granular access control throughout the system
- **Comprehensive Analytics**: Dashboard stats, trends, and performance metrics

## 🛠 Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: MySQL (configurable)
- **Authentication**: JWT tokens with refresh mechanism
- **Documentation**: Swagger/OpenAPI
- **Task Queue**: Celery (Redis)
- **Email**: Django email backend (configurable)

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+ (or SQLite for development)
- Redis (for Celery tasks)
- Node.js (for frontend integration)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd student_cms_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=student_cms
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# For SQLite (Development)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery (Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 4. Run the Server

```bash
# Development server
python manage.py runserver

# API will be available at http://localhost:8000/
# Admin panel at http://localhost:8000/admin/
# API docs at http://localhost:8000/swagger/
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - Student registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `POST /api/users/token/refresh/` - Refresh JWT token

### Complaint Endpoints
- `GET /api/complaints/` - List complaints
- `POST /api/complaints/` - Create complaint
- `GET /api/complaints/{id}/` - Get complaint details
- `PUT /api/complaints/{id}/` - Update complaint
- `POST /api/complaints/{id}/forward/` - Forward complaint
- `GET /api/complaints/{id}/comments/` - Get comments
- `POST /api/complaints/{id}/comments/` - Add comment
- `POST /api/complaints/{id}/comments/{comment_id}/reply/` - Reply to comment

### Withdrawal Endpoints
- `GET /api/withdrawals/` - List withdrawal requests
- `POST /api/withdrawals/` - Create withdrawal request
- `GET /api/withdrawals/{id}/` - Get withdrawal details
- `POST /api/withdrawals/{id}/review/` - Review withdrawal request

### Feedback Endpoints
- `GET /api/feedback/` - List feedback
- `POST /api/feedback/` - Submit feedback
- `GET /api/feedback/{id}/` - Get feedback details
- `POST /api/feedback/{id}/responses/` - Add management response

### Analytics Endpoints
- `GET /api/analytics/dashboard/` - Dashboard statistics
- `GET /api/analytics/complaints/` - Complaint analytics
- `GET /api/analytics/feedback/` - Feedback analytics
- `GET /api/analytics/users/` - User analytics

## 🔐 User Roles & Permissions

### Student
- Register and manage profile
- Create and track complaints
- Submit withdrawal requests
- Provide feedback on resolved complaints
- Reply to staff comments/questions

### Staff
- View assigned complaints
- Add comments and responses
- Forward complaints
- Review withdrawal requests
- View department analytics

### Department Head
- All staff permissions
- Assign complaints within department
- Approve/reject withdrawal requests
- View department analytics
- Manage department staff

### VC (Vice Chancellor)
- All head permissions across departments
- System-wide complaint management
- Global analytics and reporting
- User management oversight

### Admin
- Full system access
- User and department management
- System configuration
- Complete analytics and logs access

## 📊 Analytics & Reporting

### Dashboard Metrics
- Total complaints by status
- Resolution rates and trends
- User activity statistics
- Feedback ratings and satisfaction

### Detailed Analytics
- **Complaints**: Status distribution, priority analysis, department performance
- **Feedback**: Rating trends, satisfaction metrics, response rates
- **Users**: Activity patterns, engagement metrics, role distribution
- **Performance**: Resolution times, escalation rates, system usage

### Automated Snapshots
```bash
# Create daily analytics snapshot
python manage.py create_daily_snapshot

# Create snapshot for specific date
python manage.py create_daily_snapshot --date 2024-01-15

# Force recreate existing snapshot
python manage.py create_daily_snapshot --force
```

## 🧹 Maintenance Commands

### Log Cleanup
```bash
# Clean logs older than 90 days
python manage.py cleanup_logs

# Clean logs older than 60 days
python manage.py cleanup_logs --days 60

# Dry run (see what would be deleted)
python manage.py cleanup_logs --dry-run

# Keep error logs regardless of age
python manage.py cleanup_logs --keep-errors
```

## 🔧 Configuration

### Email Notifications
Configure email settings in `.env` file. The system supports:
- SMTP configuration for production
- Console backend for development
- User notification preferences
- HTML email templates

### File Uploads
- Complaint attachments: `media/complaints/attachments/`
- Withdrawal documents: `media/withdrawals/documents/`
- User profile pictures: `media/users/profiles/`

### Celery Tasks (Optional)
For background tasks like sending emails:

```bash
# Start Celery worker
celery -A student_cms worker -l info

# Start Celery beat (for scheduled tasks)
celery -A student_cms beat -l info
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test complaints
python manage.py test users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📁 Project Structure

```
student_cms_api/
├── student_cms/          # Main project settings
├── users/                # User management and authentication
├── complaints/           # Complaint management system
├── withdrawals/          # Withdrawal request system
├── feedback/             # Feedback and rating system
├── notifications/        # Notification system
├── analytics/            # Analytics and reporting
├── logs/                 # Activity logging system
├── templates/            # Email templates
├── media/                # File uploads
├── staticfiles/          # Static files
└── requirements.txt      # Python dependencies
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in production
2. Configure proper database (MySQL/PostgreSQL)
3. Set up Redis for Celery
4. Configure email backend
5. Set up proper static/media file serving
6. Configure CORS for frontend domain
7. Set up SSL/HTTPS
8. Configure logging and monitoring

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/swagger/`

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added analytics and reporting
- **v1.2.0** - Enhanced notification system
- **v1.3.0** - Added activity logging and audit trail

---

**Built with ❤️ for educational institutions to streamline student complaint management.**

