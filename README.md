# 🎓 Student Voice CMS - Complete Complaint Management System

A comprehensive, modern complaint management system built for educational institutions. This full-stack application provides a seamless experience for students to submit complaints and for staff to manage and resolve them efficiently.

![Student Voice CMS](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-brightgreen)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)

## 🌟 Features

### 👨‍🎓 **Student Features**
- **Self-Registration**: Students can register themselves
- **Complaint Submission**: Easy-to-use complaint filing system
- **Real-time Tracking**: Track complaint status with unique complaint numbers
- **Notifications**: Get notified about complaint updates
- **Feedback System**: Provide feedback after complaint resolution
- **Withdrawal Requests**: Submit private withdrawal requests

### 👨‍💼 **Staff Features**
- **Complaint Management**: View, update, and resolve assigned complaints
- **Comment System**: Add comments, request information, ask questions
- **Forwarding System**: Forward complaints to appropriate departments
- **Dashboard Analytics**: View performance metrics and statistics
- **Notification System**: Stay updated on complaint activities

### 👨‍💻 **Department Head Features**
- **Department Overview**: Complete department complaint analytics
- **Staff Management**: Manage department staff assignments
- **Performance Tracking**: Monitor department resolution rates
- **Advanced Analytics**: Interactive charts and trend analysis
- **Withdrawal Approvals**: Review and approve withdrawal requests

### 👑 **Vice Chancellor Features**
- **System-wide Overview**: Executive dashboard with global metrics
- **Department Performance**: Compare department effectiveness
- **Critical Issues**: Monitor high-priority complaints
- **System Health**: Real-time system monitoring
- **Strategic Reports**: Generate comprehensive reports

### ⚙️ **Admin Features**
- **User Management**: Complete CRUD operations for all users
- **Department Management**: Manage departments and assignments
- **System Settings**: Configure system-wide settings
- **Activity Logs**: Monitor all system activities
- **Advanced Analytics**: Deep insights into system performance

## 🏗️ Architecture

### **Backend (Django + DRF)**
- **Framework**: Django 5.0 with Django REST Framework
- **Database**: MySQL with optimized queries
- **Authentication**: JWT-based authentication system
- **Permissions**: Role-based access control (RBAC)
- **API**: RESTful API with comprehensive endpoints
- **File Handling**: Support for complaint attachments

### **Frontend (Vue.js 3)**
- **Framework**: Vue.js 3 with Composition API
- **Build Tool**: Vite for fast development and building
- **Routing**: Vue Router for SPA navigation
- **State Management**: Pinia for reactive state management
- **UI Framework**: BootstrapVue 3 for responsive components
- **Charts**: Chart.js for beautiful data visualization
- **Styling**: Custom SCSS with modern design patterns

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Git

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd student-voice-cms

# Navigate to backend
cd student_cms_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
# Update DATABASES in settings.py with your MySQL credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
# Navigate to frontend
cd student-cms-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📊 System Workflow

### Complaint Lifecycle
1. **Submission**: Student submits complaint with auto-generated number (CMP-YYYY-XXXX)
2. **Assignment**: Admin/Head assigns to appropriate staff
3. **Processing**: Staff processes and updates status
4. **Communication**: Comments, questions, and information requests
5. **Forwarding**: Forward to other departments if needed
6. **Resolution**: Mark as resolved, rejected, or not resolved
7. **Feedback**: Student provides feedback after closure
8. **Analytics**: System tracks all metrics and performance

### User Roles & Permissions

| Feature | Student | Staff | Head | VC | Admin |
|---------|---------|-------|------|----|----|
| Submit Complaints | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Own Complaints | ✅ | ❌ | ❌ | ❌ | ❌ |
| Manage Assigned Complaints | ❌ | ✅ | ✅ | ✅ | ✅ |
| Forward Complaints | ❌ | ✅ | ✅ | ✅ | ✅ |
| Department Analytics | ❌ | ❌ | ✅ | ✅ | ✅ |
| System-wide Analytics | ❌ | ❌ | ❌ | ✅ | ✅ |
| User Management | ❌ | ❌ | ❌ | ❌ | ✅ |
| System Settings | ❌ | ❌ | ❌ | ❌ | ✅ |

## 🎨 UI/UX Features

### Modern Design
- **Responsive Design**: Works perfectly on all devices
- **Professional Gradients**: Beautiful gradient headers and cards
- **Glassmorphism Effects**: Modern translucent design elements
- **Smooth Animations**: Micro-interactions and hover effects
- **Consistent Typography**: Professional font hierarchy
- **Color-coded Status**: Intuitive status indicators

### Interactive Elements
- **Interactive Charts**: Hover effects and data tooltips
- **Advanced Filtering**: Multi-criteria search and filtering
- **Sortable Tables**: Click-to-sort functionality
- **Modal Dialogs**: Professional forms and detail views
- **Loading States**: Skeleton loaders and spinners
- **Empty States**: Helpful illustrations and messages

## 📱 Mobile Responsiveness

The application is fully responsive with:
- **Mobile-first Design**: Optimized for mobile devices
- **Touch-friendly Interface**: Large buttons and touch targets
- **Collapsible Navigation**: Space-efficient mobile navigation
- **Readable Typography**: Optimized text sizes for mobile
- **Swipe Gestures**: Natural mobile interactions

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Granular permissions system
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Prevention**: Template escaping and sanitization
- **CSRF Protection**: Cross-site request forgery protection

## 📈 Analytics & Reporting

### Dashboard Metrics
- **Complaint Statistics**: Total, pending, resolved counts
- **Performance Metrics**: Resolution rates and times
- **Department Comparison**: Cross-department analytics
- **Trend Analysis**: Historical data visualization
- **User Activity**: System usage statistics

### Chart Types
- **Line Charts**: Trend analysis over time
- **Bar Charts**: Department comparisons
- **Doughnut Charts**: Status distributions
- **Dual-axis Charts**: Multiple metrics comparison

## 🔧 Technical Specifications

### Backend Technologies
- **Django 5.0**: Web framework
- **Django REST Framework**: API development
- **MySQL**: Primary database
- **JWT**: Authentication tokens
- **Pillow**: Image processing
- **Django CORS**: Cross-origin requests
- **Django Filters**: Advanced filtering

### Frontend Technologies
- **Vue.js 3**: Progressive framework
- **Vite**: Build tool and dev server
- **Vue Router**: Client-side routing
- **Pinia**: State management
- **BootstrapVue 3**: UI components
- **Chart.js**: Data visualization
- **Axios**: HTTP client
- **SCSS**: Styling preprocessor

## 📁 Project Structure

```
student-voice-cms/
├── student_cms_api/          # Django Backend
│   ├── student_cms/          # Main project settings
│   ├── users/                # User management app
│   ├── complaints/           # Complaint management app
│   ├── notifications/        # Notification system
│   ├── feedback/             # Feedback system
│   ├── withdrawals/          # Withdrawal requests
│   ├── analytics/            # Analytics and reporting
│   └── logs/                 # Activity logging
├── student-cms-ui/           # Vue.js Frontend
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── views/            # Page components
│   │   ├── stores/           # Pinia stores
│   │   ├── services/         # API services
│   │   └── assets/           # Static assets
│   ├── public/               # Public assets
│   └── package.json          # Dependencies
└── README.md                 # This file
```

## 🚀 Deployment

### Production Setup

1. **Backend Deployment**
   ```bash
   # Install production dependencies
   pip install gunicorn
   
   # Collect static files
   python manage.py collectstatic
   
   # Run with Gunicorn
   gunicorn student_cms.wsgi:application
   ```

2. **Frontend Deployment**
   ```bash
   # Build for production
   npm run build
   
   # Serve with nginx or any static server
   ```

### Environment Variables
Create `.env` files for both backend and frontend with appropriate configuration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Hammad Gujjar**
- GitHub: [@hammad-0987](https://github.com/hammad-0987)
- Email: hammadgujjar01234@gmail.com

## 🙏 Acknowledgments

- Django community for the excellent framework
- Vue.js team for the progressive framework
- Chart.js for beautiful data visualization
- Bootstrap team for responsive components
- All contributors and testers

---

## 📞 Support

If you have any questions or need support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Contact the maintainer

**Made with ❤️ for educational institutions worldwide**

