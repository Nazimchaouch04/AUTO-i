#!/usr/bin/env python
"""
Tests de performance complets pour AutoIntel Backend
"""
import time
import requests
import threading
import concurrent.futures
import statistics
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1ODU0MjQ2LCJpYXQiOjE3NzU4NTA2NDYsImp0aSI6IjIxMTI4MjZkZGU3YzQ1MTg4NDcwMjE2ZTAwOTk5ZjRjIiwidXNlcl9pZCI6IjMifQ.0iMTfq76pHZt4ZupE2LhwT1pSG2BPv2icgv_oip2VeQ"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

class PerformanceTestSuite:
    """Suite de tests de performance pour AutoIntel"""
    
    def __init__(self):
        self.results = {}
        
    def single_request_test(self, name, url, method="GET", data=None):
        """Test une requête unique"""
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(f"{BASE_URL}{url}", headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(f"{BASE_URL}{url}", headers=headers, json=data, timeout=10)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # en ms
            
            return {
                'success': response.status_code == 200,
                'response_time': response_time,
                'status_code': response.status_code,
                'content_length': len(response.content)
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': 0,
                'status_code': 0,
                'content_length': 0,
                'error': str(e)
            }
    
    def concurrent_test(self, name, url, num_threads=10, requests_per_thread=5):
        """Test avec requêtes concurrentes"""
        results = []
        
        def worker():
            thread_results = []
            for _ in range(requests_per_thread):
                result = self.single_request_test(name, url)
                thread_results.append(result['response_time'])
            results.extend(thread_results)
        
        # Démarrer les threads
        start_time = time.time()
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Attendre que tous les threads terminent
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculer les statistiques
        if results:
            return {
                'total_requests': len(results),
                'total_time': total_time,
                'requests_per_second': len(results) / total_time,
                'avg_response_time': statistics.mean(results),
                'min_response_time': min(results),
                'max_response_time': max(results),
                'median_response_time': statistics.median(results),
                'p95_response_time': sorted(results)[int(len(results) * 0.95)],
                'p99_response_time': sorted(results)[int(len(results) * 0.99)]
            }
        return None
    
    def stress_test(self, name, url, duration=30, max_workers=20):
        """Test de stress sur une durée donnée"""
        results = []
        start_time = time.time()
        
        def worker():
            while time.time() - start_time < duration:
                result = self.single_request_test(name, url)
                if result['success']:
                    results.append(result['response_time'])
                time.sleep(0.1)  # Pause pour éviter la surcharge
        
        # Démarrer les workers
        threads = []
        for _ in range(max_workers):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Attendre la fin
        for thread in threads:
            thread.join()
        
        actual_duration = time.time() - start_time
        
        if results:
            return {
                'duration': actual_duration,
                'total_requests': len(results),
                'requests_per_second': len(results) / actual_duration,
                'avg_response_time': statistics.mean(results),
                'success_rate': len(results) / (len(results) + sum(1 for r in results if not r)) * 100
            }
        return None
    
    def database_performance_test(self):
        """Test des performances de la base de données"""
        print("\n=== Test Performance Base de Données ===")
        
        # Test de lecture
        db_tests = [
            ("Lecture Profil", "/api/gamification/profil/"),
            ("Lecture Leaderboard", "/api/gamification/leaderboard/"),
            ("Lecture Annonces", "/api/annonces/"),
            ("Lecture Véhicules", "/api/vehicules/"),
            ("Lecture Plans", "/api/subscriptions/plans/"),
        ]
        
        for name, url in db_tests:
            result = self.concurrent_test(name, url, num_threads=5, requests_per_thread=10)
            if result:
                print(f"{name:25} | {result['requests_per_second']:.1f} req/s | "
                      f"Avg: {result['avg_response_time']:.1f}ms | "
                      f"P95: {result['p95_response_time']:.1f}ms")
    
    def api_performance_test(self):
        """Test des performances de l'API"""
        print("\n=== Test Performance API ===")
        
        api_tests = [
            ("Health Check", "/api/health/"),
            ("Gamification Root", "/api/gamification/"),
            ("Subscriptions Root", "/api/subscriptions/"),
            ("AI Assistant Root", "/api/ai/"),
            ("Notifications Root", "/api/notifications/"),
            ("Annonces Root", "/api/annonces/"),
            ("Alertes", "/api/alertes/"),
            ("Dashboard", "/api/dashboard/"),
        ]
        
        for name, url in api_tests:
            # Test simple
            single = self.single_request_test(name, url)
            
            # Test concurrent
            concurrent = self.concurrent_test(name, url, num_threads=10, requests_per_thread=5)
            
            if single and concurrent:
                print(f"{name:25} | Single: {single['response_time']:.1f}ms | "
                      f"Concurrent: {concurrent['requests_per_second']:.1f} req/s | "
                      f"Avg: {concurrent['avg_response_time']:.1f}ms")
    
    def load_test(self):
        """Test de charge"""
        print("\n=== Test de Charge ===")
        
        # Test avec différentes charges
        loads = [
            (5, 10, "Légère"),
            (10, 20, "Moyenne"),
            (20, 30, "Élevée"),
        ]
        
        for threads, requests, level in loads:
            result = self.concurrent_test("Load Test", "/api/gamification/profil/", 
                                         num_threads=threads, requests_per_thread=requests)
            if result:
                print(f"Charge {level:10} | Threads: {threads:2} | Req/thread: {requests:2} | "
                      f"Total: {result['total_requests']:3} | "
                      f"Req/s: {result['requests_per_second']:.1f} | "
                      f"Avg: {result['avg_response_time']:.1f}ms | "
                      f"P95: {result['p95_response_time']:.1f}ms")
    
    def stress_test_suite(self):
        """Suite de tests de stress"""
        print("\n=== Test de Stress (30 secondes) ===")
        
        endpoints = [
            "/api/health/",
            "/api/gamification/profil/",
            "/api/annonces/",
            "/api/vehicules/",
        ]
        
        for endpoint in endpoints:
            result = self.stress_test("Stress", endpoint, duration=30, max_workers=15)
            if result:
                print(f"{endpoint:30} | Req/s: {result['requests_per_second']:.1f} | "
                      f"Avg: {result['avg_response_time']:.1f}ms | "
                      f"Success: {result['success_rate']:.1f}%")
    
    def memory_usage_test(self):
        """Test d'utilisation mémoire"""
        print("\n=== Test d'Utilisation Mémoire ===")
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Effectuer 100 requêtes
            for _ in range(100):
                self.single_request_test("Memory Test", "/api/gamification/profil/")
            
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = memory_after - memory_before
            
            print(f"Mémoire avant test: {memory_before:.1f} MB")
            print(f"Mémoire après test: {memory_after:.1f} MB")
            print(f"Augmentation: {memory_increase:.1f} MB")
            print(f"Mémoire par requête: {memory_increase/100:.3f} MB")
            
        except ImportError:
            print("psutil non installé - impossible de tester l'utilisation mémoire")
    
    def run_all_tests(self):
        """Exécuter tous les tests de performance"""
        print("=" * 60)
        print("SUITE DE TESTS DE PERFORMANCE - AUTOINTEL BACKEND")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {BASE_URL}")
        print(f"Base de données: PostgreSQL")
        print("=" * 60)
        
        # Tests de base
        self.api_performance_test()
        self.database_performance_test()
        
        # Tests de charge
        self.load_test()
        
        # Test de stress
        self.stress_test_suite()
        
        # Test mémoire
        self.memory_usage_test()
        
        print("\n" + "=" * 60)
        print("TESTS DE PERFORMANCE TERMINÉS")
        print("=" * 60)

if __name__ == "__main__":
    tester = PerformanceTestSuite()
    tester.run_all_tests()
