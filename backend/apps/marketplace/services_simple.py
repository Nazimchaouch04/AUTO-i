"""
Services marketplace simplifiés et fonctionnels.
Remplace le fichier services.py complexe qui référence des modèles inexistants.
"""
from __future__ import annotations

import secrets
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.annonces.models import Annonce

from .models import (
    Listing,
    Transaction,
    SellerProfile,
    Review,
    Favorite,
    Message,
)

try:
    import stripe
except ImportError:
    stripe = None


class MarketplaceError(Exception):
    """Erreur métier du marketplace."""


class MarketplacePaymentService:
    @staticmethod
    def _should_use_stripe():
        secret_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        return bool(
            stripe
            and secret_key
            and 'placeholder' not in secret_key
            and secret_key != 'sk_test_...'
        )

    @classmethod
    def create_payment(cls, transaction: Transaction):
        """Crée un paiement Stripe pour une transaction."""
        amount = Decimal(transaction.total_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if cls._should_use_stripe():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency='eur',
                metadata={
                    'transaction_id': str(transaction.id),
                    'listing_id': str(transaction.listing_id),
                    'buyer_id': str(transaction.buyer_id),
                },
                automatic_payment_methods={'enabled': True},
            )
            return {
                'provider': 'stripe',
                'client_secret': intent.client_secret,
                'provider_reference': intent.id,
            }

        return {
            'provider': 'mock',
            'client_secret': f"mock_secret_{secrets.token_hex(12)}",
            'provider_reference': f"mock_pi_{secrets.token_hex(8)}",
        }

    @classmethod
    def confirm_payment(cls, transaction: Transaction, provider_reference: str = None):
        """Confirme un paiement."""
        if cls._should_use_stripe() and provider_reference:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.retrieve(provider_reference)
            if intent.status not in {'succeeded', 'requires_capture'}:
                raise MarketplaceError("Le paiement n'est pas encore confirmé par Stripe.")
        
        transaction.status = Transaction.Status.PAID
        transaction.save(update_fields=['status', 'updated_at'])
        return transaction


class MarketplaceService:
    @staticmethod
    def _ensure_seller_profile(user):
        """Vérifie/crée le profil vendeur."""
        profile, created = SellerProfile.objects.get_or_create(
            user=user,
            defaults={'company_name': user.username}
        )
        return profile

    @staticmethod
    @transaction.atomic
    def create_listing(seller, title, description, brand, model, year, price):
        """Crée une annonce marketplace."""
        profile = MarketplaceService._ensure_seller_profile(seller)
        
        listing = Listing.objects.create(
            seller=profile,
            title=title,
            description=description,
            brand=brand,
            model=model,
            year=year,
            price=price,
            status=Listing.Status.PUBLISHED,
        )
        return listing

    @staticmethod
    @transaction.atomic  
    def create_transaction(buyer, listing):
        """Crée une transaction pour un achat."""
        if listing.seller.user == buyer:
            raise MarketplaceError("Le vendeur ne peut pas acheter sa propre annonce.")
        if listing.status != Listing.Status.PUBLISHED:
            raise MarketplaceError("Cette annonce n'est pas disponible à l'achat.")
        
        transaction = Transaction.objects.create(
            listing=listing,
            buyer=buyer,
            seller=listing.seller,
            total_amount=listing.price,
            status=Transaction.Status.PENDING,
        )
        
        # Réserver l'annonce
        listing.status = Listing.Status.SOLD
        listing.save(update_fields=['status', 'updated_at'])
        
        return transaction

    @staticmethod
    def add_review(transaction, reviewer, rating, comment=''):
        """Ajoute un avis sur une transaction."""
        if transaction.status != Transaction.Status.COMPLETED:
            raise MarketplaceError("La transaction doit être complétée pour laisser un avis.")
        
        review, created = Review.objects.update_or_create(
            transaction=transaction,
            reviewer=reviewer,
            defaults={
                'reviewed': transaction.seller,
                'rating': rating,
                'comment': comment,
            }
        )
        return review

    @staticmethod
    def send_message(sender, recipient, content, listing=None, transaction=None):
        """Envoie un message entre utilisateurs."""
        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=content,
            listing=listing,
            transaction=transaction,
        )
        return message

    @staticmethod
    def toggle_favorite(user, listing):
        """Ajoute/retire un favori."""
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            listing=listing,
        )
        if not created:
            favorite.delete()
            return False
        return True
