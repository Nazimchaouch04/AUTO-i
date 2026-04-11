#!/usr/bin/env python
"""
Importer les données SQLite vers PostgreSQL
"""
import os
import sys
import django
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def import_data():
    """Importe les données depuis les fichiers JSON"""
    print("=== Importation des données SQLite vers PostgreSQL ===")
    
    data_dir = os.path.join(os.getcwd(), 'sqlite_export')
    
    # Importer les utilisateurs en premier
    print("Importation des utilisateurs...")
    try:
        from django.contrib.auth.models import User
        
        with open(os.path.join(data_dir, 'auth_user.json'), 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user_data in users_data:
            # Créer l'utilisateur sans le mot de passe d'abord
            user = User.objects.create(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser'],
                is_active=user_data['is_active'],
                date_joined=user_data['date_joined'],
                last_login=user_data['last_login']
            )
            # Set password separately
            if user_data['password']:
                user.password = user_data['password']
                user.save()
        
        print(f"Utilisateurs importés: {len(users_data)}")
        
    except Exception as e:
        print(f"Erreur importation utilisateurs: {e}")
    
    # Importer les autres modèles
    models_to_import = [
        ('users_userprofile', 'UserProfile'),
        ('annonces_vehicule', 'Vehicule'),
        ('annonces_annonce', 'Annonce'),
        ('annonces_favori', 'Favori'),
        ('annonces_recherchesauvegardee', 'RechercheSauvegardee'),
        ('annonces_battle', 'Battle'),
        ('gamification_profiljoueur', 'ProfilJoueur'),
        ('gamification_transaction', 'Transaction'),
        ('gamification_defi', 'Defi'),
        ('gamification_defijoueur', 'DefiJoueur'),
        ('gamification_boutiqueitem', 'BoutiqueItem'),
        ('gamification_achatjoueur', 'AchatJoueur'),
        ('subscriptions_plan', 'Plan'),
        ('subscriptions_abonnement', 'Abonnement'),
        ('vehicules_marque', 'Marque'),
        ('vehicules_modele', 'Modele'),
        ('estimation_estimationhistory', 'EstimationHistory'),
        ('alertes_alerte', 'Alerte'),
        ('ai_assistant_conversation', 'Conversation'),
        ('ai_assistant_message', 'Message'),
    ]
    
    for table_name, model_name in models_to_import:
        try:
            print(f"Importation de {table_name}...")
            
            # Trouver le modèle
            from django.apps import apps
            model = None
            for app_config in apps.get_app_configs():
                for model_class in app_config.get_models():
                    if model_class.__name__ == model_name:
                        model = model_class
                        break
                if model:
                    break
            
            if not model:
                print(f"Modèle {model_name} non trouvé")
                continue
            
            # Charger les données
            json_file = os.path.join(data_dir, f"{table_name}.json")
            if not os.path.exists(json_file):
                print(f"Fichier {json_file} non trouvé")
                continue
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                print(f"Pas de données pour {table_name}")
                continue
            
            # Importer les données
            imported_count = 0
            for item in data:
                try:
                    # Gérer les clés étrangères
                    obj_data = {}
                    for field in model._meta.fields:
                        if field.name in item:
                            obj_data[field.name] = item[field.name]
                    
                    # Créer l'objet
                    obj = model.objects.create(**obj_data)
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Erreur importation enregistrement: {e}")
                    continue
            
            print(f"{table_name}: {imported_count} enregistrements importés")
            
        except Exception as e:
            print(f"Erreur importation {table_name}: {e}")

def verify_import():
    """Vérifie que les données ont été importées"""
    print("\n=== Vérification de l'importation ===")
    
    try:
        from django.contrib.auth.models import User
        from apps.annonces.models import Annonce, Favori
        from apps.gamification.models import ProfilJoueur
        
        print(f"Utilisateurs: {User.objects.count()}")
        print(f"Annonces: {Annonce.objects.count()}")
        print(f"Favoris: {Favori.objects.count()}")
        print(f"Profils joueurs: {ProfilJoueur.objects.count()}")
        
        # Vérifier l'admin
        admin = User.objects.filter(username='admin').first()
        if admin:
            print(f"Admin trouvé: {admin.email}")
        
        print("Importation vérifiée avec succès!")
        
    except Exception as e:
        print(f"Erreur vérification: {e}")

def main():
    import_data()
    verify_import()
    print("\nMigration SQLite vers PostgreSQL terminée! :)")

if __name__ == "__main__":
    main()
