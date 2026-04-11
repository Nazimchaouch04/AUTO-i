from django.urls import path
from .views import (
    ConversationListView, 
    MessageView, 
    MessageRapideView,
    UsageStatsView,
    SupprimerConversationView,
    AIAssistantRootView,
    AnalyserMessageView,
    RecommandationsVehiculesView,
    ProfilIAView,
    MarketInsightsView,
    PredictionPrixView,
    AnalysePredictiveView,
    ConversationIntelligenteView
)

urlpatterns = [
    path('', AIAssistantRootView.as_view(), name='ai_root'),
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conv_id>/messages/', MessageView.as_view(), name='messages'),
    path('conversations/<int:conv_id>/supprimer/', SupprimerConversationView.as_view(), name='supprimer_conversation'),
    path('message-rapide/', MessageRapideView.as_view(), name='message_rapide'),
    path('usage-stats/', UsageStatsView.as_view(), name='usage_stats'),
    
    # Nouveaux endpoints IA avancés
    path('analyser-message/', AnalyserMessageView.as_view(), name='analyser_message'),
    path('recommandations-vehicules/', RecommandationsVehiculesView.as_view(), name='recommandations_vehicules'),
    path('profil-ia/', ProfilIAView.as_view(), name='profil_ia'),
    path('market-insights/', MarketInsightsView.as_view(), name='market_insights'),
    path('prediction-prix/', PredictionPrixView.as_view(), name='prediction_prix'),
    path('analyse-predictive/', AnalysePredictiveView.as_view(), name='analyse_predictive'),
    path('conversation-intelligente/', ConversationIntelligenteView.as_view(), name='conversation_intelligente'),
]
