from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class AnalyticsSnapshot(models.Model):
    """
    Store periodic snapshots of system analytics for historical tracking
    """
    
    # Snapshot metadata
    snapshot_date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Complaint statistics
    total_complaints = models.IntegerField(default=0)
    pending_complaints = models.IntegerField(default=0)
    in_progress_complaints = models.IntegerField(default=0)
    resolved_complaints = models.IntegerField(default=0)
    rejected_complaints = models.IntegerField(default=0)
    not_resolved_complaints = models.IntegerField(default=0)
    closed_complaints = models.IntegerField(default=0)
    
    # New complaints created on this date
    new_complaints_today = models.IntegerField(default=0)
    
    # Withdrawal statistics
    total_withdrawals = models.IntegerField(default=0)
    pending_withdrawals = models.IntegerField(default=0)
    approved_withdrawals = models.IntegerField(default=0)
    rejected_withdrawals = models.IntegerField(default=0)
    new_withdrawals_today = models.IntegerField(default=0)
    
    # Feedback statistics
    total_feedback = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    new_feedback_today = models.IntegerField(default=0)
    
    # User statistics
    total_users = models.IntegerField(default=0)
    active_users_today = models.IntegerField(default=0)
    new_users_today = models.IntegerField(default=0)
    
    # Performance metrics
    avg_resolution_time_days = models.FloatField(default=0.0)
    avg_response_time_hours = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-snapshot_date']
        indexes = [
            models.Index(fields=['snapshot_date']),
        ]
    
    def __str__(self):
        return f"Analytics Snapshot - {self.snapshot_date}"
    
    @classmethod
    def create_daily_snapshot(cls, date=None):
        """
        Create a daily analytics snapshot
        """
        if date is None:
            date = timezone.now().date()
        
        # Avoid duplicate snapshots
        if cls.objects.filter(snapshot_date=date).exists():
            return cls.objects.get(snapshot_date=date)
        
        from complaints.models import Complaint
        from withdrawals.models import WithdrawalRequest
        from feedback.models import ComplaintFeedback
        from users.models import User
        from logs.models import ActivityLog
        from django.db.models import Avg, Count
        
        # Calculate complaint statistics
        complaints_qs = Complaint.objects.all()
        total_complaints = complaints_qs.count()
        pending_complaints = complaints_qs.filter(status='pending').count()
        in_progress_complaints = complaints_qs.filter(status='in_progress').count()
        resolved_complaints = complaints_qs.filter(status='resolved').count()
        rejected_complaints = complaints_qs.filter(status='rejected').count()
        not_resolved_complaints = complaints_qs.filter(status='not_resolved').count()
        closed_complaints = complaints_qs.filter(status='closed').count()
        
        # New complaints today
        new_complaints_today = complaints_qs.filter(created_at__date=date).count()
        
        # Calculate withdrawal statistics
        withdrawals_qs = WithdrawalRequest.objects.all()
        total_withdrawals = withdrawals_qs.count()
        pending_withdrawals = withdrawals_qs.filter(status='pending').count()
        approved_withdrawals = withdrawals_qs.filter(status='approved').count()
        rejected_withdrawals = withdrawals_qs.filter(status='rejected').count()
        new_withdrawals_today = withdrawals_qs.filter(created_at__date=date).count()
        
        # Calculate feedback statistics
        feedback_qs = ComplaintFeedback.objects.all()
        total_feedback = feedback_qs.count()
        avg_rating = feedback_qs.aggregate(avg=Avg('rating'))['avg'] or 0.0
        new_feedback_today = feedback_qs.filter(submitted_at__date=date).count()
        
        # Calculate user statistics
        users_qs = User.objects.all()
        total_users = users_qs.count()
        new_users_today = users_qs.filter(date_joined__date=date).count()
        
        # Active users today (users who performed any action)
        active_users_today = ActivityLog.objects.filter(
            timestamp__date=date
        ).values('user').distinct().count()
        
        # Calculate performance metrics
        resolved_complaints_with_time = complaints_qs.filter(
            status='resolved',
            resolved_at__isnull=False
        )
        
        avg_resolution_time_days = 0.0
        if resolved_complaints_with_time.exists():
            total_resolution_time = sum([
                (complaint.resolved_at - complaint.created_at).days
                for complaint in resolved_complaints_with_time
                if complaint.resolved_at and complaint.created_at
            ])
            avg_resolution_time_days = total_resolution_time / resolved_complaints_with_time.count()
        
        # Create snapshot
        snapshot = cls.objects.create(
            snapshot_date=date,
            total_complaints=total_complaints,
            pending_complaints=pending_complaints,
            in_progress_complaints=in_progress_complaints,
            resolved_complaints=resolved_complaints,
            rejected_complaints=rejected_complaints,
            not_resolved_complaints=not_resolved_complaints,
            closed_complaints=closed_complaints,
            new_complaints_today=new_complaints_today,
            total_withdrawals=total_withdrawals,
            pending_withdrawals=pending_withdrawals,
            approved_withdrawals=approved_withdrawals,
            rejected_withdrawals=rejected_withdrawals,
            new_withdrawals_today=new_withdrawals_today,
            total_feedback=total_feedback,
            average_rating=round(avg_rating, 2),
            new_feedback_today=new_feedback_today,
            total_users=total_users,
            active_users_today=active_users_today,
            new_users_today=new_users_today,
            avg_resolution_time_days=round(avg_resolution_time_days, 2),
        )
        
        return snapshot


class DepartmentAnalytics(models.Model):
    """
    Department-specific analytics
    """
    
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    snapshot_date = models.DateField()
    
    # Complaint statistics for this department
    total_complaints = models.IntegerField(default=0)
    pending_complaints = models.IntegerField(default=0)
    resolved_complaints = models.IntegerField(default=0)
    avg_resolution_time_days = models.FloatField(default=0.0)
    
    # Feedback statistics
    total_feedback = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    # Staff performance
    active_staff_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['department', 'snapshot_date']
        ordering = ['-snapshot_date', 'department__name']
        indexes = [
            models.Index(fields=['department', 'snapshot_date']),
        ]
    
    def __str__(self):
        return f"{self.department.name} Analytics - {self.snapshot_date}"
    
    @classmethod
    def create_department_snapshots(cls, date=None):
        """
        Create analytics snapshots for all departments
        """
        if date is None:
            date = timezone.now().date()
        
        from users.models import Department
        from complaints.models import Complaint
        from feedback.models import ComplaintFeedback
        from django.db.models import Avg, Count
        
        snapshots = []
        
        for department in Department.objects.all():
            # Skip if snapshot already exists
            if cls.objects.filter(department=department, snapshot_date=date).exists():
                continue
            
            # Calculate department complaint statistics
            dept_complaints = Complaint.objects.filter(department=department)
            total_complaints = dept_complaints.count()
            pending_complaints = dept_complaints.filter(status='pending').count()
            resolved_complaints = dept_complaints.filter(status='resolved').count()
            
            # Calculate average resolution time
            resolved_with_time = dept_complaints.filter(
                status='resolved',
                resolved_at__isnull=False
            )
            
            avg_resolution_time = 0.0
            if resolved_with_time.exists():
                total_time = sum([
                    (complaint.resolved_at - complaint.created_at).days
                    for complaint in resolved_with_time
                    if complaint.resolved_at and complaint.created_at
                ])
                avg_resolution_time = total_time / resolved_with_time.count()
            
            # Calculate feedback statistics
            dept_feedback = ComplaintFeedback.objects.filter(
                complaint__department=department
            )
            total_feedback = dept_feedback.count()
            avg_rating = dept_feedback.aggregate(avg=Avg('rating'))['avg'] or 0.0
            
            # Count active staff
            active_staff = department.user_set.filter(
                role='staff',
                is_active=True
            ).count()
            
            # Create snapshot
            snapshot = cls.objects.create(
                department=department,
                snapshot_date=date,
                total_complaints=total_complaints,
                pending_complaints=pending_complaints,
                resolved_complaints=resolved_complaints,
                avg_resolution_time_days=round(avg_resolution_time, 2),
                total_feedback=total_feedback,
                average_rating=round(avg_rating, 2),
                active_staff_count=active_staff,
            )
            
            snapshots.append(snapshot)
        
        return snapshots


class UserActivitySummary(models.Model):
    """
    Daily summary of user activity
    """
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Activity counts
    complaints_created = models.IntegerField(default=0)
    complaints_updated = models.IntegerField(default=0)
    comments_added = models.IntegerField(default=0)
    withdrawals_submitted = models.IntegerField(default=0)
    feedback_submitted = models.IntegerField(default=0)
    
    # Login activity
    login_count = models.IntegerField(default=0)
    total_session_time_minutes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date', 'user__username']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} Activity - {self.date}"

