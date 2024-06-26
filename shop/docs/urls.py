from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Online-Shop API",
        default_version='v1',
        description="Test Task for Precoro",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    patterns=[path('api/', include('api.urls')), path('auth/', include('authentication.urls'))],
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, ],
)

urlpatterns = [
    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
]
