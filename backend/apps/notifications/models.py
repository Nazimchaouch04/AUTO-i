from django.db import models
from django.contrib.auth.models import User

class CanalNotification(models.Model):
    CANAL_CHOICES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='canaux_notification')
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES)
    valeur = models.CharField(max_length=200, help_text="Email, Chat ID Telegram ou numéro WhatsApp")
    is_verified = models.BooleanField(default=False, help_text="Le canal a été vérifié")
    is_active = models.BooleanField(default=True, help_text="Le canal est actif pour les notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'canal']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_canal_display()} - {self.valeur}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.canal == 'email':
            from django.core.validators import validate_email
            try:
                validate_email(self.valeur)
            except:
                raise ValidationError("Email invalide")
        elif self.canal == 'whatsapp':
            # Format international : +213xxxxxxxxx
            if not self.valeur.startswith('+'):
                raise ValidationError("Le numéro WhatsApp doit commencer par + (ex: +213)")
            if not self.valeur.replace('+', '').isdigit():
                raise ValidationError("Le numéro WhatsApp ne doit contenir que des chiffres")

class NotificationHistory(models.Model):
    """Historique des notifications envoyées"""
    STATUT_CHOICES = [
        ('sent', 'Envoyé'),
        ('failed', 'Échec'),
        ('pending', 'En attente'),
    ]
    
    canal = models.ForeignKey(CanalNotification, on_delete=models.CASCADE,
                               related_name='historique')
    alerte = models.ForeignKey('alertes.Alerte', on_delete=models.CASCADE,
                                null=True, blank=True)
    annonce = models.ForeignKey('annonces.Annonce', on_delete=models.CASCADE,
                                null=True, blank=True)
    contenu = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='pending')
    erreur_message = models.TextField(blank=True, null=True)
    is_lu = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification {self.get_statut_display()} - {self.canal.canal}"
