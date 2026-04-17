from django.urls import path
from .views import CheckoutView, StripeWebhookView, AbonnementActuelView, PlanListView, SubscriptionsRootView

urlpatterns = [
    path('', SubscriptionsRootView.as_view(), name='subscriptions_root'),
    path('plans/', PlanListView.as_view()),
    path('me/', AbonnementActuelView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('webhook/', StripeWebhookView.as_view()),
]
