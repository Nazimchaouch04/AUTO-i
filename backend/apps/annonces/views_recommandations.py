from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .services import RecommendationEngine, SearchService, AnalyticsService
from .models import Annonce, Favori
from .models_advanced import HistoriqueRecherche, NotificationAnnonce
from .serializers_advanced import AnnonceDetailSerializer, UserStatsSerializer


class RecommendationsView(APIView):
    """Vue pour les recommandations personnalisées"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            engine = RecommendationEngine(request.user)
            recommendations = engine.get_recommendations(limit)
            
            return Response({
                'recommendations': recommendations,
                'count': len(recommendations)
            })
        except Exception as e:
            return Response(
                {'error': 'Erreur lors de la génération des recommandations'},
                status=500
            )


class SearchSuggestionsView(APIView):
    """Vue pour les suggestions de recherche"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            query = request.query_params.get('q', '')
            suggestions = SearchService.get_suggestions(query)
            
            return Response(suggestions)
        except Exception as e:
            return Response(
                {'error': 'Erreur lors de la génération des suggestions'},
                status=500
            )


class SmartSearchView(APIView):
    """Vue pour la recherche intelligente"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Extraire tous les paramètres de recherche
            query_params = dict(request.query_params)
            
            # Effectuer la recherche
            queryset = SearchService.advanced_search(query_params, request.user)
            
            # Pagination
            page = int(query_params.get('page', 1))
            page_size = int(query_params.get('page_size', 20))
            start = (page - 1) * page_size
            end = start + page_size
            
            total_count = queryset.count()
            annonces = queryset[start:end]
            
            # Sérialisation
            serializer = AnnonceDetailSerializer(
                annonces, 
                many=True, 
                context={'request': request}
            )
            
            return Response({
                'annonces': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size,
                    'has_next': end < total_count,
                    'has_previous': page > 1
                },
                'filters_applied': {k: v for k, v in query_params.items() if v}
            })
            
        except Exception as e:
            return Response(
                {'error': 'Erreur lors de la recherche'},
                status=500
            )


class UserDashboardView(APIView):
    """Vue pour le dashboard utilisateur avancé"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Statistiques personnelles
            engine = RecommendationEngine(user)
            stats = engine._get_user_stats()
            
            # Recommandations
            recommendations = engine.get_recommendations(5)
            
            # Activité récente
            activite_recente = self._get_recent_activity(user)
            
            # Notifications non lues
            notifications_non_lues = NotificationAnnonce.objects.filter(
                utilisateur=user,
                est_lue=False
            ).order_by('-date_creation')[:5]
            
            # Recherches récentes
            recherches_recentes = HistoriqueRecherche.objects.filter(
                user=user
            ).order_by('-date_recherche')[:5]
            
            return Response({
                'statistiques': stats,
                'recommendations': recommendations,
                'activite_recente': activite_recente,
                'notifications_non_lues': [
                    {
                        'id': notif.id,
                        'titre': notif.titre,
                        'message': notif.message,
                        'type': notif.type_notification,
                        'date': notif.date_creation,
                        'annonce_id': str(notif.annonce.id) if notif.annonce else None
                    }
                    for notif in notifications_non_lues
                ],
                'recherches_recentes': [
                    {
                        'id': recherche.id,
                        'terme': recherche.terme,
                        'nombre_resultats': recherche.nombre_resultats,
                        'date': recherche.date_recherche
                    }
                    for recherche in recherches_recentes
                ]
            })
            
        except Exception as e:
            return Response(
                {'error': 'Erreur lors du chargement du dashboard'},
                status=500
            )
    
    def _get_recent_activity(self, user):
        """Récupère l'activité récente de l'utilisateur"""
        from .models_advanced import VisiteAnnonce, ContactVendeur
        
        activity = []
        
        # Dernières visites
        visites = VisiteAnnonce.objects.filter(
            utilisateur=user
        ).select_related('annonce__vehicule').order_by('-date_visite')[:3]
        
        for visite in visites:
            activity.append({
                'type': 'visite',
                'titre': f"Consultation: {visite.annonce.vehicule.marque} {visite.annonce.vehicule.modele}",
                'date': visite.date_visite,
                'annonce_id': str(visite.annonce.id)
            })
        
        # Derniers contacts
        contacts = ContactVendeur.objects.filter(
            acheteur_potentiel=user
        ).select_related('annonce__vehicule').order_by('-date_contact')[:3]
        
        for contact in contacts:
            activity.append({
                'type': 'contact',
                'titre': f"Contact: {contact.annonce.vehicule.marque} {contact.annonce.vehicule.modele}",
                'date': contact.date_contact,
                'annonce_id': str(contact.annonce.id)
            })
        
        # Derniers favoris
        favoris = Favori.objects.filter(
            user=user
        ).select_related('annonce__vehicule').order_by('-created_at')[:3]
        
        for favori in favoris:
            activity.append({
                'type': 'favori',
                'titre': f"Favori: {favori.annonce.vehicule.marque} {favori.annonce.vehicule.modele}",
                'date': favori.created_at,
                'annonce_id': str(favori.annonce.id)
            })
        
        # Trier par date
        activity.sort(key=lambda x: x['date'], reverse=True)
        
        return activity[:10]


class MarketInsightsView(APIView):
    """Vue pour les insights du marché"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            days = int(request.query_params.get('days', 30))
            insights = AnalyticsService.get_market_trends(days)
            
            # Ajouter des insights personnalisés
            user_insights = self._get_user_market_insights(request.user)
            
            return Response({
                'market_trends': insights,
                'user_insights': user_insights
            })
            
        except Exception as e:
            return Response(
                {'error': 'Erreur lors du chargement des insights'},
                status=500
            )
    
    def _get_user_market_insights(self, user):
        """Génère des insights personnalisés pour l'utilisateur"""
        try:
            # Analyser le comportement de l'utilisateur
            visites = VisiteAnnonce.objects.filter(utilisateur=user)
            favoris = Favori.objects.filter(user=user)
            
            if not visites.exists():
                return {
                    'message': 'Commencez à explorer pour obtenir des insights personnalisés',
                    'type': 'beginner'
                }
            
            # Prix moyen consulté
            prix_moyen = visites.aggregate(
                avg_prix=Avg('annonce__prix')
            )['avg_prix'] or 0
            
            # Marques préférées
            marques_preferees = (
                visites.values('annonce__vehicule__marque')
                .annotate(count=Count('id'))
                .order_by('-count')[:3]
            )
            
            # Insights basés sur les données
            insights = {
                'prix_moyen_consulte': float(prix_moyen),
                'marques_preferees': list(marques_preferees),
                'type': 'personalized'
            }
            
            # Recommandations personnalisées
            if prix_moyen > 0:
                # Comparer avec le marché
                prix_marche = Annonce.objects.filter(
                    est_active=True
                ).aggregate(avg_prix=Avg('prix'))['avg_prix'] or 0
                
                if prix_moyen > prix_marche * 1.2:
                    insights['conseil'] = "Vous consultez des véhicules assez chers. Découvrez notre section bonnes affaires !"
                elif prix_moyen < prix_marche * 0.8:
                    insights['conseil'] = "Vous cherchez des bonnes affaires ! Consultez nos alertes pour ne rien manquer."
                else:
                    insights['conseil'] = "Votre budget est bien aligné avec le marché actuel."
            
            return insights
            
        except Exception as e:
            return {
                'message': 'Erreur lors de la génération des insights',
                'type': 'error'
            }


class QuickActionsView(APIView):
    """Vue pour les actions rapides"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne les actions rapides disponibles"""
        try:
            user = request.user
            
            # Compteurs pour les badges
            nombre_favoris = Favori.objects.filter(user=user).count()
            nombre_notifications = NotificationAnnonce.objects.filter(
                utilisateur=user,
                est_lue=False
            ).count()
            
            # Actions rapides suggérées
            actions_suggerees = []
            
            # Si l'utilisateur a des favoris, suggérer de les comparer
            if nombre_favoris >= 2:
                actions_suggerees.append({
                    'id': 'comparer_favoris',
                    'titre': 'Comparer mes favoris',
                    'description': f'Comparez vos {nombre_favoris} favoris',
                    'icon': 'compare',
                    'action': '/comparer/favoris'
                })
            
            # Suggérer de créer une alerte si l'utilisateur a fait des recherches
            if HistoriqueRecherche.objects.filter(user=user).exists():
                actions_suggerees.append({
                    'id': 'creer_alerte',
                    'titre': 'Créer une alerte',
                    'description': 'Soyez notifié des nouvelles annonces',
                    'icon': 'bell',
                    'action': '/alertes/creer'
                })
            
            # Suggérer d'explorer les bonnes affaires
            bonnes_affaires = Annonce.objects.filter(
                est_bonne_affaire=True,
                est_active=True
            ).count()
            
            if bonnes_affaires > 0:
                actions_suggerees.append({
                    'id': 'bonnes_affaires',
                    'titre': 'Découvrir les bonnes affaires',
                    'description': f'{bonnes_affaires} offres intéressantes disponibles',
                    'icon': 'star',
                    'action': '/annonces?bonnes_affaires=true'
                })
            
            return Response({
                'compteurs': {
                    'favoris': nombre_favoris,
                    'notifications': nombre_notifications,
                    'bonnes_affaires': bonnes_affaires
                },
                'actions_suggerees': actions_suggerees
            })
            
        except Exception as e:
            return Response(
                {'error': 'Erreur lors du chargement des actions rapides'},
                status=500
            )
