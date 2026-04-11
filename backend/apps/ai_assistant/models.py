from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='conversations')
    titre = models.CharField(max_length=200, default='Nouvelle conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.titre}"

class Message(models.Model):
    ROLE_CHOICES = [('user', 'Utilisateur'), ('assistant', 'Assistant')]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                      related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation.titre} - {self.role}"

class UsageIA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    messages_utilises = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.messages_utilises} messages"

class UserProfileAnalysis(models.Model):
    """Analyse du profil utilisateur pour l'IA"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ia_profile')
    
    # Préférences de véhicule
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    marques_preferrees = models.ManyToManyField('vehicules.Marque', blank=True)
    types_vehicule = models.JSONField(default=list, blank=True)  # ['SUV', 'Berline', 'Citadine']
    
    # Besoins identifiés
    usage_principal = models.CharField(max_length=100, choices=[
        ('quotidien', 'Usage quotidien'),
        ('professionnel', 'Usage professionnel'),
        ('loisir', 'Loisir'),
        ('famille', 'Familial'),
        ('sportif', 'Sportif'),
    ], default='quotidien')
    
    kilometrage_annuel = models.IntegerField(default=15000)
    preferences_carburant = models.JSONField(default=list, blank=True)  # ['Essence', 'Diesel', 'Électrique', 'Hybride']
    
    # Contraintes
    places_minimales = models.IntegerField(default=4)
    porte_minimales = models.IntegerField(default=3)
    transmission_preferree = models.CharField(max_length=20, choices=[
        ('manuelle', 'Manuelle'),
        ('automatique', 'Automatique'),
        ('les_deux', 'Les deux'),
    ], default='les_deux')
    
    # Analyse IA
    score_ecologique = models.IntegerField(default=50)  # 0-100
    score_budget = models.IntegerField(default=50)     # 0-100
    score_praticite = models.IntegerField(default=50)  # 0-100
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analyse profil IA"
        verbose_name_plural = "Analyses profils IA"

class VehicleRecommendation(models.Model):
    """Recommandations de véhicules générées par l'IA"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    vehicule = models.ForeignKey('vehicules.Vehicule', on_delete=models.CASCADE, related_name='recommendations')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    
    # Score de recommandation
    score_total = models.IntegerField(default=0)  # 0-100
    score_prix = models.IntegerField(default=0)
    score_besoins = models.IntegerField(default=0)
    score_marche = models.IntegerField(default=0)
    score_disponibilite = models.IntegerField(default=0)
    
    # Justification IA
    raisons_recommandation = models.JSONField(default=list, blank=True)
    points_forts = models.JSONField(default=list, blank=True)
    points_faibles = models.JSONField(default=list, blank=True)
    
    # Prédictions
    prix_estime_1an = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_estime_3ans = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    confiance_prediction = models.IntegerField(default=0)  # 0-100
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score_total', '-created_at']
        verbose_name = "Recommandation véhicule"
        verbose_name_plural = "Recommandations véhicules"

class MarketInsight(models.Model):
    """Aperçus du marché générés par l'IA"""
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_insight = models.CharField(max_length=50, choices=[
        ('tendance_prix', 'Tendance des prix'),
        ('opportunite', 'Opportunité'),
        ('alerte_marche', 'Alerte marché'),
        ('conseil_achat', 'Conseil achat'),
        ('conseil_vente', 'Conseil vente'),
        ('prediction', 'Prédiction'),
    ])
    
    # Données associées
    marques_concernees = models.ManyToManyField('vehicules.Marque', blank=True)
    categories_vehicules = models.JSONField(default=list, blank=True)
    fourchettes_prix = models.JSONField(default=dict, blank=True)  # {"min": 10000, "max": 50000}
    
    # Impact et confiance
    niveau_impact = models.IntegerField(default=50)  # 0-100
    confiance = models.IntegerField(default=70)     # 0-100
    
    # Période de validité
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-niveau_impact', '-created_at']
        verbose_name = "Aperçu marché"
        verbose_name_plural = "Aperçus marché"

class IntentAnalysis(models.Model):
    """Analyse des intentions utilisateur dans les conversations"""
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='intent_analysis')
    
    # Intentions détectées
    intent_principale = models.CharField(max_length=100, choices=[
        ('recherche_vehicule', 'Recherche véhicule'),
        ('conseil_achat', 'Conseil achat'),
        ('estimation_prix', 'Estimation prix'),
        ('information_marche', 'Information marché'),
        ('comparaison', 'Comparaison'),
        ('avis_expert', 'Avis expert'),
        ('autre', 'Autre'),
    ])
    
    # Entités extraites
    entites = models.JSONField(default=dict, blank=True)  # {"marques": ["Renault", "Peugeot"], "budget": 20000}
    
    # Sentiment et urgence
    sentiment = models.CharField(max_length=20, choices=[
        ('positif', 'Positif'),
        ('neutre', 'Neutre'),
        ('negatif', 'Négatif'),
    ], default='neutre')
    
    niveau_urgence = models.IntegerField(default=50)  # 0-100
    
    # Contexte
    contexte_conversation = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Analyse intention"
        verbose_name_plural = "Analyses intentions"

class LearningData(models.Model):
    """Données d'apprentissage pour améliorer l'IA"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Type de donnée
    type_donnee = models.CharField(max_length=50, choices=[
        ('conversation', 'Conversation'),
        ('recommandation_feedback', 'Feedback recommandation'),
        ('prediction_resultat', 'Résultat prédiction'),
        ('comportement_recherche', 'Comportement recherche'),
    ])
    
    # Données
    donnees_entree = models.JSONField(default=dict)
    donnees_sortie = models.JSONField(default=dict)
    
    # Performance
    performance_score = models.IntegerField(null=True, blank=True)  # 0-100
    feedback_utilisateur = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donnée apprentissage"
        verbose_name_plural = "Données apprentissage"
