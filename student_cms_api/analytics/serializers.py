from rest_framework import serializers
from .models import AnalyticsSnapshot, DepartmentAnalytics, UserActivitySummary


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    resolution_rate = serializers.SerializerMethodField()
    satisfaction_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyticsSnapshot
        fields = [
            'id', 'snapshot_date', 'total_complaints', 'pending_complaints',
            'in_progress_complaints', 'resolved_complaints', 'rejected_complaints',
            'not_resolved_complaints', 'closed_complaints', 'new_complaints_today',
            'total_withdrawals', 'pending_withdrawals', 'approved_withdrawals',
            'rejected_withdrawals', 'new_withdrawals_today', 'total_feedback',
            'average_rating', 'new_feedback_today', 'total_users', 'active_users_today',
            'new_users_today', 'avg_resolution_time_days', 'resolution_rate',
            'satisfaction_rate', 'created_at'
        ]
    
    def get_resolution_rate(self, obj):
        """Calculate resolution rate percentage"""
        if obj.total_complaints == 0:
            return 0.0
        return round((obj.resolved_complaints / obj.total_complaints) * 100, 2)
    
    def get_satisfaction_rate(self, obj):
        """Calculate satisfaction rate based on average rating"""
        if obj.average_rating == 0:
            return 0.0
        return round((obj.average_rating / 5.0) * 100, 2)


class DepartmentAnalyticsSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    resolution_rate = serializers.SerializerMethodField()
    satisfaction_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = DepartmentAnalytics
        fields = [
            'id', 'department', 'department_name', 'department_code', 'snapshot_date',
            'total_complaints', 'pending_complaints', 'resolved_complaints',
            'avg_resolution_time_days', 'total_feedback', 'average_rating',
            'active_staff_count', 'resolution_rate', 'satisfaction_rate', 'created_at'
        ]
    
    def get_resolution_rate(self, obj):
        """Calculate resolution rate percentage"""
        if obj.total_complaints == 0:
            return 0.0
        return round((obj.resolved_complaints / obj.total_complaints) * 100, 2)
    
    def get_satisfaction_rate(self, obj):
        """Calculate satisfaction rate based on average rating"""
        if obj.average_rating == 0:
            return 0.0
        return round((obj.average_rating / 5.0) * 100, 2)


class UserActivitySummarySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    total_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = UserActivitySummary
        fields = [
            'id', 'user', 'user_name', 'user_role', 'date', 'complaints_created',
            'complaints_updated', 'comments_added', 'withdrawals_submitted',
            'feedback_submitted', 'login_count', 'total_session_time_minutes',
            'total_activities', 'created_at'
        ]
    
    def get_total_activities(self, obj):
        """Calculate total activities for the day"""
        return (obj.complaints_created + obj.complaints_updated + 
                obj.comments_added + obj.withdrawals_submitted + 
                obj.feedback_submitted)


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    
    # Overview stats
    total_complaints = serializers.IntegerField()
    pending_complaints = serializers.IntegerField()
    resolved_complaints = serializers.IntegerField()
    resolution_rate = serializers.FloatField()
    
    total_withdrawals = serializers.IntegerField()
    pending_withdrawals = serializers.IntegerField()
    
    total_feedback = serializers.IntegerField()
    average_rating = serializers.FloatField()
    
    total_users = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    
    # Trends (compared to previous period)
    complaints_trend = serializers.DictField()
    resolution_trend = serializers.DictField()
    satisfaction_trend = serializers.DictField()
    
    # Recent activity
    recent_complaints = serializers.ListField()
    recent_feedback = serializers.ListField()


class ComplaintAnalyticsSerializer(serializers.Serializer):
    """Serializer for complaint analytics"""
    
    # Status distribution
    status_distribution = serializers.DictField()
    
    # Priority distribution
    priority_distribution = serializers.DictField()
    
    # Department distribution
    department_distribution = serializers.ListField()
    
    # Time-based analytics
    monthly_trends = serializers.ListField()
    resolution_time_trends = serializers.ListField()
    
    # Performance metrics
    avg_resolution_time = serializers.FloatField()
    resolution_rate = serializers.FloatField()
    escalation_rate = serializers.FloatField()


class FeedbackAnalyticsSerializer(serializers.Serializer):
    """Serializer for feedback analytics"""
    
    # Rating distribution
    rating_distribution = serializers.DictField()
    
    # Satisfaction trends
    satisfaction_trends = serializers.ListField()
    
    # Department comparison
    department_satisfaction = serializers.ListField()
    
    # Response rate
    response_rate = serializers.FloatField()
    
    # Recent feedback highlights
    recent_positive_feedback = serializers.ListField()
    recent_negative_feedback = serializers.ListField()


class UserAnalyticsSerializer(serializers.Serializer):
    """Serializer for user analytics"""
    
    # User distribution by role
    role_distribution = serializers.DictField()
    
    # Activity metrics
    most_active_users = serializers.ListField()
    user_engagement_trends = serializers.ListField()
    
    # Registration trends
    registration_trends = serializers.ListField()
    
    # Department-wise user stats
    department_user_stats = serializers.ListField()


class SystemPerformanceSerializer(serializers.Serializer):
    """Serializer for system performance metrics"""
    
    # Response times
    avg_response_time = serializers.FloatField()
    response_time_trends = serializers.ListField()
    
    # System usage
    daily_active_users = serializers.IntegerField()
    peak_usage_hours = serializers.ListField()
    
    # Error rates
    error_rate = serializers.FloatField()
    error_trends = serializers.ListField()
    
    # Popular features
    feature_usage = serializers.DictField()

