'''
CORE URL PATTERNS
'''
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

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
    path('api/users/', include("apps.users.api.urls"), name="user-urls")

]