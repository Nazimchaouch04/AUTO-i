#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

from django.db import connection
from apps.annonces.models import Marque, Modele, Annonce, Estimation, Alert, Image

def consulter_base_donnees():
    print("=== CONSULTATION DE LA BASE DE DONNÉES ===\n")
    
    cursor = connection.cursor()
    
    # Lister toutes les tables
    print("📋 Tables disponibles:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n" + "="*50)
    
    # Consulter les modèles
    print("\n🚗 MODÈLES:")
    try:
        modeles = Modele.objects.all()
        if modeles:
            for modele in modeles:
                print(f"  ID: {modele.id} | Nom: {modele.nom} | Marque: {modele.marque.nom if modele.marque else 'N/A'}")
        else:
            print("  Aucun modèle trouvé")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    # Consulter les marques
    print("\n🏭 MARQUES:")
    try:
        marques = Marque.objects.all()
        if marques:
            for marque in marques:
                print(f"  ID: {marque.id} | Nom: {marque.nom}")
        else:
            print("  Aucune marque trouvée")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    # Consulter les annonces
    print("\n📢 ANNONCES:")
    try:
        annonces = Annonce.objects.all()
        if annonces:
            for annonce in annonces[:5]:  # Limiter à 5 pour la lisibilité
                print(f"  ID: {annonce.id} | Titre: {annonce.titre} | Prix: {annonce.prix}")
            if annonces.count() > 5:
                print(f"  ... et {annonces.count() - 5} autres annonces")
        else:
            print("  Aucune annonce trouvée")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    # Statistiques
    print("\n📊 STATISTIQUES:")
    try:
        stats = {
            'Marques': Marque.objects.count(),
            'Modèles': Modele.objects.count(),
            'Annonces': Annonce.objects.count(),
            'Estimations': Estimation.objects.count(),
            'Alertes': Alert.objects.count(),
            'Images': Image.objects.count(),
        }
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"  Erreur: {e}")

if __name__ == "__main__":
    consulter_base_donnees()
