from django.core.cache import cache
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import JobApplication
from .serializers import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the job applications
        for the currently authenticated user.
        """
        return self.request.user.jobapplication_set.filter(is_deleted=False)

    def perform_create(self, serializer):
        """Associate the user with the job application."""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Soft delete the job application."""
        instance.is_deleted = True
        instance.save()


class ExampleJobApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides 5 sample job applications for anonymous users.
    This view is cached for 24 hours to reduce database load.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.AllowAny]
    CACHE_KEY = "example_job_applications"
    CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours

    def get_queryset(self):
        """
        This view should return a list of 5 sample job applications.
        """
        return JobApplication.objects.filter(is_example=True)[:5]

    def list(self, request, *args, **kwargs):
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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Save the raw serialized data to the cache
        cache.set(self.CACHE_KEY, serializer.data, self.CACHE_TIMEOUT)
        
        # Prepare response body with status
        response_data = {
            'cache_status': 'MISS (Response from database)',
            'data': serializer.data
        }
        return Response(response_data, headers={'X-Cache-Status': 'MISS'})