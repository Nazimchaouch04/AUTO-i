from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

class HistoriqueRecherche(models.Model):
    """Historique des recherches des utilisateurs pour améliorer les recommandations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historiques_recherche')
    terme = models.CharField(max_length=200)
    filtres = models.JSONField(default=dict)
    nombre_resultats = models.IntegerField(default=0)
    date_recherche = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_recherche']
        indexes = [
            models.Index(fields=['user', 'date_recherche']),
            models.Index(fields=['terme']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.terme}"

class Signalement(models.Model):
    """Système de signalement d'annonces abusives"""
    RAISON_CHOICES = [
        ('prix_fictif', 'Prix fictif'),
        ('vehicule_volé', 'Véhicule volé'),
        ('arnaque', 'Tentative d\'arnaque'),
        ('infos_fausses', 'Informations fausses'),
        ('vehicule_existe_pas', 'Véhicule n\'existe pas'),
        ('double_annonce', 'Annonce en double'),
        ('autre', 'Autre'),
    ]
    
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE, related_name='signalements')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    raison = models.CharField(max_length=20, choices=RAISON_CHOICES)
    description = models.TextField(blank=True)
    date_signalement = models.DateTimeField(auto_now_add=True)
    est_traite = models.BooleanField(default=False)
    traite_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='signalements_traites')
    date_traitement = models.DateTimeField(null=True, blank=True)
    note_traitement = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['annonce', 'utilisateur']
        ordering = ['-date_signalement']
    
    def __str__(self):
        return f"Signalement de {self.annonce.titre} par {self.utilisateur.username}"

class VisiteAnnonce(models.Model):
    """Suivi des visites pour les analytics"""
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE, related_name='visites')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    date_visite = models.DateTimeField(auto_now_add=True)
    duree_visite = models.IntegerField(null=True, blank=True)  # en secondes
    provient_de = models.CharField(max_length=100, blank=True)  # source de la visite
    
    class Meta:
        ordering = ['-date_visite']
        indexes = [
            models.Index(fields=['annonce', 'date_visite']),
            models.Index(fields=['utilisateur', 'date_visite']),
        ]
    
    def __str__(self):
        return f"Visite de {self.annonce.titre}"

class ContactVendeur(models.Model):
    """Suivi des contacts avec les vendeurs"""
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE, related_name='contacts')
    acheteur_potentiel = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    telephone_contact = models.CharField(max_length=20, blank=True)
    email_contact = models.EmailField(blank=True)
    date_contact = models.DateTimeField(auto_now_add=True)
    est_repondu = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['annonce', 'acheteur_potentiel']
        ordering = ['-date_contact']
    
    def __str__(self):
        return f"Contact pour {self.annonce.titre} par {self.acheteur_potentiel.username}"

class EvaluationVendeur(models.Model):
    """Système d'évaluation des vendeurs"""
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_recues')
    evaluateur = models.ForeignKey(User, on_delete=models.CASCADE)
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE)
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 à 5 étoiles
    commentaire = models.TextField(blank=True)
    aspects = models.JSONField(default=dict)  # {'communication': 5, 'fiabilite': 4, 'rapidite': 5}
    date_evaluation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['vendeur', 'evaluateur', 'annonce']
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"Évaluation de {self.vendeur.username} par {self.evaluateur.username}"

class NotificationAnnonce(models.Model):
    """Notifications personnalisées pour les annonces"""
    TYPE_CHOICES = [
        ('nouvelle_annonce', 'Nouvelle annonce correspondante'),
        ('prix_baisse', 'Baisse de prix'),
        ('bonne_affaire', 'Bonne affaire détectée'),
        ('annonces_similaires', 'Annonces similaires'),
        ('expiration_alerte', 'Alerte expiration'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_annonces')
    type_notification = models.CharField(max_length=30, choices=TYPE_CHOICES)
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE, null=True, blank=True)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_lue = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    donnees_supplementaires = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', 'est_lue', 'date_creation']),
        ]
    
    def __str__(self):
        return f"Notification pour {self.utilisateur.username}: {self.titre}"

class ComparaisonAnnonce(models.Model):
    """Sauvegarde des comparaisons d'annonces"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comparaisons')
    nom = models.CharField(max_length=100)
    annonces = models.ManyToManyField('annonces.Annonce', related_name='comparaisons')
    criteres = models.JSONField(default=dict)  # critères de comparaison personnalisés
    date_creation = models.DateTimeField(auto_now_add=True)
    est_publique = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Comparaison de {self.user.username}: {self.nom}"

class AlerteRecherche(models.Model):
    """Alertes de recherche personnalisées"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertes_recherche')
    nom = models.CharField(max_length=100)
    filtres = models.JSONField(default=dict)
    frequence = models.CharField(max_length=20, choices=[
        ('immediat', 'Immédiat'),
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
    ], default='quotidien')
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_notification = models.DateTimeField(null=True, blank=True)
    nombre_resultats = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Alerte '{self.nom}' de {self.user.username}"

class StatistiqueAnnonce(models.Model):
    """Statistiques détaillées des annonces"""
    annonce = models.OneToOneField('annonces.Annonce', on_delete=models.CASCADE, related_name='statistiques')
    vues_totales = models.IntegerField(default=0)
    vues_uniques = models.IntegerField(default=0)
    contacts_totales = models.IntegerField(default=0)
    favoris_totales = models.IntegerField(default=0)
    vues_jour = models.JSONField(default=dict)  # {'2024-01-01': 10, '2024-01-02': 15}
    contacts_jour = models.JSONField(default=dict)
    favoris_jour = models.JSONField(default=dict)
    pays_visiteurs = models.JSONField(default=dict)  # {'DZ': 100, 'FR': 50}
    sources_visiteurs = models.JSONField(default=dict)  # {'direct': 80, 'search': 20}
    dernier_calcul = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-dernier_calcul']
    
    def __str__(self):
        return f"Stats pour {self.annonce.titre}"
