from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q, F
from datetime import timedelta, date
import calendar

from .models import AnalyticsSnapshot, DepartmentAnalytics, UserActivitySummary
from .serializers import (
    AnalyticsSnapshotSerializer, DepartmentAnalyticsSerializer,
    UserActivitySummarySerializer, DashboardStatsSerializer,
    ComplaintAnalyticsSerializer, FeedbackAnalyticsSerializer,
    UserAnalyticsSerializer, SystemPerformanceSerializer
)
from users.permissions import CanViewAnalytics, IsHeadOrAbove, IsVCOrAdmin


class AnalyticsSnapshotListView(generics.ListAPIView):
    """List analytics snapshots"""
    queryset = AnalyticsSnapshot.objects.all()
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [CanViewAnalytics]
    ordering = ['-snapshot_date']


class DepartmentAnalyticsListView(generics.ListAPIView):
    """List department analytics"""
    queryset = DepartmentAnalytics.objects.all()
    serializer_class = DepartmentAnalyticsSerializer
    permission_classes = [IsHeadOrAbove]
    ordering = ['-snapshot_date', 'department__name']

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Department heads can only see their own department
        if user.role == 'head' and user.department:
            queryset = queryset.filter(department=user.department)
        
        return queryset


@api_view(['GET'])
@permission_classes([CanViewAnalytics])
def dashboard_stats(request):
    """Get dashboard statistics"""
    from complaints.models import Complaint
    from withdrawals.models import WithdrawalRequest
    from feedback.models import ComplaintFeedback
    from users.models import User
    from logs.models import ActivityLog
    
    user = request.user
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    # Base querysets based on user role
    if user.role == 'head' and user.department:
        complaints_qs = Complaint.objects.filter(department=user.department)
        feedback_qs = ComplaintFeedback.objects.filter(complaint__department=user.department)
    elif user.role in ['vc', 'admin']:
        complaints_qs = Complaint.objects.all()
        feedback_qs = ComplaintFeedback.objects.all()
    else:
        # Staff or other roles - limited access
        complaints_qs = Complaint.objects.filter(assigned_to=user)
        feedback_qs = ComplaintFeedback.objects.filter(complaint__assigned_to=user)
    
    # Current stats
    total_complaints = complaints_qs.count()
    pending_complaints = complaints_qs.filter(status='pending').count()
    resolved_complaints = complaints_qs.filter(status='resolved').count()
    resolution_rate = (resolved_complaints / total_complaints * 100) if total_complaints > 0 else 0
    
    total_withdrawals = WithdrawalRequest.objects.count() if user.role in ['vc', 'admin'] else 0
    pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').count() if user.role in ['vc', 'admin'] else 0
    
    total_feedback = feedback_qs.count()
    average_rating = feedback_qs.aggregate(avg=Avg('rating'))['avg'] or 0.0
    
    total_users = User.objects.count() if user.role in ['vc', 'admin'] else 0
    active_users_today = ActivityLog.objects.filter(
        timestamp__date=today
    ).values('user').distinct().count() if user.role in ['vc', 'admin'] else 0
    
    # Calculate trends (compare with yesterday)
    yesterday_complaints = complaints_qs.filter(created_at__date=yesterday).count()
    today_complaints = complaints_qs.filter(created_at__date=today).count()
    complaints_trend = {
        'value': today_complaints - yesterday_complaints,
        'percentage': ((today_complaints - yesterday_complaints) / max(yesterday_complaints, 1)) * 100
    }
    
    # Resolution trend (last 7 days vs previous 7 days)
    week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)
    
    recent_resolution_rate = 0
    previous_resolution_rate = 0
    
    recent_resolved = complaints_qs.filter(
        resolved_at__date__gte=week_ago,
        resolved_at__date__lt=today
    ).count()
    recent_total = complaints_qs.filter(
        created_at__date__gte=week_ago,
        created_at__date__lt=today
    ).count()
    
    if recent_total > 0:
        recent_resolution_rate = (recent_resolved / recent_total) * 100
    
    previous_resolved = complaints_qs.filter(
        resolved_at__date__gte=two_weeks_ago,
        resolved_at__date__lt=week_ago
    ).count()
    previous_total = complaints_qs.filter(
        created_at__date__gte=two_weeks_ago,
        created_at__date__lt=week_ago
    ).count()
    
    if previous_total > 0:
        previous_resolution_rate = (previous_resolved / previous_total) * 100
    
    resolution_trend = {
        'value': recent_resolution_rate - previous_resolution_rate,
        'percentage': recent_resolution_rate - previous_resolution_rate
    }
    
    # Satisfaction trend
    recent_rating = feedback_qs.filter(
        submitted_at__date__gte=week_ago
    ).aggregate(avg=Avg('rating'))['avg'] or 0.0
    
    previous_rating = feedback_qs.filter(
        submitted_at__date__gte=two_weeks_ago,
        submitted_at__date__lt=week_ago
    ).aggregate(avg=Avg('rating'))['avg'] or 0.0
    
    satisfaction_trend = {
        'value': recent_rating - previous_rating,
        'percentage': ((recent_rating - previous_rating) / max(previous_rating, 1)) * 100
    }
    
    # Recent activity
    recent_complaints = list(complaints_qs.order_by('-created_at')[:5].values(
        'id', 'complaint_number', 'title', 'status', 'created_at'
    ))
    
    recent_feedback = list(feedback_qs.order_by('-submitted_at')[:5].values(
        'id', 'rating', 'complaint__complaint_number', 'submitted_at'
    ))
    
    stats_data = {
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'resolution_rate': round(resolution_rate, 2),
        'total_withdrawals': total_withdrawals,
        'pending_withdrawals': pending_withdrawals,
        'total_feedback': total_feedback,
        'average_rating': round(average_rating, 2),
        'total_users': total_users,
        'active_users_today': active_users_today,
        'complaints_trend': complaints_trend,
        'resolution_trend': resolution_trend,
        'satisfaction_trend': satisfaction_trend,
        'recent_complaints': recent_complaints,
        'recent_feedback': recent_feedback,
    }
    
    serializer = DashboardStatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([CanViewAnalytics])
def complaint_analytics(request):
    """Get detailed complaint analytics"""
    from complaints.models import Complaint
    
    user = request.user
    
    # Base queryset based on user role
    if user.role == 'head' and user.department:
        complaints_qs = Complaint.objects.filter(department=user.department)
    elif user.role in ['vc', 'admin']:
        complaints_qs = Complaint.objects.all()
    else:
        complaints_qs = Complaint.objects.filter(assigned_to=user)
    
    # Status distribution
    status_distribution = {}
    for status_code, status_name in Complaint.STATUS_CHOICES:
        count = complaints_qs.filter(status=status_code).count()
        status_distribution[status_code] = {
            'name': status_name,
            'count': count
        }
    
    # Priority distribution
    priority_distribution = {}
    for priority_code, priority_name in Complaint.PRIORITY_CHOICES:
        count = complaints_qs.filter(priority=priority_code).count()
        priority_distribution[priority_code] = {
            'name': priority_name,
            'count': count
        }
    
    # Department distribution (for VC and Admin)
    department_distribution = []
    if user.role in ['vc', 'admin']:
        from users.models import Department
        for dept in Department.objects.all():
            count = complaints_qs.filter(department=dept).count()
            if count > 0:
                department_distribution.append({
                    'department': dept.name,
                    'count': count
                })
    
    # Monthly trends (last 12 months)
    monthly_trends = []
    now = timezone.now()
    for i in range(12):
        month_start = now.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(
            day=calendar.monthrange(month_start.year, month_start.month)[1]
        )
        
        month_complaints = complaints_qs.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        
        monthly_trends.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%B %Y'),
            'count': month_complaints
        })
    
    monthly_trends.reverse()
    
    # Performance metrics
    resolved_complaints = complaints_qs.filter(status='resolved')
    total_complaints = complaints_qs.count()
    
    avg_resolution_time = 0.0
    if resolved_complaints.exists():
        resolution_times = []
        for complaint in resolved_complaints:
            if complaint.resolved_at and complaint.created_at:
                days = (complaint.resolved_at - complaint.created_at).days
                resolution_times.append(days)
        
        if resolution_times:
            avg_resolution_time = sum(resolution_times) / len(resolution_times)
    
    resolution_rate = (resolved_complaints.count() / total_complaints * 100) if total_complaints > 0 else 0
    
    # Escalation rate (complaints forwarded more than once)
    escalated_complaints = complaints_qs.annotate(
        forward_count=Count('forwards')
    ).filter(forward_count__gt=1).count()
    
    escalation_rate = (escalated_complaints / total_complaints * 100) if total_complaints > 0 else 0
    
    analytics_data = {
        'status_distribution': status_distribution,
        'priority_distribution': priority_distribution,
        'department_distribution': department_distribution,
        'monthly_trends': monthly_trends,
        'resolution_time_trends': [],  # Could add more detailed resolution time analysis
        'avg_resolution_time': round(avg_resolution_time, 2),
        'resolution_rate': round(resolution_rate, 2),
        'escalation_rate': round(escalation_rate, 2),
    }
    
    serializer = ComplaintAnalyticsSerializer(analytics_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsHeadOrAbove])
def feedback_analytics(request):
    """Get detailed feedback analytics"""
    from feedback.models import ComplaintFeedback
    from complaints.models import Complaint
    
    user = request.user
    
    # Base queryset based on user role
    if user.role == 'head' and user.department:
        feedback_qs = ComplaintFeedback.objects.filter(complaint__department=user.department)
        complaints_qs = Complaint.objects.filter(department=user.department)
    else:  # vc, admin
        feedback_qs = ComplaintFeedback.objects.all()
        complaints_qs = Complaint.objects.all()
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        count = feedback_qs.filter(rating=i).count()
        rating_distribution[f'{i}_star'] = count
    
    # Satisfaction trends (last 12 months)
    satisfaction_trends = []
    now = timezone.now()
    for i in range(12):
        month_start = now.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(
            day=calendar.monthrange(month_start.year, month_start.month)[1]
        )
        
        month_feedback = feedback_qs.filter(
            submitted_at__gte=month_start,
            submitted_at__lte=month_end
        )
        
        avg_rating = month_feedback.aggregate(avg=Avg('rating'))['avg'] or 0.0
        
        satisfaction_trends.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%B %Y'),
            'average_rating': round(avg_rating, 2),
            'count': month_feedback.count()
        })
    
    satisfaction_trends.reverse()
    
    # Department comparison (for VC and Admin)
    department_satisfaction = []
    if user.role in ['vc', 'admin']:
        from users.models import Department
        for dept in Department.objects.all():
            dept_feedback = feedback_qs.filter(complaint__department=dept)
            if dept_feedback.exists():
                avg_rating = dept_feedback.aggregate(avg=Avg('rating'))['avg'] or 0.0
                department_satisfaction.append({
                    'department': dept.name,
                    'average_rating': round(avg_rating, 2),
                    'feedback_count': dept_feedback.count()
                })
    
    # Response rate
    closed_complaints = complaints_qs.filter(
        status__in=['resolved', 'rejected', 'not_resolved']
    ).count()
    
    response_rate = (feedback_qs.count() / closed_complaints * 100) if closed_complaints > 0 else 0
    
    # Recent feedback highlights
    recent_positive = list(feedback_qs.filter(
        rating__gte=4
    ).order_by('-submitted_at')[:5].values(
        'rating', 'feedback_text', 'complaint__complaint_number', 'submitted_at'
    ))
    
    recent_negative = list(feedback_qs.filter(
        rating__lte=2
    ).order_by('-submitted_at')[:5].values(
        'rating', 'feedback_text', 'complaint__complaint_number', 'submitted_at'
    ))
    
    analytics_data = {
        'rating_distribution': rating_distribution,
        'satisfaction_trends': satisfaction_trends,
        'department_satisfaction': department_satisfaction,
        'response_rate': round(response_rate, 2),
        'recent_positive_feedback': recent_positive,
        'recent_negative_feedback': recent_negative,
    }
    
    serializer = FeedbackAnalyticsSerializer(analytics_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsVCOrAdmin])
def user_analytics(request):
    """Get user analytics - VC and Admin only"""
    from users.models import User
    from logs.models import ActivityLog
    
    # Role distribution
    role_distribution = {}
    for role_code, role_name in User.ROLE_CHOICES:
        count = User.objects.filter(role=role_code).count()
        role_distribution[role_code] = {
            'name': role_name,
            'count': count
        }
    
    # Most active users (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    most_active = list(
        ActivityLog.objects.filter(timestamp__gte=thirty_days_ago)
        .values('user__username', 'user__first_name', 'user__last_name', 'user__role')
        .annotate(activity_count=Count('id'))
        .order_by('-activity_count')[:10]
    )
    
    # Add full names
    for user_data in most_active:
        full_name = f"{user_data['user__first_name']} {user_data['user__last_name']}".strip()
        user_data['full_name'] = full_name or user_data['user__username']
    
    # Registration trends (last 12 months)
    registration_trends = []
    now = timezone.now()
    for i in range(12):
        month_start = now.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(
            day=calendar.monthrange(month_start.year, month_start.month)[1]
        )
        
        new_users = User.objects.filter(
            date_joined__gte=month_start,
            date_joined__lte=month_end
        ).count()
        
        registration_trends.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%B %Y'),
            'count': new_users
        })
    
    registration_trends.reverse()
    
    # Department-wise user stats
    department_user_stats = []
    from users.models import Department
    for dept in Department.objects.all():
        dept_users = User.objects.filter(department=dept)
        department_user_stats.append({
            'department': dept.name,
            'total_users': dept_users.count(),
            'staff_count': dept_users.filter(role='staff').count(),
            'student_count': dept_users.filter(role='student').count(),
        })
    
    analytics_data = {
        'role_distribution': role_distribution,
        'most_active_users': most_active,
        'user_engagement_trends': [],  # Could add more detailed engagement analysis
        'registration_trends': registration_trends,
        'department_user_stats': department_user_stats,
    }
    
    serializer = UserAnalyticsSerializer(analytics_data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsVCOrAdmin])
def generate_snapshot(request):
    """Generate analytics snapshot for a specific date"""
    from datetime import datetime
    
    date_str = request.data.get('date')
    if date_str:
        try:
            snapshot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    else:
        snapshot_date = timezone.now().date()
    
    # Generate snapshots
    snapshot = AnalyticsSnapshot.create_daily_snapshot(snapshot_date)
    dept_snapshots = DepartmentAnalytics.create_department_snapshots(snapshot_date)
    
    return Response({
        'message': f'Analytics snapshot generated for {snapshot_date}',
        'snapshot_id': snapshot.id,
        'department_snapshots_created': len(dept_snapshots),
    })

