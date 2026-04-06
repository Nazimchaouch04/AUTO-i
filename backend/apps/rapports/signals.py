from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import RapportPDF

@receiver(post_save, sender=RapportPDF)
def rapport_post_save(sender, instance, created, **kwargs):
    """Signal pour les actions après sauvegarde de rapport"""
    if created:
        # Log la création d'un nouveau rapport
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Nouveau rapport créé: {instance.id} - {instance.titre} par {instance.user.username}")
        
        # Définit la date d'expiration si non définie
        if not instance.expire_at:
            instance.expire_at = timezone.now() + timezone.timedelta(days=30)
            instance.save(update_fields=['expire_at'])
