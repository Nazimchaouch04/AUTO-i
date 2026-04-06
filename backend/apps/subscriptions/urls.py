from django.urls import path
from .views import CheckoutView, StripeWebhookView, AbonnementActuelView, PlanListView

urlpatterns = [
    path('plans/', PlanListView.as_view()),
    path('mon-abonnement/', AbonnementActuelView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('webhook/', StripeWebhookView.as_view()),
]
