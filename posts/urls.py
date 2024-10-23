from django.urls import path, include
from rest_framework.routers import DefaultRouter

# viewsets
from .viewsets import posts as post_views


router = DefaultRouter()
router.register(r'posts', post_views.PostViewSet, basename="post_views")

urlpatterns = [
    path('', include(router.urls))
]
