"""
Configuration admin pour les modèles Notifications avec thème AutoIntel
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import CanalNotification, NotificationHistory


@admin.register(CanalNotification)
class CanalNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user_display',
        'canal_display',
        'value_display',
        'verification_display',
        'status_display',
        'created_at'
    )
    list_filter = ('canal', 'is_verified', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'valeur')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Canal de notification', {
            'fields': ('user', 'canal', 'valeur', 'is_verified', 'is_active'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['verifier_canaux', 'activer_canaux', 'desactiver_canaux']
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def canal_display(self, obj):
        colors = {
            'email': 'ai-badge-teal',
            'telegram': 'ai-badge-blue',
            'whatsapp': 'ai-badge-green',
        }
        icons = {
            'email': '📧',
            'telegram': '📱',
            'whatsapp': '💬',
        }
        css = colors.get(obj.canal, 'ai-badge-gray')
        icon = icons.get(obj.canal, '📢')
        return format_html('<span class="ai-badge {}">{} {}</span>', css, icon, obj.get_canal_display())
    canal_display.short_description = 'Canal'
    
    def value_display(self, obj):
        if obj.canal == 'email':
            return format_html('<span style="color:#8B8BA0">{}</span>', obj.valeur)
        elif obj.canal == 'telegram':
            return format_html('<span style="color:#6C63FF">@{}</span>', obj.valeur)
        elif obj.canal == 'whatsapp':
            return format_html('<span style="color:#00D4AA">{}</span>', obj.valeur)
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.valeur)
    value_display.short_description = 'Valeur'
    
    def verification_display(self, obj):
        if obj.is_verified:
            return format_html('<span class="ai-badge ai-badge-teal">✓ Vérifié</span>')
        return format_html('<span class="ai-badge ai-badge-gray">Non vérifié</span>')
    verification_display.short_description = 'Vérification'
    
    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')
    status_display.short_description = 'Statut'
    
    def verifier_canaux(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} canaux vérifiés.')
    verifier_canaux.short_description = 'Vérifier les canaux'
    
    def activer_canaux(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} canaux activés.')
    activer_canaux.short_description = 'Activer les canaux'
    
    def desactiver_canaux(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} canaux désactivés.')
    desactiver_canaux.short_description = 'Désactiver les canaux'


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'canal_display',
        'type_display',
        'content_preview',
        'status_display',
        'sent_display',
        'created_at'
    )
    list_filter = ('statut', 'canal__canal', 'created_at')
    search_fields = ('contenu', 'canal__user__username', 'erreur_message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'sent_at')
    
    fieldsets = (
        ('Notification', {
            'fields': ('canal', 'alerte', 'annonce', 'contenu', 'statut'),
            'classes': ('wide',),
        }),
        ('Erreurs', {
            'fields': ('erreur_message',),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': (('created_at', 'sent_at'),),
            'classes': ('wide',),
        }),
    )
    
    # Actions personnalisées
    actions = ['renvoyer_notifications', 'marquer_envoye']
    
    def canal_display(self, obj):
        colors = {
            'email': 'ai-badge-teal',
            'telegram': 'ai-badge-blue',
            'whatsapp': 'ai-badge-green',
        }
        icons = {
            'email': '📧',
            'telegram': '📱',
            'whatsapp': '💬',
        }
        css = colors.get(obj.canal.canal, 'ai-badge-gray')
        icon = icons.get(obj.canal.canal, '📢')
        return format_html('<span class="ai-badge {}">{} {}</span>', css, icon, obj.canal.get_canal_display())
    canal_display.short_description = 'Canal'
    
    def type_display(self, obj):
        if obj.alerte:
            return format_html('<span class="ai-badge ai-badge-amber">🔔 Alerte</span>')
        elif obj.annonce:
            return format_html('<span class="ai-badge ai-badge-violet">🚗 Annonce</span>')
        else:
            return format_html('<span class="ai-badge ai-badge-gray">📢 Général</span>')
    type_display.short_description = 'Type'
    
    def content_preview(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.contenu[:80] + '...' if len(obj.contenu) > 80 else obj.contenu)
    content_preview.short_description = 'Contenu'
    
    def status_display(self, obj):
        colors = {
            'sent': 'ai-badge-teal',
            'failed': 'ai-badge-red',
            'pending': 'ai-badge-amber',
        }
        icons = {
            'sent': '✓',
            'failed': '✗',
            'pending': '⏳',
        }
        css = colors.get(obj.statut, 'ai-badge-gray')
        icon = icons.get(obj.statut, '❓')
        return format_html('<span class="ai-badge {}">{} {}</span>', css, icon, obj.get_statut_display())
    status_display.short_description = 'Statut'
    
    def sent_display(self, obj):
        if obj.sent_at:
            days_ago = (timezone.now() - obj.sent_at).days
            if days_ago == 0:
                return format_html('<span style="color:#00D4AA">Aujourd\'hui</span>')
            elif days_ago == 1:
                return format_html('<span style="color:#F59E0B">Hier</span>')
            elif days_ago < 7:
                return format_html('<span style="color:#8B8BA0">{}j</span>', days_ago)
            else:
                return format_html('<span style="color:#55556A">{}j</span>', days_ago)
        return format_html('<span style="color:#55556A">—</span>')
    sent_display.short_description = 'Envoyé il y a'
    
    def renvoyer_notifications(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} notifications sélectionnées pour renvoi (simulation). '
            'Fonctionnalité à implémenter avec le service d\'envoi.'
        )
    renvoyer_notifications.short_description = 'Renvoyer (simulation)'
    
    def marquer_envoye(self, request, queryset):
        updated = queryset.update(statut='sent', sent_at=timezone.now())
        self.message_user(request, f'{updated} notifications marquées comme envoyées.')
    marquer_envoye.short_description = 'Marquer comme envoyé'
