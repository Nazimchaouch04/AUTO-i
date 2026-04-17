"""
Configuration admin pour les modèles marketplace fonctionnels
"""

from django.contrib import admin
from .models import (
    SellerProfile, Listing, Transaction, Review, Favorite, Message
)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'company_name', 'is_verified', 'total_sales',
        'average_rating', 'created_at'
    ]
    list_filter = [
        'is_verified', 'created_at'
    ]
    search_fields = [
        'user__username', 'user__email', 'company_name'
    ]
    readonly_fields = [
        'total_sales', 'average_rating', 'created_at'
    ]


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'brand', 'model', 'year', 'price', 'seller',
        'status', 'created_at'
    ]
    list_filter = [
        'status', 'brand', 'seller', 'created_at'
    ]
    search_fields = [
        'title', 'brand', 'model', 'description'
    ]
    readonly_fields = [
        'created_at'
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'listing', 'buyer', 'seller', 'total_amount',
        'status', 'created_at'
    ]
    list_filter = [
        'status', 'created_at'
    ]
    search_fields = [
        'listing__title', 'buyer__username', 'seller__user__username'
    ]
    readonly_fields = [
        'total_amount', 'created_at'
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'transaction', 'reviewer', 'reviewed', 'rating',
        'created_at'
    ]
    list_filter = [
        'rating', 'created_at'
    ]
    search_fields = [
        'transaction__listing__title', 'reviewer__username'
    ]
    readonly_fields = [
        'created_at'
    ]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'listing', 'created_at'
    ]
    list_filter = [
        'created_at'
    ]
    search_fields = [
        'user__username', 'listing__title'
    ]
    readonly_fields = [
        'created_at'
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'transaction', 'listing', 'sender', 'recipient',
        'subject', 'is_read', 'created_at'
    ]
    list_filter = [
        'is_read', 'created_at'
    ]
    search_fields = [
        'subject', 'content', 'sender__username'
    ]
    readonly_fields = [
        'created_at'
    ]
