#!/usr/bin/env python3
"""
Test simple des modèles marketplace pour vérifier les erreurs
"""

import os
import sys
import django

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_models():
    """Test simple des modèles marketplace"""
    try:
        from apps.marketplace.models import SellerVerification, MarketplaceListing, MarketplaceOrder
        
        print("✅ Importation des modèles marketplace réussie")
        
        # Test création d'un objet SellerVerification
        print("\n--- Test SellerVerification ---")
        try:
            from django.contrib.auth.models import User
            user = User.objects.first()
            
            verification = SellerVerification.objects.create(
                user=user,
                legal_name="Test User",
                phone_number="0123456789",
                country="DZ",
                city="Alger",
                address_line="123 Rue Test",
                document_type="national_id",
                document_number_last4="1234"
            )
            print(f"✅ SellerVerification créé: {verification}")
            
        except Exception as e:
            print(f"❌ Erreur SellerVerification: {e}")
        
        # Test création d'un objet MarketplaceListing
        print("\n--- Test MarketplaceListing ---")
        try:
            listing = MarketplaceListing.objects.create(
                seller=user.seller_profile if hasattr(user, 'seller_profile') else None,
                title="Voiture Test",
                brand="Renault",
                model="Clio",
                year=2020,
                price=15000
            )
            print(f"✅ MarketplaceListing créé: {listing}")
            
        except Exception as e:
            print(f"❌ Erreur MarketplaceListing: {e}")
        
        # Test création d'un objet MarketplaceOrder
        print("\n--- Test MarketplaceOrder ---")
        try:
            order = MarketplaceOrder.objects.create(
                listing=listing,
                buyer=user,
                reference=f"TEST-{listing.id}"
            )
            print(f"✅ MarketplaceOrder créé: {order}")
            
        except Exception as e:
            print(f"❌ Erreur MarketplaceOrder: {e}")
        
        print("\n=== Test des modèles terminé avec succès ===")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

if __name__ == "__main__":
    test_models()
