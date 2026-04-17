from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ListingViewSet,
    TransactionViewSet,
    SellerProfileViewSet,
    ReviewViewSet,
    FavoriteViewSet,
    MessageViewSet,
    MarketplaceRootView,
)

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='marketplace-listing')
router.register(r'transactions', TransactionViewSet, basename='marketplace-transaction')
router.register(r'profile', SellerProfileViewSet, basename='marketplace-profile')
router.register(r'reviews', ReviewViewSet, basename='marketplace-review')
router.register(r'favorites', FavoriteViewSet, basename='marketplace-favorite')
router.register(r'messages', MessageViewSet, basename='marketplace-message')

urlpatterns = [
    path('', MarketplaceRootView.as_view(), name='marketplace-root'),
    path('', include(router.urls)),
]
