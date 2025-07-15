from rest_framework import serializers
from .models import AIModel

class AIModelSerializer(serializers.ModelSerializer):
    """
    Serializer for listing available AI models to the frontend.
    """
    class Meta:
        model = AIModel
        fields = [
            'display_name',
            'description',
            'response_time_info',
            'login_required',
        ]

class ResumeGenerationSerializer(serializers.Serializer):
    """
    Serializer to validate the request for generating a resume.
    """
    model = serializers.CharField(required=True)
    user_input = serializers.CharField(required=True, min_length=50)

    def validate_model(self, value):
        """
        Check that the chosen model exists, is active, and meets login requirements.
        """
        try:
            model_instance = AIModel.objects.get(display_name__iexact=value, is_active=True)
        except AIModel.DoesNotExist:
            raise serializers.ValidationError("This model is not valid or is currently disabled.")
        
        # Check login requirements
        user = self.context['request'].user
        if model_instance.login_required and not user.is_authenticated:
            raise serializers.ValidationError(f"You must be logged in to use the {model_instance.display_name} model.")

        return model_instance
