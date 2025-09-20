from rest_framework import serializers
from django.utils import timezone
from .models import Complaint, ComplaintForward, ComplaintComment, ComplaintResponse
from users.serializers import UserSerializer


class ComplaintForwardSerializer(serializers.ModelSerializer):
    from_user_name = serializers.CharField(source='from_user.full_name', read_only=True)
    to_user_name = serializers.CharField(source='to_user.full_name', read_only=True)
    
    class Meta:
        model = ComplaintForward
        fields = ['id', 'from_user', 'from_user_name', 'to_user', 'to_user_name', 'remarks', 'created_at']
        read_only_fields = ['id', 'from_user', 'created_at']


class ComplaintCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    can_reply = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintComment
        fields = [
            'id', 'user', 'user_name', 'user_role', 'comment_type', 'text',
            'reply', 'replied_at', 'created_at', 'can_reply'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'replied_at']
    
    def get_can_reply(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        # Only the complaint creator (student) can reply
        user = request.user
        return (user.role == 'student' and 
                user == obj.complaint.created_by and 
                obj.can_be_replied_to())


class ComplaintCommentReplySerializer(serializers.Serializer):
    reply = serializers.CharField(max_length=1000)
    
    def validate_reply(self, value):
        if not value.strip():
            raise serializers.ValidationError("Reply cannot be empty")
        return value.strip()


class ComplaintResponseSerializer(serializers.ModelSerializer):
    added_by_name = serializers.CharField(source='added_by.full_name', read_only=True)
    
    class Meta:
        model = ComplaintResponse
        fields = ['id', 'message', 'added_by', 'added_by_name', 'created_at']
        read_only_fields = ['id', 'added_by', 'created_at']


class ComplaintListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'complaint_number', 'title', 'priority', 'priority_display',
            'status', 'status_display', 'created_by', 'created_by_name',
            'assigned_to', 'assigned_to_name', 'department', 'department_name',
            'created_at', 'updated_at'
        ]


class ComplaintDetailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    # Related data
    forwards = ComplaintForwardSerializer(many=True, read_only=True)
    comments = ComplaintCommentSerializer(many=True, read_only=True)
    responses = ComplaintResponseSerializer(many=True, read_only=True)
    
    # Computed fields
    is_closed = serializers.BooleanField(read_only=True)
    can_receive_feedback = serializers.BooleanField(read_only=True)
    timeline = serializers.SerializerMethodField()
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'complaint_number', 'title', 'description', 'priority', 'priority_display',
            'status', 'status_display', 'created_by', 'created_by_name',
            'assigned_to', 'assigned_to_name', 'department', 'department_name',
            'attachment', 'created_at', 'updated_at', 'resolved_at', 'closed_at',
            'is_closed', 'can_receive_feedback', 'forwards', 'comments', 'responses', 'timeline'
        ]
    
    def get_timeline(self, obj):
        return obj.get_timeline()


class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'priority', 'department', 'attachment']
    
    def validate_title(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters long")
        return value.strip()
    
    def validate_description(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Description must be at least 20 characters long")
        return value.strip()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['status', 'assigned_to', 'priority']
    
    def validate_status(self, value):
        # Only certain roles can change status to certain values
        user = self.context['request'].user
        current_status = self.instance.status if self.instance else None
        
        # Students cannot change status
        if user.role == 'student':
            raise serializers.ValidationError("Students cannot change complaint status")
        
        # Validate status transitions
        valid_transitions = {
            'pending': ['in_progress', 'rejected'],
            'in_progress': ['resolved', 'not_resolved', 'rejected'],
            'resolved': ['closed'],
            'rejected': ['closed'],
            'not_resolved': ['closed', 'in_progress'],
            'closed': []  # Cannot change from closed
        }
        
        if current_status and value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(f"Cannot change status from {current_status} to {value}")
        
        return value
    
    def validate_assigned_to(self, value):
        # Cannot assign to students
        if value and value.role == 'student':
            raise serializers.ValidationError("Cannot assign complaints to students")
        return value


class ComplaintForwardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintForward
        fields = ['to_user', 'remarks']
    
    def validate_to_user(self, value):
        user = self.context['request'].user
        
        # Check if user can forward to this person
        if not user.can_forward_to(value):
            raise serializers.ValidationError("You cannot forward complaints to this user")
        
        return value
    
    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        validated_data['complaint'] = self.context['complaint']
        
        # Update complaint assignment
        complaint = validated_data['complaint']
        complaint.assigned_to = validated_data['to_user']
        complaint.save()
        
        return super().create(validated_data)


class ComplaintCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintComment
        fields = ['comment_type', 'text']
    
    def validate_comment_type(self, value):
        user = self.context['request'].user
        
        # Only staff and above can add comments
        if user.role == 'student':
            raise serializers.ValidationError("Students cannot add comments")
        
        return value
    
    def validate_text(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters long")
        return value.strip()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['complaint'] = self.context['complaint']
        return super().create(validated_data)

