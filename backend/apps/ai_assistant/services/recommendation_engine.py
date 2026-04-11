"""
Moteur de recommandation de véhicules pour AutoIntel
Utilise l'IA pour recommander les meilleurs véhicules selon les besoins utilisateur
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any
from django.db.models import Q, F, Avg, Count, StdDev
from django.utils import timezone
from annonces.models import Annonce
from .models import UserProfileAnalysis, VehicleRecommendation, MarketInsight


class VehicleRecommendationEngine:
    """Moteur de recommandation intelligent de véhicules"""
    
    def __init__(self, user):
        self.user = user
        self.profil_ia = self._get_or_create_profil()
    
    def _get_or_create_profil(self) -> UserProfileAnalysis:
        """Récupère ou crée le profil IA de l'utilisateur"""
        profil, created = UserProfileAnalysis.objects.get_or_create(user=self.user)
        return profil
    
    def generer_recommandations(self, limit: int = 10, filtres_supplementaires: Dict = None) -> List[VehicleRecommendation]:
        """Génère des recommandations de véhicules personnalisées"""
        
        # Construire la requête de base
        vehicules_query = self._construire_query_vehicules(filtres_supplementaires)
        
        # Récupérer les véhicules candidats
        vehicules_candidats = vehicules_query[:100]  # Limiter pour la performance
        
        # Scorer chaque véhicule
        vehicules_scores = []
        for vehicule in vehicules_candidats:
            score_details = self._calculer_score_vehicule(vehicule)
            vehicules_scores.append((vehicule, score_details))
        
        # Trier par score total
        vehicules_scores.sort(key=lambda x: x[1]['total'], reverse=True)
        
        # Créer les recommandations
        recommandations = []
        for vehicule, score_details in vehicules_scores[:limit]:
            recommandation = self._creer_recommandation(vehicule, score_details)
            recommandations.append(recommandation)
        
        return recommandations
    
    def _construire_query_vehicules(self, filtres_supplementaires: Dict = None):
        """Construit la requête pour filtrer les véhicules"""
        query = Vehicule.objects.filter(is_active=True)
        
        # Filtrer par budget
        if self.profil_ia.budget_max:
            query = query.filter(prix_moyen__lte=self.profil_ia.budget_max)
        
        if self.profil_ia.budget_min:
            query = query.filter(prix_moyen__gte=self.profil_ia.budget_min)
        
        # Filtrer par marques préférées
        if self.profil_ia.marques_preferrees.exists():
            query = query.filter(marque__in=self.profil_ia.marques_preferees.all())
        
        # Filtrer par types de carburant
        if self.profil_ia.preferences_carburant:
            query = query.filter(type_carburant__in=self.profil_ia.preferences_carburant)
        
        # Filtrer par places minimales
        query = query.filter(nombre_places__gte=self.profil_ia.places_minimales)
        
        # Filtrer par portes minimales
        query = query.filter(nombre_portes__gte=self.profil_ia.porte_minimales)
        
        # Appliquer les filtres supplémentaires
        if filtres_supplementaires:
            for key, value in filtres_supplementaires.items():
                if hasattr(Vehicule, key) and value is not None:
                    if isinstance(value, list):
                        query = query.filter(**{f'{key}__in': value})
                    else:
                        query = query.filter(**{key: value})
        
        return query.distinct()
    
    def _calculer_score_vehicule(self, vehicule: Vehicule) -> Dict[str, int]:
        """Calcule le score de compatibilité d'un véhicule"""
        scores = {
            'prix': 0,
            'besoins': 0,
            'marche': 0,
            'disponibilite': 0,
            'total': 0
        }
        
        # Score de prix (0-25)
        scores['prix'] = self._calculer_score_prix(vehicule)
        
        # Score de besoins (0-30)
        scores['besoins'] = self._calculer_score_besoins(vehicule)
        
        # Score de marché (0-25)
        scores['marche'] = self._calculer_score_marche(vehicule)
        
        # Score de disponibilité (0-20)
        scores['disponibilite'] = self._calculer_score_disponibilite(vehicule)
        
        # Score total
        scores['total'] = sum(scores.values())
        
        return scores
    
    def _calculer_score_prix(self, vehicule: Vehicule) -> int:
        """Calcule le score de compatibilité de prix"""
        if not self.profil_ia.budget_max:
            return 15  # Score neutre si pas de budget
        
        prix = vehicule.prix_moyen
        
        # Si le prix est dans la fourchette idéale (50-80% du budget max)
        budget_ideal_min = self.profil_ia.budget_max * 0.5
        budget_ideal_max = self.profil_ia.budget_max * 0.8
        
        if budget_ideal_min <= prix <= budget_ideal_max:
            return 25
        elif prix <= self.profil_ia.budget_max:
            # Dans le budget mais pas idéal
            ratio = prix / self.profil_ia.budget_max
            return int(15 + (1 - ratio) * 10)
        else:
            # Au-dessus du budget
            ratio = prix / self.profil_ia.budget_max
            return max(0, int(25 - (ratio - 1) * 50))
    
    def _calculer_score_besoins(self, vehicule: Vehicule) -> int:
        """Calcule le score de compatibilité avec les besoins utilisateur"""
        score = 15  # Score de base
        
        # Types de véhicules
        if self.profil_ia.types_vehicule:
            vehicule_type = self._get_type_vehicule(vehicule)
            if vehicule_type in self.profil_ia.types_vehicule:
                score += 8
        
        # Carburant
        if self.profil_ia.preferences_carburant:
            if vehicule.type_carburant in self.profil_ia.preferences_carburant:
                score += 6
        
        # Usage principal
        score += self._calculer_score_usage(vehicule)
        
        # Transmission
        if self.profil_ia.transmission_preferree != 'les_deux':
            if vehicule.transmission == self.profil_ia.transmission_preferree:
                score += 4
        
        # Places et portes
        if vehicule.nombre_places >= self.profil_ia.places_minimales:
            score += 3
        
        if vehicule.nombre_portes >= self.profil_ia.porte_minimales:
            score += 2
        
        # Écologie
        if self.profil_ia.score_ecologique > 70:
            if vehicule.type_carburant == 'electrique':
                score += 5
            elif vehicule.type_carburant == 'hybride':
                score += 3
        
        return min(score, 30)
    
    def _calculer_score_marche(self, vehicule: Vehicule) -> int:
        """Calcule le score basé sur les tendances du marché"""
        score = 12  # Score de base
        
        try:
            # Analyser les annonces récentes pour ce modèle
            annonces_recentes = Annonce.objects.filter(
                vehicule=vehicule,
                date_creation__gte=timezone.now() - timedelta(days=30)
            )
            
            if annonces_recentes.exists():
                # Prix moyen du marché
                prix_marche = annonces_recentes.aggregate(
                    avg_prix=Avg('prix')
                )['avg_prix'] or vehicule.prix_moyen
                
                # Si le prix du véhicule est en dessous du marché
                if vehicule.prix_moyen < prix_marche * 0.95:
                    score += 8
                elif vehicule.prix_moyen < prix_marche:
                    score += 4
                
                # Disponibilité (plus d'annonces = plus disponible)
                nombre_annonces = annonces_recentes.count()
                if nombre_annonces > 10:
                    score += 5
                elif nombre_annonces > 5:
                    score += 3
            
            # Tendance des prix
            tendance = self._analyser_tendance_prix(vehicule)
            if tendance == 'hausse':
                score += 3
            elif tendance == 'stable':
                score += 1
        
        except Exception as e:
            print(f"Erreur calcul score marché: {e}")
        
        return min(score, 25)
    
    def _calculer_score_disponibilite(self, vehicule: Vehicule) -> int:
        """Calcule le score de disponibilité"""
        score = 10  # Score de base
        
        try:
            # Nombre d'annonces actives
            annonces_actives = Annonce.objects.filter(
                vehicule=vehicule,
                est_active=True
            ).count()
            
            if annonces_actives >= 20:
                score += 10
            elif annonces_actives >= 10:
                score += 7
            elif annonces_actives >= 5:
                score += 4
            elif annonces_actives >= 1:
                score += 2
            
            # Vérifier si le véhicule est récent
            if vehicule.annee_debut >= datetime.now().year - 3:
                score += 5
            elif vehicule.annee_debut >= datetime.now().year - 5:
                score += 3
        
        except Exception as e:
            print(f"Erreur calcul score disponibilité: {e}")
        
        return min(score, 20)
    
    def _get_type_vehicule(self, vehicule: Vehicule) -> str:
        """Détermine le type de véhicule basé sur ses caractéristiques"""
        nom_modele = vehicule.modele.nom.lower()
        
        if any(mot in nom_modele for mot in ['suv', 'cross', 'allroad']):
            return 'suv'
        elif any(mot in nom_modele for mot in ['break', 'sw', 'estate']):
            return 'break'
        elif any(mot in nom_modele for mot in ['berline', 'sedan', 'saloon']):
            return 'berline'
        elif any(mot in nom_modele for mot in ['citadine', 'city', 'urban']):
            return 'citadine'
        elif any(mot in nom_modele for mot in ['monospace', 'mpv', 'space']):
            return 'monospace'
        elif any(mot in nom_modele for mot in ['coupe', 'gtc']):
            return 'coupe'
        elif any(mot in nom_modele for mot in ['cabriolet', 'cabrio', 'convertible']):
            return 'cabriolet'
        
        return 'berline'  # Par défaut
    
    def _calculer_score_usage(self, vehicule: Vehicule) -> int:
        """Calcule le score basé sur l'usage principal"""
        usage = self.profil_ia.usage_principal
        score = 0
        
        if usage == 'quotidien':
            # Véhicules pratiques pour tous les jours
            if self._get_type_vehicule(vehicule) in ['citadine', 'berline', 'suv']:
                score += 5
            if vehicule.consommation_moyenne <= 7:  # Faible consommation
                score += 3
                
        elif usage == 'professionnel':
            # Image professionnelle et confort
            if vehicule.marque.nom in ['BMW', 'Mercedes', 'Audi', 'Volkswagen']:
                score += 4
            if self._get_type_vehicule(vehicule) in ['berline', 'suv']:
                score += 4
                
        elif usage == 'famille':
            # Espace et sécurité
            if vehicule.nombre_places >= 5:
                score += 4
            if self._get_type_vehicule(vehicule) in ['monospace', 'break', 'suv']:
                score += 4
                
        elif usage == 'loisir':
            # Performance et style
            if vehicule.puissance_max > 150:
                score += 4
            if self._get_type_vehicule(vehicule) in ['coupe', 'cabriolet', 'suv']:
                score += 3
                
        elif usage == 'sportif':
            # Performance pure
            if vehicule.puissance_max > 200:
                score += 6
            if vehicule.acceleration_0_100 and vehicule.acceleration_0_100 < 8:
                score += 4
        
        return score
    
    def _analyser_tendance_prix(self, vehicule: Vehicule) -> str:
        """Analyse la tendance des prix pour un véhicule"""
        try:
            # Récupérer les prix sur les 90 derniers jours
            date_limite = timezone.now() - timedelta(days=90)
            
            annonces_passees = Annonce.objects.filter(
                vehicule=vehicule,
                date_creation__gte=date_limite - timedelta(days=30),
                date_creation__lt=date_limite
            )
            
            annonces_recentes = Annonce.objects.filter(
                vehicule=vehicule,
                date_creation__gte=date_limite
            )
            
            if annonces_passees.exists() and annonces_recentes.exists():
                prix_passe = annonces_passees.aggregate(avg_prix=Avg('prix'))['avg_prix']
                prix_recent = annonces_recentes.aggregate(avg_prix=Avg('prix'))['avg_prix']
                
                if prix_recent and prix_passe:
                    variation = ((prix_recent - prix_passe) / prix_passe) * 100
                    
                    if variation > 2:
                        return 'hausse'
                    elif variation < -2:
                        return 'baisse'
                    else:
                        return 'stable'
        
        except Exception as e:
            print(f"Erreur analyse tendance prix: {e}")
        
        return 'stable'
    
    def _creer_recommandation(self, vehicule: Vehicule, scores: Dict[str, int]) -> VehicleRecommendation:
        """Crée une recommandation de véhicule"""
        
        # Supprimer les anciennes recommandations pour ce véhicule
        VehicleRecommendation.objects.filter(
            user=self.user,
            vehicule=vehicule
        ).delete()
        
        # Créer la nouvelle recommandation
        recommandation = VehicleRecommendation.objects.create(
            user=self.user,
            vehicule=vehicule,
            score_total=scores['total'],
            score_prix=scores['prix'],
            score_besoins=scores['besoins'],
            score_marche=scores['marche'],
            score_disponibilite=scores['disponibilite'],
            raisons_recommandation=self._generer_raisons(vehicule, scores),
            points_forts=self._generer_points_forts(vehicule),
            points_faibles=self._generer_points_faibles(vehicule),
            prix_estime_1an=self._predire_prix_futur(vehicule, 1),
            prix_estime_3ans=self._predire_prix_futur(vehicule, 3),
            confiance_prediction=self._calculer_confiance_prediction(vehicule)
        )
        
        return recommandation
    
    def _generer_raisons(self, vehicule: Vehicule, scores: Dict[str, int]) -> List[str]:
        """Génère les raisons de la recommandation"""
        raisons = []
        
        if scores['prix'] >= 20:
            raisons.append(f"Prix excellent ({vehicule.prix_moyen:.0f}EUR) dans votre budget")
        
        if scores['besoins'] >= 25:
            raisons.append("Correspond parfaitement à vos besoins et préférences")
        
        if scores['marche'] >= 20:
            raisons.append("Bon rapport qualité-prix sur le marché actuel")
        
        if scores['disponibilite'] >= 15:
            raisons.append("Disponible immédiatement chez plusieurs vendeurs")
        
        # Ajouter des raisons spécifiques
        if vehicule.type_carburant == 'electrique':
            raisons.append("Économique à l'usage et écologique")
        elif vehicule.type_carburant == 'hybride':
            raisons.append("Faible consommation et polyvalent")
        
        if vehicule.nombre_places >= 7:
            raisons.append("Idéal pour les grandes familles")
        
        if vehicule.puissance_max > 200:
            raisons.append("Performances élevées pour une conduite dynamique")
        
        return raisons[:5]  # Limiter à 5 raisons
    
    def _generer_points_forts(self, vehicule: Vehicule) -> List[str]:
        """Génère les points forts du véhicule"""
        points = []
        
        if vehicule.consommation_moyenne and vehicule.consommation_moyenne <= 6:
            points.append("Faible consommation")
        
        if vehicule.nombre_places >= 5:
            points.append("Spacieux")
        
        if vehicule.puissance_max >= 150:
            points.append("Bonne motorisation")
        
        if vehicule.marque.nom in ['Toyota', 'Honda', 'Mazda']:
            points.append("Fiabilité reconnue")
        
        if vehicule.type_carburant in ['electrique', 'hybride']:
            points.append("Respectueux de l'environnement")
        
        if vehicule.annee_debut >= datetime.now().year - 2:
            points.append("Design moderne")
        
        return points[:4]
    
    def _generer_points_faibles(self, vehicule: Vehicule) -> List[str]:
        """Génère les points faibles du véhicule"""
        points = []
        
        if vehicule.consommation_moyenne and vehicule.consommation_moyenne >= 9:
            points.append("Consommation élevée")
        
        if vehicule.prix_moyen > 40000:
            points.append("Prix élevé")
        
        if vehicule.type_carburant == 'diesel':
            points.append("Restrictions urbaines possibles")
        
        if vehicule.nombre_places <= 4:
            points.append("Espace limité")
        
        if vehicule.annee_debut <= datetime.now().year - 8:
            points.append("Design daté")
        
        return points[:3]
    
    def _predire_prix_futur(self, vehicule: Vehicule, annees: int) -> float:
        """Prédit le prix futur du véhicule"""
        try:
            # Taux de décroissance moyen par type de véhicule
            taux_decroissance = {
                'electrique': 0.15,  # 15% par an
                'hybride': 0.18,
                'essence': 0.20,
                'diesel': 0.22
            }
            
            taux = taux_decroissance.get(vehicule.type_carburant, 0.20)
            
            # Ajustement selon la marque
            if vehicule.marque.nom in ['Toyota', 'Honda', 'Mazda']:
                taux *= 0.8  # Meilleure tenue de valeur
            elif vehicule.marque.nom in ['BMW', 'Mercedes', 'Audi']:
                taux *= 0.9
            
            prix_actuel = float(vehicule.prix_moyen)
            prix_futur = prix_actuel * ((1 - taux) ** annees)
            
            return round(prix_futur, 2)
        
        except Exception as e:
            print(f"Erreur prédiction prix futur: {e}")
            return float(vehicule.prix_moyen)
    
    def _calculer_confiance_prediction(self, vehicule: Vehicule) -> int:
        """Calcule le niveau de confiance dans les prédictions"""
        confiance = 70  # Base
        
        # Plus de données = plus de confiance
        try:
            nombre_annonces = Annonce.objects.filter(vehicule=vehicule).count()
            if nombre_annonces >= 50:
                confiance += 20
            elif nombre_annonces >= 20:
                confiance += 10
            elif nombre_annonces >= 10:
                confiance += 5
            
            # Véhicules récents = plus prévisibles
            if vehicule.annee_debut >= datetime.now().year - 3:
                confiance += 10
            elif vehicule.annee_debut >= datetime.now().year - 5:
                confiance += 5
            
        except Exception as e:
            print(f"Erreur calcul confiance: {e}")
        
        return min(confiance, 95)


class MarketAnalyzer:
    """Analyseur des tendances du marché"""
    
    def __init__(self):
        self.insights_cache = {}
    
    def generer_insights_marche(self) -> List[MarketInsight]:
        """Génère des aperçus du marché"""
        insights = []
        
        # Tendance des prix
        insight_prix = self._analyser_tendance_globale_prix()
        if insight_prix:
            insights.append(insight_prix)
        
        # Opportunités
        opportunites = self._identifier_opportunites()
        insights.extend(opportunites)
        
        # Conseils d'achat
        conseils = self._generer_conseils_achat()
        insights.extend(conseils)
        
        return insights[:10]  # Limiter à 10 insights
    
    def _analyser_tendance_globale_prix(self) -> MarketInsight:
        """Analyse la tendance globale des prix"""
        try:
            date_limite = timezone.now() - timedelta(days=30)
            date_precedente = timezone.now() - timedelta(days=60)
            
            # Prix moyens par période
            prix_recent = Annonce.objects.filter(
                date_creation__gte=date_limite
            ).aggregate(avg_prix=Avg('prix'))['avg_prix'] or 0
            
            prix_precedent = Annonce.objects.filter(
                date_creation__gte=date_precedente,
                date_creation__lt=date_limite
            ).aggregate(avg_prix=Avg('prix'))['avg_prix'] or 0
            
            if prix_recent and prix_precedent:
                variation = ((prix_recent - prix_precedent) / prix_precedent) * 100
                
                if abs(variation) > 1:
                    titre = f"Tendance des prix: {variation:+.1f}% ce mois-ci"
                    description = f"Les prix du marché automobile ont {'augmenté' if variation > 0 else 'baissé'} de {abs(variation):.1f}% ce mois-ci."
                    
                    if variation > 0:
                        description += " C'est le moment d'acheter avant que les prix n'augmentent davantage."
                    else:
                        description += " C'est une opportunité pour obtenir un bon prix."
                    
                    return MarketInsight.objects.create(
                        titre=titre,
                        description=description,
                        type_insight='tendance_prix',
                        niveau_impact=min(int(abs(variation) * 5), 80),
                        confiance=85
                    )
        
        except Exception as e:
            print(f"Erreur analyse tendance prix: {e}")
        
        return None
    
    def _identifier_opportunites(self) -> List[MarketInsight]:
        """Identifie les opportunités du marché"""
        opportunites = []
        
        try:
            # Véhicules sous-évalués
            date_limite = timezone.now() - timedelta(days=30)
            
            vehicules_sous_evalues = Vehicule.objects.filter(
                annonce__date_creation__gte=date_limite,
                annonce__prix__lt=F('prix_moyen') * 0.9
            ).distinct()
            
            if vehicules_sous_evalues.exists():
                titre = f"{vehicules_sous_evalues.count()} véhicules sous-évalués disponibles"
                description = f"Nous avons identifié {vehicules_sous_evalues.count()} véhicules vendus à moins de 10% sous leur prix de marché. C'est le moment idéal pour faire une affaire."
                
                opportunite = MarketInsight.objects.create(
                    titre=titre,
                    description=description,
                    type_insight='opportunite',
                    niveau_impact=75,
                    confiance=80
                )
                opportunites.append(opportunite)
        
        except Exception as e:
            print(f"Erreur identification opportunités: {e}")
        
        return opportunites
    
    def _generer_conseils_achat(self) -> List[MarketInsight]:
        """Génère des conseils d'achat"""
        conseils = []
        
        try:
            # Meilleur moment pour acheter
            mois_actuel = timezone.now().month
            
            if mois_actuel in [6, 7, 8]:  # Été
                titre = "Conseil d'achat: Profitez de l'été"
                description = "L'été est une excellente période pour acheter un véhicule. Les vendeurs sont plus flexibles et les promotions sont nombreuses."
                niveau_impact = 60
            elif mois_actuel in [11, 12, 1]:  # Fin d'année
                titre = "Conseil d'achat: Bonnes affaires de fin d'année"
                description = "Les concessionnaires veulent écouler leurs stocks avant la fin d'année. C'est le moment idéal pour négocier."
                niveau_impact = 70
            else:
                titre = "Conseil d'achat: Comparez les prix"
                description = "Prenez le temps de comparer plusieurs offres. Les différences de prix peuvent être significatives pour le même véhicule."
                niveau_impact = 50
            
            conseil = MarketInsight.objects.create(
                titre=titre,
                description=description,
                type_insight='conseil_achat',
                niveau_impact=niveau_impact,
                confiance=75
            )
            conseils.append(conseil)
        
        except Exception as e:
            print(f"Erreur génération conseils: {e}")
        
        return conseils
