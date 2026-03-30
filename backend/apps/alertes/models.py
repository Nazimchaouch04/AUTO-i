from django.db import models
from django.contrib.auth.models import User


class Alerte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertes')
    titre = models.CharField(max_length=200)
    marque = models.CharField(max_length=100, blank=True)
    modele = models.CharField(max_length=100, blank=True)
    prix_max = models.IntegerField(null=True, blank=True)
    km_max = models.IntegerField(null=True, blank=True)
    carburant = models.CharField(max_length=20, blank=True)
    pays = models.CharField(max_length=5, default='DZ')

    email_actif = models.BooleanField(default=True)
    est_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Alerte - {self.titre}"
