from django.db import models

class AIModel(models.Model):
    """
    A database model to store configuration for various AI models.
    This allows for dynamic management of AI providers via the Django admin.
    """
    PROVIDER_CHOICES = [
        ('google_gemini', 'Google Gemini'),
        ('open_router', 'OpenRouter'),
    ]

    display_name = models.CharField(max_length=100, unique=True, help_text="User-friendly name for the model (e.g., 'Deepseek').")
    model_name = models.CharField(max_length=100, help_text="The technical model identifier for the API call (e.g., 'deepseek/deepseek-r1-0528:free').")
    api_provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, help_text="The service that provides this model.")
    api_key_name = models.CharField(max_length=100, help_text="The name of the environment variable holding the API key (e.g., 'OPENROUTER_API_KEY').")

    is_active = models.BooleanField(default=True, help_text="Enable or disable this model for all users.")
    login_required = models.BooleanField(default=False, help_text="If checked, only logged-in users can use this model.")
    daily_limit = models.PositiveIntegerField(default=0, help_text="Max number of requests per day for a logged-in user. 0 means no limit.")

    # Display fields
    response_time_info = models.CharField(max_length=100, blank=True, help_text="Aprox. response time to show to the user (e.g., 'Fast', '5-10 seconds').")
    description = models.TextField(blank=True, help_text="A short description of the model for the user.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ['display_name']