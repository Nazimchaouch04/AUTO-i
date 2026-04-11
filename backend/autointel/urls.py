from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from apps.users.auth import EmailOrUsernameTokenObtainPairView
from .views import api_health, api_root

urlpatterns = [
    path('', api_root),
    path('api/health/', api_health),
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/login/', EmailOrUsernameTokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/verify/', TokenVerifyView.as_view()),
    path('api/auth/', include('apps.users.urls')),

    # Apps
    path('api/annonces/', include('apps.annonces.urls')),
    path('api/vehicules/', include('apps.vehicules.urls_library')),
    path('api/estimation/', include('apps.estimation.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/alertes/', include('apps.alertes.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/gamification/', include('apps.gamification.urls')),
    path('api/ai/', include('apps.ai_assistant.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/rapports/', include('apps.rapports.urls')),
]
