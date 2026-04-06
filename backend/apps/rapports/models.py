from django.db import models
from django.contrib.auth.models import User
from apps.annonces.models import Annonce
from apps.alertes.models import Alerte
import uuid

class RapportPDF(models.Model):
    """Modèle pour les rapports PDF générés par les utilisateurs"""
    
    TYPE_RAPPORT_CHOICES = [
        ('complet', 'Rapport Complet'),
        ('comparatif', 'Analyse Comparative'),
        ('historique', 'Historique Prix'),
        ('estimation', 'Rapport d\'Estimation'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('paye', 'Payé'),
        ('generation', 'En cours de génération'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur'),
        ('expire', 'Expiré'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rapports')
    type_rapport = models.CharField(max_length=20, choices=TYPE_RAPPORT_CHOICES)
    titre = models.CharField(max_length=200)
    
    # Paramètres du rapport
    annonce_principale = models.ForeignKey(Annonce, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapports_principaux')
    annonces_comparees = models.ManyToManyField(Annonce, blank=True, related_name='rapports_comparatifs')
    alerte_source = models.ForeignKey(Alerte, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Contenu généré
    contenu_json = models.JSONField(default=dict, blank=True)  # Données structurées pour le PDF
    fichier_pdf = models.FileField(upload_to='rapports/pdf/', null=True, blank=True)
    
    # Paiement
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=9.99)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genere_at = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)  # 30 jours après génération
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rapport PDF"
        verbose_name_plural = "Rapports PDF"
    
    def __str__(self):
        return f"{self.titre} - {self.user.username}"
    
    @property
    def est_valide(self):
        """Vérifie si le rapport est encore valide (non expiré)"""
        if not self.expire_at:
            return False
        from django.utils import timezone
        return timezone.now() < self.expire_at
    
    @property
    def peut_etre_telecharge(self):
        """Vérifie si le rapport peut être téléchargé"""
        return self.statut_paiement == 'termine' and self.est_valide and self.fichier_pdf

class TemplateRapport(models.Model):
    """Modèles de templates pour les rapports PDF"""
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_rapport = models.CharField(max_length=20, choices=RapportPDF.TYPE_RAPPORT_CHOICES)
    template_html = models.TextField()
    styles_css = models.TextField(blank=True)
    
    # Configuration
    est_actif = models.BooleanField(default=True)
    est_par_defaut = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template de rapport"
        verbose_name_plural = "Templates de rapports"
    
    def __str__(self):
        return f"{self.nom} ({self.get_type_rapport_display()})"

class HistoriqueGeneration(models.Model):
    """Historique des tentatives de génération de rapports"""
    
    rapport = models.ForeignKey(RapportPDF, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=50)  # 'generation', 'regeneration', 'telechargement'
    statut = models.CharField(max_length=20)  # 'succes', 'erreur', 'en_cours'
    message = models.TextField(blank=True)
    temps_execution = models.DurationField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Historique de génération"
        verbose_name_plural = "Historiques de génération"
    
    def __str__(self):
        return f"{self.rapport.titre} - {self.action} ({self.statut})"
