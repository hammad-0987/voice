from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Permission class for students only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsStaff(permissions.BasePermission):
    """Permission class for staff only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'staff'


class IsDepartmentHead(permissions.BasePermission):
    """Permission class for department heads only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'head'


class IsVC(permissions.BasePermission):
    """Permission class for VC only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vc'


class IsAdmin(permissions.BasePermission):
    """Permission class for admin only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsStaffOrAbove(permissions.BasePermission):
    """Permission class for staff, head, vc, or admin"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['staff', 'head', 'vc', 'admin'])


class IsHeadOrAbove(permissions.BasePermission):
    """Permission class for head, vc, or admin"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['head', 'vc', 'admin'])


class IsVCOrAdmin(permissions.BasePermission):
    """Permission class for VC or admin only"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['vc', 'admin'])


class CanForwardComplaints(permissions.BasePermission):
    """Permission class for users who can forward complaints"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['staff', 'head', 'vc', 'admin'])


class CanManageUsers(permissions.BasePermission):
    """Permission class for users who can manage other users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrStaffAbove(permissions.BasePermission):
    """Permission class for object owner or staff and above"""
    
    def has_object_permission(self, request, view, obj):
        # Owner can always access
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        elif hasattr(obj, 'submitted_by') and obj.submitted_by == request.user:
            return True
        elif hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # Staff and above can access
        return request.user.role in ['staff', 'head', 'vc', 'admin']


class CanViewAnalytics(permissions.BasePermission):
    """Permission class for users who can view analytics"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['head', 'vc', 'admin'])


class CanViewLogs(permissions.BasePermission):
    """Permission class for users who can view activity logs"""
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['vc', 'admin'])

