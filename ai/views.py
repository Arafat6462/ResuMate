from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import AIModel
from resume.models import Resume
from .serializers import AIModelSerializer, ResumeGenerationSerializer
from .services import generate_resume_content

class ListAIModelsView(APIView):
    """
    Lists all active AI models available for use.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        active_models = AIModel.objects.filter(is_active=True)
        serializer = AIModelSerializer(active_models, many=True)
        return Response(serializer.data)

class GenerateResumeView(APIView):
    """
    Receives user input and a model choice, then generates a resume.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResumeGenerationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model_instance = serializer.validated_data['model']
        user_input = serializer.validated_data['user_input']

        try:
            ai_response_text = generate_resume_content(model_instance, user_input)
            
            # For now, we just return the content. Saving will be a separate step.
            return Response({"content": ai_response_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)