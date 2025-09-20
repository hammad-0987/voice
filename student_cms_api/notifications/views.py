from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta

from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer,
    NotificationMarkReadSerializer, NotificationStatsSerializer
)
from .utils import mark_all_as_read, get_unread_count


class NotificationListView(generics.ListAPIView):
    """List user's notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """Notification detail view - mainly for marking as read"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        # Only allow updating is_read field
        notification = self.get_object()
        if 'is_read' in self.request.data:
            if self.request.data['is_read'] and not notification.is_read:
                notification.mark_as_read()
            elif not self.request.data['is_read'] and notification.is_read:
                notification.mark_as_unread()


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """User notification preferences"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return NotificationPreference.get_or_create_for_user(self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notifications_read(request):
    """Mark notifications as read"""
    serializer = NotificationMarkReadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    notification_ids = serializer.validated_data.get('notification_ids', [])
    user = request.user
    
    if notification_ids:
        # Mark specific notifications as read
        notifications = Notification.objects.filter(
            id__in=notification_ids,
            recipient=user,
            is_read=False
        )
        
        count = 0
        for notification in notifications:
            notification.mark_as_read()
            count += 1
        
        message = f"Marked {count} notifications as read"
    else:
        # Mark all notifications as read
        count = mark_all_as_read(user)
        message = f"Marked all {count} notifications as read"
    
    return Response({
        'message': message,
        'marked_count': count,
        'unread_count': get_unread_count(user)
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_notification(request, notification_id):
    """Delete a specific notification"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.delete()
        
        return Response({
            'message': 'Notification deleted successfully',
            'unread_count': get_unread_count(request.user)
        })
    
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_all_read_notifications(request):
    """Delete all read notifications for the user"""
    user = request.user
    
    deleted_count = Notification.objects.filter(
        recipient=user,
        is_read=True
    ).delete()[0]
    
    return Response({
        'message': f'Deleted {deleted_count} read notifications',
        'deleted_count': deleted_count,
        'unread_count': get_unread_count(user)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """Get notification statistics for the user"""
    user = request.user
    
    # Get all notifications for the user
    all_notifications = Notification.objects.filter(recipient=user)
    
    # Calculate stats
    total_count = all_notifications.count()
    unread_count = all_notifications.filter(is_read=False).count()
    read_count = total_count - unread_count
    
    # Recent notifications (last 24 hours)
    recent_cutoff = timezone.now() - timedelta(hours=24)
    recent_count = all_notifications.filter(created_at__gte=recent_cutoff).count()
    
    # Breakdown by type
    complaint_count = all_notifications.filter(
        notification_type__in=[
            'complaint_created', 'complaint_forwarded', 
            'complaint_status_changed', 'comment_added', 'reply_added'
        ]
    ).count()
    
    withdrawal_count = all_notifications.filter(
        notification_type__in=['withdrawal_submitted', 'withdrawal_reviewed']
    ).count()
    
    feedback_count = all_notifications.filter(
        notification_type__in=['feedback_submitted', 'feedback_response']
    ).count()
    
    system_count = all_notifications.filter(
        notification_type='system'
    ).count()
    
    stats_data = {
        'total_notifications': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
        'recent_count': recent_count,
        'complaint_notifications': complaint_count,
        'withdrawal_notifications': withdrawal_count,
        'feedback_notifications': feedback_count,
        'system_notifications': system_count,
    }
    
    serializer = NotificationStatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications(request):
    """Get only unread notifications"""
    user = request.user
    
    unread_notifications = Notification.objects.filter(
        recipient=user,
        is_read=False
    ).order_by('-created_at')
    
    # Limit to recent unread notifications for performance
    limit = int(request.GET.get('limit', 20))
    unread_notifications = unread_notifications[:limit]
    
    serializer = NotificationSerializer(unread_notifications, many=True)
    
    return Response({
        'count': get_unread_count(user),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_notifications(request):
    """Get recent notifications (last 7 days)"""
    user = request.user
    
    # Get notifications from last 7 days
    recent_cutoff = timezone.now() - timedelta(days=7)
    recent_notifications = Notification.objects.filter(
        recipient=user,
        created_at__gte=recent_cutoff
    ).order_by('-created_at')
    
    # Limit results
    limit = int(request.GET.get('limit', 50))
    recent_notifications = recent_notifications[:limit]
    
    serializer = NotificationSerializer(recent_notifications, many=True)
    
    return Response({
        'count': recent_notifications.count(),
        'results': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_notification(request):
    """Create a test notification (for development/testing)"""
    from .utils import create_notification
    
    # Only allow in debug mode
    from django.conf import settings
    if not settings.DEBUG:
        return Response(
            {'error': 'Test notifications only available in debug mode'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user = request.user
    message = request.data.get('message', 'This is a test notification')
    title = request.data.get('title', 'Test Notification')
    notification_type = request.data.get('type', 'system')
    
    notification = create_notification(
        recipient=user,
        message=message,
        title=title,
        notification_type=notification_type,
        send_email=False  # Don't send email for test notifications
    )
    
    serializer = NotificationSerializer(notification)
    return Response({
        'message': 'Test notification created',
        'notification': serializer.data
    })

