from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, AnnonceViewSet, RechercheSauvegardeeViewSet, BattleViewSet

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet, basename='vehicule')
router.register(r'recherches', RechercheSauvegardeeViewSet, basename='recherche_sauvegardee')
router.register(r'battles', BattleViewSet, basename='battle')
router.register(r'', AnnonceViewSet, basename='annonce')

urlpatterns = [
    path('', include(router.urls)),
]
