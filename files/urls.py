from django.urls import path, include
from rest_framework.routers import DefaultRouter

# viewsets
from .viewsets import files as file_views


router = DefaultRouter()
router.register(r'files', file_views.FileViewSet, basename="file_views")

urlpatterns = [
    path('', include(router.urls))
]
