from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_advanced import (
    AnnonceViewSet, RechercheAvanceeViewSet, ExportViewSet
)

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet, basename='annonce-advanced')
router.register(r'recherche', RechercheAvanceeViewSet, basename='recherche-avancee')
router.register(r'export', ExportViewSet, basename='export')

app_name = 'annonces_advanced'

urlpatterns = [
    path('', include(router.urls)),
]
