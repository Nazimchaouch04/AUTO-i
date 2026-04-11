#!/usr/bin/env python
"""
Installation portable de PostgreSQL pour AutoIntel
"""
import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

def download_postgres_portable():
    """Télécharge PostgreSQL portable"""
    print("Téléchargement de PostgreSQL portable...")
    
    # URL de PostgreSQL portable (version 15)
    postgres_url = "https://get.enterprisedb.com/postgresql/postgresql-15.7-1-windows-x64-binaries.zip"
    
    try:
        # Télécharger
        zip_path = os.path.join(os.getcwd(), "postgres_portable.zip")
        print(f"Téléchargement vers: {zip_path}")
        
        urllib.request.urlretrieve(postgres_url, zip_path)
        print("Téléchargement terminé!")
        
        # Extraire
        extract_path = os.path.join(os.getcwd(), "postgresql")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        print(f"PostgreSQL extrait dans: {extract_path}")
        
        # Nettoyer
        os.remove(zip_path)
        
        return extract_path
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return None

def setup_postgres(postgres_path):
    """Configure PostgreSQL portable"""
    print("Configuration de PostgreSQL...")
    
    # Chemins
    bin_path = os.path.join(postgres_path, "pgsql", "bin")
    data_path = os.path.join(os.getcwd(), "postgres_data")
    
    # Variables d'environnement
    os.environ["PATH"] = bin_path + os.pathsep + os.environ.get("PATH", "")
    
    try:
        # Initialiser la base de données
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            
            initdb_cmd = [
                os.path.join(bin_path, "initdb.exe"),
                "-D", data_path,
                "-U", "postgres",
                "--pwfile", os.path.join(os.getcwd(), "postgres_password.txt")
            ]
            
            # Créer fichier de mot de passe
            with open("postgres_password.txt", "w") as f:
                f.write("postgres123")
            
            subprocess.run(initdb_cmd, check=True)
            os.remove("postgres_password.txt")
            
            print("Base de données initialisée!")
        
        # Démarrer PostgreSQL
        pg_ctl = os.path.join(bin_path, "pg_ctl.exe")
        start_cmd = [pg_ctl, "-D", data_path, "start"]
        
        subprocess.run(start_cmd, check=True)
        print("PostgreSQL démarré!")
        
        # Créer la base de données AutoIntel
        psql = os.path.join(bin_path, "psql.exe")
        create_db_cmd = [psql, "-U", "postgres", "-c", "CREATE DATABASE autointel_db;"]
        
        subprocess.run(create_db_cmd, check=True)
        print("Base de données autointel_db créée!")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de la configuration: {e}")
        return False

def main():
    print("=== Installation Portable PostgreSQL ===")
    
    # Télécharger PostgreSQL
    postgres_path = download_postgres_portable()
    if not postgres_path:
        print("Échec du téléchargement")
        return False
    
    # Configurer PostgreSQL
    if setup_postgres(postgres_path):
        print("\nPostgreSQL installé et configuré avec succès!")
        print("Vous pouvez maintenant lancer: python migrate_to_postgres.py")
        return True
    else:
        print("Échec de la configuration")
        return False

if __name__ == "__main__":
    main()
