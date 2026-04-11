from celery import shared_task
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Annonce, Favori
from .models_advanced import (
    NotificationAnnonce, AlerteRecherche, HistoriqueRecherche,
    ContactVendeur, EvaluationVendeur
)
from .services import RecommendationEngine, SearchService
from .cache_manager import CacheManager
import logging

logger = logging.getLogger(__name__)


@shared_task(name='annonces.update_recommendations')
def update_user_recommendations():
    """Met à jour les recommandations pour tous les utilisateurs actifs"""
    try:
        # Récupérer les utilisateurs actifs (connectés dans les 30 derniers jours)
        date_limite = timezone.now() - timedelta(days=30)
        utilisateurs_actifs = User.objects.filter(
            last_login__gte=date_limite
        ).prefetch_related('favoris')
        
        total_mis_a_jour = 0
        
        for user in utilisateurs_actifs:
            try:
                # Générer les recommandations
                engine = RecommendationEngine(user)
                recommendations = engine.get_recommendations(10)
                
                # Mettre en cache
                cache_key = f'user_recommendations_{user.id}_10'
                cache.set(cache_key, recommendations, 1800)  # 30 minutes
                
                total_mis_a_jour += 1
                
            except Exception as e:
                logger.error(f"Erreur mise à jour recommandations utilisateur {user.id}: {e}")
                continue
        
        logger.info(f"Recommandations mises à jour pour {total_mis_a_jour} utilisateurs")
        return f"{total_mis_a_jour} recommandations mises à jour"
        
    except Exception as e:
        logger.error(f"Erreur dans update_user_recommendations: {e}")
        return "Erreur lors de la mise à jour des recommandations"


@shared_task(name='annonces.process_alertes')
def process_alertes_recherche():
    """Traite les alertes de recherche et envoie des notifications"""
    try:
        alertes_actives = AlerteRecherche.objects.filter(
            est_active=True
        ).select_related('user')
        
        notifications_envoyees = 0
        
        for alerte in alertes_actives:
            try:
                # Vérifier si une notification a déjà été envoyée récemment
                if alerte.derniere_notification:
                    temps_ecoule = timezone.now() - alerte.derniere_notification
                    if alerte.frequence == 'quotidien' and temps_ecoule < timedelta(days=1):
                        continue
                    elif alerte.frequence == 'hebdomadaire' and temps_ecoule < timedelta(weeks=1):
                        continue
                
                # Appliquer les filtres de l'alerte
                queryset = Annonce.objects.filter(est_active=True)
                filtres = alerte.filtres
                
                # Appliquer les filtres
                if filtres.get('marque'):
                    queryset = queryset.filter(vehicule__marque__icontains=filtres['marque'])
                if filtres.get('prix_max'):
                    queryset = queryset.filter(prix__lte=filtres['prix_max'])
                if filtres.get('km_max'):
                    queryset = queryset.filter(kilometrage__lte=filtres['km_max'])
                if filtres.get('annee_min'):
                    queryset = queryset.filter(annee__gte=filtres['annee_min'])
                if filtres.get('carburant'):
                    queryset = queryset.filter(carburant=filtres['carburant'])
                if filtres.get('pays'):
                    queryset = queryset.filter(pays=filtres['pays'])
                
                # Uniquement les annonces récentes
                date_limite = timezone.now() - timedelta(days=1)
                if alerte.derniere_notification:
                    date_limite = alerte.derniere_notification
                
                nouvelles_annonces = queryset.filter(
                    date_publication__gte=date_limite
                ).order_by('-date_publication')[:5]
                
                if nouvelles_annonces.exists():
                    # Créer une notification
                    notification = NotificationAnnonce.objects.create(
                        utilisateur=alerte.user,
                        type_notification='nouvelle_annonce',
                        titre=f'Nouvelles annonces: {alerte.nom}',
                        message=f'{nouvelles_annonces.count()} nouvelle(s) annonce(s) correspondent à votre alerte "{alerte.nom}"',
                        donnees_supplementaires={
                            'alerte_id': alerte.id,
                            'nombre_annonces': nouvelles_annonces.count(),
                            'annonces': [
                                {
                                    'id': str(annonce.id),
                                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                                    'prix': float(annonce.prix)
                                }
                                for annonce in nouvelles_annonces
                            ]
                        }
                    )
                    
                    # Mettre à jour la date de dernière notification
                    alerte.derniere_notification = timezone.now()
                    alerte.nombre_resultats = nouvelles_annonces.count()
                    alerte.save()
                    
                    notifications_envoyees += 1
                
            except Exception as e:
                logger.error(f"Erreur traitement alerte {alerte.id}: {e}")
                continue
        
        logger.info(f"{notifications_envoyees} notifications d'alertes envoyées")
        return f"{notifications_envoyees} notifications envoyées"
        
    except Exception as e:
        logger.error(f"Erreur dans process_alertes_recherche: {e}")
        return "Erreur lors du traitement des alertes"


@shared_task(name='annonces.update_statistics')
def update_annonce_statistics():
    """Met à jour les statistiques des annonces"""
    try:
        # Récupérer les annonces actives
        annonces = Annonce.objects.filter(est_active=True)
        
        total_mises_a_jour = 0
        
        for annonce in annonces:
            try:
                # Mettre à jour les statistiques
                from .cache_manager import CacheManager
                CacheManager.update_annonce_stats(annonce)
                total_mises_a_jour += 1
                
            except Exception as e:
                logger.error(f"Erreur mise à jour stats annonce {annonce.id}: {e}")
                continue
        
        logger.info(f"Statistiques mises à jour pour {total_mises_a_jour} annonces")
        return f"{total_mises_a_jour} statistiques mises à jour"
        
    except Exception as e:
        logger.error(f"Erreur dans update_annonce_statistics: {e}")
        return "Erreur lors de la mise à jour des statistiques"


@shared_task(name='annonces.cleanup_old_data')
def cleanup_old_data():
    """Nettoie les anciennes données pour optimiser la base"""
    try:
        date_limite = timezone.now() - timedelta(days=90)
        
        # Nettoyer l'historique de recherche
        recherches_supprimees = HistoriqueRecherche.objects.filter(
            date_recherche__lt=date_limite
        ).count()
        HistoriqueRecherche.objects.filter(
            date_recherche__lt=date_limite
        ).delete()
        
        # Nettoyer les anciennes notifications lues
        notifications_supprimees = NotificationAnnonce.objects.filter(
            est_lue=True,
            date_creation__lt=date_limite
        ).count()
        NotificationAnnonce.objects.filter(
            est_lue=True,
            date_creation__lt=date_limite
        ).delete()
        
        logger.info(f"Nettoyage terminé: {recherches_supprimees} recherches, {notifications_supprimees} notifications supprimées")
        return f"Nettoyage effectué: {recherches_supprimees} recherches, {notifications_supprimees} notifications"
        
    except Exception as e:
        logger.error(f"Erreur dans cleanup_old_data: {e}")
        return "Erreur lors du nettoyage"


@shared_task(name='annonces.warm_cache')
def warm_cache_task():
    """Préchauffe le cache"""
    try:
        CacheManager.warm_up_cache()
        return "Cache préchauffé avec succès"
        
    except Exception as e:
        logger.error(f"Erreur dans warm_cache_task: {e}")
        return "Erreur lors du préchauffage du cache"


@shared_task(name='annonces.send_bonnes_affaires_notifications')
def send_bonnes_affaires_notifications():
    """Envoie des notifications pour les nouvelles bonnes affaires"""
    try:
        # Récupérer les nouvelles bonnes affaires (dernières 24h)
        date_limite = timezone.now() - timedelta(days=1)
        nouvelles_bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True,
            est_active=True,
            date_publication__gte=date_limite
        ).select_related('vehicule')
        
        if not nouvelles_bonnes_affaires.exists():
            return "Aucune nouvelle bonne affaire"
        
        # Récupérer les utilisateurs intéressés par les bonnes affaires
        utilisateurs_interesses = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=7)
        ).prefetch_related('favoris')
        
        notifications_envoyees = 0
        
        for user in utilisateurs_interesses:
            try:
                # Analyser les préférences de l'utilisateur
                marques_preferees = list(
                    user.favoris.all()
                    .values_list('annonce__vehicule__marque', flat=True)
                    .distinct()[:3]
                )
                
                # Filtrer les bonnes affaires selon les préférences
                affaires_pertinentes = nouvelles_bonnes_affaires.filter(
                    vehicule__marque__in=marques_preferees
                ) if marques_preferees else nouvelles_bonnes_affaires
                
                if affaires_pertinentes.exists():
                    # Créer une notification personnalisée
                    notification = NotificationAnnonce.objects.create(
                        utilisateur=user,
                        type_notification='bonne_affaire',
                        titre='🔥 Nouvelles bonnes affaires !',
                        message=f'{affaires_pertinentes.count()} bonne(s) affaire(s) détectée(s) selon vos préférences',
                        donnees_supplementaires={
                            'nombre_affaires': affaires_pertinentes.count(),
                            'affaires': [
                                {
                                    'id': str(annonce.id),
                                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                                    'prix': float(annonce.prix),
                                    'ecart_prix': annonce.ecart_prix,
                                    'score_affaire': annonce.score_affaire
                                }
                                for annonce in affaires_pertinentes
                            ]
                        }
                    )
                    
                    notifications_envoyees += 1
                
            except Exception as e:
                logger.error(f"Erreur notification bonnes affaires utilisateur {user.id}: {e}")
                continue
        
        logger.info(f"{notifications_envoyees} notifications de bonnes affaires envoyées")
        return f"{notifications_envoyees} notifications envoyées"
        
    except Exception as e:
        logger.error(f"Erreur dans send_bonnes_affaires_notifications: {e}")
        return "Erreur lors de l'envoi des notifications de bonnes affaires"


@shared_task(name='annonces.update_market_insights')
def update_market_insights():
    """Met à jour les insights du marché"""
    try:
        from .services import AnalyticsService
        
        # Générer les insights des 30 derniers jours
        insights = AnalyticsService.get_market_trends(30)
        
        # Mettre en cache pour un accès rapide
        cache_key = 'market_insights_30_days'
        cache.set(cache_key, insights, 3600)  # 1 heure
        
        logger.info("Insights du marché mis à jour")
        return "Insights du marché mis à jour avec succès"
        
    except Exception as e:
        logger.error(f"Erreur dans update_market_insights: {e}")
        return "Erreur lors de la mise à jour des insights"


# Configuration des tâches périodiques
from celery.schedules import crontab

# Planification des tâches
CELERYBEAT_SCHEDULE = {
    'update-recommendations': {
        'task': 'annonces.update_recommendations',
        'schedule': crontab(minute=0, hour='*/6'),  # Toutes les 6 heures
    },
    'process-alertes': {
        'task': 'annonces.process_alertes_recherche',
        'schedule': crontab(minute=0, hour='*/2'),  # Toutes les 2 heures
    },
    'update-statistics': {
        'task': 'annonces.update_annonce_statistics',
        'schedule': crontab(minute=0, hour='*/4'),  # Toutes les 4 heures
    },
    'cleanup-old-data': {
        'task': 'annonces.cleanup_old_data',
        'schedule': crontab(minute=0, hour=2, day_of_week=0),  # Dimanche à 2h
    },
    'warm-cache': {
        'task': 'annonces.warm_cache',
        'schedule': crontab(minute=0, hour='*/1'),  # Toutes les heures
    },
    'bonnes-affaires-notifications': {
        'task': 'annonces.send_bonnes_affaires_notifications',
        'schedule': crontab(minute=0, hour='*/3'),  # Toutes les 3 heures
    },
    'update-market-insights': {
        'task': 'annonces.update_market_insights',
        'schedule': crontab(minute=0, hour=6, day_of_week=1),  # Lundi à 6h
    },
}
