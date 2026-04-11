from __future__ import annotations

import secrets
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.annonces.models import Annonce, Vehicule

from .models import (
    EscrowAccount,
    LogisticsShipment,
    MarketplaceEvent,
    MarketplaceListing,
    MarketplaceOrder,
    MarketplacePayment,
    SellerVerification,
)

try:
    import stripe
except ImportError:  # pragma: no cover - depends on environment
    stripe = None


class MarketplaceError(Exception):
    """Business error raised by marketplace services."""


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
    def create_payment(cls, order: MarketplaceOrder) -> MarketplacePayment:
        amount = order.total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if cls._should_use_stripe():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=order.currency.lower(),
                metadata={
                    'order_reference': str(order.reference),
                    'listing_id': order.listing_id,
                    'buyer_id': order.buyer_id,
                    'seller_id': order.seller_id,
                },
                automatic_payment_methods={'enabled': True},
            )
            return MarketplacePayment.objects.create(
                order=order,
                provider=MarketplacePayment.Provider.STRIPE,
                status=MarketplacePayment.Status.REQUIRES_ACTION,
                amount=amount,
                currency=order.currency,
                provider_reference=intent.id,
                client_secret=intent.client_secret or '',
                provider_payload={'status': intent.status},
            )

        reference = f"mock_pi_{secrets.token_hex(8)}"
        secret = f"mock_secret_{secrets.token_hex(12)}"
        return MarketplacePayment.objects.create(
            order=order,
            provider=MarketplacePayment.Provider.MOCK,
            status=MarketplacePayment.Status.REQUIRES_ACTION,
            amount=amount,
            currency=order.currency,
            provider_reference=reference,
            client_secret=secret,
            provider_payload={'mode': 'mock'},
        )

    @classmethod
    def confirm_payment(
        cls,
        payment: MarketplacePayment,
        provider_reference: str | None = None,
    ) -> MarketplacePayment:
        if payment.status == MarketplacePayment.Status.SUCCEEDED:
            return payment

        if payment.provider == MarketplacePayment.Provider.STRIPE and cls._should_use_stripe():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent_id = provider_reference or payment.provider_reference
            intent = stripe.PaymentIntent.retrieve(intent_id)
            if intent.status not in {'succeeded', 'requires_capture'}:
                raise MarketplaceError("Le paiement n'est pas encore confirme par Stripe.")
            payment.provider_payload = {'status': intent.status}

        payment.status = MarketplacePayment.Status.SUCCEEDED
        payment.confirmed_at = timezone.now()
        payment.save(update_fields=['status', 'confirmed_at', 'provider_payload', 'updated_at'])
        return payment

    @classmethod
    def refund_payment(cls, payment: MarketplacePayment) -> MarketplacePayment:
        if payment.status == MarketplacePayment.Status.REFUNDED:
            return payment

        if payment.provider == MarketplacePayment.Provider.STRIPE and cls._should_use_stripe():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Refund.create(payment_intent=payment.provider_reference)

        payment.status = MarketplacePayment.Status.REFUNDED
        payment.refunded_at = timezone.now()
        payment.save(update_fields=['status', 'refunded_at', 'updated_at'])
        return payment


class MarketplaceService:
    @staticmethod
    def _log_event(event_type, actor=None, listing=None, order=None, payload=None):
        MarketplaceEvent.objects.create(
            event_type=event_type,
            actor=actor,
            listing=listing,
            order=order,
            payload=payload or {},
        )

    @staticmethod
    def _ensure_verified_seller(user):
        verification = SellerVerification.objects.filter(user=user).first()
        if not verification or verification.status != SellerVerification.Status.APPROVED:
            raise MarketplaceError(
                "La verification d'identite du vendeur doit etre approuvee avant publication."
            )
        return verification

    @staticmethod
    def submit_verification(user, payload):
        document_number = str(payload.get('document_number', '')).strip()
        if len(document_number) < 4:
            raise MarketplaceError("Le numero de document doit contenir au moins 4 caracteres.")

        verification, _ = SellerVerification.objects.get_or_create(
            user=user,
            defaults={
                'legal_name': payload.get('legal_name', user.get_full_name() or user.username),
                'phone_number': payload.get('phone_number', ''),
                'country': payload.get('country', 'DZ'),
                'address_line': payload.get('address_line', ''),
                'document_type': payload.get('document_type', SellerVerification.DocumentType.NATIONAL_ID),
                'document_number_last4': document_number[-4:],
            },
        )

        verification.legal_name = payload.get('legal_name', verification.legal_name)
        verification.phone_number = payload.get('phone_number', verification.phone_number)
        verification.country = payload.get('country', verification.country)
        verification.city = payload.get('city', verification.city)
        verification.address_line = payload.get('address_line', verification.address_line)
        verification.document_type = payload.get('document_type', verification.document_type)
        verification.document_number_last4 = document_number[-4:]
        verification.document_front_url = payload.get('document_front_url', verification.document_front_url)
        verification.document_back_url = payload.get('document_back_url', verification.document_back_url)
        verification.selfie_url = payload.get('selfie_url', verification.selfie_url)
        verification.business_name = payload.get('business_name', verification.business_name)
        verification.tax_id = payload.get('tax_id', verification.tax_id)
        verification.metadata = payload.get('metadata', verification.metadata or {})
        verification.status = SellerVerification.Status.SUBMITTED
        verification.submitted_at = timezone.now()
        verification.review_notes = ''
        verification.reviewed_at = None
        verification.reviewed_by = None
        verification.verified_at = None
        verification.save()

        MarketplaceService._log_event(
            event_type='seller_verification_submitted',
            actor=user,
            payload={'status': verification.status},
        )
        return verification

    @staticmethod
    def review_verification(verification, reviewer, approved, review_notes=''):
        verification.status = (
            SellerVerification.Status.APPROVED if approved else SellerVerification.Status.REJECTED
        )
        verification.review_notes = review_notes
        verification.reviewed_at = timezone.now()
        verification.reviewed_by = reviewer
        verification.verified_at = timezone.now() if approved else None
        verification.save()

        MarketplaceService._log_event(
            event_type='seller_verification_reviewed',
            actor=reviewer,
            payload={'approved': approved, 'user_id': verification.user_id},
        )
        return verification

    @staticmethod
    @transaction.atomic
    def create_listing(user, validated_data):
        verification = MarketplaceService._ensure_verified_seller(user)

        vehicule_data = validated_data.pop('vehicule')
        annonce_data = validated_data.pop('annonce')
        vehicule, _ = Vehicule.objects.get_or_create(
            marque=vehicule_data['marque'],
            modele=vehicule_data['modele'],
            defaults={'categorie': vehicule_data.get('categorie', 'berline')},
        )
        if vehicule_data.get('categorie') and vehicule.categorie != vehicule_data['categorie']:
            vehicule.categorie = vehicule_data['categorie']
            vehicule.save(update_fields=['categorie'])

        annonce = Annonce.objects.create(
            vehicule=vehicule,
            annee=annonce_data['annee'],
            kilometrage=annonce_data['kilometrage'],
            carburant=annonce_data.get('carburant', 'essence'),
            boite=annonce_data.get('boite', 'manuelle'),
            puissance=annonce_data.get('puissance'),
            prix=annonce_data['prix'],
            ville=annonce_data.get('ville'),
            pays=annonce_data.get('pays', 'DZ'),
            description=annonce_data.get('description', ''),
            source='marketplace',
            url_originale=annonce_data.get('url_originale'),
            est_active=True,
        )

        listing = MarketplaceListing.objects.create(
            seller=user,
            annonce=annonce,
            status=MarketplaceListing.Status.PUBLISHED,
            logistics_mode=validated_data.get(
                'logistics_mode',
                MarketplaceListing.LogisticsMode.PLATFORM,
            ),
            secure_payment_required=validated_data.get('secure_payment_required', True),
            escrow_required=validated_data.get('escrow_required', True),
            logistics_enabled=validated_data.get('logistics_enabled', True),
            marketplace_fee_pct=validated_data.get('marketplace_fee_pct', Decimal('5.00')),
            escrow_window_days=validated_data.get('escrow_window_days', 7),
            verification_snapshot=verification.status,
            published_at=timezone.now(),
            metadata=validated_data.get('metadata', {}),
        )

        MarketplaceService._log_event(
            event_type='listing_created',
            actor=user,
            listing=listing,
            payload={'annonce_id': annonce.id},
        )
        return listing

    @staticmethod
    @transaction.atomic
    def publish_listing(listing, user):
        if listing.seller_id != user.id:
            raise MarketplaceError("Seul le vendeur proprietaire peut publier cette annonce.")
        MarketplaceService._ensure_verified_seller(user)
        listing.status = MarketplaceListing.Status.PUBLISHED
        listing.verification_snapshot = SellerVerification.Status.APPROVED
        listing.published_at = timezone.now()
        listing.cancelled_at = None
        listing.save(update_fields=['status', 'verification_snapshot', 'published_at', 'cancelled_at', 'updated_at'])
        MarketplaceService._log_event('listing_published', actor=user, listing=listing)
        return listing

    @staticmethod
    @transaction.atomic
    def cancel_listing(listing, user):
        if listing.seller_id != user.id and not user.is_staff:
            raise MarketplaceError("Vous ne pouvez pas annuler cette annonce.")
        if listing.status == MarketplaceListing.Status.SOLD:
            raise MarketplaceError("Une annonce vendue ne peut pas etre annulee.")
        listing.status = MarketplaceListing.Status.CANCELLED
        listing.cancelled_at = timezone.now()
        listing.annonce.est_active = False
        listing.annonce.save(update_fields=['est_active', 'updated_at'])
        listing.save(update_fields=['status', 'cancelled_at', 'updated_at'])
        MarketplaceService._log_event('listing_cancelled', actor=user, listing=listing)
        return listing

    @staticmethod
    @transaction.atomic
    def create_order(buyer, listing, payload):
        if listing.seller_id == buyer.id:
            raise MarketplaceError("Le vendeur ne peut pas acheter sa propre annonce.")
        if listing.status != MarketplaceListing.Status.PUBLISHED:
            raise MarketplaceError("Cette annonce n'est pas disponible a l'achat.")

        MarketplaceService._ensure_verified_seller(listing.seller)

        vehicle_price = Decimal(listing.annonce.prix)
        fee_pct = Decimal(listing.marketplace_fee_pct or Decimal('5.00'))
        marketplace_fee = (vehicle_price * fee_pct / Decimal('100')).quantize(Decimal('0.01'))
        logistics_required = bool(payload.get('logistics_required', listing.logistics_enabled))
        logistics_fee = Decimal('250.00') if logistics_required else Decimal('0.00')
        escrow_amount = vehicle_price if listing.escrow_required else Decimal('0.00')
        total_amount = vehicle_price + marketplace_fee + logistics_fee

        order = MarketplaceOrder.objects.create(
            listing=listing,
            buyer=buyer,
            seller=listing.seller,
            status=MarketplaceOrder.Status.PAYMENT_PENDING,
            currency=payload.get('currency', 'EUR'),
            vehicle_price=vehicle_price,
            marketplace_fee=marketplace_fee,
            logistics_fee=logistics_fee,
            escrow_amount=escrow_amount,
            total_amount=total_amount,
            secure_payment_required=listing.secure_payment_required,
            escrow_required=listing.escrow_required,
            logistics_required=logistics_required,
            shipping_address=payload.get('shipping_address', {}),
            buyer_note=payload.get('buyer_note', ''),
        )

        release_token = EscrowAccount.issue_release_token()
        escrow = EscrowAccount(order=order, held_amount=escrow_amount)
        escrow.set_release_token(release_token)
        escrow.save()

        destination = payload.get('shipping_address', {})
        LogisticsShipment.objects.create(
            order=order,
            provider='AutoIntel Logistics' if logistics_required else 'Retrait direct',
            pickup_address=payload.get('pickup_address', listing.annonce.ville or ''),
            destination_address=destination.get('full_address', destination.get('city', '')),
            status=LogisticsShipment.Status.PENDING if logistics_required else LogisticsShipment.Status.SCHEDULED,
            notes=payload.get('delivery_note', ''),
        )

        payment = MarketplacePaymentService.create_payment(order)
        listing.status = MarketplaceListing.Status.RESERVED
        listing.save(update_fields=['status', 'updated_at'])

        order._issued_release_token = release_token

        MarketplaceService._log_event(
            'order_created',
            actor=buyer,
            listing=listing,
            order=order,
            payload={'payment_id': payment.id},
        )
        return order

    @staticmethod
    @transaction.atomic
    def confirm_payment(order, actor, provider_reference=None):
        if actor.id not in {order.buyer_id, order.seller_id} and not actor.is_staff:
            raise MarketplaceError("Vous n'etes pas autorise a confirmer ce paiement.")

        payment = order.payments.order_by('-created_at').first()
        if not payment:
            raise MarketplaceError("Aucun paiement n'est associe a cette commande.")

        payment = MarketplacePaymentService.confirm_payment(payment, provider_reference)
        order.status = MarketplaceOrder.Status.ESCROW_FUNDED
        order.save(update_fields=['status', 'updated_at'])

        escrow = order.escrow
        escrow.status = EscrowAccount.Status.FUNDED
        escrow.funded_at = timezone.now()
        escrow.save(update_fields=['status', 'funded_at', 'updated_at'])

        shipment = getattr(order, 'shipment', None)
        if shipment and shipment.status == LogisticsShipment.Status.PENDING:
            shipment.status = LogisticsShipment.Status.SCHEDULED
            shipment.save(update_fields=['status', 'updated_at'])

        MarketplaceService._log_event(
            'payment_confirmed',
            actor=actor,
            order=order,
            listing=order.listing,
            payload={'payment_id': payment.id},
        )
        return order

    @staticmethod
    @transaction.atomic
    def mark_shipped(order, seller, payload):
        if order.seller_id != seller.id:
            raise MarketplaceError("Seul le vendeur peut expedier cette commande.")
        if order.status not in {
            MarketplaceOrder.Status.ESCROW_FUNDED,
            MarketplaceOrder.Status.PROCESSING,
        }:
            raise MarketplaceError("La commande doit etre payee avant expedition.")

        shipment = order.shipment
        shipment.provider = payload.get('provider', shipment.provider)
        shipment.tracking_number = payload.get('tracking_number', shipment.tracking_number)
        shipment.notes = payload.get('notes', shipment.notes)
        shipment.status = LogisticsShipment.Status.IN_TRANSIT
        shipment.shipped_at = timezone.now()
        shipment.save()

        order.status = MarketplaceOrder.Status.IN_TRANSIT
        order.save(update_fields=['status', 'updated_at'])

        MarketplaceService._log_event(
            'shipment_in_transit',
            actor=seller,
            order=order,
            listing=order.listing,
            payload={'tracking_number': shipment.tracking_number},
        )
        return order

    @staticmethod
    @transaction.atomic
    def confirm_delivery(order, buyer, release_token):
        if order.buyer_id != buyer.id:
            raise MarketplaceError("Seul l'acheteur peut confirmer la livraison.")
        if order.status not in {
            MarketplaceOrder.Status.ESCROW_FUNDED,
            MarketplaceOrder.Status.IN_TRANSIT,
            MarketplaceOrder.Status.DELIVERED,
        }:
            raise MarketplaceError("La commande n'est pas prete pour confirmation.")

        escrow = order.escrow
        if order.escrow_required and not escrow.check_release_token(release_token):
            raise MarketplaceError("Le code de liberation d'escrow est invalide.")

        shipment = order.shipment
        shipment.status = LogisticsShipment.Status.DELIVERED
        shipment.delivered_at = timezone.now()
        shipment.save(update_fields=['status', 'delivered_at', 'updated_at'])

        order.status = MarketplaceOrder.Status.COMPLETED
        order.save(update_fields=['status', 'updated_at'])

        escrow.status = EscrowAccount.Status.RELEASED
        escrow.released_at = timezone.now()
        escrow.save(update_fields=['status', 'released_at', 'updated_at'])

        listing = order.listing
        listing.status = MarketplaceListing.Status.SOLD
        listing.sold_at = timezone.now()
        listing.annonce.est_active = False
        listing.annonce.save(update_fields=['est_active', 'updated_at'])
        listing.save(update_fields=['status', 'sold_at', 'updated_at'])

        MarketplaceService._log_event(
            'escrow_released',
            actor=buyer,
            order=order,
            listing=listing,
        )
        return order

    @staticmethod
    @transaction.atomic
    def open_dispute(order, actor, reason):
        if actor.id not in {order.buyer_id, order.seller_id} and not actor.is_staff:
            raise MarketplaceError("Vous ne pouvez pas ouvrir de litige sur cette commande.")

        order.status = MarketplaceOrder.Status.DISPUTED
        order.dispute_reason = reason
        order.save(update_fields=['status', 'dispute_reason', 'updated_at'])

        escrow = order.escrow
        escrow.status = EscrowAccount.Status.DISPUTED
        escrow.disputed_at = timezone.now()
        escrow.dispute_notes = reason
        escrow.save(update_fields=['status', 'disputed_at', 'dispute_notes', 'updated_at'])

        MarketplaceService._log_event(
            'order_disputed',
            actor=actor,
            order=order,
            listing=order.listing,
            payload={'reason': reason},
        )
        return order

    @staticmethod
    @transaction.atomic
    def resolve_dispute(order, reviewer, decision, notes=''):
        if not reviewer.is_staff:
            raise MarketplaceError("Seul un administrateur peut resoudre un litige.")

        escrow = order.escrow
        payment = order.payments.order_by('-created_at').first()

        if decision == 'release_to_seller':
            order.status = MarketplaceOrder.Status.COMPLETED
            order.save(update_fields=['status', 'updated_at'])
            escrow.status = EscrowAccount.Status.RELEASED
            escrow.released_at = timezone.now()
            escrow.dispute_notes = notes
            escrow.save(update_fields=['status', 'released_at', 'dispute_notes', 'updated_at'])
            order.listing.status = MarketplaceListing.Status.SOLD
            order.listing.sold_at = timezone.now()
            order.listing.save(update_fields=['status', 'sold_at', 'updated_at'])
        elif decision == 'refund_buyer':
            order.status = MarketplaceOrder.Status.REFUNDED
            order.save(update_fields=['status', 'updated_at'])
            escrow.status = EscrowAccount.Status.REFUNDED
            escrow.refunded_at = timezone.now()
            escrow.dispute_notes = notes
            escrow.save(update_fields=['status', 'refunded_at', 'dispute_notes', 'updated_at'])
            order.listing.status = MarketplaceListing.Status.PUBLISHED
            order.listing.save(update_fields=['status', 'updated_at'])
            if payment:
                MarketplacePaymentService.refund_payment(payment)
        else:
            raise MarketplaceError("Decision de litige invalide.")

        MarketplaceService._log_event(
            'dispute_resolved',
            actor=reviewer,
            order=order,
            listing=order.listing,
            payload={'decision': decision},
        )
        return order
