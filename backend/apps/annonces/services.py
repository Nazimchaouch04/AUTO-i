from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from .models import Annonce, Favori, RechercheSauvegardee
from .models_advanced import HistoriqueRecherche, VisiteAnnonce, ContactVendeur
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Moteur de recommandations intelligent pour les annonces"""
    
    def __init__(self, user):
        self.user = user
    
    def get_recommendations(self, limit=10):
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        # 1. Recommandations basées sur l'historique de navigation
        nav_recs = self._get_navigation_based_recommendations(limit=3)
        recommendations.extend(nav_recs)
        
        # 2. Recommandations basées sur les favoris
        fav_recs = self._get_favorites_based_recommendations(limit=3)
        recommendations.extend(fav_recs)
        
        # 3. Recommandations basées sur les recherches
        search_recs = self._get_search_based_recommendations(limit=3)
        recommendations.extend(search_recs)
        
        # 4. Recommandations basées sur les contacts
        contact_recs = self._get_contact_based_recommendations(limit=2)
        recommendations.extend(contact_recs)
        
        # 5. Recommandations populaires (fallback)
        if len(recommendations) < limit:
            popular_recs = self._get_popular_recommendations(limit - len(recommendations))
            recommendations.extend(popular_recs)
        
        # Éliminer les doublons et limiter
        unique_recs = []
        seen_ids = set()
        
        for rec in recommendations:
            if rec['id'] not in seen_ids:
                unique_recs.append(rec)
                seen_ids.add(rec['id'])
        
        return unique_recs[:limit]
    
    def _get_navigation_based_recommendations(self, limit=3):
        """Recommandations basées sur les annonces visitées"""
        try:
            # Récupérer les marques et modèles les plus visités
            visites = VisiteAnnonce.objects.filter(
                utilisateur=self.user,
                date_visite__gte=timezone.now() - timedelta(days=30)
            ).select_related('annonce__vehicule')
            
            if not visites.exists():
                return []
            
            # Extraire les marques et modèles préférés
            marques = list(visites.values_list('annonce__vehicule__marque', flat=True).distinct())
            modeles = list(visites.values_list('annonce__vehicule__modele', flat=True).distinct())
            
            # Trouver des annonces similaires
            similar_annonces = Annonce.objects.filter(
                Q(vehicule__marque__in=marques) | Q(vehicule__modele__in=modeles),
                est_active=True
            ).exclude(
                id__in=visites.values('annonce__id')
            ).select_related('vehicule')[:limit]
            
            return [
                {
                    'id': str(annonce.id),
                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                    'marque': annonce.vehicule.marque,
                    'modele': annonce.vehicule.modele,
                    'prix': annonce.prix,
                    'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                    'ville': annonce.ville,
                    'images': annonce.images,
                    'score_affaire': annonce.score_affaire,
                    'raison': 'Basé sur vos visites récentes',
                    'type': 'navigation'
                }
                for annonce in similar_annonces
            ]
            
        except Exception as e:
            logger.error(f"Erreur dans navigation_based_recommendations: {e}")
            return []
    
    def _get_favorites_based_recommendations(self, limit=3):
        """Recommandations basées sur les favoris"""
        try:
            favoris = Favori.objects.filter(
                user=self.user
            ).select_related('annonce__vehicule')
            
            if not favoris.exists():
                return []
            
            # Extraire les caractéristiques des favoris
            marques = list(favoris.values_list('annonce__vehicule__marque', flat=True).distinct())
            prix_moyen = favoris.aggregate(avg_prix=Avg('annonce__prix'))['avg_prix'] or 0
            
            # Trouver des annonces similaires
            similar_annonces = Annonce.objects.filter(
                vehicule__marque__in=marques,
                prix__lte=prix_moyen * 1.2,  # 20% plus cher maximum
                prix__gte=prix_moyen * 0.8,  # 20% moins cher minimum
                est_active=True
            ).exclude(
                id__in=favoris.values('annonce__id')
            ).select_related('vehicule')[:limit]
            
            return [
                {
                    'id': str(annonce.id),
                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                    'marque': annonce.vehicule.marque,
                    'modele': annonce.vehicule.modele,
                    'prix': annonce.prix,
                    'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                    'ville': annonce.ville,
                    'images': annonce.images,
                    'score_affaire': annonce.score_affaire,
                    'raison': 'Similaire à vos favoris',
                    'type': 'favoris'
                }
                for annonce in similar_annonces
            ]
            
        except Exception as e:
            logger.error(f"Erreur dans favorites_based_recommendations: {e}")
            return []
    
    def _get_search_based_recommendations(self, limit=3):
        """Recommandations basées sur l'historique de recherche"""
        try:
            recherches = HistoriqueRecherche.objects.filter(
                user=self.user,
                date_recherche__gte=timezone.now() - timedelta(days=30)
            ).order_by('-date_recherche')[:5]
            
            if not recherches.exists():
                return []
            
            recommendations = []
            
            for recherche in recherches:
                # Reconstruire la recherche
                queryset = Annonce.objects.filter(est_active=True)
                
                filtres = recherche.filtres
                if filtres.get('marque'):
                    queryset = queryset.filter(vehicule__marque__icontains=filtres['marque'])
                if filtres.get('prix_max'):
                    queryset = queryset.filter(prix__lte=filtres['prix_max'])
                if filtres.get('km_max'):
                    queryset = queryset.filter(kilometrage__lte=filtres['km_max'])
                
                annonces = queryset.select_related('vehicule')[:2]
                
                for annonce in annonces:
                    recommendations.append({
                        'id': str(annonce.id),
                        'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                        'marque': annonce.vehicule.marque,
                        'modele': annonce.vehicule.modele,
                        'prix': annonce.prix,
                        'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                        'ville': annonce.ville,
                        'images': annonce.images,
                        'score_affaire': annonce.score_affaire,
                        'raison': f'Basé sur votre recherche "{recherche.terme}"',
                        'type': 'recherche'
                    })
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Erreur dans search_based_recommendations: {e}")
            return []
    
    def _get_contact_based_recommendations(self, limit=2):
        """Recommandations basées sur les contacts effectués"""
        try:
            contacts = ContactVendeur.objects.filter(
                acheteur_potentiel=self.user
            ).select_related('annonce__vehicule')
            
            if not contacts.exists():
                return []
            
            # Analyser les caractéristiques des annonces contactées
            prix_moyen = contacts.aggregate(avg_prix=Avg('annonce__prix'))['avg_prix'] or 0
            marques = list(contacts.values_list('annonce__vehicule__marque', flat=True).distinct())
            
            # Trouver des annonces similaires
            similar_annonces = Annonce.objects.filter(
                Q(vehicule__marque__in=marques) | Q(prix__lte=prix_moyen * 1.15),
                est_active=True
            ).exclude(
                id__in=contacts.values('annonce__id')
            ).select_related('vehicule')[:limit]
            
            return [
                {
                    'id': str(annonce.id),
                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                    'marque': annonce.vehicule.marque,
                    'modele': annonce.vehicule.modele,
                    'prix': annonce.prix,
                    'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                    'ville': annonce.ville,
                    'images': annonce.images,
                    'score_affaire': annonce.score_affaire,
                    'raison': 'Similaire aux annonces que vous avez contactées',
                    'type': 'contact'
                }
                for annonce in similar_annonces
            ]
            
        except Exception as e:
            logger.error(f"Erreur dans contact_based_recommendations: {e}")
            return []
    
    def _get_popular_recommendations(self, limit=5):
        """Recommandations populaires (fallback)"""
        try:
            # Annonces populaires basées sur les vues et les favoris
            popular_annonces = Annonce.objects.filter(
                est_active=True,
                date_publication__gte=timezone.now() - timedelta(days=7)
            ).annotate(
                score_popularite=F('vues') + F('sauvegardes') * 3 + F('contacts') * 2
            ).order_by('-score_popularite', '-score_affaire')[:limit]
            
            return [
                {
                    'id': str(annonce.id),
                    'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                    'marque': annonce.vehicule.marque,
                    'modele': annonce.vehicule.modele,
                    'prix': annonce.prix,
                    'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                    'ville': annonce.ville,
                    'images': annonce.images,
                    'score_affaire': annonce.score_affaire,
                    'raison': 'Populaire cette semaine',
                    'type': 'populaire'
                }
                for annonce in popular_annonces
            ]
            
        except Exception as e:
            logger.error(f"Erreur dans popular_recommendations: {e}")
            return []


class SearchService:
    """Service de recherche avancée"""
    
    @staticmethod
    def advanced_search(query_params, user=None):
        """Recherche avancée avec filtres multiples"""
        queryset = Annonce.objects.filter(est_active=True)
        
        # Enregistrer la recherche si utilisateur connecté
        if user:
            terme = query_params.get('recherche', '')
            filtres = {k: v for k, v in query_params.items() if k != 'recherche' and v}
            
            HistoriqueRecherche.objects.create(
                user=user,
                terme=terme,
                filtres=filtres,
                nombre_resultats=queryset.count()
            )
        
        # Appliquer les filtres
        if query_params.get('recherche'):
            search_term = query_params['recherche']
            queryset = queryset.filter(
                Q(vehicule__marque__icontains=search_term) |
                Q(vehicule__modele__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(ville__icontains=search_term)
            )
        
        # Filtres de prix
        if query_params.get('prix_min'):
            queryset = queryset.filter(prix__gte=query_params['prix_min'])
        if query_params.get('prix_max'):
            queryset = queryset.filter(prix__lte=query_params['prix_max'])
        
        # Filtres de kilométrage
        if query_params.get('km_min'):
            queryset = queryset.filter(kilometrage__gte=query_params['km_min'])
        if query_params.get('km_max'):
            queryset = queryset.filter(kilometrage__lte=query_params['km_max'])
        
        # Filtres d'année
        if query_params.get('annee_min'):
            queryset = queryset.filter(annee__gte=query_params['annee_min'])
        if query_params.get('annee_max'):
            queryset = queryset.filter(annee__lte=query_params['annee_max'])
        
        # Filtres techniques
        if query_params.get('marque'):
            queryset = queryset.filter(vehicule__marque__icontains=query_params['marque'])
        if query_params.get('modele'):
            queryset = queryset.filter(vehicule__modele__icontains=query_params['modele'])
        if query_params.get('carburant'):
            queryset = queryset.filter(carburant=query_params['carburant'])
        if query_params.get('boite'):
            queryset = queryset.filter(boite=query_params['boite'])
        
        # Filtres géographiques
        if query_params.get('pays'):
            queryset = queryset.filter(pays=query_params['pays'])
        if query_params.get('ville'):
            queryset = queryset.filter(ville__icontains=query_params['ville'])
        
        # Filtres spéciaux
        if query_params.get('bonnes_affaires') == 'true':
            queryset = queryset.filter(est_bonne_affaire=True)
        if query_params.get('urgence') == 'true':
            queryset = queryset.filter(score_affaire__gte=70)
        
        # Tri
        tri = query_params.get('tri', '-date_publication')
        if tri == 'prix_croissant':
            queryset = queryset.order_by('prix')
        elif tri == 'prix_decroissant':
            queryset = queryset.order_by('-prix')
        elif tri == 'km_croissant':
            queryset = queryset.order_by('kilometrage')
        elif tri == 'km_decroissant':
            queryset = queryset.order_by('-kilometrage')
        elif tri == 'annee_croissant':
            queryset = queryset.order_by('annee')
        elif tri == 'annee_decroissant':
            queryset = queryset.order_by('-annee')
        elif tri == 'score_affaire':
            queryset = queryset.order_by('-score_affaire')
        elif tri == 'popularite':
            queryset = queryset.annotate(
                score_popularite=F('vues') + F('sauvegardes') * 3
            ).order_by('-score_popularite')
        else:
            queryset = queryset.order_by('-date_publication')
        
        return queryset.select_related('vehicule').prefetch_related('favoris_selectionnes')
    
    @staticmethod
    def get_suggestions(partial_query):
        """Obtenir des suggestions de recherche automatique"""
        suggestions = {
            'marques': [],
            'modeles': [],
            'villes': []
        }
        
        if len(partial_query) < 2:
            return suggestions
        
        # Suggestions de marques
        marques = Annonce.objects.filter(
            vehicule__marque__icontains=partial_query
        ).values_list('vehicule__marque', flat=True).distinct()[:5]
        suggestions['marques'] = list(marques)
        
        # Suggestions de modèles
        modeles = Annonce.objects.filter(
            vehicule__modele__icontains=partial_query
        ).values_list('vehicule__modele', flat=True).distinct()[:5]
        suggestions['modeles'] = list(modeles)
        
        # Suggestions de villes
        villes = Annonce.objects.filter(
            ville__icontains=partial_query
        ).values_list('ville', flat=True).distinct()[:5]
        suggestions['villes'] = list(villes)
        
        return suggestions


class AnalyticsService:
    """Service d'analytics pour les annonces"""
    
    @staticmethod
    def update_annonce_stats(annonce):
        """Met à jour les statistiques d'une annonce"""
        from .models_advanced import StatistiqueAnnonce
        
        stats, created = StatistiqueAnnonce.objects.get_or_create(
            annonce=annonce,
            defaults={
                'vues_totales': annonce.vues,
                'contacts_totales': annonce.contacts,
                'sauvegardes_totales': annonce.sauvegardes,
            }
        )
        
        if not created:
            stats.vues_totales = annonce.vues
            stats.contacts_totales = annonce.contacts
            stats.sauvegardes_totales = annonce.sauvegardes
            stats.save()
    
    @staticmethod
    def get_market_trends(days=30):
        """Obtenir les tendances du marché"""
        from django.db.models.functions import TruncDay
        
        date_debut = timezone.now() - timedelta(days=days)
        
        # Prix moyen par jour
        prix_moyen_journalier = (
            Annonce.objects.filter(
                date_publication__gte=date_debut,
                est_active=True
            ).annotate(
                date=TruncDay('date_publication')
            ).values('date')
            .annotate(prix_moyen=Avg('prix'))
            .order_by('date')
        )
        
        # Nombre d'annonces par jour
        annonces_journalieres = (
            Annonce.objects.filter(
                date_publication__gte=date_debut,
                est_active=True
            ).annotate(
                date=TruncDay('date_publication')
            ).values('date')
            .annotate(nombre=Count('id'))
            .order_by('date')
        )
        
        # Top marques
        top_marques = (
            Annonce.objects.filter(
                est_active=True,
                date_publication__gte=date_debut
            ).values('vehicule__marque')
            .annotate(nombre=Count('id'), prix_moyen=Avg('prix'))
            .order_by('-nombre')[:10]
        )
        
        return {
            'prix_moyen_journalier': list(prix_moyen_journalier),
            'annonces_journalieres': list(annonces_journalieres),
            'top_marques': list(top_marques),
        }
