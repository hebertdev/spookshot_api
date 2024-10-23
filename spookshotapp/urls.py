from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('users.urls', 'users'), namespace="users")),
    path('api/', include(('files.urls', 'files'), namespace="files")),
    path('api/', include(('posts.urls', 'posts'), namespace="posts")),
    path('api/', include(('cloudinary_api.urls', 'cloudinary_api'), namespace="cloudinary_api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
