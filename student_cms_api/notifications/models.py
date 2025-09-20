from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('complaint_created', 'Complaint Created'),
        ('complaint_forwarded', 'Complaint Forwarded'),
        ('complaint_status_changed', 'Complaint Status Changed'),
        ('comment_added', 'Comment Added'),
        ('reply_added', 'Reply Added'),
        ('withdrawal_submitted', 'Withdrawal Request Submitted'),
        ('withdrawal_reviewed', 'Withdrawal Request Reviewed'),
        ('feedback_submitted', 'Feedback Submitted'),
        ('feedback_response', 'Feedback Response'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=25, 
        choices=NOTIFICATION_TYPES, 
        default='system'
    )
    
    # Optional link to related object
    link = models.URLField(blank=True, null=True, help_text="Link to related page")
    
    # Related object tracking (generic foreign key could be used here)
    related_complaint_id = models.IntegerField(null=True, blank=True)
    related_withdrawal_id = models.IntegerField(null=True, blank=True)
    related_feedback_id = models.IntegerField(null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)  # For email notifications
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=['is_read', 'read_at'])
    
    @property
    def is_recent(self):
        """Check if notification is recent (within last 24 hours)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(hours=24)
    
    def get_related_object(self):
        """Get the related object based on the notification type"""
        if self.related_complaint_id:
            try:
                from complaints.models import Complaint
                return Complaint.objects.get(id=self.related_complaint_id)
            except Complaint.DoesNotExist:
                pass
        
        if self.related_withdrawal_id:
            try:
                from withdrawals.models import WithdrawalRequest
                return WithdrawalRequest.objects.get(id=self.related_withdrawal_id)
            except WithdrawalRequest.DoesNotExist:
                pass
        
        if self.related_feedback_id:
            try:
                from feedback.models import ComplaintFeedback
                return ComplaintFeedback.objects.get(id=self.related_feedback_id)
            except ComplaintFeedback.DoesNotExist:
                pass
        
        return None


class NotificationPreference(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notification_preferences'
    )
    
    # Email notifications
    email_complaint_updates = models.BooleanField(default=True)
    email_withdrawal_updates = models.BooleanField(default=True)
    email_feedback_updates = models.BooleanField(default=True)
    email_system_updates = models.BooleanField(default=True)
    
    # In-app notifications
    app_complaint_updates = models.BooleanField(default=True)
    app_withdrawal_updates = models.BooleanField(default=True)
    app_feedback_updates = models.BooleanField(default=True)
    app_system_updates = models.BooleanField(default=True)
    
    # Frequency settings
    email_digest_frequency = models.CharField(
        max_length=10,
        choices=[
            ('immediate', 'Immediate'),
            ('daily', 'Daily Digest'),
            ('weekly', 'Weekly Digest'),
            ('never', 'Never'),
        ],
        default='immediate'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
    
    @classmethod
    def get_or_create_for_user(cls, user):
        """Get or create notification preferences for a user"""
        preferences, created = cls.objects.get_or_create(user=user)
        return preferences

