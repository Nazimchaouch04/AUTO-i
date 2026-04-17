from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import csv
from django.http import HttpResponse
from .models import EstimationHistory
from .serializers import EstimationHistorySerializer, EstimationRequestSerializer
from .ml_model import get_modele

PREMIUM_BRANDS = {'bmw', 'mercedes', 'audi', 'porsche', 'lexus', 'volvo'}

def normalise_marque(s: str) -> str:
    """Normalise la marque pour la DB (première lettre en majuscule)."""
    if not s:
        return s
    m = s.strip().lower()
    # Cas spéciaux
    specials = {'bmw': 'BMW', 'kia': 'Kia', 'volkswagen': 'Volkswagen'}
    return specials.get(m, m.capitalize())


class EstimationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if getattr(self, 'action', None) == 'history':
            return [IsAuthenticated()]
        return [AllowAny()]

    def _resolve_annee(self, data):
        annee = data.get('annee')
        if annee is not None:
            return int(annee)
        annee_min = data.get('annee_min')
        annee_max = data.get('annee_max')
        if annee_min is None or annee_max is None:
            return 2020
        return int(round((annee_min + annee_max) / 2))

    def create(self, request):
        """POST /api/estimation/"""
        serializer = EstimationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        annee_used = self._resolve_annee(data)

        marque = normalise_marque(data['marque'])
        
        # Appel au modèle ML
        modele = get_modele()
        result = modele.estimer(
            marque=marque,
            annee=annee_used,
            kilometrage=data['kilometrage'],
            carburant=data['carburant'],
            boite=data.get('boite', ''),
            puissance=data.get('puissance', 100) or 100,
            pays=data.get('pays', 'DZ')
        )

        fiabilite_label = result.get('fiabilite', 'Moyenne').capitalize()
        score_confiance = 85 if fiabilite_label.lower() == 'haute' else 65
        
        nb = 100 # Valeur factice par défaut pour le ML
        source = 'modele_ml'
        source_msg = "Estimation basée sur notre modèle d'Intelligence Artificielle"

        # ── Pills d'influence (frontend) ─────────────────────────────────────
        marque_key = str(data.get('marque', '')).lower()
        premium_impact = 15 if marque_key in PREMIUM_BRANDS else -5
        km = int(data.get('kilometrage') or 0)
        km_impact_pill = -8 if km >= 120_000 else 3
        region = data.get('pays', 'DZ')
        region_impact = 3 if region == 'FR' else -3

        influence_facteurs_ml = [
            {'name': f.get('label', ''), 'impact': f.get('poids', 0)} for f in result.get('facteurs', [])
        ]
        if not influence_facteurs_ml:
            influence_facteurs_ml = [
                {'name': 'Marque premium' if marque_key in PREMIUM_BRANDS else 'Marque standard', 'impact': premium_impact},
                {'name': 'Kilométrage', 'impact': km_impact_pill},
                {'name': 'Région', 'impact': region_impact},
            ]

        # ── Annonces exemples (on peut garder un fallback ou laisser vide) ──
        exemples = []
        try:
            from apps.annonces.models import Annonce
            qs_ex = Annonce.objects.filter(
                est_active=True,
                modele__iexact=data['modele']
            ).order_by('?')[:3]
            for a in qs_ex:
                exemples.append({
                    'id': a.id,
                    'annee': a.annee,
                    'kilometrage': a.kilometrage,
                    'carburant': a.carburant,
                    'prix': float(a.prix),
                    'ville': a.ville or '',
                })
        except Exception:
            pass

        # ── Sauvegarde si authentifié ────────────────────────────────────────
        estimation_id = None
        if getattr(request, 'user', None) and request.user.is_authenticated:
            try:
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
                    prix_estime=result.get('prix_estime', 15000),
                    fourchette_basse=result.get('fourchette_basse', 13000),
                    fourchette_haute=result.get('fourchette_haute', 17000),
                    fiabilite=fiabilite_label,
                    nb_annonces_reference=nb,
                )
                estimation_id = estimation.id
            except Exception:
                pass
            
            try:
                profile = request.user.profile
                profile.add_coins(50)
                profile.add_xp(100)
            except Exception:
                pass

        return Response({
            'prix_estime': result.get('prix_estime', 15000),
            'fourchette_basse': result.get('fourchette_basse', 13000),
            'fourchette_haute': result.get('fourchette_haute', 17000),
            'fiabilite': fiabilite_label,
            'score_confiance': score_confiance,
            'nb_annonces': nb,
            'source_donnees': source,
            'source_message': source_msg,
            'facteurs': influence_facteurs_ml,
            'facteurs_detailles': influence_facteurs_ml,
            'exemples_marche': exemples,
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
        """Backward compatible: POST /api/estimation/estimate/"""
        return self.create(request)

    @action(detail=False, methods=['get'])
    def history(self, request):
        estimations = EstimationHistory.objects.filter(user=request.user)
        serializer = EstimationHistorySerializer(estimations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_mes_estimations(self, request):
        abonnement = getattr(request.user, 'subscription', None)
        plan_nom = abonnement.plan.nom if abonnement else None
        if plan_nom not in ['pro', 'business']:
            return Response(
                {'error': 'Export CSV disponible uniquement en plan Pro ou Business'},
                status=status.HTTP_403_FORBIDDEN)

        estimations = EstimationHistory.objects.filter(
            user=request.user).order_by('-created_at')[:500]

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="mes_estimations.csv"'
        response.write('\ufeff')

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'Date', 'Marque', 'Modèle', 'Année', 'Kilométrage',
            'Carburant', 'Pays', 'Prix estimé',
            'Fourchette basse', 'Fourchette haute', 'Fiabilité'
        ])

        for e in estimations:
            writer.writerow([
                e.created_at.strftime('%d/%m/%Y %H:%M'),
                e.marque,
                e.modele,
                e.annee,
                e.kilometrage,
                e.carburant,
                e.pays,
                e.prix_estime,
                e.fourchette_basse,
                e.fourchette_haute,
                e.fiabilite
            ])

        return response
