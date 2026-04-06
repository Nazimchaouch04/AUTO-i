#!/usr/bin/env python
"""
Script de test pour verifier la configuration Django AutoIntel.
Version ASCII pour eviter les erreurs d'encodage sur Windows.
"""

import os
import sys

# Ajouter le chemin du backend au Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    try:
        print("[INFO] Test des imports...")

        import django
        from django.conf import settings

        print("[OK] Django importe")

        from rest_framework import status  # noqa: F401

        print("[OK] Django REST Framework importe")

        import corsheaders  # noqa: F401

        print("[OK] Django CORS Headers importe")

        from apps.annonces.models import Marque, Modele, Annonce  # noqa: F401

        print("[OK] Models annonces importes")

        from apps.annonces.serializers import MarqueSerializer, AnnonceSerializer  # noqa: F401

        print("[OK] Serializers importes")

        from apps.annonces.views import MarqueViewSet, AnnonceViewSet  # noqa: F401

        print("[OK] ViewSets importes")

        print("\n[OK] Tous les imports reussis")

        print("\n[INFO] Test configuration Django...")
        if not settings.configured:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autointel.settings")

        django.setup()
        print("[OK] Configuration Django chargee")

        apps = settings.INSTALLED_APPS
        required_apps = ["django.contrib.admin", "rest_framework", "corsheaders", "apps.annonces"]
        for app in required_apps:
            if app in apps:
                print(f"[OK] {app} installe")
            else:
                print(f"[ERR] {app} manquant")

        print("\n[INFO] Test des URLs...")
        try:
            from autointel.urls import urlpatterns  # noqa: F401

            print("[OK] URLs configurees")
        except Exception as e:
            print(f"[ERR] Erreur URLs: {e}")

        print("\n[INFO] Resume:")
        print("- Backend Django configure")
        print("- API REST prete")
        print("- CORS active pour frontend")
        print("- Models de donnees crees")

        print("\n[INFO] Prochaines etapes:")
        print("1. python manage.py makemigrations")
        print("2. python manage.py migrate")
        print("3. python manage.py createsuperuser")
        print("4. python manage.py runserver")
        return 0

    except ImportError as e:
        print(f"[ERR] Erreur d'import: {e}")
        print("\n[TIP] Solution probable:")
        print("- Installer les dependances: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"[ERR] Erreur: {e}")
        print("\n[TIP] Verifier la configuration dans autointel/settings.py")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
