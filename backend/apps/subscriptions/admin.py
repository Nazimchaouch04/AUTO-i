from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Plan, Abonnement


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'name_display',
        'price_display',
        'features_display',
        'users_count',
        'revenue_display'
    )
    ordering = ('prix_mensuel', 'nom')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'prix_mensuel'),
            'classes': ('wide',),
        }),
        ('Limites et fonctionnalités', {
            'fields': (('estimations_par_mois', 'alertes_max'), ('export_csv', 'acces_api')),
            'classes': ('wide',),
        }),
    )
    
    # Actions personnalisées
    actions = ['activer_export_csv', 'activer_acces_api']
    
    def name_display(self, obj):
        colors = {
            'free': 'ai-badge-gray',
            'pro': 'ai-badge-violet',
            'business': 'ai-badge-amber',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.nom, 'ai-badge-gray'), obj.get_nom_display())
    name_display.short_description = 'Plan'
    
    def price_display(self, obj):
        if obj.prix_mensuel == 0:
            return format_html('<span style="color:#00D4AA;font-weight:600">GRATUIT</span>')
        return format_html('<span style="color:#F59E0B;font-weight:600">{} DA/mois</span>', f'{int(obj.prix_mensuel):,}')
    price_display.short_description = 'Prix'
    
    def features_display(self, obj):
        features = []
        if obj.export_csv:
            features.append('<span class="ai-badge ai-badge-teal">📊 CSV</span>')
        if obj.acces_api:
            features.append('<span class="ai-badge ai-badge-amber">🔑 API</span>')
        features.append(f'<span class="ai-badge ai-badge-green">{obj.estimations_par_mois} estimations</span>')
        features.append(f'<span class="ai-badge ai-badge-amber">{obj.alertes_max} alertes</span>')
        
        return format_html(' '.join(features))
    features_display.short_description = 'Fonctionnalités'
    
    def users_count(self, obj):
        count = obj.abonnement_set.filter(actif=True).count()
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', count)
    users_count.short_description = 'Utilisateurs actifs'
    
    def revenue_display(self, obj):
        if obj.prix_mensuel > 0:
            active_count = obj.abonnement_set.filter(actif=True).count()
            monthly_revenue = obj.prix_mensuel * active_count
            annual_revenue = monthly_revenue * 12
            return format_html(
                '<span style="color:#00D4AA">{:,} DA/mois</span><br>'
                '<span style="color:#8B8BA0;font-size:12px">{:,} DA/an</span>',
                int(monthly_revenue), int(annual_revenue)
            )
        return format_html('<span style="color:#8B8BA0">—</span>')
    revenue_display.short_description = 'Revenus'
    
    def activer_export_csv(self, request, queryset):
        updated = queryset.update(export_csv=True)
        self.message_user(request, f'{updated} plans : export CSV activé.')
    activer_export_csv.short_description = 'Activer export CSV'
    
    def activer_acces_api(self, request, queryset):
        updated = queryset.update(acces_api=True)
        self.message_user(request, f'{updated} plans : accès API activé.')
    activer_acces_api.short_description = 'Activer accès API'


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = (
        'user_display',
        'plan_display',
        'status_display',
        'duration_display',
        'renewal_display',
        'stripe_display'
    )
    search_fields = ('user__username', 'user__email', 'stripe_customer_id')
    list_filter = ('plan', 'actif', 'date_debut')
    ordering = ('-date_debut',)
    readonly_fields = ('date_debut', 'stripe_subscription_id', 'stripe_customer_id')
    
    fieldsets = (
        ('Abonnement', {
            'fields': ('user', 'plan', 'actif'),
            'classes': ('wide',),
        }),
        ('Dates', {
            'fields': (('date_debut', 'date_fin'),),
            'classes': ('wide',),
        }),
        ('Stripe', {
            'fields': (('stripe_subscription_id', 'stripe_customer_id')),
            'classes': ('wide',),
        }),
    )
    
    # Actions personnalisées
    actions = ['activer_abonnements', 'desactiver_abonnements', 'prolonger_abonnements']
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def plan_display(self, obj):
        colors = {
            'free': 'ai-badge-gray',
            'pro': 'ai-badge-violet',
            'business': 'ai-badge-amber',
        }
        return format_html('<span class="ai-badge {}">{}</span>', colors.get(obj.plan.nom, 'ai-badge-gray'), obj.plan.get_nom_display())
    plan_display.short_description = 'Plan'
    
    def status_display(self, obj):
        if obj.actif:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')
    status_display.short_description = 'Statut'
    
    def duration_display(self, obj):
        if obj.date_debut:
            start_date = obj.date_debut.date()
            end_date = obj.date_fin.date() if obj.date_fin else timezone.now().date()
            duration = (end_date - start_date).days
            if duration == 0:
                return format_html('<span style="color:#8B8BA0">Aujourd\'hui</span>')
            elif duration == 1:
                return format_html('<span style="color:#8B8BA0">1 jour</span>')
            elif duration < 30:
                return format_html('<span style="color:#8B8BA0">{} jours</span>', duration)
            elif duration < 365:
                months = duration // 30
                return format_html('<span style="color:#8B8BA0">{} mois</span>', months)
            else:
                years = duration // 365
                return format_html('<span style="color:#8B8BA0">{} an(s)</span>', years)
        return format_html('<span style="color:#55556A">—</span>')
    duration_display.short_description = 'Durée'
    
    def renewal_display(self, obj):
        if obj.date_fin and obj.actif:
            days_left = (obj.date_fin.date() - timezone.now().date()).days
            if days_left <= 0:
                return format_html('<span class="ai-badge ai-badge-red">⏰ Expiré</span>')
            elif days_left <= 7:
                return format_html('<span class="ai-badge ai-badge-amber">⏰ {} jours</span>', days_left)
            elif days_left <= 30:
                return format_html('<span class="ai-badge ai-badge-teal">✓ {} jours</span>', days_left)
            else:
                return format_html('<span class="ai-badge ai-badge-green">✓ {} jours</span>', days_left)
        elif obj.actif:
            return format_html('<span class="ai-badge ai-badge-green">∞ Auto</span>')
        return format_html('<span class="ai-badge ai-badge-gray">—</span>')
    renewal_display.short_description = 'Renouvellement'
    
    def stripe_display(self, obj):
        if obj.stripe_subscription_id:
            return format_html('<span class="ai-badge ai-badge-teal">✓ Stripe</span>')
        return format_html('<span class="ai-badge ai-badge-gray">—</span>')
    stripe_display.short_description = 'Stripe'
    
    def activer_abonnements(self, request, queryset):
        updated = queryset.update(actif=True)
        self.message_user(request, f'{updated} abonnements activés.')
    activer_abonnements.short_description = 'Activer les abonnements'
    
    def desactiver_abonnements(self, request, queryset):
        updated = queryset.update(actif=False)
        self.message_user(request, f'{updated} abonnements désactivés.')
    desactiver_abonnements.short_description = 'Désactiver les abonnements'
    
    def prolonger_abonnements(self, request, queryset):
        from datetime import timedelta
        updated = queryset.update(date_fin=timezone.now() + timedelta(days=30))
        self.message_user(request, f'{updated} abonnements prolongés de 30 jours.')
    prolonger_abonnements.short_description = 'Prolonger de 30 jours'
