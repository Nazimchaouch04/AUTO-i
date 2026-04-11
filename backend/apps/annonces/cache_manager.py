from django.core.cache import cache
from django.db.models import Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from .models import Annonce, Favori
from .models_advanced import StatistiqueAnnonce
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Gestionnaire de cache pour optimiser les performances"""
    
    CACHE_TIMEOUTS = {
        'market_stats': 300,      # 5 minutes
        'popular_annonces': 600,  # 10 minutes
        'user_recommendations': 1800,  # 30 minutes
        'search_suggestions': 900,  # 15 minutes
        'trending_marques': 600,   # 10 minutes
        'price_ranges': 1800,     # 30 minutes
    }
    
    @staticmethod
    def get_market_stats():
        """Récupère les statistiques du marché avec cache"""
        cache_key = 'market_stats'
        stats = cache.get(cache_key)
        
        if stats is None:
            try:
                stats = Annonce.objects.filter(est_active=True).aggregate(
                    total_annonces=Count('id'),
                    prix_moyen=Avg('prix'),
                    prix_min=Avg('prix'),
                    prix_max=Avg('prix'),
                    bonnes_affaires=Count('id', filter=models.Q(est_bonne_affaire=True))
                )
                
                # Formater les prix
                if stats['prix_moyen']:
                    stats['prix_moyen_formate'] = f"{int(stats['prix_moyen']):,}€".replace(',', ' ')
                if stats['prix_min']:
                    stats['prix_min_formate'] = f"{int(stats['prix_min']):,}€".replace(',', ' ')
                if stats['prix_max']:
                    stats['prix_max_formate'] = f"{int(stats['prix_max']):,}€".replace(',', ' ')
                
                # Mettre en cache
                cache.set(cache_key, stats, CacheManager.CACHE_TIMEOUTS['market_stats'])
                
            except Exception as e:
                logger.error(f"Erreur lors du calcul des stats marché: {e}")
                stats = {}
        
        return stats
    
    @staticmethod
    def get_popular_annonces(limit=10):
        """Récupère les annonces populaires avec cache"""
        cache_key = f'popular_annonces_{limit}'
        annonces = cache.get(cache_key)
        
        if annonces is None:
            try:
                annonces = list(
                    Annonce.objects.filter(
                        est_active=True,
                        date_publication__gte=timezone.now() - timedelta(days=7)
                    ).annotate(
                        score_popularite=F('vues') + F('sauvegardes') * 3 + F('contacts') * 2
                    ).order_by('-score_popularite', '-score_affaire')[:limit]
                )
                
                cache.set(cache_key, annonces, CacheManager.CACHE_TIMEOUTS['popular_annonces'])
                
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des annonces populaires: {e}")
                annonces = []
        
        return annonces
    
    @staticmethod
    def get_trending_marques(limit=10):
        """Récupère les marques tendances avec cache"""
        cache_key = f'trending_marques_{limit}'
        marques = cache.get(cache_key)
        
        if marques is None:
            try:
                marques = list(
                    Annonce.objects.filter(
                        est_active=True,
                        date_publication__gte=timezone.now() - timedelta(days=30)
                    ).values('vehicule__marque')
                    .annotate(
                        nombre=Count('id'),
                        prix_moyen=Avg('prix')
                    )
                    .order_by('-nombre')[:limit]
                )
                
                cache.set(cache_key, marques, CacheManager.CACHE_TIMEOUTS['trending_marques'])
                
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des marques tendances: {e}")
                marques = []
        
        return marques
    
    @staticmethod
    def get_price_ranges():
        """Récupère les fourchettes de prix avec cache"""
        cache_key = 'price_ranges'
        ranges = cache.get(cache_key)
        
        if ranges is None:
            try:
                # Calculer les fourchettes de prix
                prix_stats = Annonce.objects.filter(est_active=True).aggregate(
                    min_price=models.Min('prix'),
                    max_price=models.Max('prix'),
                    avg_price=models.Avg('prix')
                )
                
                if prix_stats['min_price'] and prix_stats['max_price']:
                    min_price = float(prix_stats['min_price'])
                    max_price = float(prix_stats['max_price'])
                    avg_price = float(prix_stats['avg_price'])
                    
                    # Créer 5 fourchettes
                    step = (max_price - min_price) / 5
                    
                    ranges = []
                    for i in range(5):
                        range_min = min_price + (i * step)
                        range_max = min_price + ((i + 1) * step)
                        
                        count = Annonce.objects.filter(
                            est_active=True,
                            prix__gte=range_min,
                            prix__lt=range_max
                        ).count()
                        
                        ranges.append({
                            'min': round(range_min),
                            'max': round(range_max),
                            'count': count,
                            'label': f"{int(range_min):,}€ - {int(range_max):,}€".replace(',', ' ')
                        })
                    
                    cache.set(cache_key, ranges, CacheManager.CACHE_TIMEOUTS['price_ranges'])
                else:
                    ranges = []
                
            except Exception as e:
                logger.error(f"Erreur lors du calcul des fourchettes de prix: {e}")
                ranges = []
        
        return ranges
    
    @staticmethod
    def get_user_recommendations(user_id, limit=10):
        """Récupère les recommandations utilisateur avec cache"""
        cache_key = f'user_recommendations_{user_id}_{limit}'
        recommendations = cache.get(cache_key)
        
        if recommendations is None:
            try:
                from .services import RecommendationEngine
                from django.contrib.auth.models import User
                
                user = User.objects.get(id=user_id)
                engine = RecommendationEngine(user)
                recommendations = engine.get_recommendations(limit)
                
                cache.set(cache_key, recommendations, CacheManager.CACHE_TIMEOUTS['user_recommendations'])
                
            except Exception as e:
                logger.error(f"Erreur lors de la génération des recommandations: {e}")
                recommendations = []
        
        return recommendations
    
    @staticmethod
    def get_search_suggestions(partial_query):
        """Récupère les suggestions de recherche avec cache"""
        cache_key = f'search_suggestions_{partial_query.lower()}'
        suggestions = cache.get(cache_key)
        
        if suggestions is None:
            try:
                from .services import SearchService
                suggestions = SearchService.get_suggestions(partial_query)
                
                cache.set(cache_key, suggestions, CacheManager.CACHE_TIMEOUTS['search_suggestions'])
                
            except Exception as e:
                logger.error(f"Erreur lors de la génération des suggestions: {e}")
                suggestions = {'marques': [], 'modeles': [], 'villes': []}
        
        return suggestions
    
    @staticmethod
    def invalidate_annonce_cache(annonce_id=None):
        """Invalide les caches liés aux annonces"""
        patterns = [
            'market_stats',
            'popular_annonces_*',
            'trending_marques_*',
            'price_ranges',
        ]
        
        for pattern in patterns:
            if '*' in pattern:
                # Invalider tous les caches correspondant au pattern
                cache.delete_many(cache.keys(pattern))
            else:
                cache.delete(pattern)
        
        # Invalider les recommandations de tous les utilisateurs
        # (plus agressif mais nécessaire pour la cohérence)
        cache.delete_many(cache.keys('user_recommendations_*'))
        
        logger.info(f"Cache invalidé pour annonce_id: {annonce_id}")
    
    @staticmethod
    def invalidate_user_cache(user_id):
        """Invalide les caches d'un utilisateur spécifique"""
        patterns = [
            f'user_recommendations_{user_id}_*',
        ]
        
        for pattern in patterns:
            cache.delete_many(cache.keys(pattern))
        
        logger.info(f"Cache utilisateur invalidé pour user_id: {user_id}")
    
    @staticmethod
    def warm_up_cache():
        """Préchauffe le cache avec les données les plus courantes"""
        try:
            logger.info("Début du préchauffage du cache...")
            
            # Préchauffer les statistiques du marché
            CacheManager.get_market_stats()
            
            # Préchauffer les annonces populaires
            CacheManager.get_popular_annonces(20)
            
            # Préchauffer les marques tendances
            CacheManager.get_trending_marques(15)
            
            # Préchauffer les fourchettes de prix
            CacheManager.get_price_ranges()
            
            logger.info("Préchauffage du cache terminé")
            
        except Exception as e:
            logger.error(f"Erreur lors du préchauffage du cache: {e}")


class CacheMiddleware:
    """Middleware pour la gestion automatique du cache"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Invalider le cache si nécessaire
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if request.path.startswith('/api/annonces/'):
                CacheManager.invalidate_annonce_cache()
            elif request.user.is_authenticated and 'favoris' in request.path:
                CacheManager.invalidate_user_cache(request.user.id)
        
        return response


def cache_view_result(timeout=300):
    """Décorateur pour mettre en cache les résultats des vues"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Générer une clé de cache unique
            cache_key = f"view_{view_func.__name__}_{hash(str(request.GET))}_{request.user.id if request.user.is_authenticated else 'anonymous'}"
            
            # Essayer de récupérer depuis le cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Exécuter la vue
            result = view_func(request, *args, **kwargs)
            
            # Mettre en cache le résultat
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator
