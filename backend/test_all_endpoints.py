#!/usr/bin/env python
"""
Test de tous les endpoints API AutoIntel
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "test"
PASSWORD = "newtest123"

BASE_HEADERS = {
    "Content-Type": "application/json",
}


def get_access_token():
    """Récupère un token JWT via l'endpoint login."""
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(
        f"{BASE_URL}/api/auth/login/", headers=BASE_HEADERS, json=payload
    )
    if response.status_code != 200:
        return None, response
    data = response.json()
    return data.get("access"), response


def build_auth_headers(token):
    headers = dict(BASE_HEADERS)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def test_endpoint(name, url, method="GET", data=None, headers=None):
    """Test un endpoint spécifique"""
    try:
        if headers is None:
            headers = BASE_HEADERS
        if method == "GET":
            response = requests.get(f"{BASE_URL}{url}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{url}", headers=headers, json=data)
        else:
            return False, "Method not supported"
        
        success = response.status_code in (200, 201)
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

    token, login_response = get_access_token()
    if not token:
        print(
            "Login JWT               | FAIL  | "
            f"Status: {login_response.status_code} | {login_response.text}"
        )
        print("\nImpossible de continuer les tests authentifiés sans token.")
        return
    print("Login JWT               | OK    | Status: 200")

    auth_headers = build_auth_headers(token)
    
    endpoints = [
        # Public
        ("Health Check", "/api/health/", False),

        # Authenticated
        ("Gamification Root", "/api/gamification/", True),
        ("Gamification Profil", "/api/gamification/profil/", True),
        ("Gamification Leaderboard", "/api/gamification/leaderboard/", True),
        ("Subscriptions Root", "/api/subscriptions/", True),
        ("Subscriptions Plans", "/api/subscriptions/plans/", True),
        ("AI Assistant Root", "/api/ai/", True),
        ("Notifications Root", "/api/notifications/", True),
        ("Annonces Root", "/api/annonces/", True),
        ("Véhicules Root", "/api/vehicules/", True),
        ("Alertes", "/api/alertes/", True),
        ("Dashboard", "/api/dashboard/", True),
        ("Rapports", "/api/rapports/", True),
    ]
    
    results = []
    
    for name, url, requires_auth in endpoints:
        headers = auth_headers if requires_auth else BASE_HEADERS
        success, message = test_endpoint(name, url, headers=headers)
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
