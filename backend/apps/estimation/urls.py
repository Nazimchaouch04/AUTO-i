from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstimationViewSet

router = DefaultRouter()
router.register(r'', EstimationViewSet, basename='estimation')

urlpatterns = [
    path('', include(router.urls)),
]
