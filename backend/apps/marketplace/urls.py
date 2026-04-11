from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MarketplaceListingViewSet,
    MarketplaceOrderViewSet,
    MarketplaceRootView,
    SellerVerificationReviewView,
    SellerVerificationView,
)

router = DefaultRouter()
router.register(r'listings', MarketplaceListingViewSet, basename='marketplace-listing')
router.register(r'orders', MarketplaceOrderViewSet, basename='marketplace-order')

urlpatterns = [
    path('', MarketplaceRootView.as_view(), name='marketplace-root'),
    path('verification/', SellerVerificationView.as_view(), name='seller-verification'),
    path(
        'verification/<int:verification_id>/review/',
        SellerVerificationReviewView.as_view(),
        name='seller-verification-review',
    ),
    path('', include(router.urls)),
]
