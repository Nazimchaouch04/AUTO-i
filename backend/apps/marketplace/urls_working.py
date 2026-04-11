"""
URLs pour le marketplace fonctionnel
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'listings', views.ListingViewSet, basename='marketplace-listing')
router.register(r'transactions', views.TransactionViewSet, basename='marketplace-transaction')

app_name = 'marketplace'

urlpatterns = [
    # Vue racine
    path('', views.MarketplaceRootView.as_view(), name='marketplace-root'),
    
    # Annonces
    path('listings/', views.ListingListView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('my-listings/', views.MyListingView.as_view(), name='my-listings'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    
    # Vérification vendeur
    path('verification/', views.SellerVerificationView.as_view(), name='seller-verification'),
    
    # API Router
    path('', include(router.urls)),
]
