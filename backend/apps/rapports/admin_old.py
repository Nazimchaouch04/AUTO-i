from django.contrib import admin
from .models import RapportPDF, TemplateRapport, HistoriqueGeneration

@admin.register(RapportPDF)
class RapportPDFAdmin(admin.ModelAdmin):
    list_display = [
        'titre', 'user', 'type_rapport', 'statut_paiement', 
        'prix', 'created_at', 'genere_at', 'expire_at'
    ]
    list_filter = [
        'type_rapport', 'statut_paiement', 'created_at'
    ]
    search_fields = ['titre', 'user__username', 'user__email']
    readonly_fields = [
        'id', 'stripe_payment_intent_id', 'genere_at', 'expire_at'
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'user', 'type_rapport', 'statut_paiement')
        }),
        ('Contenu', {
            'fields': ('annonce_principale', 'annonces_comparees', 'alerte_source')
        }),
        ('Fichiers', {
            'fields': ('contenu_json', 'fichier_pdf')
        }),
        ('Paiement', {
            'fields': ('prix', 'stripe_payment_intent_id')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at', 'genere_at', 'expire_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(TemplateRapport)
class TemplateRapportAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_rapport', 'est_actif', 'est_par_defaut', 'created_at']
    list_filter = ['type_rapport', 'est_actif', 'est_par_defaut']
    search_fields = ['nom', 'description']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'type_rapport')
        }),
        ('Templates', {
            'fields': ('template_html', 'styles_css')
        }),
        ('Configuration', {
            'fields': ('est_actif', 'est_par_defaut')
        }),
    )

@admin.register(HistoriqueGeneration)
class HistoriqueGenerationAdmin(admin.ModelAdmin):
    list_display = ['rapport', 'action', 'statut', 'message', 'created_at']
    list_filter = ['action', 'statut', 'created_at']
    search_fields = ['rapport__titre', 'message']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('rapport')
