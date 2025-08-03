from django.contrib.auth.models import User
from django.core.cache import cache
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
    This view is cached for 1 hour to reduce database load.
    """
    permission_classes = [AllowAny]
    CACHE_KEY = "ai_models_list"
    CACHE_TIMEOUT = 60 * 60  # 1 hour in seconds

    def get(self, request, *args, **kwargs):
        # Try to get the data from the cache first
        cached_data = cache.get(self.CACHE_KEY)
        if cached_data:
            # Cache Hit: Add status and return
            response_data = {
                'cache_status': 'HIT (Response from Redis cache)',
                'data': cached_data
            }
            return Response(response_data, headers={'X-Cache-Status': 'HIT'})

        # Cache Miss: Fetch from DB
        active_models = AIModel.objects.filter(is_active=True)
        serializer = AIModelSerializer(active_models, many=True)
        
        # Save the raw serialized data to the cache
        cache.set(self.CACHE_KEY, serializer.data, self.CACHE_TIMEOUT)
        
        # Prepare response body with status
        response_data = {
            'cache_status': 'MISS (Response from database)',
            'data': serializer.data
        }
        return Response(response_data, headers={'X-Cache-Status': 'MISS'})

class GenerateResumeView(APIView):
    """
    Receives user input and a model choice, then generates and saves a resume.
    Returns the ID of the newly created resume.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResumeGenerationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model_instance = serializer.validated_data['model']
        user_input = serializer.validated_data['user_input']
        title = serializer.validated_data.get('title', 'Untitled Resume')

        try:
            ai_response_text = generate_resume_content(model_instance, user_input)

            # Determine the user for the resume
            if request.user.is_authenticated:
                user = request.user
            else:
                # Get or create the dedicated anonymous user
                user, _ = User.objects.get_or_create(
                    username='anonymous_user',
                    defaults={'is_active': False} # This user cannot log in
                )

            # Create and save the new resume
            new_resume = Resume.objects.create(
                user=user,
                title=title,
                content=ai_response_text
            )

            return Response({"resume_id": new_resume.id, "content": ai_response_text}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)