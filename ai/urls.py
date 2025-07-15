from django.urls import path
from .views import ListAIModelsView, GenerateResumeView

urlpatterns = [
    path('models/', ListAIModelsView.as_view(), name='list-ai-models'),
    path('generate/', GenerateResumeView.as_view(), name='generate-resume'),
]
