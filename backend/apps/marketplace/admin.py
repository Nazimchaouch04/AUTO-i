"""
Configuration admin pour les modèles marketplace fonctionnels avec thème AutoIntel
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import (
    SellerProfile, Listing, Transaction, Review, Favorite, Message
)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_display',
        'company_display',
        'verification_display',
        'sales_display',
        'rating_display',
        'created_at'
    )
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name')
    ordering = ('-created_at',)
    readonly_fields = ('total_sales', 'average_rating', 'created_at')
    
    fieldsets = (
        ('Informations vendeur', {
            'fields': ('user', 'company_name', 'phone_number', 'description', 'is_verified'),
            'classes': ('wide',),
        }),
        ('Statistiques', {
            'fields': (('total_sales', 'average_rating'),),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['verifier_vendeurs', 'desactiver_vendeurs']
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def company_display(self, obj):
        name = obj.company_name or obj.user.username
        return format_html('<strong style="color:#F0F0F5">{}</strong>', name)
    company_display.short_description = 'Entreprise'
    
    def verification_display(self, obj):
        if obj.is_verified:
            return format_html('<span class="ai-badge ai-badge-teal">✓ Vérifié</span>')
        return format_html('<span class="ai-badge ai-badge-gray">Non vérifié</span>')
    verification_display.short_description = 'Vérification'
    
    def sales_display(self, obj):
        if obj.total_sales == 0:
            return format_html('<span style="color:#55556A">0</span>')
        elif obj.total_sales < 10:
            return format_html('<span class="ai-badge ai-badge-green">{}</span>', obj.total_sales)
        elif obj.total_sales < 50:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.total_sales)
        else:
            return format_html('<span class="ai-badge ai-badge-red">{}</span>', obj.total_sales)
    sales_display.short_description = 'Ventes'
    
    def rating_display(self, obj):
        if obj.average_rating == 0:
            return format_html('<span style="color:#55556A">—</span>')
        elif obj.average_rating >= 4.5:
            return format_html('<span class="ai-badge ai-badge-teal">⭐ {:.1f}</span>', obj.average_rating)
        elif obj.average_rating >= 3.5:
            return format_html('<span class="ai-badge ai-badge-green">⭐ {:.1f}</span>', obj.average_rating)
        elif obj.average_rating >= 2.5:
            return format_html('<span class="ai-badge ai-badge-amber">⭐ {:.1f}</span>', obj.average_rating)
        else:
            return format_html('<span class="ai-badge ai-badge-red">⭐ {:.1f}</span>', obj.average_rating)
    rating_display.short_description = 'Note'
    
    def verifier_vendeurs(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} vendeurs vérifiés.')
    verifier_vendeurs.short_description = 'Vérifier les vendeurs'
    
    def desactiver_vendeurs(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} vendeurs dévérifiés.')
    desactiver_vendeurs.short_description = 'Dévérifier les vendeurs'


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title_display',
        'vehicle_display',
        'price_display',
        'seller_display',
        'status_display',
        'created_at'
    )
    list_filter = ('status', 'brand', 'seller', 'created_at')
    search_fields = ('title', 'brand', 'model', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Annonce', {
            'fields': ('title', 'description', 'status'),
            'classes': ('wide',),
        }),
        ('Véhicule', {
            'fields': (('brand', 'model'), 'year'),
            'classes': ('wide',),
        }),
        ('Prix', {
            'fields': ('price',),
            'classes': ('wide',),
        }),
        ('Vendeur', {
            'fields': ('seller',),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['publier_annonces', 'marquer_vendu', 'archiver_annonces']
    
    def title_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.title[:40] + '...' if len(obj.title) > 40 else obj.title)
    title_display.short_description = 'Titre'
    
    def vehicle_display(self, obj):
        return format_html(
            '<span style="color:#8B8BA0">{} {} {}</span>',
            obj.brand, obj.model, obj.year
        )
    vehicle_display.short_description = 'Véhicule'
    
    def price_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">{:,} DA</span>', int(obj.price))
    price_display.short_description = 'Prix'
    
    def seller_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.seller.company_name or obj.seller.user.username)
    seller_display.short_description = 'Vendeur'
    
    def status_display(self, obj):
        colors = {
            'draft': 'ai-badge-gray',
            'published': 'ai-badge-green',
            'sold': 'ai-badge-teal',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.status, 'ai-badge-gray'), obj.get_status_display())
    status_display.short_description = 'Statut'
    
    def publier_annonces(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} annonces publiées.')
    publier_annonces.short_description = 'Publier les annonces'
    
    def marquer_vendu(self, request, queryset):
        updated = queryset.update(status='sold')
        self.message_user(request, f'{updated} annonces marquées comme vendues.')
    marquer_vendu.short_description = 'Marquer comme vendu'
    
    def archiver_annonces(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} annonces archivées.')
    archiver_annonces.short_description = 'Archiver les annonces'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id_display',
        'listing_display',
        'buyer_display',
        'seller_display',
        'amount_display',
        'status_display',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('listing__title', 'buyer__username', 'seller__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('total_amount', 'created_at')
    
    fieldsets = (
        ('Transaction', {
            'fields': ('listing', 'buyer', 'seller', 'status'),
            'classes': ('wide',),
        }),
        ('Montant', {
            'fields': ('total_amount',),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['marquer_paye', 'completer_transactions']
    
    def id_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-amber">#{}<span>', obj.id)
    id_display.short_description = 'ID'
    
    def listing_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.listing.title[:30] + '...' if len(obj.listing.title) > 30 else obj.listing.title)
    listing_display.short_description = 'Annonce'
    
    def buyer_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.buyer.username)
    buyer_display.short_description = 'Acheteur'
    
    def seller_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.seller.company_name or obj.seller.user.username)
    seller_display.short_description = 'Vendeur'
    
    def amount_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">{:,} DA</span>', int(obj.total_amount))
    amount_display.short_description = 'Montant'
    
    def status_display(self, obj):
        colors = {
            'pending': 'ai-badge-amber',
            'paid': 'ai-badge-green',
            'completed': 'ai-badge-teal',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.status, 'ai-badge-gray'), obj.get_status_display())
    status_display.short_description = 'Statut'
    
    def marquer_paye(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} transactions marquées comme payées.')
    marquer_paye.short_description = 'Marquer comme payé'
    
    def completer_transactions(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} transactions complétées.')
    completer_transactions.short_description = 'Compléter les transactions'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_display',
        'reviewer_display',
        'seller_display',
        'rating_display',
        'comment_preview',
        'created_at'
    )
    list_filter = ('rating', 'created_at')
    search_fields = ('transaction__listing__title', 'reviewer__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Avis', {
            'fields': ('transaction', 'reviewer', 'reviewed', 'rating', 'comment'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def transaction_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-amber">#{}<span>', obj.transaction.id)
    transaction_display.short_description = 'Transaction'
    
    def reviewer_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.reviewer.username)
    reviewer_display.short_description = 'Avisé par'
    
    def seller_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.reviewed.company_name or obj.reviewed.user.username)
    seller_display.short_description = 'Vendeur'
    
    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="color:#F59E0B">{}</span>', stars)
    rating_display.short_description = 'Note'
    
    def comment_preview(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment)
    comment_preview.short_description = 'Commentaire'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'listing_display', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'listing__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Favori', {
            'fields': ('user', 'listing'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def listing_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.listing.title[:40] + '...' if len(obj.listing.title) > 40 else obj.listing.title)
    listing_display.short_description = 'Annonce'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'subject_display',
        'sender_display',
        'recipient_display',
        'listing_display',
        'read_display',
        'created_at'
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Message', {
            'fields': ('transaction', 'listing', 'sender', 'recipient', 'subject', 'content', 'is_read'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['marquer_lu', 'marquer_non_lu']
    
    def subject_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.subject[:40] + '...' if len(obj.subject) > 40 else obj.subject)
    subject_display.short_description = 'Sujet'
    
    def sender_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.sender.username)
    sender_display.short_description = 'Expéditeur'
    
    def recipient_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.recipient.username)
    recipient_display.short_description = 'Destinataire'
    
    def listing_display(self, obj):
        if obj.listing:
            return format_html('<span style="color:#8B8BA0">{}</span>', obj.listing.title[:30] + '...' if len(obj.listing.title) > 30 else obj.listing.title)
        return format_html('<span style="color:#55556A">—</span>')
    listing_display.short_description = 'Annonce'
    
    def read_display(self, obj):
        if obj.is_read:
            return format_html('<span class="ai-badge ai-badge-green">✓ Lu</span>')
        return format_html('<span class="ai-badge ai-badge-amber">⏳ Non lu</span>')
    read_display.short_description = 'Lecture'
    
    def marquer_lu(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages marqués comme lus.')
    marquer_lu.short_description = 'Marquer comme lu'
    
    def marquer_non_lu(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} messages marqués comme non lus.')
    marquer_non_lu.short_description = 'Marquer comme non lu'
