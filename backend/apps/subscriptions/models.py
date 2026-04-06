from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    NOM_CHOICES = [('free', 'Gratuit'), ('pro', 'Pro'), ('business', 'Business')]

    nom = models.CharField(max_length=20, choices=NOM_CHOICES, unique=True)
    prix_mensuel = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    estimations_par_mois = models.IntegerField(default=5)
    alertes_max = models.IntegerField(default=2)
    export_csv = models.BooleanField(default=False)
    acces_api = models.BooleanField(default=False)

    def __str__(self):
        return self.get_nom_display()


class Abonnement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    actif = models.BooleanField(default=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Abonnement {self.user.username} - {self.plan.nom}"
