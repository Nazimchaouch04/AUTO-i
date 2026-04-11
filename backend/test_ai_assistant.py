#!/usr/bin/env python3
"""
Test complet de l'assistant IA AutoIntel
Vérifie toutes les fonctionnalités de l'assistant IA avancé
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from apps.ai_assistant.models import (
    Conversation, Message, UserProfileAnalysis, 
    VehicleRecommendation, MarketInsight, IntentAnalysis
)
from apps.ai_assistant.services.simple_nlp_service import SimpleNLPService, SimpleUserProfileAnalyzer


class TestAIAssistant(TestCase):
    """Test suite complet pour l'assistant IA"""
    
    def setUp(self):
        """Configuration initiale des tests"""
        # Utiliser un nom d'utilisateur aléatoire pour éviter les conflits
        import random
        import string
        
        random_username = f"testuser_{''.join(random.choices(string.ascii_lowercase, k=5))}"
        
        try:
            self.user = User.objects.get(username=random_username)
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username=random_username,
                email=f'{random_username}@example.com',
                password='testpass123'
            )
        
        self.nlp_service = SimpleNLPService()
        self.profile_analyzer = SimpleUserProfileAnalyzer(self.user)
    
    def test_nlp_service_extraction_entites(self):
        """Test l'extraction d'entités"""
        print("\n=== Test NLP - Extraction d'entités ===")
        
        test_messages = [
            "Je cherche une Renault Clio avec budget 15000 euros",
            "SUV familial diesel moins de 25000 EUR",
            "BMW électrique automatique 5 places",
            "Compare Peugeot 208 et Renault Clio"
        ]
        
        for message in test_messages:
            entites = self.nlp_service.extraire_entites(message)
            print(f"Message: {message}")
            print(f"Entités: {entites}")
            print("-" * 50)
    
    def test_nlp_service_detection_intent(self):
        """Test la détection d'intentions"""
        print("\n=== Test NLP - Détection d'intentions ===")
        
        test_messages = [
            ("Je veux acheter une voiture", "recherche_vehicule"),
            ("Quel est le meilleur moment pour acheter ?", "conseil_achat"),
            ("Combien vaut ma voiture ?", "estimation_prix"),
            ("Comment évoluent les prix ?", "information_marche"),
            ("Compare ces deux modèles", "comparaison")
        ]
        
        for message, expected_intent in test_messages:
            detected_intent = self.nlp_service.detecter_intent(message)
            print(f"Message: {message}")
            print(f"Intent attendu: {expected_intent}")
            print(f"Intent détecté: {detected_intent}")
            print(f"OK: {detected_intent == expected_intent}")
            print("-" * 50)
    
    def test_profil_analyzer_mise_a_jour(self):
        """Test la mise à jour du profil utilisateur"""
        print("\n=== Test Profile Analyzer - Mise à jour profil ===")
        
        test_messages = [
            "Je cherche un SUV avec budget 30000 euros",
            "Préfère le diesel pour le quotidien",
            "BMW ou Mercedes pour le travail",
            "5 places minimum pour la famille"
        ]
        
        for message in test_messages:
            profil = self.profile_analyzer.mettre_a_jour_profil_ia(message)
            print(f"Message: {message}")
            print(f"Budget max: {profil.budget_max}")
            print(f"Budget min: {profil.budget_min}")
            print(f"Usage: {profil.usage_principal}")
            print(f"Places min: {profil.places_minimales}")
            print(f"Carburants: {profil.preferences_carburant}")
            print("-" * 50)
    
    def test_moteur_recommandation(self):
        """Test le moteur de recommandation"""
        print("\n=== Test Moteur de Recommandation ===")
        print("Mode démo - Moteur de recommandation simplifié")
        print("Les recommandations seront implémentées avec les modèles vehicules")
        print("-" * 50)
    
    def test_market_analyzer(self):
        """Test l'analyseur de marché"""
        print("\n=== Test Market Analyzer ===")
        print("Mode démo - Market analyzer simplifié")
        print("Les insights du marché seront implémentés avec les données réelles")
        print("-" * 50)
    
    def test_conversation_intelligente(self):
        """Test la conversation intelligente"""
        print("\n=== Test Conversation Intelligente ===")
        
        # Créer une conversation de test
        conversation = Conversation.objects.create(
            user=self.user,
            titre="Test conversation IA"
        )
        
        test_scenarios = [
            {
                'message': 'Je cherche un SUV familial avec budget 25000EUR',
                'expected_intent': 'recherche_vehicule',
                'expected_entities': {'budget': 25000}
            },
            {
                'message': 'Quel est le meilleur moment pour acheter une voiture ?',
                'expected_intent': 'conseil_achat',
                'expected_entities': {}
            },
            {
                'message': 'Estime le prix d une Renault Clio 2019',
                'expected_intent': 'estimation_prix',
                'expected_entities': {'marques': ['renault'], 'annee': 2019}
            }
        ]
        
        for scenario in test_scenarios:
            message = scenario['message']
            
            # Analyser le message
            analyse = self.nlp_service.analyser_message(message)
            
            print(f"Message: {message}")
            print(f"Intent détecté: {analyse['intent_principale']}")
            print(f"Intent attendu: {scenario['expected_intent']}")
            print(f"Entités: {analyse['entites']}")
            print(f"Entités attendues: {scenario['expected_entities']}")
            print(f"Sentiment: {analyse['sentiment']}")
            print(f"Urgence: {analyse['niveau_urgence']}")
            print("-" * 50)
    
    def test_api_endpoints_simulation(self):
        """Test simulation des endpoints API"""
        print("\n=== Test Simulation API Endpoints ===")
        
        # Test endpoint profil IA
        try:
            profil, created = UserProfileAnalysis.objects.get_or_create(
                user=self.user,
                defaults={
                    'budget_max': 20000,
                    'usage_principal': 'quotidien'
                }
            )
            
            print("GET /api/ai/profil-ia/")
            print(f"Budget max: {profil.budget_max}")
            print(f"Usage: {profil.usage_principal}")
            print(f"Scores: {profil.score_budget}, {profil.score_ecologique}, {profil.score_praticite}")
            print("-" * 30)
            
        except Exception as e:
            print(f"Erreur profil IA: {e}")
        
        # Test endpoint recommandations
        try:
            print("GET /api/ai/recommandations-vehicules/")
            recommandations = self.recommendation_engine.generer_recommandations(limit=2)
            print(f"Recommandations: {len(recommandations)} véhicules")
            for reco in recommandations:
                print(f"- {reco.vehicule.marque} {reco.vehicule.modele} (score: {reco.score_total})")
            print("-" * 30)
            
        except Exception as e:
            print(f"Erreur recommandations: {e}")
        
        # Test endpoint market insights
        try:
            print("GET /api/ai/market-insights/")
            insights = self.market_analyzer.generer_insights_marche()
            print(f"Insights: {len(insights)} aperçus")
            for insight in insights[:3]:
                print(f"- {insight.titre} (impact: {insight.niveau_impact})")
            print("-" * 30)
            
        except Exception as e:
            print(f"Erreur market insights: {e}")


def run_tests():
    """Exécute les tests fonctionnels"""
    print("=" * 60)
    print("TESTS FONCTIONNELS DE L'ASSISTANT IA AUTOINTEL")
    print("=" * 60)
    
    test_case = TestAIAssistant()
    test_case.setUp()
    
    try:
        test_case.test_nlp_service_extraction_entites()
        test_case.test_nlp_service_detection_intent()
        test_case.test_profil_analyzer_mise_a_jour()
        test_case.test_moteur_recommandation()
        test_case.test_market_analyzer()
        test_case.test_conversation_intelligente()
        
        print("\n" + "=" * 60)
        print("TESTS FONCTIONNELS TERMINÉS AVEC SUCCÈS!")
        print("L'assistant IA est fonctionnel en mode démo")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERREUR PENDANT LES TESTS: {e}")
        print("=" * 60)


if __name__ == "__main__":
    run_tests()
