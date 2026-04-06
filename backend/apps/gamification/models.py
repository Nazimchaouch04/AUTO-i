from django.db import models
from django.contrib.auth.models import User


class ProfilJoueur(models.Model):
    NIVEAUX = [
        (1, 'Apprenti Mécanicien'),
        (2, 'Pilote Amateur'),
        (3, "Chasseur d'Affaires"),
        (4, 'Expert Automobile'),
        (5, 'Maître du Marché'),
        (6, 'Légende AutoIntel'),
    ]
    XP_PALIERS = [0, 500, 2000, 5000, 10000, 25000]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    xp = models.IntegerField(default=0)
    niveau = models.IntegerField(default=1)
    autocoin_balance = models.IntegerField(default=100)
    estimations_ce_mois = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def nom_niveau(self):
        return dict(self.NIVEAUX).get(self.niveau, 'Inconnu')

    def xp_prochain_niveau(self):
        if self.niveau >= 6:
            return self.xp
        return self.XP_PALIERS[self.niveau]

    def progression_pct(self):
        if self.niveau >= 6:
            return 100
        xp_debut = self.XP_PALIERS[self.niveau - 1]
        xp_fin = self.XP_PALIERS[self.niveau]
        if xp_fin == xp_debut:
            return 100
        return round((self.xp - xp_debut) / (xp_fin - xp_debut) * 100)

    def add_xp(self, amount):
        self.xp += amount
        while self.niveau < 6 and self.xp >= self.XP_PALIERS[self.niveau]:
            self.niveau += 1
        self.save()

    def add_coins(self, amount):
        self.autocoin_balance += amount
        self.save()

    def __str__(self):
        return f"ProfilJoueur {self.user.username} - Niveau {self.niveau}"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('gain_estimation', 'Estimation effectuée'),
        ('gain_bonne_affaire', 'Bonne affaire détectée'),
        ('gain_defi', 'Défi complété'),
        ('depense_boutique', 'Achat en boutique'),
        ('gain_battle', 'Battle gagnée'),
    ]
    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE, related_name='transactions')
    montant = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.profil.user.username} - {self.montant} AC"


class Defi(models.Model):
    TYPE_CHOICES = [
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('legendaire', 'Légendaire')
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    xp_reward = models.IntegerField(default=50)
    ac_reward = models.IntegerField(default=25)
    cible_count = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class DefiJoueur(models.Model):
    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE, related_name='defis_en_cours')
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE)
    progression = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['profil', 'defi']

    def __str__(self):
        return f"{self.profil.user.username} - {self.defi.titre}"


class BoutiqueItem(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_ac = models.IntegerField()
    image_url = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class AchatJoueur(models.Model):
    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE, related_name='achats')
    item = models.ForeignKey(BoutiqueItem, on_delete=models.CASCADE)
    date_achat = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_achat']

    def __str__(self):
        return f"{self.profil.user.username} a acheté {self.item.nom}"
