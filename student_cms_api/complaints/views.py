from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Complaint, ComplaintForward, ComplaintComment
from .serializers import (
    ComplaintListSerializer, ComplaintDetailSerializer, ComplaintCreateSerializer,
    ComplaintUpdateSerializer, ComplaintForwardCreateSerializer, ComplaintCommentCreateSerializer,
    ComplaintCommentSerializer, ComplaintCommentReplySerializer
)
from users.permissions import IsStudent, IsStaffOrAbove, IsOwnerOrStaffAbove


class ComplaintListCreateView(generics.ListCreateAPIView):
    """List and create complaints"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'department', 'assigned_to']
    search_fields = ['complaint_number', 'title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students can only see their own complaints
            return Complaint.objects.filter(created_by=user)
        elif user.role == 'staff':
            # Staff can see assigned complaints and department complaints
            return Complaint.objects.filter(
                Q(assigned_to=user) | Q(department=user.department)
            ).distinct()
        elif user.role == 'head':
            # Department heads can see all complaints in their department
            return Complaint.objects.filter(department=user.department)
        else:  # vc, admin
            # VC and Admin can see all complaints
            return Complaint.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ComplaintCreateSerializer
        return ComplaintListSerializer

    def perform_create(self, serializer):
        # Only students can create complaints
        if self.request.user.role != 'student':
            raise permissions.PermissionDenied("Only students can create complaints")
        serializer.save()


class ComplaintDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Complaint detail view"""
    queryset = Complaint.objects.all()
    permission_classes = [IsOwnerOrStaffAbove]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ComplaintUpdateSerializer
        return ComplaintDetailSerializer

    def perform_update(self, serializer):
        # Only staff and above can update complaints
        if self.request.user.role == 'student':
            raise permissions.PermissionDenied("Students cannot update complaints")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Only admin can delete complaints
        if request.user.role != 'admin':
            raise permissions.PermissionDenied("Only admin can delete complaints")
        return super().destroy(request, *args, **kwargs)


class ComplaintForwardView(generics.CreateAPIView):
    """Forward complaint to another user"""
    serializer_class = ComplaintForwardCreateSerializer
    permission_classes = [IsStaffOrAbove]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        complaint_id = self.kwargs.get('complaint_id')
        context['complaint'] = get_object_or_404(Complaint, id=complaint_id)
        return context

    def create(self, request, *args, **kwargs):
        complaint = self.get_serializer_context()['complaint']
        
        # Check if user has permission to forward this complaint
        user = request.user
        if user.role == 'staff' and complaint.assigned_to != user:
            return Response(
                {'error': 'You can only forward complaints assigned to you'},
                status=status.HTTP_403_FORBIDDEN
            )
        elif user.role == 'head' and complaint.department != user.department:
            return Response(
                {'error': 'You can only forward complaints from your department'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = super().create(request, *args, **kwargs)
        
        # Create notification for the recipient
        from notifications.utils import create_notification
        forward = ComplaintForward.objects.get(id=response.data['id'])
        create_notification(
            recipient=forward.to_user,
            message=f'Complaint {complaint.complaint_number} has been forwarded to you by {user.full_name}',
            link=f'/complaints/{complaint.id}/'
        )
        
        return response


class ComplaintCommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a complaint"""
    serializer_class = ComplaintCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        complaint_id = self.kwargs.get('complaint_id')
        return ComplaintComment.objects.filter(complaint_id=complaint_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ComplaintCommentCreateSerializer
        return ComplaintCommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        complaint_id = self.kwargs.get('complaint_id')
        context['complaint'] = get_object_or_404(Complaint, id=complaint_id)
        return context

    def create(self, request, *args, **kwargs):
        complaint = self.get_serializer_context()['complaint']
        
        # Check permissions
        user = request.user
        if user.role == 'student':
            return Response(
                {'error': 'Students cannot add comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = super().create(request, *args, **kwargs)
        
        # Create notification for complaint creator
        from notifications.utils import create_notification
        create_notification(
            recipient=complaint.created_by,
            message=f'New {request.data.get("comment_type", "comment")} added to your complaint {complaint.complaint_number}',
            link=f'/complaints/{complaint.id}/'
        )
        
        return response


class ComplaintCommentReplyView(generics.UpdateAPIView):
    """Reply to a comment (students only)"""
    queryset = ComplaintComment.objects.all()
    serializer_class = ComplaintCommentReplySerializer
    permission_classes = [IsStudent]

    def get_object(self):
        complaint_id = self.kwargs.get('complaint_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(
            ComplaintComment,
            id=comment_id,
            complaint_id=complaint_id
        )

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        
        # Check if user can reply to this comment
        user = request.user
        if user != comment.complaint.created_by:
            return Response(
                {'error': 'You can only reply to comments on your own complaints'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not comment.can_be_replied_to():
            return Response(
                {'error': 'This comment cannot be replied to or already has a reply'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Add reply
        success = comment.add_reply(serializer.validated_data['reply'], user)
        if not success:
            return Response(
                {'error': 'Failed to add reply'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification for comment author
        from notifications.utils import create_notification
        create_notification(
            recipient=comment.user,
            message=f'Student replied to your {comment.get_comment_type_display().lower()} on complaint {comment.complaint.complaint_number}',
            link=f'/complaints/{comment.complaint.id}/'
        )
        
        return Response({
            'message': 'Reply added successfully',
            'comment': ComplaintCommentSerializer(comment, context={'request': request}).data
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def complaint_by_number(request, complaint_number):
    """Get complaint by complaint number (for public tracking)"""
    try:
        complaint = Complaint.objects.get(complaint_number=complaint_number)
        
        # Check permissions
        user = request.user
        if user.role == 'student' and complaint.created_by != user:
            return Response(
                {'error': 'You can only view your own complaints'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ComplaintDetailSerializer(complaint, context={'request': request})
        return Response(serializer.data)
    
    except Complaint.DoesNotExist:
        return Response(
            {'error': 'Complaint not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def track_complaint(request, complaint_number):
    """Public complaint tracking endpoint"""
    try:
        complaint = Complaint.objects.get(complaint_number=complaint_number)
        
        # Return limited information for public tracking
        data = {
            'complaint_number': complaint.complaint_number,
            'title': complaint.title,
            'status': complaint.status,
            'status_display': complaint.get_status_display(),
            'created_at': complaint.created_at,
            'updated_at': complaint.updated_at,
        }
        
        return Response(data)
    
    except Complaint.DoesNotExist:
        return Response(
            {'error': 'Complaint not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsStaffOrAbove])
def complaint_statistics(request):
    """Get complaint statistics"""
    user = request.user
    
    # Base queryset based on user role
    if user.role == 'staff':
        queryset = Complaint.objects.filter(assigned_to=user)
    elif user.role == 'head':
        queryset = Complaint.objects.filter(department=user.department)
    else:  # vc, admin
        queryset = Complaint.objects.all()
    
    stats = {
        'total': queryset.count(),
        'pending': queryset.filter(status='pending').count(),
        'in_progress': queryset.filter(status='in_progress').count(),
        'resolved': queryset.filter(status='resolved').count(),
        'rejected': queryset.filter(status='rejected').count(),
        'not_resolved': queryset.filter(status='not_resolved').count(),
        'closed': queryset.filter(status='closed').count(),
    }
    
    # Priority breakdown
    stats['priority'] = {
        'low': queryset.filter(priority='low').count(),
        'medium': queryset.filter(priority='medium').count(),
        'high': queryset.filter(priority='high').count(),
        'urgent': queryset.filter(priority='urgent').count(),
    }
    
    return Response(stats)

