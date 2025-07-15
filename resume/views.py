from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing resume instances.
    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the resumes
        for the currently authenticated user.
        """
        return self.request.user.resumes.all()

    def perform_create(self, serializer):
        """
        Assign the current user to the resume when it is created.
        """
        serializer.save(user=self.request.user)