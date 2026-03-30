from django.contrib import admin
from .models import Plan, Abonnement


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_mensuel', 'estimations_par_mois', 'alertes_max', 'export_csv')
    ordering = ('nom',)


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'actif', 'date_debut', 'date_fin')
    search_fields = ('user__username', 'user__email')
    list_filter = ('plan', 'actif')
    ordering = ('-date_debut',)
