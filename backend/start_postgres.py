#!/usr/bin/env python
"""
Démarrer PostgreSQL portable sur le port 5433
"""
import os
import sys
import subprocess
import time

def start_postgres():
    """Démarre PostgreSQL sur le port 5433"""
    postgres_path = os.path.join(os.getcwd(), "postgresql")
    bin_path = os.path.join(postgres_path, "pgsql", "bin")
    data_path = os.path.join(os.getcwd(), "postgres_data")
    
    if not os.path.exists(postgres_path):
        print("PostgreSQL n'est pas installé. Lancez d'abord: python install_postgres_portable.py")
        return False
    
    # Ajouter au PATH
    os.environ["PATH"] = bin_path + os.pathsep + os.environ.get("PATH", "")
    
    try:
        # Modifier le port dans postgresql.conf
        conf_path = os.path.join(data_path, "postgresql.conf")
        if os.path.exists(conf_path):
            with open(conf_path, 'r') as f:
                content = f.read()
            
            # Changer le port
            content = content.replace("#port = 5432", "port = 5433")
            content = content.replace("port = 5432", "port = 5433")
            
            with open(conf_path, 'w') as f:
                f.write(content)
        
        # Démarrer PostgreSQL
        pg_ctl = os.path.join(bin_path, "pg_ctl.exe")
        start_cmd = [pg_ctl, "-D", data_path, "-l", os.path.join(data_path, "logfile"), "start"]
        
        print("Démarrage de PostgreSQL sur le port 5433...")
        subprocess.run(start_cmd, check=True)
        
        # Attendre que PostgreSQL démarre
        time.sleep(3)
        
        # Créer la base de données si elle n'existe pas
        psql = os.path.join(bin_path, "psql.exe")
        
        try:
            # Vérifier si la base existe
            check_db_cmd = [psql, "-U", "postgres", "-p", "5433", "-d", "autointel", "-c", "SELECT 1;"]
            subprocess.run(check_db_cmd, check=True, capture_output=True)
            print("Base de données 'autointel' existe déjà")
        except subprocess.CalledProcessError:
            # Créer la base de données
            create_db_cmd = [psql, "-U", "postgres", "-p", "5433", "-c", "CREATE DATABASE autointel;"]
            subprocess.run(create_db_cmd, check=True)
            print("Base de données 'autointel' créée!")
        
        print("PostgreSQL est démarré sur le port 5433!")
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_connection():
    """Teste la connexion à PostgreSQL"""
    try:
        # Test avec psql
        psql = os.path.join(os.getcwd(), "postgresql", "pgsql", "bin", "psql.exe")
        test_cmd = [psql, "-U", "postgres", "-p", "5433", "-d", "autointel", "-c", "SELECT version();"]
        
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Connexion réussie!")
            print("Version PostgreSQL:", result.stdout.strip())
            return True
        else:
            print("Erreur de connexion:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Erreur de test: {e}")
        return False

def main():
    print("=== Démarrage PostgreSQL AutoIntel ===")
    
    if start_postgres():
        test_connection()
        print("\nPostgreSQL est prêt!")
        print("Vous pouvez maintenant lancer: python migrate_to_postgres.py")
    else:
        print("Échec du démarrage")

if __name__ == "__main__":
    main()
