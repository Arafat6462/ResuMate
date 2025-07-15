from rest_framework import viewsets, permissions

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
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        This view should return a list of 5 sample job applications.
        """
        return JobApplication.objects.filter(is_example=True)[:5]