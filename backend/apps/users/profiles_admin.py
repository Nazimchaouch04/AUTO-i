"""
Configuration admin dédiée pour UserProfile avec interface améliorée
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.utils import timezone
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_display',
        'plan_badge',
        'xp_display',
        'level_display',
        'coins_display',
        'country_display',
        'updated_at'
    )
    list_filter = ('country', 'level', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',),
            'classes': ('wide',),
        }),
        ('Informations de profil', {
            'fields': ('country',),
            'classes': ('wide',),
        }),
        ('Gamification', {
            'fields': (('xp', 'level'), 'coins'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['ajouter_xp', 'ajouter_coins', 'reinitialiser_progression', 'attribuer_plan_pro', 'attribuer_plan_business']
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def plan_badge(self, obj):
        plan = getattr(obj, 'plan', 'free')
        css_map = {
            'pro': 'ai-badge-violet',
            'business': 'ai-badge-amber',
            'free': 'ai-badge-gray',
        }
        css = css_map.get(plan, 'ai-badge-gray')
        return format_html('<span class="ai-badge {}">{}</span>', css, str(plan).upper())
    plan_badge.short_description = 'Plan'
    
    def xp_display(self, obj):
        return format_html('<span style="color:#6C63FF;font-weight:600">⚡ {} XP</span>', obj.xp)
    xp_display.short_description = 'XP'
    
    def level_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">Niv {}</span>', obj.level)
    level_display.short_description = 'Niveau'
    
    def coins_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">🪙 {}</span>', obj.coins)
    coins_display.short_description = 'Coins'
    
    def country_display(self, obj):
        flags = {'DZ': '🇩🇿', 'TN': '🇹🇳', 'FR': '🇫🇷', 'MA': '🇲🇦'}
        return format_html('<span style="font-size:16px">{}</span> {}', 
                         flags.get(obj.country, obj.country), obj.country)
    country_display.short_description = 'Pays'
    
    def ajouter_xp(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} profils sélectionnés pour ajout XP (simulation). '
            'Fonctionnalité à implémenter avec formulaire de saisie.'
        )
    ajouter_xp.short_description = 'Ajouter XP (simulation)'
    
    def ajouter_coins(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} profils sélectionnés pour ajout Coins (simulation). '
            'Fonctionnalité à implémenter avec formulaire de saisie.'
        )
    ajouter_coins.short_description = 'Ajouter Coins (simulation)'
    
    def reinitialiser_progression(self, request, queryset):
        updated = queryset.update(xp=0, level=1, coins=100)
        self.message_user(request, f'{updated} profils réinitialisés.')
    reinitialiser_progression.short_description = 'Réinitialiser progression'
    
    def attribuer_plan_pro(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} profils sélectionnés pour attribution plan Pro (simulation). '
            'Fonctionnalité à implémenter avec le système d\'abonnement.'
        )
    attribuer_plan_pro.short_description = 'Attribuer plan Pro (simulation)'
    
    def attribuer_plan_business(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} profils sélectionnés pour attribution plan Business (simulation). '
            'Fonctionnalité à implémenter avec le système d\'abonnement.'
        )
    attribuer_plan_business.short_description = 'Attribuer plan Business (simulation)'
