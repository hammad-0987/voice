from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('head', 'Department Head'),
        ('vc', 'Vice Chancellor'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def can_forward_to(self, user):
        """Check if current user can forward complaints to another user"""
        # Students cannot forward complaints
        if self.role == 'student':
            return False
        
        # Cannot forward to students
        if user.role == 'student':
            return False
        
        return True

    def can_view_withdrawal_request(self, withdrawal_request):
        """Check if user can view a withdrawal request"""
        # Student can only view their own requests
        if self.role == 'student':
            return withdrawal_request.submitted_by == self
        
        # Staff, Head, VC, Admin can view all requests
        return self.role in ['staff', 'head', 'vc', 'admin']

    def can_approve_withdrawal_request(self, withdrawal_request):
        """Check if user can approve/reject withdrawal requests"""
        return self.role in ['head', 'vc', 'admin']


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

