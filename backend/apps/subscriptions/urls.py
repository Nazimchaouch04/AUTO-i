from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, AbonnementViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'abonnement', AbonnementViewSet, basename='abonnement')

urlpatterns = [
    path('', include(router.urls)),
]
