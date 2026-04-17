from django.contrib import admin
from .models import EstimationHistory


@admin.register(EstimationHistory)
class EstimationHistoryAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'annee', 'prix_estime', 'created_at')
    search_fields = ('marque', 'modele', 'user__username')
    list_filter = ('carburant', 'pays')
    ordering = ('-created_at',)
