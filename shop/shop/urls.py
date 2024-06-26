from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls')),
    path('docs/', include('docs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
