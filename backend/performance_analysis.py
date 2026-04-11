#!/usr/bin/env python
"""
Analyse et optimisation des performances
"""
import time
import requests
import django
from django.db import connection
from django.conf import settings
import os

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def analyze_database_queries():
    """Analyse les requêtes database"""
    print("=== Analyse des Requêtes Database ===")
    
    from django.test.utils import override_settings
    from django.db import reset_queries
    
    # Test avec monitoring des requêtes
    with override_settings(DEBUG=True):
        reset_queries()
        
        # Test endpoint gamification/profil
        from apps.gamification.models import ProfilJoueur
        from django.contrib.auth.models import User
        
        start_time = time.time()
        
        # Simuler la requête du profil
        user = User.objects.get(username='admin')
        profil = ProfilJoueur.objects.get(user=user)
        
        end_time = time.time()
        
        queries = connection.queries
        print(f"Requêtes exécutées: {len(queries)}")
        print(f"Temps total: {(end_time - start_time) * 1000:.2f}ms")
        
        for i, query in enumerate(queries):
            print(f"  {i+1}. {query['time']}s - {query['sql'][:100]}...")

def test_database_connection():
    """Test la connexion database"""
    print("\n=== Test Connexion Database ===")
    
    start_time = time.time()
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
        
        end_time = time.time()
        print(f"Connexion réussie: {(end_time - start_time) * 1000:.2f}ms")
        print(f"Résultat: {result}")
        
        # Vérifier la configuration
        print(f"Engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"Host: {settings.DATABASES['default']['HOST']}")
        print(f"Port: {settings.DATABASES['default']['PORT']}")
        print(f"Name: {settings.DATABASES['default']['NAME']}")
        
    except Exception as e:
        print(f"Erreur de connexion: {e}")

def analyze_middleware():
    """Analyse les middlewares"""
    print("\n=== Analyse Middlewares ===")
    
    middlewares = settings.MIDDLEWARE
    print("Middlewares configurés:")
    for i, middleware in enumerate(middlewares):
        print(f"  {i+1}. {middleware}")
    
    # Vérifier s'il y a des middlewares lourds
    heavy_middlewares = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',
    ]
    
    for middleware in heavy_middlewares:
        if middleware in middlewares:
            print(f"  ⚠️  Middleware potentiellement lourd: {middleware}")

def check_debug_mode():
    """Vérifie le mode debug"""
    print("\n=== Configuration Debug ===")
    
    print(f"DEBUG = {settings.DEBUG}")
    if settings.DEBUG:
        print("⚠️  Le mode DEBUG est activé - cela ralentit les performances")
        print("Actions recommandées:")
        print("  - Désactiver DEBUG en production")
        print("  - Utiliser les settings de production")

def test_simple_endpoint():
    """Test un endpoint simple"""
    print("\n=== Test Endpoint Simple ===")
    
    # Test avec curl pour éviter le overhead Python
    import subprocess
    
    try:
        start_time = time.time()
        result = subprocess.run([
            'curl', '-w', '%{time_total}',
            '-s', '-o', '/dev/null',
            'http://localhost:8000/api/health/'
        ], capture_output=True, text=True, timeout=10)
        
        end_time = time.time()
        
        curl_time = float(result.stdout.strip())
        python_time = (end_time - start_time) * 1000
        
        print(f"Temps avec curl: {curl_time * 1000:.2f}ms")
        print(f"Temps avec Python requests: {python_time:.2f}ms")
        print(f"Différence: {abs(curl_time * 1000 - python_time):.2f}ms")
        
    except Exception as e:
        print(f"Erreur test curl: {e}")

def optimize_settings_recommendations():
    """Recommandations d'optimisation"""
    print("\n=== Recommandations d'Optimisation ===")
    
    recommendations = []
    
    # Vérifier la configuration database
    db_config = settings.DATABASES['default']
    if 'OPTIONS' not in db_config:
        recommendations.append("Ajouter OPTIONS de connexion PostgreSQL optimisées")
    
    # Vérifier les middlewares
    if len(settings.MIDDLEWARE) > 10:
        recommendations.append("Réduire le nombre de middlewares")
    
    # Vérifier le debug
    if settings.DEBUG:
        recommendations.append("Désactiver DEBUG en production")
    
    # Vérifier le logging
    if not hasattr(settings, 'LOGGING') or not settings.LOGGING:
        recommendations.append("Configurer un logging efficace")
    
    print("Recommandations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")

def create_optimized_settings():
    """Crée des suggestions de settings optimisés"""
    print("\n=== Suggestions Settings Optimisés ===")
    
    optimized_db = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
            'connect_timeout': 10,
            'application_name': 'autointel',
        }
    }
}
"""
    
    optimized_middleware = """
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
"""
    
    print("1. Configuration Database optimisée:")
    print(optimized_db)
    
    print("2. Middlewares optimisés:")
    print(optimized_middleware)

def main():
    """Fonction principale d'analyse"""
    print("=" * 60)
    print("ANALYSE DE PERFORMANCE - AUTOINTEL")
    print("=" * 60)
    
    test_database_connection()
    analyze_database_queries()
    check_debug_mode()
    analyze_middleware()
    test_simple_endpoint()
    optimize_settings_recommendations()
    create_optimized_settings()
    
    print("\n" + "=" * 60)
    print("ANALYSE TERMINÉE")
    print("=" * 60)

if __name__ == "__main__":
    main()
