from django.db import models
from django.contrib.auth.models import User


class EstimationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimations')
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    kilometrage = models.IntegerField()
    carburant = models.CharField(max_length=20)
    boite = models.CharField(max_length=20, blank=True)
    puissance = models.IntegerField(null=True, blank=True)
    pays = models.CharField(max_length=5)

    prix_estime = models.DecimalField(max_digits=10, decimal_places=2)
    fourchette_basse = models.DecimalField(max_digits=10, decimal_places=2)
    fourchette_haute = models.DecimalField(max_digits=10, decimal_places=2)
    fiabilite = models.CharField(max_length=20)
    nb_annonces_reference = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee}) - {self.prix_estime}€"
