from rest_framework import serializers
from .models import WithdrawalRequest


class WithdrawalRequestListSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = [
            'id', 'request_number', 'type', 'type_display', 'status', 'status_display',
            'submitted_by', 'submitted_by_name', 'reviewed_by', 'reviewed_by_name',
            'created_at', 'reviewed_at'
        ]


class WithdrawalRequestDetailSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    # Computed fields
    is_pending = serializers.BooleanField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    is_rejected = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = [
            'id', 'request_number', 'type', 'type_display', 'reason', 'status', 'status_display',
            'submitted_by', 'submitted_by_name', 'reviewed_by', 'reviewed_by_name',
            'response', 'supporting_document', 'created_at', 'updated_at', 'reviewed_at',
            'is_pending', 'is_approved', 'is_rejected'
        ]


class WithdrawalRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['type', 'reason', 'supporting_document']
    
    def validate_reason(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Reason must be at least 20 characters long")
        return value.strip()
    
    def create(self, validated_data):
        validated_data['submitted_by'] = self.context['request'].user
        return super().create(validated_data)


class WithdrawalRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['type', 'reason', 'supporting_document']
    
    def validate_reason(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Reason must be at least 20 characters long")
        return value.strip()
    
    def validate(self, attrs):
        # Only allow updates if request is still pending
        if self.instance and self.instance.status != 'pending':
            raise serializers.ValidationError("Cannot update a reviewed withdrawal request")
        return attrs


class WithdrawalRequestReviewSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    response = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    
    def validate_response(self, value):
        if value:
            return value.strip()
        return value

