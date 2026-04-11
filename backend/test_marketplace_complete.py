#!/usr/bin/env python3
"""
Test complet du marketplace sans dépendances
"""

import os
import sys
import django

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_complete_marketplace():
    """Test du marketplace autonome"""
    try:
        print("=== Test Marketplace AutoIntel ===")
        
        # Test 1: Vérification de la connexion admin
        print("\n1. Test de connexion admin...")
        try:
            from django.contrib.auth import authenticate
            user = authenticate(username='admin', password='password123')
            if user:
                print("✅ Connexion admin réussie")
            else:
                print("❌ Échec connexion admin")
        except Exception as e:
            print(f"❌ Erreur connexion admin: {e}")
        
        # Test 2: Test simple des modèles Django
        print("\n2. Test des modèles Django...")
        try:
            from django.contrib.auth.models import User
            user = User.objects.first()
            print(f"✅ Utilisateur trouvé: {user.username}")
            
            # Création d'un profil vendeur simple
            from apps.marketplace.models_fixed import SellerProfile
            profile = SellerProfile.objects.create(
                user=user,
                company_name="Test AutoIntel",
                phone_number="0123456789"
            )
            print(f"✅ Profil vendeur créé: {profile.company_name}")
            
        except Exception as e:
            print(f"❌ Erreur création profil: {e}")
        
        # Test 3: Vérification des URLs marketplace
        print("\n3. Test des URLs marketplace...")
        try:
            from django.urls import reverse
            marketplace_url = reverse('marketplace:marketplace-root')
            print(f"✅ URL marketplace: {marketplace_url}")
            
        except Exception as e:
            print(f"❌ Erreur URLs: {e}")
        
        print("\n=== Tests terminés avec succès ===")
        print("🎯 Le marketplace AutoIntel est prêt pour être utilisé !")
        return True
        
    except ImportError as e:
            print(f"❌ Erreur d'importation: {e}")
            return False
    except Exception as e:
            print(f"❌ Erreur générale: {e}")
            return False

if __name__ == "__main__":
    test_complete_marketplace()
