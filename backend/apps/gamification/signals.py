from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfilJoueur


@receiver(post_save, sender=User)
def create_profil_joueur(sender, instance, created, **kwargs):
    """Crée automatiquement un profil joueur pour tout nouvel utilisateur"""
    if created:
        ProfilJoueur.objects.create(user=instance, autocoin_balance=100)
