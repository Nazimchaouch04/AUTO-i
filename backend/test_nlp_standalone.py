#!/usr/bin/env python3
"""
Test standalone du service NLP sans aucune dépendance Django
"""

import re
import json
from typing import Dict, List, Any


class SimpleNLPService:
    """Service NLP simplifié pour test standalone"""
    
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


def main():
    """Test du service NLP standalone"""
    print("=" * 60)
    print("TEST STANDALONE DU SERVICE NLP")
    print("=" * 60)
    
    nlp_service = SimpleNLPService()
    
    # Messages de test
    test_scenarios = [
        {
            'message': 'Je cherche une Renault Clio avec budget 15000 euros',
            'expected_intent': 'recherche_vehicule',
            'expected_entities': {'budget': 15000, 'marques': ['Renault']}
        },
        {
            'message': 'SUV familial diesel moins de 25000 EUR',
            'expected_intent': 'recherche_vehicule',
            'expected_entities': {'budget_max': 25000, 'types': ['suv'], 'carburants': ['diesel']}
        },
        {
            'message': 'BMW électrique automatique 5 places',
            'expected_intent': 'recherche_vehicule',
            'expected_entities': {'marques': ['Bmw'], 'carburants': ['electrique'], 'transmission': 'automatique', 'places': 5}
        },
        {
            'message': 'Quel est le meilleur moment pour acheter une voiture ?',
            'expected_intent': 'conseil_achat',
            'expected_entities': {}
        },
        {
            'message': 'Combien vaut ma voiture de 2019 ?',
            'expected_intent': 'estimation_prix',
            'expected_entities': {'annee': 2019}
        },
        {
            'message': 'Comment évoluent les prix des voitures électriques ?',
            'expected_intent': 'information_marche',
            'expected_entities': {'carburants': ['electrique']}
        },
        {
            'message': 'Compare Peugeot 208 et Renault Clio',
            'expected_intent': 'autre',
            'expected_entities': {'marques': ['Peugeot', 'Renault']}
        }
    ]
    
    print("\n=== Test d'analyse complète ===")
    
    success_count = 0
    total_count = len(test_scenarios)
    
    for i, scenario in enumerate(test_scenarios, 1):
        message = scenario['message']
        analyse = nlp_service.analyser_message(message)
        
        print(f"\n--- Test {i}/{total_count} ---")
        print(f"Message: {message}")
        print(f"Intent détecté: {analyse['intent_principale']}")
        print(f"Intent attendu: {scenario['expected_intent']}")
        print(f"Entités détectées: {analyse['entites']}")
        print(f"Entités attendues: {scenario['expected_entities']}")
        print(f"Sentiment: {analyse['sentiment']}")
        print(f"Urgence: {analyse['niveau_urgence']}")
        
        # Vérification
        intent_ok = analyse['intent_principale'] == scenario['expected_intent']
        
        # Vérification des entités principales
        entities_ok = True
        for key, expected_value in scenario['expected_entities'].items():
            if isinstance(expected_value, list):
                if key not in analyse['entites']:
                    entities_ok = False
                    break
                elif not all(item in analyse['entites'][key] for item in expected_value):
                    entities_ok = False
                    break
            else:
                if key not in analyse['entites'] or analyse['entites'][key] != expected_value:
                    entities_ok = False
                    break
        
        result = "SUCCESS" if intent_ok and entities_ok else "ÉCHEC"
        print(f"Résultat: {result}")
        if result == "SUCCESS":
            success_count += 1
        else:
            if not intent_ok:
                print(f"  - Intent incorrect")
            if not entities_ok:
                print(f"  - Entités incorrectes")
        
        print("-" * 50)
    
    print(f"\n" + "=" * 60)
    print(f"RÉSULTAT FINAL: {success_count}/{total_count} tests réussis")
    print(f"Précision: {(success_count/total_count)*100:.1f}%")
    print("=" * 60)
    
    if success_count == total_count:
        print("Le service NLP fonctionne parfaitement!")
    else:
        print("Quelques améliorations sont nécessaires.")
    
    return success_count == total_count


if __name__ == "__main__":
    main()
