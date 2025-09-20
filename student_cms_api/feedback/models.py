from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class ComplaintFeedback(models.Model):
    complaint = models.OneToOneField(
        'complaints.Complaint', 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )
    feedback_text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Relationships
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='submitted_feedback'
    )
    
    # Auto-forwarding tracking
    forwarded_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='received_feedback',
        blank=True,
        help_text="Users who received this feedback (Head, VC, Admin)"
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['complaint']),
            models.Index(fields=['submitted_by']),
            models.Index(fields=['rating']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"Feedback for {self.complaint.complaint_number} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Auto-forward to Head, VC, and Admin on creation
        if is_new:
            self.auto_forward_feedback()
    
    def auto_forward_feedback(self):
        """Auto-forward feedback to Head, VC, and Admin"""
        from users.models import User
        
        # Get Head, VC, and Admin users
        recipients = User.objects.filter(role__in=['head', 'vc', 'admin'])
        
        # Add them to forwarded_to
        self.forwarded_to.set(recipients)
        
        # Create notifications for each recipient
        from notifications.utils import create_notification
        for recipient in recipients:
            create_notification(
                recipient=recipient,
                message=f'New feedback received for complaint {self.complaint.complaint_number} - {self.rating} stars',
                link=f'/feedback/{self.id}/'
            )
    
    @property
    def rating_stars(self):
        """Get rating as stars string"""
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    @property
    def rating_percentage(self):
        """Get rating as percentage"""
        return (self.rating / 5) * 100
    
    def can_be_viewed_by(self, user):
        """Check if user can view this feedback"""
        # Student can view their own feedback
        if user.role == 'student':
            return self.submitted_by == user
        
        # Staff can view feedback for complaints they handled
        if user.role == 'staff':
            return (self.complaint.assigned_to == user or 
                    self.complaint.created_by == user)
        
        # Head, VC, Admin can view all feedback
        return user.role in ['head', 'vc', 'admin']
    
    def can_be_edited_by(self, user):
        """Check if user can edit this feedback"""
        # Only the student who submitted can edit (within a time limit if needed)
        return (user.role == 'student' and 
                self.submitted_by == user)


class FeedbackResponse(models.Model):
    """Response to feedback from management"""
    feedback = models.ForeignKey(
        ComplaintFeedback, 
        on_delete=models.CASCADE, 
        related_name='responses'
    )
    response_text = models.TextField()
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='feedback_responses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Response to feedback for {self.feedback.complaint.complaint_number}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create notification for the student who submitted feedback
        if is_new:
            from notifications.utils import create_notification
            create_notification(
                recipient=self.feedback.submitted_by,
                message=f'Management responded to your feedback for complaint {self.feedback.complaint.complaint_number}',
                link=f'/feedback/{self.feedback.id}/'
            )

