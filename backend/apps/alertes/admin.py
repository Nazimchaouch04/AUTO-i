from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Alerte


@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = (
        'titre_display', 
        'user_display', 
        'criteria_display', 
        'notifications_display', 
        'status_display', 
        'last_trigger_display',
        'created_at'
    )
    list_filter = (
        'est_active', 
        'email_actif', 
        'push_actif', 
        'pays',
        'carburant',
        'boite_vitesse',
        'created_at'
    )
    search_fields = ('titre', 'user__username', 'user__email', 'marque', 'modele')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_triggered')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'titre', 'est_active'),
            'classes': ('wide',),
        }),
        ('Critères de recherche', {
            'fields': (
                ('marque', 'modele'),
                ('prix_min', 'prix_max'),
                ('km_max', 'annee_min'),
                ('carburant', 'boite_vitesse'),
                'pays'
            ),
            'classes': ('wide',),
        }),
        ('Notifications', {
            'fields': ('email_actif', 'push_actif'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'last_triggered'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['activer_alertes', 'desactiver_alertes', 'activer_notifications', 'desactiver_notifications']
    
    def titre_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.titre)
    titre_display.short_description = 'Titre'
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def criteria_display(self, obj):
        criteria = []
        if obj.marque:
            criteria.append(f"Marque: {obj.marque}")
        if obj.modele:
            criteria.append(f"Modèle: {obj.modele}")
        if obj.prix_min or obj.prix_max:
            prix = f"{obj.prix_min or '?'}-{obj.prix_max or '?'} DA"
            criteria.append(f"Prix: {prix}")
        if obj.km_max:
            criteria.append(f"KM: ≤{obj.km_max:,}")
        if obj.annee_min:
            criteria.append(f"Année: ≥{obj.annee_min}")
        
        if not criteria:
            return format_html('<span style="color:#55556A">Tous</span>')
        
        return format_html(
            '<span style="color:#8B8BA0">{}</span>',
            ' | '.join(criteria[:3]) + ('...' if len(criteria) > 3 else '')
        )
    criteria_display.short_description = 'Critères'
    
    def notifications_display(self, obj):
        badges = []
        if obj.email_actif:
            badges.append('<span class="ai-badge ai-badge-teal">📧 Email</span>')
        if obj.push_actif:
            badges.append('<span class="ai-badge ai-badge-amber">📱 Push</span>')
        
        if not badges:
            return format_html('<span class="ai-badge ai-badge-gray">Aucune</span>')
        
        return format_html(' '.join(badges))
    notifications_display.short_description = 'Notifications'
    
    def status_display(self, obj):
        if obj.est_active:
            return format_html('<span class="ai-badge ai-badge-green">● Active</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactive</span>')
    status_display.short_description = 'Statut'
    
    def last_trigger_display(self, obj):
        if obj.last_triggered:
            days_ago = (timezone.now() - obj.last_triggered).days
            if days_ago == 0:
                return format_html('<span style="color:#00D4AA">Aujourd\'hui</span>')
            elif days_ago == 1:
                return format_html('<span style="color:#F59E0B">Hier</span>')
            elif days_ago < 7:
                return format_html('<span style="color:#8B8BA0">{}j</span>', days_ago)
            else:
                return format_html('<span style="color:#55556A">{}j</span>', days_ago)
        return format_html('<span style="color:#55556A">Jamais</span>')
    last_trigger_display.short_description = 'Dernière alerte'
    
    def activer_alertes(self, request, queryset):
        updated = queryset.update(est_active=True)
        self.message_user(request, f'{updated} alertes activées.')
    activer_alertes.short_description = 'Activer les alertes'
    
    def desactiver_alertes(self, request, queryset):
        updated = queryset.update(est_active=False)
        self.message_user(request, f'{updated} alertes désactivées.')
    desactiver_alertes.short_description = 'Désactiver les alertes'
    
    def activer_notifications(self, request, queryset):
        updated = queryset.update(email_actif=True, push_actif=True)
        self.message_user(request, f'{updated} alertes : notifications activées.')
    activer_notifications.short_description = 'Activer toutes les notifications'
    
    def desactiver_notifications(self, request, queryset):
        updated = queryset.update(email_actif=False, push_actif=False)
        self.message_user(request, f'{updated} alertes : notifications désactivées.')
    desactiver_notifications.short_description = 'Désactiver toutes les notifications'
