from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from apps.gamification.models import ProfilJoueur
from apps.subscriptions.models import Abonnement, Plan


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil utilisateur quand un User est créé"""
    if created:
        UserProfile.objects.create(user=instance)
        
        # Création du profil gamification (donne automatiquement 100 AC de base via le modèle)
        ProfilJoueur.objects.get_or_create(user=instance)
        
        # Création de l'abonnement gratuit par défaut
        try:
            free_plan, _ = Plan.objects.get_or_create(
                nom='free',
                defaults={
                    'prix_mensuel': 0,
                    'estimations_par_mois': 5,
                    'alertes_max': 2
                }
            )
            Abonnement.objects.get_or_create(user=instance, plan=free_plan)
        except Exception as e:
            # Sécurité en cas d'erreur DB
            pass
