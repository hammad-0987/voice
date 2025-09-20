from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('not_resolved', 'Not Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    complaint_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Relationships
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    department = models.ForeignKey('users.Department', on_delete=models.SET_NULL, null=True, blank=True)
    
    # File attachment
    attachment = models.FileField(upload_to='complaints/attachments/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['complaint_number']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"{self.complaint_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.complaint_number:
            self.complaint_number = self.generate_complaint_number()
        
        # Set resolved_at when status changes to resolved
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        # Set closed_at when status changes to closed
        if self.status == 'closed' and not self.closed_at:
            self.closed_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def generate_complaint_number(self):
        """Generate unique complaint number in format CMP-YYYY-XXXX"""
        year = datetime.now().year
        
        # Get the last complaint number for this year
        last_complaint = Complaint.objects.filter(
            complaint_number__startswith=f'CMP-{year}-'
        ).order_by('-complaint_number').first()
        
        if last_complaint:
            # Extract the sequence number and increment
            last_seq = int(last_complaint.complaint_number.split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f'CMP-{year}-{new_seq:04d}'
    
    @property
    def is_closed(self):
        """Check if complaint is in a closed state"""
        return self.status in ['resolved', 'rejected', 'not_resolved', 'closed']
    
    @property
    def can_receive_feedback(self):
        """Check if complaint can receive feedback"""
        return self.status in ['resolved', 'rejected', 'not_resolved']
    
    def get_timeline(self):
        """Get complaint timeline including forwards and comments"""
        timeline = []
        
        # Add complaint creation
        timeline.append({
            'type': 'created',
            'timestamp': self.created_at,
            'user': self.created_by,
            'message': f'Complaint created by {self.created_by.full_name}'
        })
        
        # Add forwards
        for forward in self.forwards.all():
            timeline.append({
                'type': 'forwarded',
                'timestamp': forward.created_at,
                'user': forward.from_user,
                'message': f'Forwarded to {forward.to_user.full_name}',
                'remarks': forward.remarks
            })
        
        # Add comments
        for comment in self.comments.all():
            timeline.append({
                'type': 'comment',
                'timestamp': comment.created_at,
                'user': comment.user,
                'message': comment.text,
                'comment_type': comment.comment_type,
                'reply': comment.reply,
                'replied_at': comment.replied_at
            })
        
        # Sort by timestamp
        timeline.sort(key=lambda x: x['timestamp'])
        return timeline


class ComplaintForward(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='forwards')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forwarded_complaints')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_complaints')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_number} forwarded from {self.from_user} to {self.to_user}"


class ComplaintComment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('comment', 'Comment'),
        ('require_info', 'Require Info'),
        ('ask_question', 'Ask Question'),
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length=15, choices=COMMENT_TYPE_CHOICES, default='comment')
    text = models.TextField()
    
    # Student reply (only for require_info and ask_question types)
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_number} - {self.get_comment_type_display()} by {self.user}"
    
    def can_be_replied_to(self):
        """Check if this comment can be replied to by student"""
        return self.comment_type in ['require_info', 'ask_question'] and not self.reply
    
    def add_reply(self, reply_text, user):
        """Add student reply to this comment"""
        if self.can_be_replied_to() and user.role == 'student' and user == self.complaint.created_by:
            self.reply = reply_text
            self.replied_at = timezone.now()
            self.save()
            return True
        return False


class ComplaintResponse(models.Model):
    """Legacy model for complaint responses - keeping for backward compatibility"""
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    message = models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Response to {self.complaint.complaint_number} by {self.added_by}"

