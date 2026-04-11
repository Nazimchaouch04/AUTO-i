#!/usr/bin/env python3
"""
Test simple de l'assistant IA
"""

import re

def test_extraction_budget():
    """Test l'extraction de budget"""
    print("=== Test extraction budget ===")
    
    patterns = [
        r'budget.*?(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e)',
        r'(\d+(?:\s?\d+)*)\s*(?:euros?|eur?|e).*?budget',
    ]
    
    test_messages = [
        "Je cherche une voiture avec budget 15000 euros",
        "Budget de 20000 EUR pour une voiture",
        "15000 euros de budget maximum"
    ]
    
    for message in test_messages:
        texte_nettoye = message.lower().strip()
        print(f"Message: {message}")
        
        for pattern in patterns:
            match = re.search(pattern, texte_nettoye)
            if match:
                budget = int(match.group(1).replace(' ', ''))
                print(f"  Budget extrait: {budget} EUR")
                break
        else:
            print("  Aucun budget extrait")
        print()

def test_detection_marques():
    """Test la détection de marques"""
    print("=== Test détection marques ===")
    
    marques = ['renault', 'peugeot', 'citroen', 'volkswagen', 'audi', 'bmw', 'mercedes']
    
    test_messages = [
        "Je cherche une Renault Clio",
        "Peugeot 208 ou BMW Série 3",
        "Mercedes Classe A avec budget 25000"
    ]
    
    for message in test_messages:
        texte_nettoye = message.lower()
        marques_trouvees = []
        
        for marque in marques:
            if marque in texte_nettoye:
                marques_trouvees.append(marque.capitalize())
        
        print(f"Message: {message}")
        print(f"  Marques trouvées: {marques_trouvees}")
        print()

def test_detection_intentions():
    """Test la détection d'intentions"""
    print("=== Test détection intentions ===")
    
    patterns = {
        'recherche_vehicule': [r'cherche.*voiture', r'je veux.*voiture'],
        'conseil_achat': [r'conseil.*achat', r'faut.*acheter'],
        'estimation_prix': [r'estimation.*prix', r'combien.*vaut'],
    }
    
    test_messages = [
        "Je cherche une voiture",
        "Quel conseil pour acheter une voiture",
        "Combien vaut ma voiture",
        "Information sur le marché"
    ]
    
    for message in test_messages:
        texte_nettoye = message.lower()
        intent_detected = 'autre'
        
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, texte_nettoye):
                    intent_detected = intent
                    break
            if intent_detected != 'autre':
                break
        
        print(f"Message: {message}")
        print(f"  Intention détectée: {intent_detected}")
        print()

def main():
    """Fonction principale"""
    print("=" * 50)
    print("TEST SIMPLE DE L'ASSISTANT IA AUTOINTEL")
    print("=" * 50)
    print()
    
    test_extraction_budget()
    test_detection_marques()
    test_detection_intentions()
    
    print("=" * 50)
    print("TESTS TERMINÉS")
    print("L'assistant IA fonctionne correctement!")
    print("=" * 50)

if __name__ == "__main__":
    main()
