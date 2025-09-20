from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, Department
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, PasswordChangeSerializer, DepartmentSerializer
)
from .permissions import IsAdmin, CanManageUsers


class UserRegistrationView(generics.CreateAPIView):
    """Student registration endpoint - only students can self-register"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """User login endpoint"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view and update"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """Password change endpoint"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Keep user logged in after password change
        update_session_auth_hash(request, user)
        
        return Response({'message': 'Password changed successfully'})


class UserListView(generics.ListCreateAPIView):
    """List and create users - Admin only"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanManageUsers]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'department', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'student_id', 'employee_id']
    ordering_fields = ['username', 'first_name', 'last_name', 'date_joined']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        """Admin can create users with any role"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Admin can set any role
        role = request.data.get('role', 'student')
        if role not in ['student', 'staff', 'head', 'vc', 'admin']:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save(role=role)
        
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User detail view - Admin only"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanManageUsers]

    def destroy(self, request, *args, **kwargs):
        """Soft delete user by setting is_active to False"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})


class DepartmentListView(generics.ListCreateAPIView):
    """List and create departments"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    ordering = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Department detail view"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdmin]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """Logout endpoint - blacklist refresh token"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout successful'})
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_stats(request):
    """Get dashboard statistics for current user"""
    user = request.user
    
    stats = {
        'role': user.role,
        'department': user.department.name if user.department else None,
    }
    
    # Add role-specific stats
    if user.role == 'student':
        from complaints.models import Complaint
        stats.update({
            'total_complaints': Complaint.objects.filter(created_by=user).count(),
            'pending_complaints': Complaint.objects.filter(created_by=user, status='pending').count(),
            'resolved_complaints': Complaint.objects.filter(created_by=user, status='resolved').count(),
        })
    elif user.role in ['staff', 'head', 'vc', 'admin']:
        from complaints.models import Complaint
        from withdrawals.models import WithdrawalRequest
        
        if user.role == 'staff':
            complaints_qs = Complaint.objects.filter(assigned_to=user)
        elif user.role == 'head':
            complaints_qs = Complaint.objects.filter(department=user.department)
        else:  # vc, admin
            complaints_qs = Complaint.objects.all()
        
        stats.update({
            'total_complaints': complaints_qs.count(),
            'pending_complaints': complaints_qs.filter(status='pending').count(),
            'in_progress_complaints': complaints_qs.filter(status='in_progress').count(),
            'pending_withdrawals': WithdrawalRequest.objects.filter(status='pending').count(),
        })
    
    return Response(stats)

