#!/usr/bin/env python
"""
Test de tous les endpoints API AutoIntel
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1ODU0MjQ2LCJpYXQiOjE3NzU4NTA2NDYsImp0aSI6IjIxMTI4MjZkZGU3YzQ1MTg4NDcwMjE2ZTAwOTk5ZjRjIiwidXNlcl9pZCI6IjMifQ.0iMTfq76pHZt4ZupE2LhwT1pSG2BPv2icgv_oip2VeQ"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_endpoint(name, url, method="GET", data=None):
    """Test un endpoint spécifique"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{url}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{url}", headers=headers, json=data)
        else:
            return False, "Method not supported"
        
        success = response.status_code == 200
        message = f"Status: {response.status_code}"
        if success:
            try:
                content = response.json()
                if "message" in content:
                    message += f" | Message: {content['message']}"
                elif "count" in content:
                    message += f" | Count: {content['count']}"
                elif len(content) > 0:
                    message += f" | Items: {len(content)}"
            except:
                message += f" | Content length: {len(response.text)}"
        
        return success, message
        
    except Exception as e:
        return False, f"Exception: {str(e)}"

def main():
    """Test tous les endpoints principaux"""
    print("=== Test de tous les endpoints API AutoIntel ===\n")
    
    endpoints = [
        ("Health Check", "/api/health/"),
        ("Gamification Root", "/api/gamification/"),
        ("Gamification Profil", "/api/gamification/profil/"),
        ("Gamification Leaderboard", "/api/gamification/leaderboard/"),
        ("Subscriptions Root", "/api/subscriptions/"),
        ("Subscriptions Plans", "/api/subscriptions/plans/"),
        ("AI Assistant Root", "/api/ai/"),
        ("Notifications Root", "/api/notifications/"),
        ("Annonces Root", "/api/annonces/"),
        ("Véhicules Root", "/api/vehicules/"),
        ("Alertes", "/api/alertes/"),
        ("Dashboard", "/api/dashboard/"),
        ("Rapports", "/api/rapports/"),
    ]
    
    results = []
    
    for name, url in endpoints:
        success, message = test_endpoint(name, url)
        status = "OK" if success else "FAIL"
        results.append((name, status, message))
        print(f"{name:25} | {status:5} | {message}")
    
    # Résumé
    print(f"\n=== Résumé ===")
    ok_count = sum(1 for _, status, _ in results if status == "OK")
    total_count = len(results)
    print(f"Endpoints testés: {total_count}")
    print(f"Succès: {ok_count}")
    print(f"Échecs: {total_count - ok_count}")
    print(f"Taux de réussite: {ok_count/total_count*100:.1f}%")
    
    if ok_count == total_count:
        print("Tous les endpoints fonctionnent parfaitement! :)")
    else:
        print("Certains endpoints ont des problèmes à vérifier.")

if __name__ == "__main__":
    main()
