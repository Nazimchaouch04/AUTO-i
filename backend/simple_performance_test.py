#!/usr/bin/env python
"""
Test simple de performance sans dépendances complexes
"""
import time
import requests
import statistics

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1ODU0MjQ2LCJpYXQiOjE3NzU4NTA2NDYsImp0aSI6IjIxMTI4MjZkZGU3YzQ1MTg4NDcwMjE2ZTAwOTk5ZjRjIiwidXNlcl9pZCI6IjMifQ.0iMTfq76pHZt4ZupE2LhwT1pSG2BPv2icgv_oip2VeQ"

def test_endpoint_performance(url, name, num_requests=10):
    """Test la performance d'un endpoint"""
    print(f"\n=== Test: {name} ===")
    
    times = []
    success_count = 0
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{BASE_URL}{url}",
                headers={"Authorization": f"Bearer {TOKEN}"},
                timeout=5
            )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # ms
            
            if response.status_code == 200:
                times.append(response_time)
                success_count += 1
                print(f"  Requête {i+1}: {response_time:.1f}ms")
            else:
                print(f"  Requête {i+1}: Erreur {response.status_code}")
                
        except Exception as e:
            print(f"  Requête {i+1}: Exception - {e}")
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        median_time = statistics.median(times)
        
        print(f"  Succès: {success_count}/{num_requests}")
        print(f"  Temps moyen: {avg_time:.1f}ms")
        print(f"  Temps médian: {median_time:.1f}ms")
        print(f"  Temps min: {min_time:.1f}ms")
        print(f"  Temps max: {max_time:.1f}ms")
        
        return {
            'name': name,
            'avg': avg_time,
            'median': median_time,
            'min': min_time,
            'max': max_time,
            'success_rate': success_count / num_requests * 100
        }
    else:
        print(f"  Aucune requête réussie")
        return None

def main():
    """Test principal"""
    print("=" * 50)
    print("TEST SIMPLE DE PERFORMANCE")
    print("=" * 50)
    
    # Vérifier si le serveur est accessible
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=2)
        if response.status_code == 200:
            print("Serveur accessible!")
        else:
            print("Problème de connexion au serveur")
            return
    except Exception as e:
        print(f"Impossible de se connecter au serveur: {e}")
        print("Assurez-vous que le serveur Django est démarré:")
        print("  python manage.py runserver")
        return
    
    # Tests des endpoints
    endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/gamification/", "Gamification Root"),
        ("/api/gamification/profil/", "Gamification Profil"),
        ("/api/subscriptions/", "Subscriptions"),
        ("/api/ai/", "AI Assistant"),
        ("/api/notifications/", "Notifications"),
        ("/api/annonces/", "Annonces"),
        ("/api/vehicules/", "Véhicules"),
    ]
    
    results = []
    
    for url, name in endpoints:
        result = test_endpoint_performance(url, name)
        if result:
            results.append(result)
    
    # Résumé
    if results:
        print("\n" + "=" * 50)
        print("RÉSUMÉ DES PERFORMANCES")
        print("=" * 50)
        print(f"{'Endpoint':20} | {'Avg':6} | {'Min':6} | {'Max':6} | {'Succès':7}")
        print("-" * 55)
        
        for result in results:
            print(f"{result['name']:20} | "
                  f"{result['avg']:6.1f} | "
                  f"{result['min']:6.1f} | "
                  f"{result['max']:6.1f} | "
                  f"{result['success_rate']:6.1f}%")
        
        # Performance globale
        avg_all = statistics.mean([r['avg'] for r in results])
        print("-" * 55)
        print(f"{'Moyenne':20} | {avg_all:6.1f} | {'':6} | {'':6} | {'':7}")
        
        # Recommandations
        print("\n=== RECOMMANDATIONS ===")
        if avg_all > 500:
            print("Les temps de réponse sont élevés (>500ms)")
            print("Recommandations:")
            print("  1. Désactiver DEBUG en production")
            print("  2. Optimiser les requêtes database")
            print("  3. Ajouter du cache")
            print("  4. Utiliser un serveur de production (gunicorn/uwsgi)")
        elif avg_all > 200:
            print("Les temps de réponse sont modérés (200-500ms)")
            print("Recommandations:")
            print("  1. Désactiver DEBUG")
            print("  2. Optimiser les middlewares")
        else:
            print("Les temps de réponse sont bons (<200ms)")
    
    print("\n" + "=" * 50)
    print("TEST TERMINÉ")
    print("=" * 50)

if __name__ == "__main__":
    main()
