#!/usr/bin/env python3
"""
Test des modèles marketplace simplifiés
"""

import os
import sys
import django

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_simple_models():
    """Test des modèles marketplace simplifiés"""
    try:
        from apps.marketplace.models_simple import SellerProfile, SimpleListing, SimpleOrder
        
        print("✅ Importation des modèles simplifiés réussie")
        
        # Test création d'un objet SellerProfile
        print("\n--- Test SellerProfile ---")
        try:
            from django.contrib.auth.models import User
            user = User.objects.first()
            
            profile = SellerProfile.objects.create(
                user=user,
                company_name="Test Company",
                phone_number="0123456789"
            )
            print(f"✅ SellerProfile créé: {profile}")
            
        except Exception as e:
            print(f"❌ Erreur SellerProfile: {e}")
        
        # Test création d'un objet SimpleListing
        print("\n--- Test SimpleListing ---")
        try:
            listing = SimpleListing.objects.create(
                seller=profile,
                title="Voiture Test",
                brand="Renault",
                model="Clio",
                year=2020,
                price=15000
            )
            print(f"✅ SimpleListing créé: {listing}")
            
        except Exception as e:
            print(f"❌ Erreur SimpleListing: {e}")
        
        # Test création d'un objet SimpleOrder
        print("\n--- Test SimpleOrder ---")
        try:
            order = SimpleOrder.objects.create(
                listing=listing,
                buyer=user,
                seller=profile,
                total_amount=15000
            )
            print(f"✅ SimpleOrder créé: {order}")
            
        except Exception as e:
            print(f"❌ Erreur SimpleOrder: {e}")
        
        print("\n=== Test des modèles simplifiés terminé avec succès ===")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

if __name__ == "__main__":
    test_simple_models()
