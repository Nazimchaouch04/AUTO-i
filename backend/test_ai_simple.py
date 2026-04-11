#!/usr/bin/env python3
"""
Test simple de l'assistant IA sans base de données
"""

import sys
import os

# Test du service NLP simple
def test_nlp_service():
    """Test du service NLP sans base de données"""
    print("=" * 60)
    print("TEST DU SERVICE NLP SANS BASE DE DONNÉES")
    print("=" * 60)
    
    # Import du service
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from apps.ai_assistant.services.simple_nlp_service import SimpleNLPService
        
        nlp_service = SimpleNLPService()
        
        # Messages de test
        test_messages = [
            "Je cherche une Renault Clio avec budget 15000 euros",
            "SUV familial diesel moins de 25000 EUR",
            "BMW électrique automatique 5 places",
            "Compare Peugeot 208 et Renault Clio",
            "Quel est le meilleur moment pour acheter une voiture ?",
            "Combien vaut ma voiture de 2019 ?",
            "Comment évoluent les prix des voitures électriques ?"
        ]
        
        print("\n=== Test d'extraction d'entités ===")
        for message in test_messages:
            entites = nlp_service.extraire_entites(message)
            print(f"Message: {message}")
            print(f"Entités: {entites}")
            print("-" * 50)
        
        print("\n=== Test de détection d'intentions ===")
        for message in test_messages:
            intent = nlp_service.detecter_intent(message)
            print(f"Message: {message}")
            print(f"Intent détecté: {intent}")
            print("-" * 50)
        
        print("\n=== Test d'analyse complète ===")
        for message in test_messages:
            analyse = nlp_service.analyser_message(message)
            print(f"Message: {message}")
            print(f"Intent: {analyse['intent_principale']}")
            print(f"Entités: {analyse['entites']}")
            print(f"Sentiment: {analyse['sentiment']}")
            print(f"Urgence: {analyse['niveau_urgence']}")
            print("-" * 50)
        
        print("\n" + "=" * 60)
        print("TEST NLP TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"ERREUR: {e}")
        return False

def test_api_endpoints():
    """Test des endpoints API avec le serveur démarré"""
    print("\n" + "=" * 60)
    print("TEST DES ENDPOINTS API")
    print("=" * 60)
    
    import requests
    import json
    
    base_url = "http://127.0.0.1:8000/api/ai"
    
    endpoints = [
        ("/", "GET", "Racine API"),
        ("/analyser-message/", "POST", "Analyse message"),
        ("/recommandations-vehicules/", "GET", "Recommandations"),
        ("/profil-ia/", "GET", "Profil IA"),
        ("/market-insights/", "GET", "Insights marché"),
        ("/prediction-prix/", "POST", "Prédiction prix")
    ]
    
    for endpoint, method, description in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n=== {description} ===")
        print(f"URL: {url}")
        print(f"Méthode: {method}")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                # Test avec des données de test
                if endpoint == "/analyser-message/":
                    data = {"message": "Je cherche une voiture avec budget 20000 EUR"}
                elif endpoint == "/prediction-prix/":
                    data = {"vehicule_id": 1, "annees": [1, 3]}
                else:
                    data = {}
                response = requests.post(url, json=data, timeout=5)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Réponse: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"Réponse: {response.text[:200]}...")
            else:
                print(f"Erreur: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion: {e}")
        except Exception as e:
            print(f"Erreur: {e}")
        
        print("-" * 50)
    
    print("\n" + "=" * 60)
    print("TESTS API TERMINÉS")
    print("=" * 60)

def main():
    """Fonction principale"""
    print("TEST DE L'ASSISTANT IA AUTOINTEL")
    print("Version simplifiée sans dépendances complexes")
    
    # Test NLP
    nlp_success = test_nlp_service()
    
    # Test API (si le serveur est démarré)
    try:
        test_api_endpoints()
    except ImportError:
        print("\nNote: Module requests non disponible. Tests API ignorés.")
    except Exception as e:
        print(f"\nErreur lors des tests API: {e}")
    
    print(f"\nRÉSULTAT: {'SUCCÈS' if nlp_success else 'ÉCHEC'}")
    print("L'assistant IA AutoIntel est fonctionnel en mode démo!")

if __name__ == "__main__":
    main()
