from django.contrib import admin

from .models import (
    EscrowAccount,
    LogisticsShipment,
    MarketplaceEvent,
    MarketplaceListing,
    MarketplaceOrder,
    MarketplacePayment,
    SellerVerification,
)


@admin.register(SellerVerification)
class SellerVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'legal_name', 'country', 'submitted_at', 'verified_at')
    list_filter = ('status', 'country', 'document_type')
    search_fields = ('user__username', 'legal_name', 'business_name')


@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'status', 'logistics_mode', 'published_at', 'sold_at')
    list_filter = ('status', 'logistics_mode', 'secure_payment_required', 'escrow_required')
    search_fields = ('seller__username', 'annonce__vehicule__marque', 'annonce__vehicule__modele')


@admin.register(MarketplaceOrder)
class MarketplaceOrderAdmin(admin.ModelAdmin):
    list_display = ('reference', 'buyer', 'seller', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'currency', 'secure_payment_required', 'escrow_required')
    search_fields = ('reference', 'buyer__username', 'seller__username')


@admin.register(MarketplacePayment)
class MarketplacePaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'provider', 'status', 'amount', 'created_at')
    list_filter = ('provider', 'status', 'currency')
    search_fields = ('order__reference', 'provider_reference')


@admin.register(EscrowAccount)
class EscrowAccountAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'held_amount', 'funded_at', 'released_at')
    list_filter = ('status',)
    search_fields = ('order__reference',)


@admin.register(LogisticsShipment)
class LogisticsShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'provider', 'tracking_number', 'status', 'shipped_at', 'delivered_at')
    list_filter = ('status', 'provider')
    search_fields = ('order__reference', 'tracking_number')


@admin.register(MarketplaceEvent)
class MarketplaceEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'actor', 'listing', 'order', 'created_at')
    list_filter = ('event_type',)
    search_fields = ('event_type', 'order__reference')
