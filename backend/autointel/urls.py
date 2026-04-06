from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

def api_root(request):
    return JsonResponse({
        'message': 'AutoIntel API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'auth_login': '/api/auth/login/',
            'auth_register': '/api/auth/register/',
            'auth_profile': '/api/auth/profile/',
            'annonces': '/api/annonces/',
            'estimation': '/api/estimation/',
            'dashboard': '/api/dashboard/',
            'alertes': '/api/alertes/',
            'subscriptions': '/api/subscriptions/',
            'gamification': '/api/gamification/',
            'ai_assistant': '/api/ai/',
            'notifications': '/api/notifications/',
            'rapports': '/api/rapports/',
        }
    })

def admin_dashboard_redirect(request):
    return redirect('/admin/')

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('admin-dashboard/', admin_dashboard_redirect),

    # Authentication (JWT)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
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
