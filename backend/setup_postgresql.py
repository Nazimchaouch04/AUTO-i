#!/usr/bin/env python
"""
Script pour configurer PostgreSQL pour AutoIntel sur Windows
"""
import subprocess
import sys
import os

def check_postgresql_installed():
    """Vérifie si PostgreSQL est installé"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_database():
    """Crée la base de données AutoIntel"""
    commands = [
        # Créer la base de données
        'createdb autointel_db',
        # Créer utilisateur (si nécessaire)
        # 'createuser autointel_user'
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Commande réussie: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur avec la commande {cmd}: {e}")
            print("La base de données existe peut-être déjà")

def main():
    print("=== Configuration PostgreSQL pour AutoIntel ===")
    
    if not check_postgresql_installed():
        print("PostgreSQL n'est pas installé.")
        print("Veuillez installer PostgreSQL depuis https://www.postgresql.org/download/windows/")
        print("Ou utiliser Chocolatey: choco install postgresql")
        return False
    
    print("PostgreSQL est installé!")
    
    # Créer la base de données
    print("Création de la base de données autointel_db...")
    create_database()
    
    print("\nConfiguration terminée!")
    print("Assurez-vous que PostgreSQL est en cours d'exécution.")
    print("Vous pouvez maintenant lancer: python manage.py migrate")
    
    return True

if __name__ == "__main__":
    main()
