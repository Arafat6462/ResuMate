from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resume model.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Resume
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']
