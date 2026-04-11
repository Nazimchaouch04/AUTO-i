#!/usr/bin/env python
"""
Configurer les données pour l'admin après migration PostgreSQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def setup_admin_data():
    print("=== Configuration des données Admin ===")
    
    from django.contrib.auth.models import User
    from apps.users.models import UserProfile
    from apps.gamification.models import ProfilJoueur
    from apps.subscriptions.models import Plan, Abonnement
    
    # Créer le profil pour l'admin
    try:
        admin = User.objects.get(username='admin')
        profile, created = UserProfile.objects.get_or_create(
            user=admin, 
            defaults={'avatar_initials': 'AD'}
        )
        print(f'Profil admin créé: {created}')
    except User.DoesNotExist:
        print("Admin user non trouvé")
        return
    
    # Créer le profil joueur
    profil_joueur, created = ProfilJoueur.objects.get_or_create(
        user=admin, 
        defaults={'xp': 0, 'niveau': 1, 'autocoin_balance': 100}
    )
    print(f'Profil joueur créé: {created}')
    
    # Créer les plans s'ils n'existent pas
    plans_data = [
        {'nom': 'free', 'prix_mensuel': 0, 'estimations_par_mois': 5, 'alertes_max': 2, 'export_csv': False, 'acces_api': False},
        {'nom': 'pro', 'prix_mensuel': 19.99, 'estimations_par_mois': 50, 'alertes_max': 20, 'export_csv': True, 'acces_api': False},
        {'nom': 'business', 'prix_mensuel': 49.99, 'estimations_par_mois': 200, 'alertes_max': 100, 'export_csv': True, 'acces_api': True},
    ]
    
    for plan_data in plans_data:
        plan, created = Plan.objects.get_or_create(
            nom=plan_data['nom'], 
            defaults=plan_data
        )
        print(f'Plan {plan_data["nom"]} créé: {created}')
    
    # Créer l'abonnement pour l'admin
    free_plan = Plan.objects.get(nom='free')
    abonnement, created = Abonnement.objects.get_or_create(
        user=admin, 
        defaults={'plan': free_plan, 'actif': True}
    )
    print(f'Abonnement admin créé: {created}')
    
    print('Configuration terminée!')

def verify_data():
    print("\n=== Vérification des données ===")
    
    from django.contrib.auth.models import User
    from apps.users.models import UserProfile
    from apps.gamification.models import ProfilJoueur
    from apps.subscriptions.models import Plan, Abonnement
    
    print(f"Utilisateurs: {User.objects.count()}")
    print(f"Profils utilisateurs: {UserProfile.objects.count()}")
    print(f"Profils joueurs: {ProfilJoueur.objects.count()}")
    print(f"Plans: {Plan.objects.count()}")
    print(f"Abonnements: {Abonnement.objects.count()}")
    
    # Vérifier l'admin
    admin = User.objects.filter(username='admin').first()
    if admin:
        print(f"Admin: {admin.email}")
        profile = UserProfile.objects.filter(user=admin).first()
        if profile:
            print(f"  - Profil: {profile.avatar_initials}")
        profil_joueur = ProfilJoueur.objects.filter(user=admin).first()
        if profil_joueur:
            print(f"  - Niveau: {profil_joueur.niveau}, AutoCoins: {profil_joueur.autocoin_balance}")

if __name__ == "__main__":
    setup_admin_data()
    verify_data()
