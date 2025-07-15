from django.contrib.auth.models import User
from django.db import models

class Resume(models.Model):
    """
    Represents a single resume document in the database.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"'{self.title}' by {self.user.username}"

    class Meta:
        ordering = ['-updated_at']