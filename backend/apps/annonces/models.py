from django.db import models
from django.contrib.auth.models import User


class Vehicule(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, default='berline')

    class Meta:
        unique_together = ['marque', 'modele']

    def __str__(self):
        return f"{self.marque} {self.modele}"


class Annonce(models.Model):
    CARBURANT_CHOICES = [
        ('essence', 'Essence'), ('diesel', 'Diesel'),
        ('electrique', 'Électrique'), ('hybride', 'Hybride'),
    ]
    BOITE_CHOICES = [('manuelle', 'Manuelle'), ('automatique', 'Automatique')]

    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='annonces')
    annee = models.IntegerField()
    kilometrage = models.IntegerField()
    carburant = models.CharField(max_length=20, choices=CARBURANT_CHOICES, default='essence')
    boite = models.CharField(max_length=20, choices=BOITE_CHOICES, default='manuelle')
    puissance = models.IntegerField(null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_estime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ecart_prix = models.FloatField(null=True, blank=True)
    score_affaire = models.IntegerField(default=0)
    est_bonne_affaire = models.BooleanField(default=False)
    source = models.CharField(max_length=100, default='manuel')
    url_originale = models.URLField(unique=True, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    pays = models.CharField(max_length=5, default='DZ',
                             choices=[('DZ', 'Algérie'), ('TN', 'Tunisie'),
                                      ('FR', 'France'), ('MA', 'Maroc')])
    description = models.TextField(blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    date_collecte = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['est_bonne_affaire']),
            models.Index(fields=['pays']),
            models.Index(fields=['prix']),
        ]

    def __str__(self):
        return f"{self.vehicule.marque} {self.vehicule.modele} - {self.prix}€"


class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favoris_selectionnes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'annonce']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.annonce.vehicule.marque} {self.annonce.vehicule.modele}"


class RechercheSauvegardee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recherches')
    nom = models.CharField(max_length=100)
    query_params = models.JSONField(default=dict)
    result_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Battle(models.Model):
    vehicule_1 = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='battles_v1')
    vehicule_2 = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='battles_v2')
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='battles_creees')
    votes_v1 = models.IntegerField(default=0)
    votes_v2 = models.IntegerField(default=0)
    titre = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Battle: {self.vehicule_1.vehicule.marque} vs {self.vehicule_2.vehicule.marque}"

    def calculate_winner(self):
        # Logique de détermination du gagnant AutoIntel
        score1 = self.vehicule_1.score_affaire
        score2 = self.vehicule_2.score_affaire
        if score1 > score2: return self.vehicule_1.id
        if score2 > score1: return self.vehicule_2.id
        return None
