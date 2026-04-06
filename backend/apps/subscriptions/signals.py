from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Abonnement, Plan


@receiver(post_save, sender=User)
def create_free_subscription(sender, instance, created, **kwargs):
    """Crée ou récupère un abonnement gratuit pour tout nouvel utilisateur"""
    if created:
        free_plan = Plan.objects.get(nom='free')
        Abonnement.objects.get_or_create(user=instance, defaults={'plan': free_plan})
