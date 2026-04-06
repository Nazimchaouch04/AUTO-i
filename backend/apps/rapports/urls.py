from django.urls import path
from .views import (
    RapportsListView,
    CreerRapportView,
    PayerRapportView,
    CheckoutRapportView,
    TelechargerRapportView,
    DetailRapportView,
    SupprimerRapportView,
    TypesRapportView,
    StatistiquesRapportsView,
)
from .stripe_service import stripe_webhook_view

urlpatterns = [
    path('', RapportsListView.as_view(), name='rapports_list'),
    path('creer/', CreerRapportView.as_view(), name='creer_rapport'),
    path('types/', TypesRapportView.as_view(), name='types_rapport'),
    path('statistiques/', StatistiquesRapportsView.as_view(), name='statistiques_rapports'),
    path('<uuid:rapport_id>/', DetailRapportView.as_view(), name='detail_rapport'),
    path('<uuid:rapport_id>/payer/', PayerRapportView.as_view(), name='payer_rapport'),
    path('<uuid:rapport_id>/checkout/', CheckoutRapportView.as_view(), name='checkout_rapport'),
    path('<uuid:rapport_id>/telecharger/', TelechargerRapportView.as_view(), name='telecharger_rapport'),
    path('<uuid:rapport_id>/supprimer/', SupprimerRapportView.as_view(), name='supprimer_rapport'),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
]
