from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel, UUIDModel

class Marque(TimeStampedModel):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    populaire = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Annonce(TimeStampedModel):
    CARBURANT = [
        ('essence', 'Essence'), ('diesel', 'Diesel'),
        ('electrique', 'Électrique'), ('hybride', 'Hybride')
    ]
    BOITE = [
        ('manuelle', 'Manuelle'), ('automatique', 'Automatique')
    ]
    PAYS = [
        ('DZ', 'Algérie'), ('TN', 'Tunisie'),
        ('FR', 'France'), ('MA', 'Maroc')
    ]

    marque = models.ForeignKey(
        Marque, on_delete=models.PROTECT, related_name='annonces',
        default=1  # Temporaire pour migration
    )
    modele = models.CharField(max_length=100, db_index=True, default='Inconnu')
    annee = models.SmallIntegerField(db_index=True)
    kilometrage = models.IntegerField()
    carburant = models.CharField(
        max_length=20, choices=CARBURANT, db_index=True
    )
    boite = models.CharField(max_length=20, choices=BOITE)
    puissance = models.SmallIntegerField(null=True, blank=True)

    prix = models.DecimalField(max_digits=12, decimal_places=2)
    prix_estime = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    ecart_prix = models.FloatField(null=True, blank=True)
    score_affaire = models.SmallIntegerField(default=0, db_index=True)
    est_bonne_affaire = models.BooleanField(default=False, db_index=True)

    ville = models.CharField(max_length=100, blank=True, default='Inconnue')
    pays = models.CharField(
        max_length=5, choices=PAYS, default='DZ', db_index=True
    )

    url_originale = models.URLField(unique=True, null=True, blank=True)
    source = models.CharField(max_length=50, default='scraping')
    description = models.TextField(blank=True)
    est_active = models.BooleanField(default=True, db_index=True)
    date_publication = models.DateTimeField(
        null=True, blank=True, db_index=True
    )

    class Meta:
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['pays', 'est_bonne_affaire']),
            models.Index(fields=['marque', 'modele', 'annee']),
            models.Index(fields=['prix', 'pays']),
            models.Index(fields=['est_active', 'date_publication']),
        ]
    
    def __str__(self):
        return f"{self.marque} {self.modele} {self.annee}"


class Favori(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favoris_selectionnes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'annonce']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.annonce.vehicule.marque} {self.annonce.vehicule.modele}"


class RechercheSauvegardee(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recherches')
    nom = models.CharField(max_length=100)
    query_params = models.JSONField(default=dict)
    result_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

class Battle(TimeStampedModel):
    vehicule_1 = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='battles_v1')
    vehicule_2 = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='battles_v2')
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='battles_creees')
    votes_v1 = models.IntegerField(default=0)
    votes_v2 = models.IntegerField(default=0)
    titre = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Battle: {self.vehicule_1.marque} vs {self.vehicule_2.marque}"

    def calculate_winner(self):
        # Logique de détermination du gagnant AutoIntel
        score1 = self.vehicule_1.score_affaire
        score2 = self.vehicule_2.score_affaire
        if score1 > score2: return self.vehicule_1.id
        if score2 > score1: return self.vehicule_2.id
        return None
