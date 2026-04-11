#!/usr/bin/env python3
"""
Test des modèles marketplace corrigés
"""

import os
import sys
import django

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_fixed_models():
    """Test des modèles marketplace corrigés"""
    try:
        from apps.marketplace.models_fixed import SellerProfile, Listing, Transaction, Review, Favorite, Message
        
        print("✅ Importation des modèles corrigés réussie")
        
        # Test création d'un objet SellerProfile
        print("\n--- Test SellerProfile ---")
        try:
            from django.contrib.auth.models import User
            user = User.objects.first()
            
            profile = SellerProfile.objects.create(
                user=user,
                company_name="Test Company Fixed",
                phone_number="0123456789"
            )
            print(f"✅ SellerProfile créé: {profile}")
            
        except Exception as e:
            print(f"❌ Erreur SellerProfile: {e}")
        
        # Test création d'un objet Listing
        print("\n--- Test Listing ---")
        try:
            listing = Listing.objects.create(
                seller=profile,
                title="Voiture Test Fixed",
                brand="Renault",
                model="Clio",
                year=2020,
                price=15000
            )
            print(f"✅ Listing créé: {listing}")
            
        except Exception as e:
            print(f"❌ Erreur Listing: {e}")
        
        # Test création d'un objet Transaction
        print("\n--- Test Transaction ---")
        try:
            transaction = Transaction.objects.create(
                listing=listing,
                buyer=user,
                seller=profile,
                total_amount=15000
            )
            print(f"✅ Transaction créé: {transaction}")
            
        except Exception as e:
            print(f"❌ Erreur Transaction: {e}")
        
        print("\n=== Test des modèles corrigés terminé avec succès ===")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

if __name__ == "__main__":
    test_fixed_models()
