#!/usr/bin/env python
"""
Test de performance en mode production
"""
import os
import subprocess
import time
import requests

def set_production_mode():
    """Configure l'environnement pour le mode production"""
    print("=== Configuration Mode Production ===")
    
    # Modifier le .env temporairement
    env_file = "c:\\Users\\PC DZ\\Desktop\\AUTO-P\\backend\\.env"
    
    # Lire le fichier .env actuel
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Remplacer DEBUG=True par DEBUG=False
    content_prod = content.replace("DEBUG=True", "DEBUG=False")
    
    # Écrire le fichier temporaire
    with open(env_file, 'w') as f:
        f.write(content_prod)
    
    print("DEBUG désactivé pour les tests de performance")

def restore_debug_mode():
    """Restaure le mode debug"""
    print("\n=== Restauration Mode Debug ===")
    
    env_file = "c:\\Users\\PC DZ\\Desktop\\AUTO-P\\backend\\.env"
    
    # Lire le fichier .env actuel
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Remplacer DEBUG=False par DEBUG=True
    content_debug = content.replace("DEBUG=False", "DEBUG=True")
    
    # Écrire le fichier
    with open(env_file, 'w') as f:
        f.write(content_debug)
    
    print("DEBUG réactivé")

def restart_server():
    """Redémarre le serveur Django"""
    print("\n=== Redémarrage Serveur ===")
    
    # Arrêter les processus Python
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
    except:
        pass
    
    # Démarrer le serveur en arrière-plan
    subprocess.Popen([
        'python', 'manage.py', 'runserver'
    ], cwd='c:\\Users\\PC DZ\\Desktop\\AUTO-P\\backend')
    
    # Attendre que le serveur démarre
    time.sleep(5)
    print("Serveur redémarré")

def test_performance(mode_name):
    """Test les performances dans le mode donné"""
    print(f"\n=== Test Performance Mode {mode_name} ===")
    
    # Test avec curl pour plus de précision
    endpoints = [
        ("Health Check", "/api/health/"),
        ("Gamification", "/api/gamification/"),
        ("Profil", "/api/gamification/profil/"),
        ("Subscriptions", "/api/subscriptions/"),
        ("AI Assistant", "/api/ai/"),
    ]
    
    results = []
    
    for name, endpoint in endpoints:
        try:
            # Faire 5 requêtes et calculer la moyenne
            times = []
            for _ in range(5):
                result = subprocess.run([
                    'curl', '-w', '%{time_total}',
                    '-s', '-o', '/dev/null',
                    f'http://localhost:8000{endpoint}'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    times.append(float(result.stdout.strip()) * 1000)  # Convertir en ms
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                results.append((name, avg_time, min_time, max_time))
                print(f"{name:20} | Avg: {avg_time:6.1f}ms | "
                      f"Min: {min_time:6.1f}ms | Max: {max_time:6.1f}ms")
            else:
                print(f"{name:20} | Échec des requêtes")
                
        except Exception as e:
            print(f"{name:20} | Erreur: {e}")
    
    return results

def compare_results(debug_results, prod_results):
    """Compare les résultats entre debug et production"""
    print("\n=== Comparaison Debug vs Production ===")
    
    if not debug_results or not prod_results:
        print("Impossible de comparer - résultats manquants")
        return
    
    print(f"{'Endpoint':20} | {'Debug':8} | {'Prod':8} | {'Amélioration':12}")
    print("-" * 55)
    
    total_improvement = 0
    count = 0
    
    for debug_result, prod_result in zip(debug_results, prod_results):
        debug_name, debug_avg, _, _ = debug_result
        prod_name, prod_avg, _, _ = prod_result
        
        if debug_name == prod_name:
            improvement = ((debug_avg - prod_avg) / debug_avg) * 100
            total_improvement += improvement
            count += 1
            
            print(f"{debug_name:20} | {debug_avg:7.1f}ms | {prod_avg:7.1f}ms | "
                  f"{improvement:+10.1f}%")
    
    if count > 0:
        avg_improvement = total_improvement / count
        print("-" * 55)
        print(f"{'Moyenne':20} | {'':8} | {'':8} | {avg_improvement:+10.1f}%")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TEST DE PERFORMANCE - COMPARAISON DEBUG VS PRODUCTION")
    print("=" * 60)
    
    try:
        # Test en mode debug d'abord
        print("1. Test en mode DEBUG (actuel)")
        debug_results = test_performance("DEBUG")
        
        # Passer en mode production
        set_production_mode()
        restart_server()
        
        # Test en mode production
        print("\n2. Test en mode PRODUCTION")
        prod_results = test_performance("PRODUCTION")
        
        # Comparer les résultats
        compare_results(debug_results, prod_results)
        
    finally:
        # Toujours restaurer le mode debug
        restore_debug_mode()
        restart_server()
    
    print("\n" + "=" * 60)
    print("TESTS TERMINÉS")
    print("=" * 60)

if __name__ == "__main__":
    main()
