#!/usr/bin/env python
"""
Test de performance avec Gunicorn
"""
import subprocess
import time
import requests
import statistics
import signal
import os

def start_gunicorn():
    """Démarre Gunicorn en arrière-plan"""
    print("=== Démarrage de Gunicorn ===")
    
    # Commande Gunicorn pour Windows (utiliser waitress si nécessaire)
    cmd = [
        'python', '-m', 'waitress', 
        '--host=0.0.0.0', 
        '--port=8000', 
        'autointel.wsgi:application'
    ]
    
    # Essayer d'installer waitress si non disponible
    try:
        import waitress
    except ImportError:
        print("Installation de waitress...")
        subprocess.run(['pip', 'install', 'waitress'], check=True)
    
    # Démarrer le serveur
    process = subprocess.Popen(
        cmd,
        cwd='c:\\Users\\PC DZ\\Desktop\\AUTO-P\\backend',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre que le serveur démarre
    time.sleep(5)
    
    # Vérifier si le process est en cours
    if process.poll() is None:
        print("Gunicorn/Waitress démarré avec succès!")
        return process
    else:
        stdout, stderr = process.communicate()
        print(f"Erreur de démarrage: {stderr.decode()}")
        return None

def test_performance_with_server(base_url, server_name):
    """Test les performances avec un serveur spécifique"""
    print(f"\n=== Test Performance avec {server_name} ===")
    
    # Token JWT
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1ODU0MjQ2LCJpYXQiOjE3NzU4NTA2NDYsImp0aSI6IjIxMTI4MjZkZGU3YzQ1MTg4NDcwMjE2ZTAwOTk5ZjRjIiwidXNlcl9pZCI6IjMifQ.0iMTfq76pHZt4ZupE2LhwT1pSG2BPv2icgv_oip2VeQ"
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/gamification/", "Gamification"),
    ]
    
    results = []
    
    for url, name in endpoints:
        times = []
        success_count = 0
        
        print(f"\nTest: {name}")
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}{url}", headers=headers, timeout=5)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = (end_time - start_time) * 1000
                    times.append(response_time)
                    success_count += 1
                    print(f"  Requête {i+1}: {response_time:.1f}ms")
                else:
                    print(f"  Requête {i+1}: Erreur {response.status_code}")
                    
            except Exception as e:
                print(f"  Requête {i+1}: Exception - {e}")
        
        if times:
            avg_time = statistics.mean(times)
            results.append((name, avg_time))
            print(f"  Moyenne: {avg_time:.1f}ms")
    
    return results

def main():
    """Test principal comparant Django runserver vs Gunicorn"""
    print("=" * 60)
    print("COMPARAISON DE PERFORMANCE: DJANGO RUNSERVER vs GUNICORN")
    print("=" * 60)
    
    # Arrêter tous les processus Python existants
    print("Arrêt des serveurs existants...")
    subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                   capture_output=True, check=False)
    time.sleep(2)
    
    # Test 1: Django runserver
    print("\n1. Test avec Django runserver")
    django_process = subprocess.Popen([
        'python', 'manage.py', 'runserver', '0.0.0.0:8000'
    ], cwd='c:\\Users\\PC DZ\\Desktop\\AUTO-P\\backend')
    
    time.sleep(5)
    
    # Vérifier si le serveur est accessible
    try:
        response = requests.get('http://localhost:8000/api/health/', timeout=2)
        if response.status_code == 200:
            django_results = test_performance_with_server(
                'http://localhost:8000', 'Django Runserver'
            )
        else:
            print("Django runserver non accessible")
            django_results = []
    except:
        print("Django runserver non accessible")
        django_results = []
    
    # Arrêter Django
    django_process.terminate()
    time.sleep(2)
    
    # Test 2: Waitress (alternative Windows à Gunicorn)
    print("\n2. Test avec Waitress")
    waitress_process = start_gunicorn()
    
    if waitress_process:
        try:
            response = requests.get('http://localhost:8000/api/health/', timeout=2)
            if response.status_code == 200:
                waitress_results = test_performance_with_server(
                    'http://localhost:8000', 'Waitress'
                )
            else:
                print("Waitress non accessible")
                waitress_results = []
        except:
            print("Waitress non accessible")
            waitress_results = []
        
        # Arrêter Waitress
        waitress_process.terminate()
        time.sleep(2)
    else:
        waitress_results = []
    
    # Comparaison
    print("\n" + "=" * 60)
    print("COMPARAISON DES RÉSULTATS")
    print("=" * 60)
    
    if django_results and waitress_results:
        print(f"{'Endpoint':20} | {'Django':8} | {'Waitress':8} | {'Différence':10}")
        print("-" * 60)
        
        for (django_name, django_time), (waitress_name, waitress_time) in zip(django_results, waitress_results):
            if django_name == waitress_name:
                diff = django_time - waitress_time
                diff_pct = (diff / django_time) * 100
                print(f"{django_name:20} | {django_time:7.1f}ms | {waitress_time:7.1f}ms | {diff_pct:+9.1f}%")
        
        # Moyenne
        django_avg = statistics.mean([t for _, t in django_results])
        waitress_avg = statistics.mean([t for _, t in waitress_results])
        avg_diff = django_avg - waitress_avg
        avg_diff_pct = (avg_diff / django_avg) * 100
        
        print("-" * 60)
        print(f"{'Moyenne':20} | {django_avg:7.1f}ms | {waitress_avg:7.1f}ms | {avg_diff_pct:+9.1f}%")
        
        if avg_diff > 0:
            print(f"\nWaitress est {avg_diff_pct:.1f}% plus rapide que Django runserver")
        else:
            print(f"\nDjango runserver est {-avg_diff_pct:.1f}% plus rapide que Waitress")
    
    # Nettoyage
    subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                   capture_output=True, check=False)
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    main()
