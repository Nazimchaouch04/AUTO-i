from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardViewSet
from .admin_views import AdminDashboardViewSet

router = DefaultRouter()
router.register(r'', DashboardViewSet, basename='dashboard')
router.register(r'admin', AdminDashboardViewSet, basename='admin-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
