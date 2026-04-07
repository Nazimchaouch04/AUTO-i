from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def api_root(request):
    return JsonResponse(
        {
            'message': 'AutoIntel API',
            'backend': 'OK',
            'frontend': 'http://127.0.0.1:5173',
            'endpoints': [
                '/admin/',
                '/api/auth/login/',
                '/api/annonces/',
                '/api/estimation/',
                '/api/dashboard/',
            ],
        }
    )

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/verify/', TokenVerifyView.as_view()),
    path('api/auth/', include('apps.users.urls')),

    # Apps
    path('api/annonces/', include('apps.annonces.urls')),
    path('api/estimation/', include('apps.estimation.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/alertes/', include('apps.alertes.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/gamification/', include('apps.gamification.urls')),
    path('api/ai/', include('apps.ai_assistant.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/rapports/', include('apps.rapports.urls')),
]
