from rest_framework import serializers
from .models import ComplaintFeedback, FeedbackResponse
from complaints.serializers import ComplaintListSerializer


class FeedbackResponseSerializer(serializers.ModelSerializer):
    responded_by_name = serializers.CharField(source='responded_by.full_name', read_only=True)
    responded_by_role = serializers.CharField(source='responded_by.role', read_only=True)
    
    class Meta:
        model = FeedbackResponse
        fields = [
            'id', 'response_text', 'responded_by', 'responded_by_name', 
            'responded_by_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'responded_by', 'created_at', 'updated_at']


class ComplaintFeedbackListSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    complaint_number = serializers.CharField(source='complaint.complaint_number', read_only=True)
    complaint_title = serializers.CharField(source='complaint.title', read_only=True)
    complaint_status = serializers.CharField(source='complaint.status', read_only=True)
    rating_stars = serializers.CharField(read_only=True)
    rating_percentage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ComplaintFeedback
        fields = [
            'id', 'complaint', 'complaint_number', 'complaint_title', 'complaint_status',
            'rating', 'rating_stars', 'rating_percentage', 'submitted_by', 'submitted_by_name',
            'submitted_at'
        ]


class ComplaintFeedbackDetailSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    complaint_details = ComplaintListSerializer(source='complaint', read_only=True)
    rating_stars = serializers.CharField(read_only=True)
    rating_percentage = serializers.FloatField(read_only=True)
    responses = FeedbackResponseSerializer(many=True, read_only=True)
    forwarded_to_names = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintFeedback
        fields = [
            'id', 'complaint', 'complaint_details', 'feedback_text', 'rating', 
            'rating_stars', 'rating_percentage', 'submitted_by', 'submitted_by_name',
            'forwarded_to_names', 'submitted_at', 'updated_at', 'responses'
        ]
    
    def get_forwarded_to_names(self, obj):
        return [user.full_name for user in obj.forwarded_to.all()]


class ComplaintFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintFeedback
        fields = ['complaint', 'feedback_text', 'rating']
    
    def validate_complaint(self, value):
        # Check if complaint can receive feedback
        if not value.can_receive_feedback:
            raise serializers.ValidationError(
                "Feedback can only be submitted for resolved, rejected, or not resolved complaints"
            )
        
        # Check if feedback already exists
        if hasattr(value, 'feedback'):
            raise serializers.ValidationError(
                "Feedback has already been submitted for this complaint"
            )
        
        # Check if user is the complaint creator
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError(
                "You can only submit feedback for your own complaints"
            )
        
        return value
    
    def validate_feedback_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Feedback must be at least 10 characters long"
            )
        return value.strip()
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )
        return value
    
    def create(self, validated_data):
        validated_data['submitted_by'] = self.context['request'].user
        return super().create(validated_data)


class ComplaintFeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintFeedback
        fields = ['feedback_text', 'rating']
    
    def validate_feedback_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Feedback must be at least 10 characters long"
            )
        return value.strip()
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )
        return value


class FeedbackResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = ['response_text']
    
    def validate_response_text(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Response must be at least 5 characters long"
            )
        return value.strip()
    
    def create(self, validated_data):
        validated_data['responded_by'] = self.context['request'].user
        validated_data['feedback'] = self.context['feedback']
        return super().create(validated_data)

