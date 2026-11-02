#!/usr/bin/env python
"""
Script pour configurer les plans d'abonnement et leurs prix
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.subscriptions.models import Plan

print("=" * 60)
print("CONFIGURATION DES PLANS D'ABONNEMENT")
print("=" * 60)

# Définition des plans avec prix
PLANS_CONFIG = [
    {
        'nom': 'free',
        'prix_mensuel': 0,
        'estimations_par_mois': 5,
        'alertes_max': 2,
        'export_csv': False,
        'acces_api': False,
        'description': 'Plan gratuit pour découvrir AutoIntel'
    },
    {
        'nom': 'pro',
        'prix_mensuel': 19.99,
        'estimations_par_mois': 50,
        'alertes_max': 20,
        'export_csv': True,
        'acces_api': False,
        'description': 'Plan Pro pour les utilisateurs réguliers'
    },
    {
        'nom': 'business',
        'prix_mensuel': 49.99,
        'estimations_par_mois': 999,  # Illimité
        'alertes_max': 100,
        'export_csv': True,
        'acces_api': True,
        'description': 'Plan Business pour les professionnels'
    }
]

for plan_config in PLANS_CONFIG:
    plan, created = Plan.objects.update_or_create(
        nom=plan_config['nom'],
        defaults={
            'prix_mensuel': plan_config['prix_mensuel'],
            'estimations_par_mois': plan_config['estimations_par_mois'],
            'alertes_max': plan_config['alertes_max'],
            'export_csv': plan_config['export_csv'],
            'acces_api': plan_config['acces_api'],
        }
    )
    
    action = "Créé" if created else "Mis à jour"
    print(f"\n✅ {action}: {plan.get_nom_display()}")
    print(f"   Prix: {plan.prix_mensuel}€/mois")
    print(f"   Estimations: {plan.estimations_par_mois}/mois")
    print(f"   Alertes: {plan.alertes_max}")
    print(f"   Export CSV: {'Oui' if plan.export_csv else 'Non'}")
    print(f"   Accès API: {'Oui' if plan.acces_api else 'Non'}")

print("\n" + "=" * 60)
print("✅ Configuration terminée!")
print(f"Total plans: {Plan.objects.count()}")
print("=" * 60)
