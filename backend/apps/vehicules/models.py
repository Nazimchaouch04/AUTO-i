from .models_library import (
    Marque, Modele, Motorisation, Finition, Equipement,
    AvisExpert, ProblemeCourant, DonneeMarche
)

# Modèle Vehicule original pour compatibilité
from django.db import models

class Vehicule(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, default='berline')

    class Meta:
        unique_together = ['marque', 'modele']

    def __str__(self):
        return f"{self.marque} {self.modele}"
