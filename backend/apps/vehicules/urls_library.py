from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_library import (
    MarqueViewSet, ModeleViewSet, MotorisationViewSet, FinitionViewSet,
    EquipementViewSet, AvisExpertViewSet, ProblemeCourantViewSet,
    DonneeMarcheViewSet, BibliothequeViewSet
)

router = DefaultRouter()
router.register(r'marques', MarqueViewSet, basename='marque')
router.register(r'modeles', ModeleViewSet, basename='modele')
router.register(r'motorisations', MotorisationViewSet, basename='motorisation')
router.register(r'finitions', FinitionViewSet, basename='finition')
router.register(r'equipements', EquipementViewSet, basename='equipement')
router.register(r'avis-experts', AvisExpertViewSet, basename='avis-expert')
router.register(r'problemes', ProblemeCourantViewSet, basename='probleme-courant')
router.register(r'donnees-marche', DonneeMarcheViewSet, basename='donnee-marche')
router.register(r'bibliotheque', BibliothequeViewSet, basename='bibliotheque')

app_name = 'vehicules_library'

urlpatterns = [
    path('', include(router.urls)),
]
