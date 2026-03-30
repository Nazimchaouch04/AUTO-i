from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, AnnonceViewSet

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet, basename='vehicule')
router.register(r'', AnnonceViewSet, basename='annonce')

urlpatterns = [
    path('', include(router.urls)),
]
