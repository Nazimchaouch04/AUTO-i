from django.contrib import admin
from django.utils.html import format_html
from .models import Marque, Annonce


@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom_display', 'slug', 'populaire_display', 'nb_annonces')
    search_fields = ('nom', 'slug')
    ordering = ('nom',)
    list_filter = ('populaire',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'slug', 'populaire'),
            'classes': ('wide',),
        }),
    )

    def nom_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.nom)
    nom_display.short_description = 'Marque'
    
    def populaire_display(self, obj):
        if obj.populaire:
            return format_html('<span class="ai-badge ai-badge-teal">⭐ Populaire</span>')
        return format_html('<span class="ai-badge ai-badge-gray">Standard</span>')
    populaire_display.short_description = 'Popularité'

    def nb_annonces(self, obj):
        n = obj.annonces.filter(est_active=True).count()
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', n)

    nb_annonces.short_description = 'Annonces'


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = (
        'vehicule_display',
        'annee',
        'km_display',
        'prix_display',
        'est_display',
        'ecart_display',
        'deal_display',
        'pays_flag',
        'active_display',
        'date_publication',
    )
    search_fields = ('marque__nom', 'modele', 'ville', 'url_originale')
    ordering = ('-date_publication',)
    list_per_page = 25

    def vehicule_display(self, obj):
        return format_html(
            '<strong style="color:#F0F0F5">{} {}</strong>',
            obj.marque.nom,
            obj.modele,
        )

    vehicule_display.short_description = 'Véhicule'

    def km_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{:,} km</span>', obj.kilometrage)

    km_display.short_description = 'Km'

    def prix_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{:,} DA</strong>', int(obj.prix))

    prix_display.short_description = 'Prix'

    def est_display(self, obj):
        if not obj.prix_estime:
            return format_html('<span style="color:#55556A">—</span>')
        return format_html('<span style="color:#8B8BA0">{:,} DA</span>', int(obj.prix_estime))

    est_display.short_description = 'Estimé'

    def ecart_display(self, obj):
        if obj.ecart_prix is None:
            return format_html('<span style="color:#55556A">—</span>')
        pct = obj.ecart_prix
        if pct <= -5:
            return format_html('<span class="ai-badge ai-badge-teal">{:+.1f}%</span>', pct)
        if pct >= 5:
            return format_html('<span class="ai-badge ai-badge-red">{:+.1f}%</span>', pct)
        return format_html('<span class="ai-badge ai-badge-amber">{:+.1f}%</span>', pct)

    ecart_display.short_description = 'Écart'

    def deal_display(self, obj):
        if obj.est_bonne_affaire:
            return format_html('<span class="ai-badge ai-badge-teal">🎯 Affaire</span>')
        return format_html('<span style="color:#55556A;font-size:11px;">—</span>')

    deal_display.short_description = 'Deal'

    def pays_flag(self, obj):
        flags = {'DZ': '🇩🇿', 'TN': '🇹🇳', 'FR': '🇫🇷', 'MA': '🇲🇦'}
        return format_html('<span style="font-size:16px">{}</span>', flags.get(obj.pays, obj.pays))

    pays_flag.short_description = 'Pays'

    def active_display(self, obj):
        if obj.est_active:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')

    active_display.short_description = 'Statut'

    # Fieldsets pour le formulaire d'ajout/modification
    fieldsets = (
        ('Informations générales', {
            'fields': ('marque', 'modele', 'annee', 'est_active'),
            'classes': ('wide',),
        }),
        ('Caractéristiques', {
            'fields': (('kilometrage', 'puissance'), ('carburant', 'boite')),
            'classes': ('wide',),
        }),
        ('Prix et estimation', {
            'fields': (('prix', 'prix_estime'), 'ecart_prix', 'score_affaire'),
            'classes': ('wide',),
        }),
        ('Localisation', {
            'fields': ('ville', 'pays'),
            'classes': ('wide',),
        }),
        ('Source et description', {
            'fields': ('source', 'url_originale', 'description'),
            'classes': ('wide',),
        }),
        ('Dates', {
            'fields': ('date_publication', 'date_collecte'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['marquer_bonne_affaire', 'activer_annonces', 'desactiver_annonces', 'exporter_csv']

    def marquer_bonne_affaire(self, request, queryset):
        updated = queryset.update(est_bonne_affaire=True)
        self.message_user(request, f'{updated} annonces marquées comme bonnes affaires.')
    marquer_bonne_affaire.short_description = 'Marquer comme bonne affaire'

    def activer_annonces(self, request, queryset):
        updated = queryset.update(est_active=True)
        self.message_user(request, f'{updated} annonces activées.')
    activer_annonces.short_description = 'Activer les annonces'

    def desactiver_annonces(self, request, queryset):
        updated = queryset.update(est_active=False)
        self.message_user(request, f'{updated} annonces désactivées.')
    desactiver_annonces.short_description = 'Désactiver les annonces'

    def exporter_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="annonces.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Marque', 'Modèle', 'Année', 'Km', 'Prix', 'Pays', 'Ville', 'Deal', 'Actif'])
        
        for obj in queryset:
            writer.writerow([
                obj.marque.nom,
                obj.modele,
                obj.annee,
                obj.kilometrage,
                obj.prix,
                obj.pays,
                obj.ville,
                'Oui' if obj.est_bonne_affaire else 'Non',
                'Oui' if obj.est_active else 'Non'
            ])
        
        return response
    exporter_csv.short_description = 'Exporter en CSV'

    # Filtres personnalisés
    list_filter = (
        'est_bonne_affaire', 
        'est_active', 
        'pays', 
        'carburant', 
        'boite',
        'date_publication',
    )
