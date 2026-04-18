"""
Dashboard Admin API Endpoints
Gestion des fonctionnalités admin: utilisateurs, abonnés pro, alertes, métriques
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta

from apps.users.models import UserProfile
from apps.subscriptions.models import Abonnement, Plan
from apps.alertes.models import Alerte
from apps.estimation.models import EstimationHistory
from apps.annonces.models import Annonce


class AdminDashboardViewSet(viewsets.ViewSet):
    """Endpoints Admin pour le dashboard de gestion"""
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Seuls les admins ou staff peuvent accéder"""
        if self.action in ['metriques_systeme', 'liste_utilisateurs', 
                          'abonnes_pro', 'alertes_actives', 
                          'bonnes_affaires_admin', 'historique_estimations']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], url_path='metriques-systeme')
    def metriques_systeme(self, request):
        """Métriques système pour le dashboard admin"""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Estimations aujourd'hui
        estimations_today = EstimationHistory.objects.filter(
            created_at__date=today
        ).count()
        
        # Total utilisateurs
        total_users = User.objects.filter(is_active=True).count()
        
        # Alertes actives
        alertes_actives = Alerte.objects.filter(est_active=True).count()
        
        # Estimations ce mois
        estimations_month = EstimationHistory.objects.filter(
            created_at__date__gte=month_start
        ).count()
        
        # Stats supplémentaires
        new_users_today = User.objects.filter(
            date_joined__date=today
        ).count()
        
        annonces_actives = Annonce.objects.filter(
            est_active=True
        ).count()
        
        bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True,
            est_active=True
        ).count()
        
        return Response({
            'estimations_aujourd_hui': estimations_today,
            'total_utilisateurs': total_users,
            'alertes_actives': alertes_actives,
            'estimations_ce_mois': estimations_month,
            'nouveaux_utilisateurs_today': new_users_today,
            'annonces_actives': annonces_actives,
            'bonnes_affaires_actives': bonnes_affaires
        })
    
    @action(detail=False, methods=['get'], url_path='utilisateurs')
    def liste_utilisateurs(self, request):
        """Liste complète des utilisateurs pour gestion admin"""
        users = User.objects.select_related('profile').annotate(
            estimations_count=Count('estimations'),
            alertes_count=Count('alertes'),
            is_pro=Count('abonnement', filter=Q(abonnement__plan__nom__in=['Pro', 'PRO', 'pro']))
        ).order_by('-date_joined')
        
        data = []
        for user in users:
            profile = getattr(user, 'profile', None)
            data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_pro': bool(user.is_pro),
                'xp': profile.xp if profile else 0,
                'level': profile.level if profile else 1,
                'coins': profile.coins if profile else 0,
                'estimations_count': user.estimations_count,
                'alertes_count': user.alertes_count,
                'phone': profile.phone if profile else None,
                'ville': profile.ville if profile else None,
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'], url_path='utilisateurs/(?P<pk>[^/.]+)')
    def detail_utilisateur(self, request, pk=None):
        """Détails d'un utilisateur spécifique"""
        try:
            user = User.objects.select_related('profile').get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=404)
        
        profile = getattr(user, 'profile', None)
        
        # Historique des estimations
        estimations = EstimationHistory.objects.filter(
            user=user
        ).order_by('-created_at')[:10]
        
        # Alertes
        alertes = Alerte.objects.filter(user=user).order_by('-created_at')
        
        # Abonnement
        try:
            abonnement = Abonnement.objects.get(user=user)
            abonnement_data = {
                'plan': abonnement.plan.nom,
                'date_debut': abonnement.date_debut,
                'date_fin': abonnement.date_fin,
                'est_actif': abonnement.est_actif,
            }
        except Abonnement.DoesNotExist:
            abonnement_data = None
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'profile': {
                'xp': profile.xp if profile else 0,
                'level': profile.level if profile else 1,
                'level_name': profile.get_level_name() if profile else 'Apprenti',
                'coins': profile.coins if profile else 0,
                'phone': profile.phone if profile else None,
                'ville': profile.ville if profile else None,
                'bio': profile.bio if profile else None,
            } if profile else None,
            'abonnement': abonnement_data,
            'estimations_recentes': [
                {
                    'id': e.id,
                    'marque': e.marque,
                    'modele': e.modele,
                    'annee': e.annee,
                    'prix_estime': float(e.prix_estime),
                    'date': e.created_at
                } for e in estimations
            ],
            'alertes': [
                {
                    'id': a.id,
                    'titre': a.titre,
                    'est_active': a.est_active,
                    'created_at': a.created_at
                } for a in alertes
            ]
        })
    
    @action(detail=False, methods=['patch'], url_path='utilisateurs/(?P<pk>[^/.]+)/modifier')
    def modifier_utilisateur(self, request, pk=None):
        """Modifier un utilisateur (admin)"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=404)
        
        data = request.data
        
        # Mise à jour des champs
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_staff' in data:
            user.is_staff = data['is_staff']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        user.save()
        
        return Response({'message': 'Utilisateur mis à jour', 'user_id': user.id})
    
    @action(detail=False, methods=['get'], url_path='abonnes-pro')
    def abonnes_pro(self, request):
        """Liste des abonnés Pro avec stats"""
        abonnements = Abonnement.objects.filter(
            plan__nom__in=['Pro', 'PRO', 'pro', 'Premium', 'premium'],
            est_actif=True
        ).select_related('user', 'plan').order_by('-date_debut')
        
        data = []
        for abo in abonnements:
            user = abo.user
            estimations_count = EstimationHistory.objects.filter(user=user).count()
            alertes_count = Alerte.objects.filter(user=user).count()
            
            data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'plan': abo.plan.nom,
                'date_debut': abo.date_debut,
                'date_fin': abo.date_fin,
                'jours_restants': (abo.date_fin - timezone.now()).days if abo.date_fin else None,
                'estimations_count': estimations_count,
                'alertes_count': alertes_count,
                'is_active': abo.est_actif,
            })
        
        return Response({
            'total_pro': len(data),
            'abonnes': data
        })
    
    @action(detail=False, methods=['get'], url_path='alertes-actives')
    def alertes_actives(self, request):
        """Toutes les alertes actives (admin view)"""
        alertes = Alerte.objects.filter(
            est_active=True
        ).select_related('user').order_by('-created_at')
        
        data = []
        for alerte in alertes:
            data.append({
                'id': alerte.id,
                'user_id': alerte.user.id,
                'username': alerte.user.username,
                'email': alerte.user.email,
                'titre': alerte.titre,
                'marque': alerte.marque,
                'modele': alerte.modele,
                'prix_min': alerte.prix_min,
                'prix_max': alerte.prix_max,
                'km_max': alerte.km_max,
                'annee_min': alerte.annee_min,
                'carburant': alerte.carburant,
                'email_actif': alerte.email_actif,
                'push_actif': alerte.push_actif,
                'created_at': alerte.created_at,
                'last_triggered': alerte.last_triggered,
            })
        
        return Response({
            'total_alertes': len(data),
            'alertes': data
        })
    
    @action(detail=False, methods=['get'], url_path='bonnes-affaires')
    def bonnes_affaires_admin(self, request):
        """Bonnes affaires pour admin (toutes actives)"""
        bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True,
            est_active=True
        ).order_by('-ecart_prix')[:50]
        
        data = []
        for annonce in bonnes_affaires:
            ecart_pct = abs(annonce.ecart_prix) if annonce.ecart_prix else 0
            
            data.append({
                'id': annonce.id,
                'marque': annonce.marque,
                'modele': annonce.modele,
                'annee': annonce.annee,
                'prix': annonce.prix,
                'prix_estime': annonce.prix_estime,
                'ecart_prix': annonce.ecart_prix,
                'ecart_pct': round(ecart_pct, 1),
                'kilometrage': annonce.kilometrage,
                'carburant': annonce.carburant,
                'ville': annonce.ville,
                'pays': annonce.pays,
                'date_publication': annonce.date_publication,
                'image_url': annonce.image_url,
            })
        
        return Response({
            'total': len(data),
            'bonnes_affaires': data
        })
    
    @action(detail=False, methods=['get'], url_path='historique-estimations')
    def historique_estimations(self, request):
        """Historique complet des estimations (admin)"""
        limit = request.query_params.get('limit', 100)
        try:
            limit = int(limit)
        except:
            limit = 100
        
        estimations = EstimationHistory.objects.select_related('user').order_by('-created_at')[:limit]
        
        data = []
        for est in estimations:
            data.append({
                'id': est.id,
                'user_id': est.user.id if est.user else None,
                'username': est.user.username if est.user else 'Anonyme',
                'marque': est.marque,
                'modele': est.modele,
                'annee': est.annee,
                'kilometrage': est.kilometrage,
                'carburant': est.carburant,
                'pays': est.pays,
                'prix_estime': float(est.prix_estime),
                'fourchette_basse': float(est.fourchette_basse),
                'fourchette_haute': float(est.fourchette_haute),
                'fiabilite': est.fiabilite,
                'nb_annonces_reference': est.nb_annonces_reference,
                'created_at': est.created_at,
            })
        
        return Response({
            'total': len(data),
            'estimations': data
        })
    
    @action(detail=False, methods=['get'], url_path='profils-joueurs')
    def profils_joueurs(self, request):
        """Classement des joueurs par XP (admin view)"""
        profiles = UserProfile.objects.select_related('user').order_by('-xp')[:100]
        
        data = []
        rank = 1
        for profile in profiles:
            data.append({
                'rank': rank,
                'user_id': profile.user.id,
                'username': profile.user.username,
                'email': profile.user.email,
                'xp': profile.xp,
                'level': profile.level,
                'level_name': profile.get_level_name(),
                'xp_pct': profile.xp_pct,
                'coins': profile.coins,
            })
            rank += 1
        
        return Response({
            'total_joueurs': UserProfile.objects.count(),
            'classement': data
        })
