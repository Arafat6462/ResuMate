from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, ExampleJobApplicationViewSet

router = DefaultRouter()
router.register(r'job-applications', JobApplicationViewSet, basename='jobapplication')
router.register(r'example-job-applications', ExampleJobApplicationViewSet, basename='examplejobapplication')

urlpatterns = [
    path('', include(router.urls)),
]
