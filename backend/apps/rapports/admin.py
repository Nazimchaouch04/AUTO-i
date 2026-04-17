from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import RapportPDF, TemplateRapport, HistoriqueGeneration


@admin.register(RapportPDF)
class RapportPDFAdmin(admin.ModelAdmin):
    list_display = (
        'title_display',
        'user_display',
        'type_display',
        'status_display',
        'price_display',
        'validity_display',
        'created_at'
    )
    list_filter = ('type_rapport', 'statut_paiement', 'created_at')
    search_fields = ('titre', 'user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'stripe_payment_intent_id', 'genere_at', 'expire_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'titre', 'type_rapport', 'statut_paiement'),
            'classes': ('wide',),
        }),
        ('Contenu du rapport', {
            'fields': ('annonce_principale', 'annonces_comparees', 'alerte_source'),
            'classes': ('wide',),
        }),
        ('Fichiers et données', {
            'fields': ('contenu_json', 'fichier_pdf'),
            'classes': ('wide',),
        }),
        ('Paiement', {
            'fields': ('prix', 'stripe_payment_intent_id'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('id', 'created_at', 'updated_at', 'genere_at', 'expire_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['marquer_paye', 'regenerer_rapports', 'etendre_validite']
    
    def title_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.titre[:40] + '...' if len(obj.titre) > 40 else obj.titre)
    title_display.short_description = 'Titre'
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def type_display(self, obj):
        colors = {
            'complet': 'ai-badge-teal',
            'comparatif': 'ai-badge-amber',
            'historique': 'ai-badge-violet',
            'estimation': 'ai-badge-green',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.type_rapport, 'ai-badge-gray'), obj.get_type_rapport_display())
    type_display.short_description = 'Type'
    
    def status_display(self, obj):
        colors = {
            'en_attente': 'ai-badge-amber',
            'paye': 'ai-badge-green',
            'generation': 'ai-badge-blue',
            'termine': 'ai-badge-teal',
            'erreur': 'ai-badge-red',
            'expire': 'ai-badge-gray',
        }
        icons = {
            'en_attente': '⏳',
            'paye': '✓',
            'generation': '⚙',
            'termine': '✓',
            'erreur': '✗',
            'expire': '⏰',
        }
        css = colors.get(obj.statut_paiement, 'ai-badge-gray')
        icon = icons.get(obj.statut_paiement, '❓')
        return format_html('<span class="ai-badge {}">{} {}</span>', css, icon, obj.get_statut_paiement_display())
    status_display.short_description = 'Statut'
    
    def price_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">{:,} DA</span>', int(obj.prix))
    price_display.short_description = 'Prix'
    
    def validity_display(self, obj):
        if obj.expire_at:
            if obj.expire_at < timezone.now():
                return format_html('<span class="ai-badge ai-badge-red">⏰ Expiré</span>')
            elif obj.expire_at < timezone.now() + timezone.timedelta(days=7):
                return format_html('<span class="ai-badge ai-badge-amber">⏰ Expire bientôt</span>')
            else:
                days_left = (obj.expire_at - timezone.now()).days
                return format_html('<span class="ai-badge ai-badge-green">✓ {} jours</span>', days_left)
        return format_html('<span class="ai-badge ai-badge-gray">—</span>')
    validity_display.short_description = 'Validité'
    
    def marquer_paye(self, request, queryset):
        updated = queryset.update(statut_paiement='paye')
        self.message_user(request, f'{updated} rapports marqués comme payés.')
    marquer_paye.short_description = 'Marquer comme payé'
    
    def regenerer_rapports(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} rapports sélectionnés pour régénération (simulation). '
            'Fonctionnalité à implémenter avec le service de génération PDF.'
        )
    regenerer_rapports.short_description = 'Régénérer (simulation)'
    
    def etendre_validite(self, request, queryset):
        from datetime import timedelta
        updated = queryset.update(expire_at=timezone.now() + timedelta(days=30))
        self.message_user(request, f'{updated} rapports : validité étendue de 30 jours.')
    etendre_validite.short_description = 'Étendre validité de 30 jours'


@admin.register(TemplateRapport)
class TemplateRapportAdmin(admin.ModelAdmin):
    list_display = (
        'name_display',
        'type_display',
        'status_display',
        'default_display',
        'created_at'
    )
    list_filter = ('type_rapport', 'est_actif', 'est_par_defaut')
    search_fields = ('nom', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'type_rapport'),
            'classes': ('wide',),
        }),
        ('Templates', {
            'fields': ('template_html', 'styles_css'),
            'classes': ('wide',),
        }),
        ('Configuration', {
            'fields': ('est_actif', 'est_par_defaut'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['activer_templates', 'desactiver_templates', 'definir_par_defaut']
    
    def name_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.nom)
    name_display.short_description = 'Nom'
    
    def type_display(self, obj):
        colors = {
            'complet': 'ai-badge-teal',
            'comparatif': 'ai-badge-amber',
            'historique': 'ai-badge-violet',
            'estimation': 'ai-badge-green',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.type_rapport, 'ai-badge-gray'), obj.get_type_rapport_display())
    type_display.short_description = 'Type'
    
    def status_display(self, obj):
        if obj.est_actif:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')
    status_display.short_description = 'Statut'
    
    def default_display(self, obj):
        if obj.est_par_defaut:
            return format_html('<span class="ai-badge ai-badge-violet">⭐ Par défaut</span>')
        return format_html('<span class="ai-badge ai-badge-gray">Standard</span>')
    default_display.short_description = 'Défaut'
    
    def activer_templates(self, request, queryset):
        updated = queryset.update(est_actif=True)
        self.message_user(request, f'{updated} templates activés.')
    activer_templates.short_description = 'Activer les templates'
    
    def desactiver_templates(self, request, queryset):
        updated = queryset.update(est_actif=False)
        self.message_user(request, f'{updated} templates désactivés.')
    desactiver_templates.short_description = 'Désactiver les templates'
    
    def definir_par_defaut(self, request, queryset):
        # D'abord, tout décocher
        TemplateRapport.objects.all().update(est_par_defaut=False)
        # Puis cocher les templates sélectionnés
        updated = queryset.update(est_par_defaut=True)
        self.message_user(request, f'{updated} templates définis par défaut.')
    definir_par_defaut.short_description = 'Définir par défaut'


@admin.register(HistoriqueGeneration)
class HistoriqueGenerationAdmin(admin.ModelAdmin):
    list_display = (
        'report_display',
        'action_display',
        'status_display',
        'duration_display',
        'message_preview',
        'created_at'
    )
    list_filter = ('action', 'statut', 'created_at')
    search_fields = ('rapport__titre', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Historique', {
            'fields': ('rapport', 'action', 'statut', 'message', 'temps_execution'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def report_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.rapport.titre[:30] + '...' if len(obj.rapport.titre) > 30 else obj.rapport.titre)
    report_display.short_description = 'Rapport'
    
    def action_display(self, obj):
        colors = {
            'generation': 'ai-badge-blue',
            'regeneration': 'ai-badge-amber',
            'telechargement': 'ai-badge-teal',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.action, 'ai-badge-gray'), obj.action)
    action_display.short_description = 'Action'
    
    def status_display(self, obj):
        colors = {
            'succes': 'ai-badge-green',
            'erreur': 'ai-badge-red',
            'en_cours': 'ai-badge-blue',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.statut, 'ai-badge-gray'), obj.statut)
    status_display.short_description = 'Statut'
    
    def duration_display(self, obj):
        if obj.temps_execution:
            total_seconds = obj.temps_execution.total_seconds()
            if total_seconds < 60:
                return format_html('<span style="color:#8B8BA0">{:.1f}s</span>', total_seconds)
            else:
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                return format_html('<span style="color:#8B8BA0">{}m {}s</span>', minutes, seconds)
        return format_html('<span style="color:#55556A">—</span>')
    duration_display.short_description = 'Durée'
    
    def message_preview(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.message[:50] + '...' if len(obj.message) > 50 else obj.message)
    message_preview.short_description = 'Message'
