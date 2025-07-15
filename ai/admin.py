from django.contrib import admin
from .models import AIModel

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the AIModel.
    """
    list_display = (
        'display_name',
        'api_provider',
        'is_active',
        'login_required',
        'daily_limit',
        'model_name'
    )
    list_filter = ('api_provider', 'is_active', 'login_required')
    search_fields = ('display_name', 'model_name')
    list_editable = ('is_active', 'login_required', 'daily_limit')
    fieldsets = (
        ('Core Configuration', {
            'fields': ('display_name', 'model_name', 'api_provider', 'api_key_name')
        }),
        ('Access Control', {
            'fields': ('is_active', 'login_required', 'daily_limit')
        }),
        ('Display Information', {
            'fields': ('description', 'response_time_info')
        }),
    )