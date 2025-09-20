from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    TYPE_CHOICES = [
        ('course_withdrawal', 'Course Withdrawal'),
        ('semester_withdrawal', 'Semester Withdrawal'),
        ('program_withdrawal', 'Program Withdrawal'),
        ('leave_of_absence', 'Leave of Absence'),
        ('transfer_request', 'Transfer Request'),
        ('other', 'Other'),
    ]
    
    request_number = models.CharField(max_length=20, unique=True, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Relationships
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='withdrawal_requests'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_withdrawals'
    )
    
    # Review details
    response = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Supporting documents
    supporting_document = models.FileField(
        upload_to='withdrawals/documents/', 
        blank=True, 
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['request_number']),
            models.Index(fields=['status']),
            models.Index(fields=['submitted_by']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return f"{self.request_number} - {self.get_type_display()}"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_request_number()
        
        # Set reviewed_at when status changes from pending
        if self.status != 'pending' and not self.reviewed_at:
            self.reviewed_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def generate_request_number(self):
        """Generate unique request number in format WRQ-YYYY-XXXX"""
        year = datetime.now().year
        
        # Get the last request number for this year
        last_request = WithdrawalRequest.objects.filter(
            request_number__startswith=f'WRQ-{year}-'
        ).order_by('-request_number').first()
        
        if last_request:
            # Extract the sequence number and increment
            last_seq = int(last_request.request_number.split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f'WRQ-{year}-{new_seq:04d}'
    
    @property
    def is_pending(self):
        """Check if request is still pending"""
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        """Check if request is approved"""
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        """Check if request is rejected"""
        return self.status == 'rejected'
    
    def can_be_reviewed_by(self, user):
        """Check if user can review this withdrawal request"""
        # Only Head, VC, and Admin can review withdrawal requests
        return user.role in ['head', 'vc', 'admin']
    
    def can_be_viewed_by(self, user):
        """Check if user can view this withdrawal request"""
        # Student can only view their own requests
        if user.role == 'student':
            return self.submitted_by == user
        
        # Staff, Head, VC, Admin can view all requests
        return user.role in ['staff', 'head', 'vc', 'admin']
    
    def approve(self, user, response=None):
        """Approve the withdrawal request"""
        if not self.can_be_reviewed_by(user):
            return False
        
        self.status = 'approved'
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        if response:
            self.response = response
        self.save()
        return True
    
    def reject(self, user, response=None):
        """Reject the withdrawal request"""
        if not self.can_be_reviewed_by(user):
            return False
        
        self.status = 'rejected'
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        if response:
            self.response = response
        self.save()
        return True

