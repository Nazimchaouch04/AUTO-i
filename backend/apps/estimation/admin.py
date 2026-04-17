from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import EstimationHistory


@admin.register(EstimationHistory)
class EstimationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_display',
        'user_display', 
        'year_km_display',
        'price_display',
        'reliability_display',
        'reference_count_display',
        'created_at'
    )
    list_filter = (
        'carburant', 
        'boite', 
        'pays', 
        'fiabilite',
        'created_at'
    )
    search_fields = (
        'marque', 'modele', 'annee', 
        'user__username', 'user__email'
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'marque', 'modele', 'annee'),
            'classes': ('wide',),
        }),
        ('Caractéristiques', {
            'fields': (('kilometrage', 'puissance'), ('carburant', 'boite')),
            'classes': ('wide',),
        }),
        ('Localisation', {
            'fields': ('pays',),
            'classes': ('wide',),
        }),
        ('Résultats d\'estimation', {
            'fields': (
                ('prix_estime', 'fourchette_basse', 'fourchette_haute'),
                ('fiabilite', 'nb_annonces_reference')
            ),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['exporter_csv_estimations', 'recalculer_prix_moyen']
    
    def vehicle_display(self, obj):
        return format_html(
            '<strong style="color:#F0F0F5">{} {} {}</strong>',
            obj.marque, obj.modele, obj.annee
        )
    vehicle_display.short_description = 'Véhicule'
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def year_km_display(self, obj):
        return format_html(
            '<span style="color:#8B8BA0">{} | {:,} km</span>',
            obj.annee, obj.kilometrage
        )
    year_km_display.short_description = 'Année | KM'
    
    def price_display(self, obj):
        if obj.fourchette_basse and obj.fourchette_haute:
            return format_html(
                '<span style="color:#F59E0B;font-weight:600">{:,} DA</span><br>'
                '<span style="color:#8B8BA0;font-size:12px">{:,} - {:,} DA</span>',
                int(obj.prix_estime),
                int(obj.fourchette_basse),
                int(obj.fourchette_haute)
            )
        return format_html(
            '<span style="color:#F59E0B;font-weight:600">{:,} DA</span>',
            int(obj.prix_estime)
        )
    price_display.short_description = 'Prix estimé'
    
    def reliability_display(self, obj):
        colors = {
            'Haute': 'ai-badge-teal',
            'Moyenne': 'ai-badge-amber',
            'Basse': 'ai-badge-red',
        }
        css = colors.get(obj.fiabilite, 'ai-badge-gray')
        return format_html('<span class="ai-badge {}">{}</span>', css, obj.fiabilite)
    reliability_display.short_description = 'Fiabilité'
    
    def reference_count_display(self, obj):
        if obj.nb_annonces_reference == 0:
            return format_html('<span style="color:#55556A">0</span>')
        elif obj.nb_annonces_reference < 10:
            return format_html('<span class="ai-badge ai-badge-gray">{}</span>', obj.nb_annonces_reference)
        elif obj.nb_annonces_reference < 50:
            return format_html('<span class="ai-badge ai-badge-green">{}</span>', obj.nb_annonces_reference)
        else:
            return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.nb_annonces_reference)
    reference_count_display.short_description = 'Références'
    
    def exporter_csv_estimations(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="estimations.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Utilisateur', 'Marque', 'Modèle', 'Année', 'Kilométrage',
            'Carburant', 'Boîte', 'Pays', 'Prix estimé', 
            'Fourchette basse', 'Fourchette haute', 'Fiabilité', 'Références'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.user.username,
                obj.marque,
                obj.modele,
                obj.annee,
                obj.kilometrage,
                obj.carburant,
                obj.boite,
                obj.pays,
                obj.prix_estime,
                obj.fourchette_basse,
                obj.fourchette_haute,
                obj.fiabilite,
                obj.nb_annonces_reference
            ])
        
        return response
    exporter_csv_estimations.short_description = 'Exporter les estimations en CSV'
    
    def recalculer_prix_moyen(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} estimations sélectionnées pour recalcul (simulation). '
            'Fonctionnalité à implémenter avec l\'algorithme IA.'
        )
    recalculer_prix_moyen.short_description = 'Recalculer prix (simulation)'
