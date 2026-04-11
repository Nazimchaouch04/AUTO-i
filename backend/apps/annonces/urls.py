from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, AnnonceViewSet, RechercheSauvegardeeViewSet, BattleViewSet
from .views_recommandations import (
    RecommendationsView, SearchSuggestionsView, SmartSearchView,
    UserDashboardView, MarketInsightsView, QuickActionsView
)

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet, basename='vehicule')
router.register(r'recherches', RechercheSauvegardeeViewSet, basename='recherche_sauvegardee')
router.register(r'battles', BattleViewSet, basename='battle')
router.register(r'', AnnonceViewSet, basename='annonce')

urlpatterns = [
    path('', include(router.urls)),
    # Nouvelles routes avancées
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    path('search/suggestions/', SearchSuggestionsView.as_view(), name='search-suggestions'),
    path('search/advanced/', SmartSearchView.as_view(), name='smart-search'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user-dashboard'),
    path('insights/market/', MarketInsightsView.as_view(), name='market-insights'),
    path('actions/quick/', QuickActionsView.as_view(), name='quick-actions'),
]
