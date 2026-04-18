from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count, Q
from django.db import models
from datetime import timedelta
from django.utils import timezone
from apps.annonces.models import Annonce


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Temporairement ouvert pour les tests

    def _get_period_days(self, period_param):
        """Convertit '7j', '30j', '90j', '1an' en nombre de jours"""
        mapping = {
            '7j': 7,
            '30j': 30,
            '90j': 90,
            '1an': 365
        }
        return mapping.get(period_param, 30)

    @action(detail=False, methods=['get'])
    def kpis(self, request):
        """Endpoint /api/dashboard/kpis?period=7j|30j|90j|1an"""
        period = request.query_params.get('period', '30j')
        days = self._get_period_days(period)

        start_date = timezone.now() - timedelta(days=days)
        previous_start = start_date - timedelta(days=days)

        # Annonces actives
        annonces_actives = Annonce.objects.filter(
            est_active=True, date_publication__gte=start_date
        ).count()

        annonces_prev = Annonce.objects.filter(
            est_active=True, date_publication__gte=previous_start,
            date_publication__lt=start_date
        ).count()

        annonces_change = ((annonces_actives - annonces_prev) / max(annonces_prev, 1) * 100) if annonces_prev > 0 else 0

        # Bonnes affaires
        bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True, date_publication__gte=start_date
        ).count()

        bonnes_affaires_prev = Annonce.objects.filter(
            est_bonne_affaire=True, date_publication__gte=previous_start,
            date_publication__lt=start_date
        ).count()

        bonnes_affaires_change = ((bonnes_affaires - bonnes_affaires_prev) / max(bonnes_affaires_prev, 1) * 100) if bonnes_affaires_prev > 0 else 0

        # Prix moyen marché
        prix_moyen = Annonce.objects.filter(
            date_publication__gte=start_date
        ).aggregate(avg=Avg('prix'))['avg'] or 0

        prix_moyen_prev = Annonce.objects.filter(
            date_publication__gte=previous_start,
            date_publication__lt=start_date
        ).aggregate(avg=Avg('prix'))['avg'] or prix_moyen

        prix_change = ((prix_moyen - prix_moyen_prev) / max(prix_moyen_prev, 1) * 100) if prix_moyen_prev > 0 else 0

        # Précision ML (mock - à remplacer par vraie métrique)
        precision_ml = 87.5
        precision_change = 3.2

        return Response({
            'annoncesActives': {
                'value': annonces_actives,
                'change': round(abs(annonces_change), 1),
                'trend': 'up' if annonces_change >= 0 else 'down',
                'yesterday': annonces_prev
            },
            'bonnesAffaires': {
                'value': bonnes_affaires,
                'change': round(abs(bonnes_affaires_change), 1),
                'trend': 'up' if bonnes_affaires_change >= 0 else 'down',
                'yesterday': bonnes_affaires_prev
            },
            'prixMoyen': {
                'value': round(prix_moyen, 0),
                'change': round(prix_change, 1),
                'trend': 'up' if prix_change >= 0 else 'down',
                'currency': '€'
            },
            'precisionML': {
                'value': precision_ml,
                'change': precision_change,
                'trend': 'up'
            }
        })

    @action(detail=False, methods=['get'])
    def charts(self, request):
        """Endpoint /api/dashboard/charts?period=7j|30j|90j|1an"""
        period = request.query_params.get('period', '30j')
        days = self._get_period_days(period)

        start_date = timezone.now() - timedelta(days=days)

        # Prix moyen par marque (top 8)
        prix_par_marque = []
        marques_data = (
            Annonce.objects.filter(date_publication__gte=start_date)
            .values('marque')
            .annotate(
                count=Count('id'),
                prix_avg=Avg('prix')
            )
            .order_by('-count')[:8]
        )

        for item in marques_data:
            prix_par_marque.append({
                'marque': item['marque'] or 'Autre',
                'prix': round(item['prix_avg'] or 0, 0),
                'annonces': item['count']
            })

        # Évolution du marché (6 mois)
        evolution_marche = []
        mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
        for i in range(6):
            month_date = timezone.now() - timedelta(days=30 * (5 - i))
            month_start = month_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1)

            prix_moyen_mois = Annonce.objects.filter(
                date_publication__gte=month_start,
                date_publication__lt=month_end
            ).aggregate(avg=Avg('prix'))['avg'] or 15000

            prix_median_mois = Annonce.objects.filter(
                date_publication__gte=month_start,
                date_publication__lt=month_end
            ).aggregate(avg=Avg('prix'))['avg'] or 14500  # Simplifié

            evolution_marche.append({
                'mois': mois_labels[month_start.month - 1],
                'prix_moyen': round(prix_moyen_mois, 0),
                'prix_median': round(prix_median_mois * 0.95, 0)  # Approximation
            })

        # Répartition carburants
        carburants_data = (
            Annonce.objects.filter(date_publication__gte=start_date)
            .values('carburant')
            .annotate(count=Count('id'))
        )

        carburants_map = {
            'essence': 'Essence',
            'diesel': 'Diesel',
            'electrique': 'Électrique',
            'hybride': 'Hybride',
            'E': 'Essence',
            'D': 'Diesel',
            'El': 'Électrique',
            'H': 'Hybride'
        }

        carburants_count = {'Essence': 0, 'Diesel': 0, 'Électrique': 0, 'Hybride': 0}
        for item in carburants_data:
            key = carburants_map.get(item['carburant'], item['carburant'])
            if key in carburants_count:
                carburants_count[key] += item['count']

        carburants = [
            {'name': name, 'value': count, 'count': count}
            for name, count in carburants_count.items() if count > 0
        ]

        return Response({
            'prixParMarque': prix_par_marque,
            'evolutionMarche': evolution_marche,
            'carburants': carburants
        })

    @action(detail=False, methods=['get'])
    def deals(self, request):
        """Endpoint /api/dashboard/deals?period=7j|30j|90j|1an"""
        period = request.query_params.get('period', '30j')
        days = self._get_period_days(period)

        start_date = timezone.now() - timedelta(days=days)

        bonnes_affaires = (
            Annonce.objects.filter(
                est_bonne_affaire=True,
                date_publication__gte=start_date
            )
            .order_by('-ecart_prix')[:6]
        )

        deals = []
        for annonce in bonnes_affaires:
            ecart_pct = abs(annonce.ecart_prix) if annonce.ecart_prix else 0
            badge = f"-{int(ecart_pct)}%" if ecart_pct > 0 else None

            deals.append({
                'id': annonce.id,
                'marque': annonce.marque,
                'model': annonce.modele,
                'annee': annonce.annee,
                'prix': annonce.prix,
                'prixEstime': annonce.prix_estime or int(annonce.prix * 1.2),
                'km': annonce.kilometrage or 0,
                'image': annonce.image_url or 'https://images.unsplash.com/photo-1542362567-b07e54358753?w=400',
                'url': f'/annonce/{annonce.id}',
                'badge': badge
            })

        return Response(deals)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_stats(self, request):
        """New: /api/dashboard/user-stats/ - Stats personnalisées utilisateur"""
        user = request.user
        
        # Alertes actives
        alertes_count = getattr(user, 'alertes', []).filter(is_active=True).count()
        
        # Favoris
        favoris_count = user.favoris.count()
        
        # Estimations récentes (10 dernières)
        try:
            from apps.estimation.models import EstimationHistory
            estimations = EstimationHistory.objects.filter(user=user).order_by('-created_at')[:5]
            recent_estimations = [{
                'id': e.id,
                'marque': e.marque,
                'modele': e.modele,
                'prix_estime': float(e.prix_estime),
                'date': e.created_at.date()
            } for e in estimations]
        except:
            recent_estimations = []
        
        # Abonnement
        try:
            abonnement = getattr(user, 'abonnement', None)
            sub_status = abonnement.plan.nom if abonnement else 'free'
            estimations_limite = abonnement.plan.estimations_par_mois if abonnement else 10
        except:
            sub_status = 'free'
            estimations_limite = 10
        
        # Gamification
        try:
            from apps.gamification.models import Player
            player = getattr(user, 'player', None)
            xp = player.xp if player else 0
            ac_balance = player.autocoin_balance if player else 100
        except:
            xp = 0
            ac_balance = 100
        
        # Notifications récentes
        try:
            from apps.notifications.models import Notification
            recent_notifs = Notification.objects.filter(user=user).order_by('-created_at')[:3]
            notifs = len(recent_notifs)
        except:
            notifs = 0
        
        return Response({
            'alertes_actives': alertes_count,
            'favoris': favoris_count,
            'estimations_recentes': recent_estimations,
            'abonnement': sub_status,
            'estimations_limite': estimations_limite,
            'xp': xp,
            'autocoin_balance': ac_balance,
            'notifications_non_lues': notifs
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Endpoint legacy /api/dashboard/stats/ - gardé pour compatibilité"""
        period = request.query_params.get('period', '30')
        try:
            days = int(period)
        except:
            days = 30

        start_date = timezone.now() - timedelta(days=days)

        # KPIs principaux
        total_annonces = Annonce.objects.filter(
            est_active=True, date_publication__gte=start_date
        ).count()
        bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True, date_publication__gte=start_date
        ).count()
        prix_moyen = Annonce.objects.filter(
            date_publication__gte=start_date
        ).aggregate(avg=Avg('prix'))['avg'] or 0

        # Variation de prix (simple)
        ancien_prix = Annonce.objects.filter(
            date_publication__lt=start_date,
            date_publication__gte=start_date - timedelta(days=days * 2)
        ).aggregate(avg=Avg('prix'))['avg'] or prix_moyen

        variation = ((prix_moyen - ancien_prix) / ancien_prix * 100) if ancien_prix > 0 else 0

        kpis = {
            'total_annonces': total_annonces,
            'bonnes_affaires': bonnes_affaires,
            'prix_moyen': round(prix_moyen, 2),
            'variation_prix_pct': round(variation, 2),
        }

        # Prix par marque (top 10)
        prix_par_marque_data = (
            Annonce.objects.filter(date_publication__gte=start_date)
            .values('marque')
            .annotate(count=Count('id'), prix_moyen=Avg('prix'))
            .order_by('-count')[:10]
        )
        prix_par_marque = [
            {'marque': item['marque'], 'count': item['count'], 'prix_moyen': item['prix_moyen']}
            for item in prix_par_marque_data
        ]

        # Répartition carburant
        repartition_carburant = list(
            Annonce.objects.filter(date_publication__gte=start_date)
            .values('carburant')
            .annotate(count=Count('id'))
        )

        # Annonces par jour (7 derniers jours)
        annonces_par_jour = []
        for i in range(7):
            date = timezone.now().date() - timedelta(days=6 - i)
            count = Annonce.objects.filter(
                date_publication__date=date
            ).count()
            annonces_par_jour.append({
                'date': date,
                'count': count
            })

        # Bonnes affaires récentes (6 dernières)
        bonnes_affaires_recentes = list(
            Annonce.objects.filter(
                est_bonne_affaire=True
            ).values(
                'id', 'prix', 'prix_estime', 'ecart_prix',
                'marque', 'modele', 'annee'
            ).order_by('-date_publication')[:6]
        )

        return Response({
            'kpis': kpis,
            'prix_par_marque': prix_par_marque,
            'repartition_carburant': repartition_carburant,
            'annonces_par_jour': annonces_par_jour,
            'bonnes_affaires_recentes': bonnes_affaires_recentes,
        })

