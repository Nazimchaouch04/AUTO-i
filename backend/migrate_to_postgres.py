#!/usr/bin/env python
"""
Script pour migrer les données de SQLite vers PostgreSQL
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
import sqlite3
import json

def export_sqlite_data():
    """Exporte toutes les données de SQLite vers des fichiers JSON"""
    print("Exportation des données SQLite...")
    
    # Connexion à SQLite
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    # Lister toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    data_dir = os.path.join(os.path.dirname(__file__), 'sqlite_export')
    os.makedirs(data_dir, exist_ok=True)
    
    for table_name, in tables:
        if table_name not in ['sqlite_sequence']:  # Ignorer les tables système
            print(f"Exportation de la table: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Convertir en liste de dictionnaires
            table_data = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                # Gérer les types spéciaux (datetime, etc.)
                for key, value in row_dict.items():
                    if isinstance(value, str) and value.startswith('datetime'):
                        try:
                            # Django gérera la conversion
                            pass
                        except:
                            pass
                table_data.append(row_dict)
            
            # Sauvegarder en JSON
            with open(os.path.join(data_dir, f"{table_name}.json"), 'w', encoding='utf-8') as f:
                json.dump(table_data, f, indent=2, default=str)
    
    conn.close()
    print(f"Données exportées dans: {data_dir}")

def import_to_postgresql():
    """Importe les données JSON vers PostgreSQL"""
    print("Importation des données vers PostgreSQL...")
    
    data_dir = os.path.join(os.path.dirname(__file__), 'sqlite_export')
    
    # Lister tous les fichiers JSON
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    for json_file in json_files:
        table_name = json_file.replace('.json', '')
        print(f"Importation de la table: {table_name}")
        
        with open(os.path.join(data_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Importer les données via Django
        if data:  # Si la table n'est pas vide
            # Utiliser le modèle Django approprié
            try:
                from django.apps import apps
                model = None
                
                # Trouver le modèle correspondant
                for app_config in apps.get_app_configs():
                    for model_class in app_config.get_models():
                        if model_class._meta.db_table == table_name:
                            model = model_class
                            break
                    if model:
                        break
                
                if model:
                    # Créer les objets
                    for item in data:
                        try:
                            # Gérer les clés étrangères et relations
                            obj_data = {}
                            for field in model._meta.fields:
                                if field.name in item:
                                    obj_data[field.name] = item[field.name]
                            
                            model.objects.create(**obj_data)
                        except Exception as e:
                            print(f"Erreur lors de l'importation d'un enregistrement: {e}")
                            continue
                else:
                    print(f"Modèle non trouvé pour la table: {table_name}")
                    
            except Exception as e:
                print(f"Erreur lors de l'importation de {table_name}: {e}")

def main():
    print("=== Migration SQLite vers PostgreSQL ===")
    
    # 1. Exporter les données SQLite
    export_sqlite_data()
    
    # 2. Créer les tables PostgreSQL
    print("\nCréation des tables PostgreSQL...")
    call_command('migrate', verbosity=2)
    
    # 3. Importer les données
    import_to_postgresql()
    
    print("\nMigration terminée!")
    print("Vérifiez que toutes les données ont été correctement migrées.")

if __name__ == "__main__":
    main()
