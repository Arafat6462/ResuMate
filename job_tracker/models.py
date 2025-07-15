from django.db import models
from django.contrib.auth.models import User
from resume.models import Resume

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interviewing', 'Interviewing'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    original_job_description = models.TextField()
    resume_used = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    date_applied = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_example = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"