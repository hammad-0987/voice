# 📚 API Documentation - Student Voice CMS

This document provides comprehensive information about the REST API endpoints available in the Student Voice CMS system.

## 🔗 Base URL

```
http://localhost:8000/api/
```

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### Register User (Student Only)
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john.doe@university.edu",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "student_id": "CS2024001",
  "phone": "+1234567890",
  "department": 1
}
```

**Response:**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@university.edu",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "is_active": true
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### Login
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@university.edu",
    "role": "student",
    "department": {
      "id": 1,
      "name": "Computer Science"
    }
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### Logout
```http
POST /api/auth/logout/
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 👥 User Management

#### Get User Profile
```http
GET /api/users/profile/
```

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "department": {
    "id": 1,
    "name": "Computer Science"
  },
  "student_id": "CS2024001",
  "phone": "+1234567890",
  "profile_picture": null,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

#### Update User Profile
```http
PUT /api/users/profile/
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@university.edu",
  "phone": "+1234567890"
}
```

#### Change Password
```http
POST /api/users/change-password/
```

**Request Body:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

#### List Users (Admin Only)
```http
GET /api/users/
```

**Query Parameters:**
- `role`: Filter by role (student, staff, head, vc, admin)
- `department`: Filter by department ID
- `is_active`: Filter by active status (true/false)
- `search`: Search by username, name, or email
- `ordering`: Sort by field (username, first_name, date_joined)

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john.doe@university.edu",
      "first_name": "John",
      "last_name": "Doe",
      "role": "student",
      "department": {
        "id": 1,
        "name": "Computer Science"
      },
      "is_active": true,
      "date_joined": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create User (Admin Only)
```http
POST /api/users/
```

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@university.edu",
  "password": "securepassword123",
  "first_name": "New",
  "last_name": "User",
  "role": "staff",
  "department": 1,
  "employee_id": "EMP001"
}
```

## 📋 Complaint Management

#### List Complaints
```http
GET /api/complaints/
```

**Query Parameters:**
- `status`: Filter by status (pending, in_progress, resolved, rejected, not_resolved, closed)
- `priority`: Filter by priority (low, medium, high, urgent)
- `department`: Filter by department ID
- `created_by`: Filter by creator ID
- `assigned_to`: Filter by assignee ID
- `search`: Search in title and description
- `ordering`: Sort by field (created_at, updated_at, priority)

**Response:**
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "complaint_number": "CMP-2024-0001",
      "title": "Library access issue",
      "description": "Unable to access library resources online",
      "status": "pending",
      "priority": "medium",
      "created_by": {
        "id": 1,
        "username": "johndoe",
        "full_name": "John Doe"
      },
      "assigned_to": null,
      "department": {
        "id": 1,
        "name": "Computer Science"
      },
      "attachment": null,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Complaint
```http
POST /api/complaints/
```

**Request Body (multipart/form-data):**
```
title: Library access issue
description: Unable to access library resources online
priority: medium
department: 1
attachment: [file]
```

**Response:**
```json
{
  "id": 1,
  "complaint_number": "CMP-2024-0001",
  "title": "Library access issue",
  "description": "Unable to access library resources online",
  "status": "pending",
  "priority": "medium",
  "created_by": {
    "id": 1,
    "username": "johndoe",
    "full_name": "John Doe"
  },
  "department": {
    "id": 1,
    "name": "Computer Science"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Complaint Details
```http
GET /api/complaints/{id}/
```

**Response:**
```json
{
  "id": 1,
  "complaint_number": "CMP-2024-0001",
  "title": "Library access issue",
  "description": "Unable to access library resources online",
  "status": "in_progress",
  "priority": "medium",
  "created_by": {
    "id": 1,
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "john.doe@university.edu"
  },
  "assigned_to": {
    "id": 2,
    "username": "staffmember",
    "full_name": "Staff Member"
  },
  "department": {
    "id": 1,
    "name": "Computer Science"
  },
  "attachment": "http://localhost:8000/media/complaints/document.pdf",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z",
  "forwards": [
    {
      "id": 1,
      "from_user": {
        "id": 2,
        "full_name": "Staff Member"
      },
      "to_user": {
        "id": 3,
        "full_name": "Department Head"
      },
      "remarks": "Forwarding to department head for review",
      "timestamp": "2024-01-16T14:20:00Z"
    }
  ],
  "comments": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "full_name": "Staff Member"
      },
      "comment_type": "comment",
      "text": "We are looking into this issue",
      "reply": null,
      "created_at": "2024-01-16T14:25:00Z"
    }
  ],
  "responses": [
    {
      "id": 1,
      "message": "Issue has been identified and fix is in progress",
      "added_by": {
        "id": 2,
        "full_name": "Staff Member"
      },
      "created_at": "2024-01-16T15:00:00Z"
    }
  ]
}
```

#### Update Complaint Status
```http
PATCH /api/complaints/{id}/
```

**Request Body:**
```json
{
  "status": "resolved",
  "assigned_to": 2
}
```

#### Forward Complaint
```http
POST /api/complaints/{id}/forward/
```

**Request Body:**
```json
{
  "to_user": 3,
  "remarks": "Forwarding to department head for review"
}
```

#### Add Comment to Complaint
```http
POST /api/complaints/{id}/comments/
```

**Request Body:**
```json
{
  "comment_type": "comment",
  "text": "We are looking into this issue"
}
```

#### Reply to Comment (Student Only)
```http
POST /api/complaints/{complaint_id}/comments/{comment_id}/reply/
```

**Request Body:**
```json
{
  "reply": "Thank you for the update"
}
```

## 🔔 Notifications

#### List Notifications
```http
GET /api/notifications/
```

**Query Parameters:**
- `is_read`: Filter by read status (true/false)
- `notification_type`: Filter by type
- `ordering`: Sort by field (created_at)

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Complaint Status Updated",
      "message": "Your complaint CMP-2024-0001 has been updated to 'In Progress'",
      "notification_type": "complaint_update",
      "is_read": false,
      "link": "/complaints/1/",
      "created_at": "2024-01-16T14:30:00Z"
    }
  ]
}
```

#### Mark Notification as Read
```http
PATCH /api/notifications/{id}/
```

**Request Body:**
```json
{
  "is_read": true
}
```

#### Mark All Notifications as Read
```http
POST /api/notifications/mark-all-read/
```

## 💬 Feedback

#### Submit Feedback
```http
POST /api/feedback/
```

**Request Body:**
```json
{
  "complaint": 1,
  "feedback_text": "The issue was resolved quickly and efficiently",
  "rating": 5
}
```

#### List Feedback (Staff/Head/VC/Admin)
```http
GET /api/feedback/
```

**Query Parameters:**
- `complaint`: Filter by complaint ID
- `rating`: Filter by rating
- `submitted_by`: Filter by submitter ID

## 📄 Withdrawal Requests

#### List Withdrawal Requests
```http
GET /api/withdrawals/
```

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "request_number": "WRQ-2024-0001",
      "type": "course_withdrawal",
      "reason": "Personal reasons",
      "status": "pending",
      "submitted_by": {
        "id": 1,
        "full_name": "John Doe"
      },
      "reviewed_by": null,
      "response": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Withdrawal Request
```http
POST /api/withdrawals/
```

**Request Body:**
```json
{
  "type": "course_withdrawal",
  "reason": "Personal reasons",
  "additional_info": "Need to withdraw due to family circumstances"
}
```

#### Update Withdrawal Request (Staff/Head/VC/Admin)
```http
PATCH /api/withdrawals/{id}/
```

**Request Body:**
```json
{
  "status": "approved",
  "response": "Request approved. Please contact the registrar's office."
}
```

## 🏢 Departments

#### List Departments
```http
GET /api/departments/
```

**Response:**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "name": "Computer Science",
      "code": "CS",
      "head": {
        "id": 3,
        "full_name": "Dr. Smith"
      },
      "description": "Department of Computer Science and Engineering"
    }
  ]
}
```

#### Create Department (Admin Only)
```http
POST /api/departments/
```

**Request Body:**
```json
{
  "name": "Computer Science",
  "code": "CS",
  "head": 3,
  "description": "Department of Computer Science and Engineering"
}
```

## 📊 Analytics & Reports

#### Dashboard Statistics
```http
GET /api/users/dashboard-stats/
```

**Response (varies by user role):**
```json
{
  "role": "student",
  "department": "Computer Science",
  "total_complaints": 5,
  "pending_complaints": 2,
  "resolved_complaints": 3
}
```

#### Complaint Statistics
```http
GET /api/complaints/statistics/
```

**Query Parameters:**
- `department`: Filter by department ID
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Response:**
```json
{
  "total_complaints": 150,
  "by_status": {
    "pending": 25,
    "in_progress": 30,
    "resolved": 80,
    "rejected": 10,
    "not_resolved": 5
  },
  "by_priority": {
    "low": 40,
    "medium": 60,
    "high": 35,
    "urgent": 15
  },
  "by_department": {
    "Computer Science": 50,
    "Engineering": 40,
    "Business": 30,
    "Arts": 30
  },
  "resolution_rate": 78.5,
  "average_resolution_time": 3.2
}
```

## 🚨 Error Responses

### Common Error Codes

#### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["This field is required."],
    "password": ["This field must be at least 8 characters long."]
  }
}
```

#### 401 Unauthorized
```json
{
  "error": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
  "error": "Not found."
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error. Please try again later."
}
```

## 📝 Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **General endpoints**: 100 requests per minute
- **File upload endpoints**: 10 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 🔍 Filtering and Searching

Most list endpoints support filtering and searching:

### Query Parameters
- `search`: Full-text search across relevant fields
- `ordering`: Sort by field (prefix with `-` for descending)
- `page`: Page number for pagination
- `page_size`: Number of items per page (max 100)

### Example
```http
GET /api/complaints/?search=library&status=pending&ordering=-created_at&page=1&page_size=20
```

## 📄 Pagination

All list endpoints use cursor-based pagination:

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/complaints/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🔒 Permissions

### Role-based Access Control

| Endpoint | Student | Staff | Head | VC | Admin |
|----------|---------|-------|------|----|----|
| POST /api/complaints/ | ✅ | ❌ | ❌ | ❌ | ❌ |
| GET /api/complaints/ | Own only | Assigned | Department | All | All |
| PATCH /api/complaints/{id}/ | ❌ | Assigned | Department | All | All |
| POST /api/complaints/{id}/forward/ | ❌ | ✅ | ✅ | ✅ | ✅ |
| GET /api/users/ | ❌ | ❌ | Department | All | All |
| POST /api/users/ | ❌ | ❌ | ❌ | ❌ | ✅ |

## 📞 Support

For API support and questions:
- Check this documentation first
- Review the Django REST Framework documentation
- Create an issue on GitHub with API-specific tags
- Contact the development team

**API Version**: v1.0  
**Last Updated**: January 2024

