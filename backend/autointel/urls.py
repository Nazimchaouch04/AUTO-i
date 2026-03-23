from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'AutoIntel API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/'
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
]
