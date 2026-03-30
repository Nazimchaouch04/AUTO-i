from django.contrib import admin
from .models import Vehicule, Annonce


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'categorie')
    search_fields = ('marque', 'modele')
    ordering = ('marque', 'modele')


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'annee', 'prix', 'est_bonne_affaire', 'pays', 'date_publication')
    search_fields = ('vehicule__marque', 'vehicule__modele', 'ville')
    list_filter = ('est_bonne_affaire', 'carburant', 'boite', 'pays')
    ordering = ('-date_publication',)
