from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import EstimationHistory
from .serializers import EstimationHistorySerializer, EstimationRequestSerializer


def estimate_price(marque, modele, annee, kilometrage, carburant, pays):
    """Formule d'estimation sans ML - basée sur les données en base"""
    from apps.annonces.models import Annonce
    from django.db.models import Avg, Count

    age = 2025 - annee

    # Prix de base par marque
    prix_base_dict = {
        'Renault': 12000, 'Peugeot': 13000, 'Volkswagen': 18000,
        'Toyota': 16000, 'Dacia': 9000, 'Ford': 14000,
        'BMW': 28000, 'Mercedes': 32000, 'Hyundai': 15000,
        'Kia': 14000,
    }
    prix_base = prix_base_dict.get(marque, 13000)

    # Cherche données réelles en base
    try:
        annonces_similaires = Annonce.objects.filter(
            vehicule__marque__iexact=marque,
            annee__gte=annee - 2,
            annee__lte=annee + 2,
            est_active=True
        ).aggregate(prix_moyen=Avg('prix'), count=Count('id'))

        if annonces_similaires['count'] and annonces_similaires['count'] >= 3:
            prix_base = float(annonces_similaires['prix_moyen'])
    except:
        pass

    # Facteurs de correction
    facteur_age = max(0.3, 1 - (age * 0.07))
    facteur_km = max(0.5, 1 - (kilometrage / 300000))
    facteur_carburant = {
        'electrique': 1.15, 'hybride': 1.08,
        'essence': 1.0, 'diesel': 0.95
    }.get(carburant, 1.0)

    prix_estime = prix_base * facteur_age * facteur_km * facteur_carburant

    try:
        nb_ref = annonces_similaires['count'] or 0
    except:
        nb_ref = 0

    return {
        'prix_estime': round(prix_estime, -2),
        'fourchette_basse': round(prix_estime * 0.88, -2),
        'fourchette_haute': round(prix_estime * 1.12, -2),
        'fiabilite': 'haute' if nb_ref >= 5 else 'moyenne',
        'nb_annonces_reference': nb_ref,
        'facteurs': [
            {'label': f'Age du véhicule ({age} ans)', 'impact': round((facteur_age - 1) * 100, 1)},
            {'label': f'Kilométrage ({kilometrage:,} km)', 'impact': round((facteur_km - 1) * 100, 1)},
            {'label': f'Carburant ({carburant})', 'impact': round((facteur_carburant - 1) * 100, 1)},
        ]
    }


class EstimationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def _resolve_annee(self, data):
        annee = data.get('annee')
        if annee is not None:
            return annee
        annee_min = data.get('annee_min')
        annee_max = data.get('annee_max')
        if annee_min is None or annee_max is None:
            return 2020
        return int(round((annee_min + annee_max) / 2))

    def create(self, request):
        """POST /api/estimation/ (frontend)."""
        serializer = EstimationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        annee_used = self._resolve_annee(data)
        result = estimate_price(
            data['marque'], data['modele'], annee_used,
            data['kilometrage'], data['carburant'], data.get('pays', 'DZ')
        )

        # Save estimation only when authenticated
        estimation_id = None
        if getattr(request, 'user', None) is not None and request.user.is_authenticated:
            estimation = EstimationHistory.objects.create(
                user=request.user,
                marque=data['marque'],
                modele=data['modele'],
                annee=annee_used,
                kilometrage=data['kilometrage'],
                carburant=data['carburant'],
                boite=data.get('boite', ''),
                puissance=data.get('puissance'),
                pays=data.get('pays', 'DZ'),
                prix_estime=result['prix_estime'],
                fourchette_basse=result['fourchette_basse'],
                fourchette_haute=result['fourchette_haute'],
                fiabilite=result['fiabilite'],
                nb_annonces_reference=result['nb_annonces_reference'],
            )
            estimation_id = estimation.id

            # Reward coins / xp (best-effort)
            try:
                profil = request.user.profil
                profil.add_coins(50)
                profil.add_xp(100)
            except Exception:
                pass

        # Map to frontend-friendly schema
        nb = result.get('nb_annonces_reference') or 0
        fiabilite_label = 'Haute' if nb >= 10 else 'Moyenne' if nb >= 5 else 'Faible'
        score_confiance = 90 if nb >= 10 else 75 if nb >= 5 else 60

        return Response({
            'prix_estime': result['prix_estime'],
            'fourchette_basse': result['fourchette_basse'],
            'fourchette_haute': result['fourchette_haute'],
            'fiabilite': fiabilite_label,
            'score_confiance': score_confiance,
            'nb_annonces': nb,
            'facteurs': [
                {'name': f.get('label', ''), 'impact': f.get('impact', 0)}
                for f in (result.get('facteurs') or [])
            ],
            'vehicule': {
                'marque': data['marque'],
                'modele': data['modele'],
                'annee': annee_used,
                'annee_min': data.get('annee_min'),
                'annee_max': data.get('annee_max'),
                'kilometrage': data['kilometrage'],
                'carburant': data['carburant'],
                'boite': data.get('boite', ''),
                'puissance': data.get('puissance'),
                'region': data.get('pays', 'DZ'),
                'pays': data.get('pays', 'DZ'),
            },
            'estimation_id': estimation_id,
            'ac_reward': 50,
            'xp_reward': 100,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def estimate(self, request):
        """Backward compatible endpoint: POST /api/estimation/estimate/"""
        return self.create(request)

    @action(detail=False, methods=['get'])
    def history(self, request):
        estimations = EstimationHistory.objects.filter(user=request.user)
        serializer = EstimationHistorySerializer(estimations, many=True)
        return Response(serializer.data)
