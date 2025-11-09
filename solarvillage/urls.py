"""
URL configuration for solarvillage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import MutualAidPostViewSet, CommunityResourceViewSet
from core.webauthn_views import webauthn_token_view
from core.webauthn_test_view import webauthn_test_page


router = routers.DefaultRouter()
router.register(r'mutual-aid-posts', MutualAidPostViewSet, basename='mutual-aid-post')
router.register(r'community-resources', CommunityResourceViewSet, basename='community-resource')

urlpatterns = [
    path('', webauthn_test_page, name='webauthn_test'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/webauthn/token/', webauthn_token_view, name='webauthn_token'),
    path('webauthn/', include('django_otp_webauthn.urls', namespace='otp_webauthn')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
