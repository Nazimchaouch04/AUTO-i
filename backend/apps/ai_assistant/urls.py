from django.urls import path
from .views import (
    ConversationListView, 
    MessageView, 
    MessageRapideView,
    UsageStatsView,
    SupprimerConversationView
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conv_id>/messages/', MessageView.as_view(), name='messages'),
    path('conversations/<int:conv_id>/supprimer/', SupprimerConversationView.as_view(), name='supprimer_conversation'),
    path('message-rapide/', MessageRapideView.as_view(), name='message_rapide'),
    path('usage-stats/', UsageStatsView.as_view(), name='usage_stats'),
]
