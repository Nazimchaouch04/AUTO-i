from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import EstimationHistory
from .serializers import EstimationHistorySerializer, EstimationRequestSerializer


# ─── Prix de référence (fallback si aucune donnée en DB) ─────────────────────
PRIX_BASE_MARQUE = {
    'renault': 12000,  'peugeot': 13000, 'citroen': 11000,
    'volkswagen': 18000, 'toyota': 16000, 'dacia': 9000,
    'ford': 14000, 'bmw': 28000, 'mercedes': 32000,
    'audi': 26000, 'hyundai': 15000, 'kia': 14000,
    'opel': 12000, 'fiat': 11000, 'seat': 13000,
}

PREMIUM_BRANDS = {'bmw', 'mercedes', 'audi', 'porsche', 'lexus', 'volvo'}


def normalise_marque(s: str) -> str:
    """Normalise la marque pour la DB (première lettre en majuscule)."""
    if not s:
        return s
    m = s.strip().lower()
    # Cas spéciaux
    specials = {'bmw': 'BMW', 'kia': 'Kia', 'volkswagen': 'Volkswagen'}
    return specials.get(m, m.capitalize())


def estimate_price(marque_raw, modele, annee, kilometrage, carburant, pays, boite='', puissance=None):
    """
    Estimation de prix basée sur les données réelles du marché en DB.

    Stratégie de requête progressive :
      1. Même marque + même modèle + année ±3  → données les plus précises
      2. Même marque + année ±5               → données marque généraliste
      3. Toute la marque                       → baseline marque
      Chaque niveau est utilisé pour calibrer le prix de base.
    """
    from apps.annonces.models import Annonce
    from django.db.models import Avg, Count, StdDev, Min, Max, Q

    marque = normalise_marque(marque_raw)
    marque_key = marque_raw.strip().lower()
    age = max(0, 2025 - annee)

    # ── Requêtes progressives ────────────────────────────────────────────────
    qs_base = Annonce.objects.filter(est_active=True, vehicule__marque__iexact=marque)

    # Niveau 1 : même modèle, même carburant, année ±3
    niveau1 = qs_base.filter(
        vehicule__modele__iexact=modele,
        annee__gte=annee - 3,
        annee__lte=annee + 3,
    )
    if carburant:
        niveau1 = niveau1.filter(carburant__iexact=carburant)

    stats1 = niveau1.aggregate(
        n=Count('id'), avg=Avg('prix'), std=StdDev('prix'),
        mn=Min('prix'), mx=Max('prix')
    )

    # Niveau 2 : même modèle, aucune restriction année
    stats2 = qs_base.filter(
        vehicule__modele__iexact=modele
    ).aggregate(n=Count('id'), avg=Avg('prix'), mn=Min('prix'), mx=Max('prix'))

    # Niveau 3 : toute la marque, année ±5
    stats3 = qs_base.filter(
        annee__gte=annee - 5,
        annee__lte=annee + 5,
    ).aggregate(n=Count('id'), avg=Avg('prix'), mn=Min('prix'), mx=Max('prix'))

    # Niveau 4 : toute la marque
    stats4 = qs_base.aggregate(n=Count('id'), avg=Avg('prix'))

    # ── Choix du prix de base ────────────────────────────────────────────────
    source = 'fallback'
    nb_ref = 0
    prix_base_brut = None

    if stats1['n'] and stats1['n'] >= 2 and stats1['avg']:
        prix_base_brut = float(stats1['avg'])
        nb_ref = stats1['n']
        source = 'modele_exact'
    elif stats2['n'] and stats2['n'] >= 2 and stats2['avg']:
        prix_base_brut = float(stats2['avg'])
        nb_ref = stats2['n']
        source = 'modele_marche'
    elif stats3['n'] and stats3['n'] >= 3 and stats3['avg']:
        prix_base_brut = float(stats3['avg'])
        nb_ref = stats3['n']
        source = 'marque_annee'
    elif stats4['n'] and stats4['avg']:
        prix_base_brut = float(stats4['avg'])
        nb_ref = stats4['n']
        source = 'marque_global'
    else:
        prix_base_brut = PRIX_BASE_MARQUE.get(marque_key, 13000)
        source = 'fallback'

    # ── Facteurs de correction ───────────────────────────────────────────────
    # Si les données viennent de la DB, elles contiennent déjà des véhicules
    # d'âges et kilométrages variés → on applique des corrections relatives
    # par rapport au véhicule "moyen" de la DB (âge ~7 ans, km ~80k).

    # Correction âge (dépréciation ~7%/an, plancher 30%)
    AGE_MOYEN_DB = 7.0
    facteur_age_db   = max(0.30, 1 - AGE_MOYEN_DB * 0.07)   # ~0.51 pour l'âge moyen
    facteur_age_cible = max(0.30, 1 - age * 0.07)
    ratio_age = facteur_age_cible / facteur_age_db if facteur_age_db > 0 else 1.0

    # Correction kilométrage (linéaire sur 300k, plancher 50%)
    KM_MOYEN_DB = 80_000
    facteur_km_db    = max(0.50, 1 - KM_MOYEN_DB / 300_000)   # ~0.73
    facteur_km_cible  = max(0.50, 1 - kilometrage / 300_000)
    ratio_km = facteur_km_cible / facteur_km_db if facteur_km_db > 0 else 1.0

    # Correction carburant
    facteur_carburant = {
        'electrique': 1.15, 'hybride': 1.08,
        'essence': 1.00,    'diesel': 0.95,
    }.get(str(carburant).lower(), 1.0)

    # Correction boîte
    facteur_boite = 1.06 if str(boite).lower() == 'automatique' else 1.0

    # Correction pays
    facteur_pays = {'FR': 1.08, 'DZ': 1.00, 'TN': 0.97, 'MA': 0.98}.get(pays, 1.0)

    # Si on utilise des données DB, on applique seulement le ratio (correction relative)
    if source != 'fallback':
        prix_estime = prix_base_brut * ratio_age * ratio_km * facteur_carburant * facteur_boite * facteur_pays
    else:
        # Fallback : application complète des facteurs sur le prix de référence
        facteur_age_abs = max(0.30, 1 - age * 0.07)
        facteur_km_abs  = max(0.50, 1 - kilometrage / 300_000)
        prix_estime = prix_base_brut * facteur_age_abs * facteur_km_abs * facteur_carburant * facteur_boite * facteur_pays

    # ── Fourchette ───────────────────────────────────────────────────────────
    # Si on a une vraie StdDev, fourchette = ±1σ (min 8%)
    if source == 'modele_exact' and stats1.get('std') and stats1['std']:
        sigma = float(stats1['std'])
        spread = min(sigma / prix_base_brut, 0.25)  # cap à 25%
        spread = max(spread, 0.08)
    else:
        spread = 0.05 if source == 'modele_exact' else 0.10 if source == 'modele_marche' else 0.15

    fourchette_basse = prix_estime * (1 - spread)
    fourchette_haute = prix_estime * (1 + spread)

    # ── Annonces exemples ────────────────────────────────────────────────────
    exemples = []
    try:
        qs_ex = qs_base.filter(
            vehicule__modele__iexact=modele
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
        if not exemples:
            qs_ex2 = qs_base.order_by('?')[:3]
            for a in qs_ex2:
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

    # ── Facteurs d'influence (pour le frontend) ──────────────────────────────
    age_impact = round((ratio_age - 1) * 100, 1) if source != 'fallback' else round((max(0.30, 1 - age * 0.07) - 1) * 100, 1)
    km_impact  = round((ratio_km  - 1) * 100, 1) if source != 'fallback' else round((max(0.50, 1 - kilometrage / 300_000) - 1) * 100, 1)
    carb_impact = round((facteur_carburant - 1) * 100, 1)

    facteurs_detailles = [
        {'name': f'Âge ({age} ans)', 'impact': age_impact},
        {'name': f'Kilométrage ({kilometrage:,} km)', 'impact': km_impact},
        {'name': f'Carburant ({carburant})', 'impact': carb_impact},
    ]

    return {
        'prix_estime': round(prix_estime, -2),
        'fourchette_basse': round(fourchette_basse, -2),
        'fourchette_haute': round(fourchette_haute, -2),
        'nb_annonces_reference': nb_ref,
        'source_donnees': source,
        'exemples_marche': exemples,
        'facteurs_detailles': facteurs_detailles,
    }


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

        result = estimate_price(
            marque_raw=data['marque'],
            modele=data['modele'],
            annee=annee_used,
            kilometrage=data['kilometrage'],
            carburant=data['carburant'],
            pays=data.get('pays', 'DZ'),
            boite=data.get('boite', ''),
            puissance=data.get('puissance'),
        )

        # ── Labels qualité ───────────────────────────────────────────────────
        nb = result['nb_annonces_reference']
        source = result['source_donnees']

        if source == 'modele_exact' and nb >= 5:
            fiabilite_label = 'Haute'
            score_confiance = min(95, 75 + nb * 2)
        elif source in ('modele_marche', 'modele_exact') and nb >= 2:
            fiabilite_label = 'Moyenne'
            score_confiance = 65
        elif source in ('marque_annee', 'marque_global'):
            fiabilite_label = 'Faible'
            score_confiance = 50
        else:
            fiabilite_label = 'Faible'
            score_confiance = 40

        # ── Pills d'influence (frontend) ─────────────────────────────────────
        marque_key = str(data.get('marque', '')).lower()
        premium_impact = 15 if marque_key in PREMIUM_BRANDS else -5
        km = int(data.get('kilometrage') or 0)
        km_impact_pill = -8 if km >= 120_000 else 3
        region = data.get('pays', 'DZ')
        region_impact = 3 if region == 'FR' else -3

        influence_facteurs = [
            {'name': 'Marque premium' if marque_key in PREMIUM_BRANDS else 'Marque standard', 'impact': premium_impact},
            {'name': 'Kilométrage', 'impact': km_impact_pill},
            {'name': 'Région', 'impact': region_impact},
        ]

        # ── Message source ───────────────────────────────────────────────────
        source_messages = {
            'modele_exact':  f'Basé sur {nb} annonces {normalise_marque(data["marque"])} {data["modele"]} similaires',
            'modele_marche': f'Basé sur {nb} annonces {normalise_marque(data["marque"])} {data["modele"]} (toutes années)',
            'marque_annee':  f'Basé sur {nb} annonces {normalise_marque(data["marque"])} de la même époque',
            'marque_global': f'Basé sur {nb} annonces {normalise_marque(data["marque"])} (marché global)',
            'fallback':      'Estimation basée sur les prix de référence du marché',
        }
        source_msg = source_messages.get(source, '')

        # ── Sauvegarde si authentifié ────────────────────────────────────────
        estimation_id = None
        if getattr(request, 'user', None) and request.user.is_authenticated:
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
                fiabilite=fiabilite_label,
                nb_annonces_reference=nb,
            )
            estimation_id = estimation.id
            try:
                profil = request.user.profil
                profil.add_coins(50)
                profil.add_xp(100)
            except Exception:
                pass

        return Response({
            'prix_estime': result['prix_estime'],
            'fourchette_basse': result['fourchette_basse'],
            'fourchette_haute': result['fourchette_haute'],
            'fiabilite': fiabilite_label,
            'score_confiance': score_confiance,
            'nb_annonces': nb,
            'source_donnees': source,
            'source_message': source_msg,
            'facteurs': influence_facteurs,
            'facteurs_detailles': result['facteurs_detailles'],
            'exemples_marche': result['exemples_marche'],
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
