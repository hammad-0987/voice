from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .models import WithdrawalRequest
from .serializers import (
    WithdrawalRequestListSerializer, WithdrawalRequestDetailSerializer,
    WithdrawalRequestCreateSerializer, WithdrawalRequestUpdateSerializer,
    WithdrawalRequestReviewSerializer
)
from users.permissions import IsStudent, IsHeadOrAbove, IsStaffOrAbove


class WithdrawalRequestListCreateView(generics.ListCreateAPIView):
    """List and create withdrawal requests"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'submitted_by']
    search_fields = ['request_number', 'reason']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students can only see their own withdrawal requests
            return WithdrawalRequest.objects.filter(submitted_by=user)
        else:
            # Staff, Head, VC, Admin can see all withdrawal requests
            return WithdrawalRequest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WithdrawalRequestCreateSerializer
        return WithdrawalRequestListSerializer

    def perform_create(self, serializer):
        # Only students can create withdrawal requests
        if self.request.user.role != 'student':
            raise permissions.PermissionDenied("Only students can create withdrawal requests")
        
        withdrawal_request = serializer.save()
        
        # Create notification for staff/admin
        from notifications.utils import create_notification
        from users.models import User
        
        # Notify all heads, VCs, and admins
        recipients = User.objects.filter(role__in=['head', 'vc', 'admin'])
        for recipient in recipients:
            create_notification(
                recipient=recipient,
                message=f'New withdrawal request {withdrawal_request.request_number} submitted by {withdrawal_request.submitted_by.full_name}',
                link=f'/withdrawals/{withdrawal_request.id}/'
            )


class WithdrawalRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Withdrawal request detail view"""
    queryset = WithdrawalRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        # Check if user can view this withdrawal request
        if not obj.can_be_viewed_by(user):
            raise permissions.PermissionDenied("You don't have permission to view this withdrawal request")
        
        return obj

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WithdrawalRequestUpdateSerializer
        return WithdrawalRequestDetailSerializer

    def perform_update(self, serializer):
        # Only the student who submitted can update (and only if pending)
        user = self.request.user
        withdrawal_request = self.get_object()
        
        if user.role != 'student' or withdrawal_request.submitted_by != user:
            raise permissions.PermissionDenied("You can only update your own withdrawal requests")
        
        if withdrawal_request.status != 'pending':
            raise permissions.PermissionDenied("Cannot update a reviewed withdrawal request")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Only the student who submitted can delete (and only if pending)
        user = request.user
        withdrawal_request = self.get_object()
        
        if user.role != 'student' or withdrawal_request.submitted_by != user:
            raise permissions.PermissionDenied("You can only delete your own withdrawal requests")
        
        if withdrawal_request.status != 'pending':
            raise permissions.PermissionDenied("Cannot delete a reviewed withdrawal request")
        
        return super().destroy(request, *args, **kwargs)


class WithdrawalRequestReviewView(generics.GenericAPIView):
    """Review (approve/reject) withdrawal request"""
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestReviewSerializer
    permission_classes = [IsHeadOrAbove]

    def post(self, request, *args, **kwargs):
        withdrawal_request = self.get_object()
        user = request.user
        
        # Check if user can review this request
        if not withdrawal_request.can_be_reviewed_by(user):
            return Response(
                {'error': 'You do not have permission to review this withdrawal request'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if request is still pending
        if not withdrawal_request.is_pending:
            return Response(
                {'error': 'This withdrawal request has already been reviewed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action = serializer.validated_data['action']
        response_text = serializer.validated_data.get('response', '')
        
        # Perform the action
        if action == 'approve':
            success = withdrawal_request.approve(user, response_text)
            message = 'Withdrawal request approved successfully'
        else:  # reject
            success = withdrawal_request.reject(user, response_text)
            message = 'Withdrawal request rejected successfully'
        
        if not success:
            return Response(
                {'error': 'Failed to process the withdrawal request'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification for the student
        from notifications.utils import create_notification
        create_notification(
            recipient=withdrawal_request.submitted_by,
            message=f'Your withdrawal request {withdrawal_request.request_number} has been {action}d',
            link=f'/withdrawals/{withdrawal_request.id}/'
        )
        
        return Response({
            'message': message,
            'withdrawal_request': WithdrawalRequestDetailSerializer(
                withdrawal_request, 
                context={'request': request}
            ).data
        })


@api_view(['GET'])
@permission_classes([IsStaffOrAbove])
def withdrawal_statistics(request):
    """Get withdrawal request statistics"""
    user = request.user
    
    # All staff and above can see all withdrawal statistics
    queryset = WithdrawalRequest.objects.all()
    
    stats = {
        'total': queryset.count(),
        'pending': queryset.filter(status='pending').count(),
        'approved': queryset.filter(status='approved').count(),
        'rejected': queryset.filter(status='rejected').count(),
    }
    
    # Type breakdown
    stats['types'] = {}
    for type_code, type_name in WithdrawalRequest.TYPE_CHOICES:
        stats['types'][type_code] = {
            'name': type_name,
            'count': queryset.filter(type=type_code).count()
        }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_withdrawal_requests(request):
    """Get current user's withdrawal requests"""
    user = request.user
    
    if user.role != 'student':
        return Response(
            {'error': 'Only students can access this endpoint'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    requests = WithdrawalRequest.objects.filter(submitted_by=user)
    serializer = WithdrawalRequestListSerializer(requests, many=True)
    
    return Response({
        'count': requests.count(),
        'results': serializer.data
    })

