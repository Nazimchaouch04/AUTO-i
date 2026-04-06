from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Alerte, ResultatAlerte
from apps.notifications.telegram_service import envoyer_message_telegram, formater_alerte_telegram
from apps.notifications.whatsapp_service import envoyer_whatsapp, formater_alerte_whatsapp
from apps.notifications.models import CanalNotification, NotificationHistory
import logging

logger = logging.getLogger(__name__)

@shared_task(name='alertes.check_alertes')
def check_alertes_task():
    """Vérifie les alertes et envoie les notifications."""
    alertes = Alerte.objects.filter(is_active=True)
    notifs_envoyees = 0
    erreurs = 0

    for alerte in alertes:
        try:
            # Cherche nouvelles annonces correspondantes
            qs = _build_annonce_query(alerte)
            
            # Seulement les nouvelles annonces (dernières 6h)
            qs = qs.filter(date_collecte__gte=timezone.now() - timedelta(hours=6))

            # Exclut déjà notifiées
            deja_notifies = ResultatAlerte.objects.filter(
                alerte=alerte).values_list('annonce_id', flat=True)
            qs = qs.exclude(id__in=deja_notifies)

            # Limite à 5 annonces par alerte pour éviter le spam
            nouvelles_annonces = qs[:5]

            # Récupère les canaux de notification de l'utilisateur
            canaux = CanalNotification.objects.filter(
                user=alerte.user, 
                is_active=True, 
                is_verified=True
            )

            if not canaux.exists():
                logger.warning(f"Aucun canal de notification actif pour l'utilisateur {alerte.user.username}")
                continue

            # Envoie les notifications pour chaque nouvelle annonce
            for annonce in nouvelles_annonces:
                # Crée le résultat d'alerte
                resultat = ResultatAlerte.objects.create(alerte=alerte, annonce=annonce)
                
                # Envoie sur chaque canal configuré
                for canal in canaux:
                    try:
                        if canal.canal == 'telegram':
                            msg = formater_alerte_telegram(annonce, alerte)
                            success = envoyer_message_telegram(canal.valeur, msg)
                            _create_notification_history(canal, annonce, alerte, msg, success)
                            
                        elif canal.canal == 'whatsapp':
                            msg = formater_alerte_whatsapp(annonce, alerte)
                            success = envoyer_whatsapp(canal.valeur, msg)
                            _create_notification_history(canal, annonce, alerte, msg, success)
                        
                        if success:
                            notifs_envoyees += 1
                        else:
                            erreurs += 1
                            
                    except Exception as e:
                        logger.error(f"Erreur envoi notification {canal.canal}: {e}")
                        erreurs += 1

        except Exception as e:
            logger.error(f"Erreur traitement alerte {alerte.id}: {e}")
            erreurs += 1

    logger.info(f"Vérification alertes terminée: {notifs_envoyees} notifications envoyées, {erreurs} erreurs")
    return f'{notifs_envoyees} notifications envoyées, {erreurs} erreurs'

def _build_annonce_query(alerte):
    """Construit la requête pour les annonces correspondant à l'alerte."""
    from apps.annonces.models import Annonce
    
    qs = Annonce.objects.filter(est_active=True)
    
    if alerte.marque:
        qs = qs.filter(vehicule__marque__iexact=alerte.marque)
    
    if alerte.modele:
        qs = qs.filter(vehicule__modele__iexact=alerte.modele)
    
    if alerte.prix_max:
        qs = qs.filter(prix__lte=alerte.prix_max)
    
    if alerte.km_max:
        qs = qs.filter(kilometrage__lte=alerte.km_max)
    
    if alerte.pays:
        qs = qs.filter(pays=alerte.pays)
    
    if alerte.ville:
        qs = qs.filter(ville__iexact=alerte.ville)
    
    if alerte.annee_min:
        qs = qs.filter(annee__gte=alerte.annee_min)
    
    if alerte.annee_max:
        qs = qs.filter(annee__lte=alerte.annee_max)
    
    if alerte.carburant:
        qs = qs.filter(carburant__iexact=alerte.carburant)
    
    if alerte.boite:
        qs = qs.filter(boite__iexact=alerte.boite)
    
    if alerte.bonnes_affaires_only:
        qs = qs.filter(est_bonne_affaire=True)
    
    return qs

def _create_notification_history(canal, annonce, alerte, message, success):
    """Crée un enregistrement dans l'historique des notifications."""
    try:
        NotificationHistory.objects.create(
            canal=canal,
            alerte=alerte,
            annonce=annonce,
            contenu=message,
            statut='sent' if success else 'failed',
            sent_at=timezone.now() if success else None
        )
    except Exception as e:
        logger.error(f"Erreur création historique notification: {e}")

@shared_task(name='alertes.nettoyer_anciens_resultats')
def nettoyer_anciens_resultats():
    """Nettoie les anciens résultats d'alertes (plus de 30 jours)."""
    date_limite = timezone.now() - timedelta(days=30)
    
    deleted_count = ResultatAlerte.objects.filter(
        created_at__lt=date_limite
    ).delete()[0]
    
    logger.info(f"Nettoyage terminé: {deleted_count} anciens résultats supprimés")
    return f'{deleted_count} résultats supprimés'

@shared_task(name='notifications.nettoyer_historique')
def nettoyer_historique_notifications():
    """Nettoie l'historique des notifications (plus de 90 jours)."""
    date_limite = timezone.now() - timedelta(days=90)
    
    deleted_count = NotificationHistory.objects.filter(
        created_at__lt=date_limite
    ).delete()[0]
    
    logger.info(f"Nettoyage historique terminé: {deleted_count} notifications supprimées")
    return f'{deleted_count} notifications supprimées'
