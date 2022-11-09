'''
CORE URL PATTERNS
'''
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

# define schema
schema_view = get_schema_view(
   openapi.Info(
      title="Option Block Generator API",
      default_version='v1',
      description=(
          "Computer science project 2022-2023. "
          "API endpoints in detail"
          ),
      contact=openapi.Contact(email="rome.salarda@edgbarrowschool.co.uk"),
   ),
   public=True,
   permission_classes=[permissions.IsAdminUser],
)

# DJANGO SPECIFIC
urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # favicon path
    re_path(r'^favicon\.ico$', favicon_view),
]

# API ENDPOINTS
urlpatterns += [
    # JWT api token endpoints
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # App API endpoints
    path('api-users/', include("apps.users.api.urls"), name="user-urls"),
    path('api-rooms/', include("apps.environment.api.urls"), name="environment-urls"),
    path('api-students/', include("apps.students.api.urls"), name="students-urls"),
    path('api-generate/', include("apps.generator.api.urls"), name="generator-urls"),
    
]

# SCHEMA ENDPOINTS
urlpatterns += [
    re_path(r'^api-schema(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api-db-schema/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0)),
    
]