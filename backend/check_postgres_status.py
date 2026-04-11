#!/usr/bin/env python
"""
Vérifier le statut de PostgreSQL
"""
import os
import subprocess
import sys

def check_postgres_status():
    """Vérifie si PostgreSQL est en cours d'exécution"""
    postgres_path = os.path.join(os.getcwd(), "postgresql")
    bin_path = os.path.join(postgres_path, "pgsql", "bin")
    data_path = os.path.join(os.getcwd(), "postgres_data")
    
    if not os.path.exists(postgres_path):
        print("PostgreSQL n'est pas installé")
        return False
    
    # Ajouter au PATH
    os.environ["PATH"] = bin_path + os.pathsep + os.environ.get("PATH", "")
    
    try:
        # Vérifier le statut
        pg_ctl = os.path.join(bin_path, "pg_ctl.exe")
        status_cmd = [pg_ctl, "-D", data_path, "status"]
        
        result = subprocess.run(status_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("PostgreSQL est déjà en cours d'exécution!")
            print(result.stdout)
            return True
        else:
            print("PostgreSQL n'est pas en cours d'exécution")
            print("Erreur:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_connection():
    """Teste la connexion à PostgreSQL"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
        django.setup()
        
        from django.db import connection
        
        # Test de connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
        
        print("Connexion à PostgreSQL réussie!")
        return True
        
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return False

def start_without_log():
    """Démarre PostgreSQL sans fichier de log"""
    postgres_path = os.path.join(os.getcwd(), "postgresql")
    bin_path = os.path.join(postgres_path, "pgsql", "bin")
    data_path = os.path.join(os.getcwd(), "postgres_data")
    
    os.environ["PATH"] = bin_path + os.pathsep + os.environ.get("PATH", "")
    
    try:
        pg_ctl = os.path.join(bin_path, "pg_ctl.exe")
        start_cmd = [pg_ctl, "-D", data_path, "start"]
        
        print("Démarrage de PostgreSQL sans fichier de log...")
        subprocess.run(start_cmd, check=True)
        print("PostgreSQL démarré!")
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def main():
    print("=== Vérification Statut PostgreSQL ===")
    
    if check_postgres_status():
        print("PostgreSQL est déjà actif!")
        test_connection()
    else:
        print("Tentative de démarrage sans log...")
        if start_without_log():
            test_connection()

if __name__ == "__main__":
    main()
