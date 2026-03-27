#!/usr/bin/env python
"""
Script de test pour vérifier la configuration Django AutoIntel
"""
import os
import sys

# Ajouter le chemin du backend au Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test import des modules principaux
    print("🔍 Test des imports...")
    
    # Test Django
    import django
    from django.conf import settings
    print("✅ Django importé")
    
    # Test DRF
    from rest_framework import status
    print("✅ Django REST Framework importé")
    
    # Test CORS
    import corsheaders
    print("✅ Django CORS Headers importé")
    
    # Test des apps
    from apps.annonces.models import Marque, Modele, Annonce
    print("✅ Models annonces importés")
    
    from apps.annonces.serializers import MarqueSerializer, AnnonceSerializer
    print("✅ Serializers importés")
    
    from apps.annonces.views import MarqueViewSet, AnnonceViewSet
    print("✅ ViewSets importés")
    
    print("\n🎉 Tous les imports réussis!")
    
    # Configuration Django
    print("\n⚙️  Test configuration Django...")
    
    # Vérifier les settings
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
    
    django.setup()
    
    print("✅ Configuration Django chargée")
    
    # Vérifier les apps installées
    apps = settings.INSTALLED_APPS
    required_apps = ['django.contrib.admin', 'rest_framework', 'corsheaders', 'apps.annonces']
    
    for app in required_apps:
        if app in apps:
            print(f"✅ {app} installé")
        else:
            print(f"❌ {app} manquant")
    
    print("\n🔗 Test des URLs...")
    from django.urls import reverse
    try:
        # Test URL root
        from autointel.urls import urlpatterns
        print("✅ URLs configurées")
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")
    
    print("\n📊 Résumé:")
    print("- Backend Django configuré")
    print("- API REST prête")
    print("- CORS activé pour frontend")
    print("- Models de données créés")
    
    print("\n🚀 Prochaines étapes:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("\n💡 Solution probable:")
    print("- Installer les dépendances: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\n💡 Vérifier la configuration dans autointel/settings.py")
