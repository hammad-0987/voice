# Student CMS - Frontend (Vue.js 3)

A modern, responsive frontend application for the Student Complaint Management System built with Vue.js 3, Vite, and Bootstrap Vue 3.

## 🚀 Tech Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and development server
- **Vue Router 4** - Official router for Vue.js
- **Pinia** - State management library
- **Bootstrap Vue 3** - Bootstrap components for Vue.js
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualization library
- **Vue Chart.js** - Vue.js wrapper for Chart.js
- **Axios** - HTTP client for API requests
- **Bootstrap Icons** - Icon library
- **Date-fns** - Date utility library

## 📁 Project Structure

```
student-cms-ui/
├── public/                 # Static assets
├── src/
│   ├── assets/            # Assets (CSS, images)
│   │   └── css/           # Custom CSS files
│   ├── components/        # Reusable Vue components
│   │   └── layout/        # Layout components
│   ├── router/            # Vue Router configuration
│   ├── services/          # API services
│   ├── stores/            # Pinia stores
│   ├── views/             # Page components
│   │   ├── public/        # Public pages (landing, login, register)
│   │   ├── student/       # Student dashboard and pages
│   │   ├── staff/         # Staff dashboard and pages
│   │   ├── head/          # Department Head pages
│   │   ├── vc/            # Vice Chancellor pages
│   │   ├── admin/         # Admin pages
│   │   └── shared/        # Shared components
│   ├── App.vue            # Root component
│   └── main.js            # Application entry point
├── .env.example           # Environment variables template
├── package.json           # Dependencies and scripts
└── vite.config.js         # Vite configuration
```

## 🛠️ Setup & Installation

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Clone and navigate to the frontend directory:**
   ```bash
   cd student-cms-ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment setup:**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your configuration:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_APP_NAME=Student CMS
   VITE_APP_VERSION=1.0.0
   VITE_NODE_ENV=development
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5173`

## 🎯 Features

### 🔐 Authentication & Authorization
- **Role-based access control** (Student, Staff, Head, VC, Admin)
- **JWT token management** with automatic refresh
- **Secure route protection** with navigation guards
- **Persistent login state** with localStorage

### 🎨 User Interface
- **Responsive design** that works on all devices
- **Modern Bootstrap 5** styling with custom themes
- **Gradient backgrounds** and smooth animations
- **Dark/Light mode** support (planned)
- **Intuitive navigation** with role-based sidebars

### 📱 Layout Components
- **Dynamic navbar** with notifications and user menu
- **Collapsible sidebar** with role-specific navigation
- **Responsive layout** that adapts to screen size
- **Loading states** and error handling

### 🏠 Public Pages
- **Landing page** with features showcase
- **Login/Register** forms with validation
- **Complaint tracking** for public access
- **Responsive design** for mobile users

### 👨‍🎓 Student Features
- **Dashboard** with complaint statistics
- **File complaints** with file attachments
- **Track complaint status** in real-time
- **Withdrawal requests** management
- **Feedback submission** after resolution
- **Profile management** and settings

### 👨‍💼 Staff Features
- **Assigned complaints** management
- **Comment system** with three types (Comment, Require Info, Ask Question)
- **Complaint forwarding** to appropriate personnel
- **Withdrawal request** review and approval
- **Department analytics** and reporting

### 👨‍💻 Admin Features
- **User management** across all roles
- **Department management** and assignments
- **System settings** and configuration
- **Activity logs** and audit trails
- **Global analytics** and reporting

## 🔧 Development

### Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

### Code Structure

#### **Stores (Pinia)**
- `auth.js` - Authentication and user management
- `complaints.js` - Complaint operations and state
- `notifications.js` - Real-time notifications

#### **Services**
- `api.js` - Axios configuration with interceptors
- Token refresh and error handling
- Request/response transformations

#### **Router**
- Role-based route protection
- Dynamic navigation based on user permissions
- Lazy loading for better performance

### **Styling**
- Custom CSS variables for theming
- Bootstrap 5 with custom overrides
- Responsive utilities and animations
- Print-friendly styles

## 🎨 UI/UX Features

### **Visual Design**
- **Gradient backgrounds** for modern look
- **Card-based layouts** for better organization
- **Smooth animations** and transitions
- **Consistent iconography** with Bootstrap Icons

### **User Experience**
- **Intuitive navigation** with breadcrumbs
- **Real-time notifications** with badges
- **Loading states** for better feedback
- **Error handling** with user-friendly messages
- **Responsive design** for all screen sizes

### **Accessibility**
- **Keyboard navigation** support
- **Screen reader** friendly
- **High contrast** color schemes
- **Focus indicators** for interactive elements

## 📊 State Management

### **Auth Store**
- User authentication state
- Token management and refresh
- Profile information
- Role-based permissions

### **Complaints Store**
- Complaint CRUD operations
- Status tracking and updates
- Comment management
- File attachments

### **Notifications Store**
- Real-time notification handling
- Unread count management
- Notification preferences

## 🔌 API Integration

### **HTTP Client (Axios)**
- Automatic token attachment
- Request/response interceptors
- Error handling and retry logic
- Token refresh mechanism

### **API Endpoints**
- RESTful API communication
- File upload support
- Real-time updates
- Error response handling

## 🚀 Deployment

### **Build for Production**
```bash
npm run build
```

### **Environment Variables**
```env
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_APP_NAME=Student CMS
VITE_NODE_ENV=production
```

### **Static Hosting**
The built application can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

## 🔮 Future Enhancements

### **Planned Features**
- **Real-time chat** for complaint discussions
- **Push notifications** for mobile devices
- **Offline support** with service workers
- **Advanced analytics** with custom charts
- **Multi-language support** (i18n)
- **Dark mode** theme toggle
- **Advanced search** and filtering
- **Export functionality** for reports

### **Technical Improvements**
- **Unit testing** with Vitest
- **E2E testing** with Cypress
- **Performance optimization** with lazy loading
- **PWA features** for mobile experience
- **TypeScript migration** for better type safety

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for educational institutions to streamline student complaint management.**

