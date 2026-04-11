"""
Service NLP simplifié pour éviter les imports circulaires
"""

import re
import json
from typing import Dict, List, Any
from django.utils import timezone
from ..models import IntentAnalysis, UserProfileAnalysis


class SimpleNLPService:
    """Service NLP simplifié sans dépendances aux modèles vehicules"""
    
    def __init__(self):
        self.mots_cles_budget = [
            'budget', 'prix', 'coût', 'cout', 'euros', 'eur', 'euro', 'price', 'cost',
            'maximum', 'max', 'minimum', 'min', 'entre', 'jusqu\'à', 'jusqua'
        ]
        
        self.mots_cles_marques = [
            'renault', 'peugeot', 'citroen', 'volkswagen', 'vw', 'audi', 'bmw', 'mercedes',
            'opel', 'ford', 'toyota', 'nissan', 'honda', 'hyundai', 'kia', 'dacia'
        ]
        
        self.mots_cles_types = [
            'suv', 'berline', 'citadine', 'break', 'monospace', 'coupe', 'cabriolet'
        ]
        
        self.mots_cles_carburant = [
            'essence', 'diesel', 'electrique', 'hybride'
        ]
        
        self.patterns_intent = {
            'recherche_vehicule': [
                r'cherche.*voiture', r'je veux.*voiture', r'recommande.*voiture'
            ],
            'conseil_achat': [
                r'conseil.*achat', r'faut.*acheter', r'bon.*achat'
            ],
            'estimation_prix': [
                r'estimation.*prix', r'combien.*vaut', r'prix.*estime'
            ],
            'information_marche': [
                r'marche.*auto', r'tendance.*prix', r'prix.*marche'
            ]
        }
    
    def nettoyer_texte(self, texte: str) -> str:
        """Nettoie le texte pour l'analyse"""
        if not texte:
            return ""
        
        texte = texte.lower().strip()
        texte = re.sub(r'[^\w\sàâäéèêëïîôöùûüÿç]', ' ', texte)
        texte = re.sub(r'\s+', ' ', texte)
        return texte
    
    def extraire_entites(self, texte: str) -> Dict[str, Any]:
        """Extrait les entités du texte"""
        texte_nettoye = self.nettoyer_texte(texte)
        entites = {
            'budget': None,
            'budget_min': None,
            'budget_max': None,
            'marques': [],
            'types': [],
            'carburants': [],
            'usage': [],
            'transmission': None,
            'places': None,
            'portes': None,
            'annee': None,
            'kilometrage': None
        }
        
        # Extraction du budget
        budget_patterns = [
            r'budget.*?(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e)',
            r'(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e).*?budget',
            r'jusqua?.*?(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e)',
            r'entre.*?(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e).*?et.*?(\d+(?:\s?\d+)*)',
            r'prix.*?(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, texte_nettoye)
            if match:
                if len(match.groups()) == 2:
                    entites['budget_min'] = int(match.group(1).replace(' ', ''))
                    entites['budget_max'] = int(match.group(2).replace(' ', ''))
                else:
                    entites['budget'] = int(match.group(1).replace(' ', ''))
                break
        
        # Extraction des marques
        for marque in self.mots_cles_marques:
            if marque in texte_nettoye:
                entites['marques'].append(marque.capitalize())
        
        # Extraction des types de véhicules
        for type_v in self.mots_cles_types:
            if type_v in texte_nettoye:
                entites['types'].append(type_v)
        
        # Extraction des types de carburant
        for carburant in self.mots_cles_carburant:
            if carburant in texte_nettoye:
                entites['carburants'].append(carburant)
        
        # Extraction de la transmission
        if 'automatique' in texte_nettoye:
            entites['transmission'] = 'automatique'
        elif 'manuelle' in texte_nettoye:
            entites['transmission'] = 'manuelle'
        
        # Extraction du nombre de places
        places_match = re.search(r'(\d+)\s*places?', texte_nettoye)
        if places_match:
            entites['places'] = int(places_match.group(1))
        
        # Extraction du nombre de portes
        portes_match = re.search(r'(\d+)\s*portes?', texte_nettoye)
        if portes_match:
            entites['portes'] = int(portes_match.group(1))
        
        # Extraction de l'année
        annee_match = re.search(r'(20\d{2})', texte_nettoye)
        if annee_match:
            entites['annee'] = int(annee_match.group(1))
        
        return entites
    
    def detecter_intent(self, texte: str) -> str:
        """Détecte l'intention principale du message"""
        texte_nettoye = self.nettoyer_texte(texte)
        
        for intent, patterns in self.patterns_intent.items():
            for pattern in patterns:
                if re.search(pattern, texte_nettoye):
                    return intent
        
        return 'autre'
    
    def analyser_sentiment(self, texte: str) -> str:
        """Analyse le sentiment du message"""
        texte_nettoye = self.nettoyer_texte(texte)
        
        mots_positifs = ['bon', 'bien', 'excellent', 'super', 'parfait', 'content']
        mots_negatifs = ['mauvais', 'nul', 'horrible', 'décevant', 'problème']
        
        score_positif = sum(1 for mot in mots_positifs if mot in texte_nettoye)
        score_negatif = sum(1 for mot in mots_negatifs if mot in texte_nettoye)
        
        if score_positif > score_negatif:
            return 'positif'
        elif score_negatif > score_positif:
            return 'negatif'
        else:
            return 'neutre'
    
    def calculer_urgence(self, texte: str) -> int:
        """Calcule le niveau d'urgence (0-100)"""
        texte_nettoye = self.nettoyer_texte(texte)
        
        mots_urgence = ['urgent', 'rapidement', 'vite', 'de suite', 'maintenant']
        score_urgence = sum(1 for mot in mots_urgence if mot in texte_nettoye)
        
        return min(score_urgence * 20, 100)
    
    def analyser_message(self, message_texte: str, contexte_conversation: Dict = None) -> Dict[str, Any]:
        """Analyse complète d'un message"""
        if contexte_conversation is None:
            contexte_conversation = {}
        
        entites = self.extraire_entites(message_texte)
        intent = self.detecter_intent(message_texte)
        sentiment = self.analyser_sentiment(message_texte)
        urgence = self.calculer_urgence(message_texte)
        
        return {
            'intent_principale': intent,
            'entites': entites,
            'sentiment': sentiment,
            'niveau_urgence': urgence,
            'contexte_conversation': contexte_conversation
        }


class SimpleUserProfileAnalyzer:
    """Analyseur de profil utilisateur simplifié"""
    
    def __init__(self, user):
        self.user = user
        self.nlp_service = SimpleNLPService()
    
    def mettre_a_jour_profil_ia(self, message_texte: str) -> UserProfileAnalysis:
        """Met à jour le profil IA basé sur le nouveau message"""
        profil, created = UserProfileAnalysis.objects.get_or_create(user=self.user)
        
        # Analyser le message
        analyse = self.nlp_service.analyser_message(message_texte)
        entites = analyse['entites']
        
        # Mettre à jour le budget
        if entites.get('budget'):
            if not profil.budget_min or entites['budget'] < profil.budget_min:
                profil.budget_min = entites['budget']
            if not profil.budget_max or entites['budget'] > profil.budget_max:
                profil.budget_max = entites['budget']
        
        if entites.get('budget_min') and entites.get('budget_max'):
            profil.budget_min = entites['budget_min']
            profil.budget_max = entites['budget_max']
        
        # Mettre à jour les types de véhicules
        if entites.get('types'):
            types_actuels = set(profil.types_vehicule)
            types_actuels.update(entites['types'])
            profil.types_vehicule = list(types_actuels)
        
        # Mettre à jour les préférences de carburant
        if entites.get('carburants'):
            carburants_actuels = set(profil.preferences_carburant)
            carburants_actuels.update(entites['carburants'])
            profil.preferences_carburant = list(carburants_actuels)
        
        # Mettre à jour les contraintes
        if entites.get('places'):
            profil.places_minimales = max(profil.places_minimales, entites['places'])
        
        if entites.get('portes'):
            profil.porte_minimales = max(profil.porte_minimales, entites['portes'])
        
        if entites.get('transmission'):
            if profil.transmission_preferree == 'les_deux':
                profil.transmission_preferree = entites['transmission']
        
        # Recalculer les scores
        profil.score_budget = self._calculer_score_budget(profil)
        profil.score_ecologique = self._calculer_score_ecologique(profil)
        profil.score_praticite = self._calculer_score_praticite(profil)
        
        profil.save()
        return profil
    
    def _calculer_score_budget(self, profil: UserProfileAnalysis) -> int:
        """Calcule le score de budget (0-100)"""
        if not profil.budget_max:
            return 50
        
        budget_normalized = min(max(profil.budget_max, 5000), 50000)
        score = 90 - ((budget_normalized - 5000) / 45000) * 80
        return int(score)
    
    def _calculer_score_ecologique(self, profil: UserProfileAnalysis) -> int:
        """Calcule le score écologique (0-100)"""
        score = 50
        
        if 'electrique' in profil.preferences_carburant:
            score += 30
        elif 'hybride' in profil.preferences_carburant:
            score += 20
        elif 'diesel' in profil.preferences_carburant:
            score -= 20
        
        return max(0, min(100, score))
    
    def _calculer_score_praticite(self, profil: UserProfileAnalysis) -> int:
        """Calcule le score de praticité (0-100)"""
        score = 50
        
        if profil.usage_principal == 'famille':
            score += 20
        elif profil.usage_principal == 'professionnel':
            score += 15
        
        if profil.places_minimales >= 5:
            score += 15
        
        if profil.porte_minimales >= 5:
            score += 10
        
        return max(0, min(100, score))
