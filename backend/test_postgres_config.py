#!/usr/bin/env python
"""
Script pour tester la configuration PostgreSQL
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_database_connection():
    """Teste la connexion à la base de données"""
    try:
        from django.db import connection
        
        # Test de connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            
        print("=== Test de Connexion PostgreSQL ===")
        print(f"Résultat du test: {result}")
        print("Connexion réussie à PostgreSQL!")
        
        # Afficher les informations de la base de données
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Version PostgreSQL: {version[0]}")
        
        # Lister les tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        print(f"Tables trouvées: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
        return True
        
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        print("\nSolutions possibles:")
        print("1. Assurez-vous que PostgreSQL est installé et en cours d'exécution")
        print("2. Vérifiez les identifiants dans le fichier .env")
        print("3. Créez la base de données autointel_db:")
        print("   createdb -U postgres autointel_db")
        print("4. Installez PostgreSQL avec: ./install_postgres_windows.bat")
        return False

def check_django_migrations():
    """Vérifie les migrations Django"""
    try:
        from django.core.management import call_command
        
        print("\n=== Vérification des Migrations ===")
        call_command('showmigrations')
        
        print("\n=== Application des Migrations ===")
        call_command('migrate', verbosity=2)
        
        return True
        
    except Exception as e:
        print(f"Erreur lors des migrations: {e}")
        return False

def main():
    print("=== Test Configuration PostgreSQL AutoIntel ===")
    
    # Test de connexion
    if not test_database_connection():
        return False
    
    # Vérification des migrations
    if not check_django_migrations():
        return False
    
    print("\n=== Test Final ===")
    
    # Test des modèles
    try:
        from django.contrib.auth.models import User
        from apps.annonces.models import Annonce
        
        # Compter les enregistrements
        user_count = User.objects.count()
        annonce_count = Annonce.objects.count()
        
        print(f"Utilisateurs dans la base: {user_count}")
        print(f"Annonces dans la base: {annonce_count}")
        
        if user_count > 0:
            admin_user = User.objects.filter(username='admin').first()
            if admin_user:
                print(f"Admin user trouvé: {admin_user.email}")
        
        print("\nConfiguration PostgreSQL réussie! :)")
        return True
        
    except Exception as e:
        print(f"Erreur lors du test des modèles: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
