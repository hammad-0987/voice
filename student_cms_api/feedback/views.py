from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count

from .models import ComplaintFeedback, FeedbackResponse
from .serializers import (
    ComplaintFeedbackListSerializer, ComplaintFeedbackDetailSerializer,
    ComplaintFeedbackCreateSerializer, ComplaintFeedbackUpdateSerializer,
    FeedbackResponseCreateSerializer, FeedbackResponseSerializer
)
from users.permissions import IsStudent, IsHeadOrAbove, IsStaffOrAbove


class ComplaintFeedbackListCreateView(generics.ListCreateAPIView):
    """List and create complaint feedback"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'complaint__status', 'complaint__department']
    search_fields = ['feedback_text', 'complaint__complaint_number', 'complaint__title']
    ordering_fields = ['submitted_at', 'rating']
    ordering = ['-submitted_at']

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students can only see their own feedback
            return ComplaintFeedback.objects.filter(submitted_by=user)
        elif user.role == 'staff':
            # Staff can see feedback for complaints they handled
            return ComplaintFeedback.objects.filter(
                Q(complaint__assigned_to=user) | Q(complaint__created_by=user)
            ).distinct()
        elif user.role == 'head':
            # Department heads can see feedback for their department
            return ComplaintFeedback.objects.filter(
                complaint__department=user.department
            )
        else:  # vc, admin
            # VC and Admin can see all feedback
            return ComplaintFeedback.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ComplaintFeedbackCreateSerializer
        return ComplaintFeedbackListSerializer

    def perform_create(self, serializer):
        # Only students can create feedback
        if self.request.user.role != 'student':
            raise permissions.PermissionDenied("Only students can submit feedback")
        serializer.save()


class ComplaintFeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Complaint feedback detail view"""
    queryset = ComplaintFeedback.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Check if user can view this feedback
        if not obj.can_be_viewed_by(user):
            raise permissions.PermissionDenied("You don't have permission to view this feedback")
        
        return obj

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ComplaintFeedbackUpdateSerializer
        return ComplaintFeedbackDetailSerializer

    def perform_update(self, serializer):
        # Only the student who submitted can update
        user = self.request.user
        feedback = self.get_object()
        
        if not feedback.can_be_edited_by(user):
            raise permissions.PermissionDenied("You can only edit your own feedback")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Only the student who submitted can delete
        user = request.user
        feedback = self.get_object()
        
        if not feedback.can_be_edited_by(user):
            raise permissions.PermissionDenied("You can only delete your own feedback")
        
        return super().destroy(request, *args, **kwargs)


class FeedbackResponseListCreateView(generics.ListCreateAPIView):
    """List and create responses to feedback"""
    permission_classes = [IsHeadOrAbove]
    serializer_class = FeedbackResponseSerializer

    def get_queryset(self):
        feedback_id = self.kwargs.get('feedback_id')
        return FeedbackResponse.objects.filter(feedback_id=feedback_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FeedbackResponseCreateSerializer
        return FeedbackResponseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        feedback_id = self.kwargs.get('feedback_id')
        context['feedback'] = get_object_or_404(ComplaintFeedback, id=feedback_id)
        return context

    def create(self, request, *args, **kwargs):
        feedback = self.get_serializer_context()['feedback']
        
        # Check if user can respond to this feedback
        user = request.user
        if not feedback.can_be_viewed_by(user) or user.role not in ['head', 'vc', 'admin']:
            return Response(
                {'error': 'You do not have permission to respond to this feedback'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_feedback(request):
    """Get current user's feedback"""
    user = request.user
    
    if user.role != 'student':
        return Response(
            {'error': 'Only students can access this endpoint'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    feedback = ComplaintFeedback.objects.filter(submitted_by=user)
    serializer = ComplaintFeedbackListSerializer(feedback, many=True)
    
    return Response({
        'count': feedback.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsHeadOrAbove])
def feedback_statistics(request):
    """Get feedback statistics"""
    user = request.user
    
    # Base queryset based on user role
    if user.role == 'head':
        queryset = ComplaintFeedback.objects.filter(complaint__department=user.department)
    else:  # vc, admin
        queryset = ComplaintFeedback.objects.all()
    
    # Basic stats
    total_feedback = queryset.count()
    avg_rating = queryset.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[f'{i}_star'] = queryset.filter(rating=i).count()
    
    # Department-wise stats (for VC and Admin)
    department_stats = []
    if user.role in ['vc', 'admin']:
        from users.models import Department
        departments = Department.objects.all()
        
        for dept in departments:
            dept_feedback = queryset.filter(complaint__department=dept)
            if dept_feedback.exists():
                department_stats.append({
                    'department': dept.name,
                    'total_feedback': dept_feedback.count(),
                    'avg_rating': dept_feedback.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
                })
    
    # Recent feedback trends (last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_feedback = queryset.filter(submitted_at__gte=thirty_days_ago)
    
    stats = {
        'total_feedback': total_feedback,
        'average_rating': round(avg_rating, 2),
        'rating_distribution': rating_distribution,
        'recent_feedback_count': recent_feedback.count(),
        'recent_average_rating': round(
            recent_feedback.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0, 2
        ),
        'department_stats': department_stats,
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsStaffOrAbove])
def feedback_analytics(request):
    """Get detailed feedback analytics"""
    user = request.user
    
    # Base queryset based on user role
    if user.role == 'staff':
        queryset = ComplaintFeedback.objects.filter(
            Q(complaint__assigned_to=user) | Q(complaint__created_by=user)
        ).distinct()
    elif user.role == 'head':
        queryset = ComplaintFeedback.objects.filter(complaint__department=user.department)
    else:  # vc, admin
        queryset = ComplaintFeedback.objects.all()
    
    # Time-based analytics
    from django.utils import timezone
    from datetime import timedelta
    import calendar
    
    now = timezone.now()
    
    # Monthly feedback count for the last 12 months
    monthly_data = []
    for i in range(12):
        month_start = now.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        
        month_feedback = queryset.filter(
            submitted_at__gte=month_start,
            submitted_at__lte=month_end
        )
        
        monthly_data.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%B %Y'),
            'count': month_feedback.count(),
            'avg_rating': round(
                month_feedback.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0, 2
            )
        })
    
    monthly_data.reverse()  # Show oldest to newest
    
    # Satisfaction levels
    satisfaction_levels = {
        'very_satisfied': queryset.filter(rating=5).count(),  # 5 stars
        'satisfied': queryset.filter(rating=4).count(),       # 4 stars
        'neutral': queryset.filter(rating=3).count(),         # 3 stars
        'dissatisfied': queryset.filter(rating=2).count(),    # 2 stars
        'very_dissatisfied': queryset.filter(rating=1).count(), # 1 star
    }
    
    analytics = {
        'monthly_trends': monthly_data,
        'satisfaction_levels': satisfaction_levels,
        'total_responses': queryset.count(),
        'response_rate': 0,  # Would need to calculate based on total closed complaints
    }
    
    # Calculate response rate if possible
    from complaints.models import Complaint
    if user.role == 'head':
        total_closed = Complaint.objects.filter(
            department=user.department,
            status__in=['resolved', 'rejected', 'not_resolved']
        ).count()
    elif user.role in ['vc', 'admin']:
        total_closed = Complaint.objects.filter(
            status__in=['resolved', 'rejected', 'not_resolved']
        ).count()
    else:
        total_closed = 0
    
    if total_closed > 0:
        analytics['response_rate'] = round((queryset.count() / total_closed) * 100, 2)
    
    return Response(analytics)

