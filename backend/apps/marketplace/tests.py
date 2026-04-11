from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.subscriptions.models import Plan

from .models import (
    EscrowAccount,
    MarketplaceListing,
    MarketplaceOrder,
    MarketplacePayment,
    SellerVerification,
)


class MarketplaceFlowTest(TestCase):
    def setUp(self):
        Plan.objects.get_or_create(
            nom='free',
            defaults={'prix_mensuel': 0, 'estimations_par_mois': 10, 'alertes_max': 2},
        )
        self.seller = User.objects.create_user(
            username='seller_market',
            email='seller@example.com',
            password='testpass123',
        )
        self.buyer = User.objects.create_user(
            username='buyer_market',
            email='buyer@example.com',
            password='testpass123',
        )
        self.admin = User.objects.create_user(
            username='admin_market',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
        )

        self.seller_client = APIClient()
        self.seller_client.force_authenticate(user=self.seller)
        self.buyer_client = APIClient()
        self.buyer_client.force_authenticate(user=self.buyer)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

    def _submit_and_approve_verification(self):
        submit_response = self.seller_client.post(
            '/api/marketplace/verification/',
            {
                'legal_name': 'Seller Verified',
                'phone_number': '+213555000000',
                'country': 'DZ',
                'city': 'Alger',
                'address_line': '12 Rue du Marche',
                'document_type': 'national_id',
                'document_number': 'AA123456',
                'document_front_url': 'https://example.com/front.jpg',
                'document_back_url': 'https://example.com/back.jpg',
                'selfie_url': 'https://example.com/selfie.jpg',
            },
            format='json',
        )
        self.assertEqual(submit_response.status_code, 201)
        verification_id = submit_response.data['id']

        review_response = self.admin_client.post(
            f'/api/marketplace/verification/{verification_id}/review/',
            {'approved': True, 'review_notes': 'Dossier valide'},
            format='json',
        )
        self.assertEqual(review_response.status_code, 200)
        self.assertEqual(review_response.data['status'], SellerVerification.Status.APPROVED)
        return verification_id

    def _create_listing(self):
        response = self.seller_client.post(
            '/api/marketplace/listings/',
            {
                'vehicule': {
                    'marque': 'Renault',
                    'modele': 'Clio',
                    'categorie': 'citadine',
                },
                'annonce': {
                    'annee': 2021,
                    'kilometrage': 28000,
                    'carburant': 'essence',
                    'boite': 'manuelle',
                    'puissance': 90,
                    'prix': '12900.00',
                    'ville': 'Alger',
                    'pays': 'DZ',
                    'description': 'Clio en excellent etat',
                },
                'logistics_mode': 'platform',
                'secure_payment_required': True,
                'escrow_required': True,
                'logistics_enabled': True,
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        return response.data['id']

    def test_unverified_seller_cannot_publish_listing(self):
        response = self.seller_client.post(
            '/api/marketplace/listings/',
            {
                'vehicule': {'marque': 'Peugeot', 'modele': '208'},
                'annonce': {
                    'annee': 2020,
                    'kilometrage': 35000,
                    'carburant': 'essence',
                    'boite': 'manuelle',
                    'prix': '9800.00',
                },
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('verification', response.data['error'].lower())

    def test_verified_seller_can_publish_listing_and_buyer_can_complete_secure_order(self):
        self._submit_and_approve_verification()
        listing_id = self._create_listing()

        order_response = self.buyer_client.post(
            '/api/marketplace/orders/',
            {
                'listing_id': listing_id,
                'currency': 'EUR',
                'logistics_required': True,
                'shipping_address': {
                    'full_address': '22 Avenue Acheteur, Oran',
                    'city': 'Oran',
                },
                'buyer_note': 'Merci de soigner l emballage',
            },
            format='json',
        )
        self.assertEqual(order_response.status_code, 201)
        order_id = order_response.data['id']
        release_token = order_response.data['escrow_release_token']
        self.assertTrue(release_token)
        self.assertEqual(order_response.data['status'], MarketplaceOrder.Status.PAYMENT_PENDING)

        confirm_payment = self.buyer_client.post(
            f'/api/marketplace/orders/{order_id}/confirm_payment/',
            {},
            format='json',
        )
        self.assertEqual(confirm_payment.status_code, 200)
        self.assertEqual(confirm_payment.data['status'], MarketplaceOrder.Status.ESCROW_FUNDED)

        ship_response = self.seller_client.post(
            f'/api/marketplace/orders/{order_id}/ship/',
            {
                'provider': 'DHL',
                'tracking_number': 'TRACK123',
                'notes': 'Expedie ce matin',
            },
            format='json',
        )
        self.assertEqual(ship_response.status_code, 200)
        self.assertEqual(ship_response.data['status'], MarketplaceOrder.Status.IN_TRANSIT)

        delivery_response = self.buyer_client.post(
            f'/api/marketplace/orders/{order_id}/confirm_delivery/',
            {'release_token': release_token},
            format='json',
        )
        self.assertEqual(delivery_response.status_code, 200)
        self.assertEqual(delivery_response.data['status'], MarketplaceOrder.Status.COMPLETED)
        self.assertEqual(delivery_response.data['escrow']['status'], EscrowAccount.Status.RELEASED)

        listing = MarketplaceListing.objects.get(id=listing_id)
        self.assertEqual(listing.status, MarketplaceListing.Status.SOLD)
        payment = MarketplacePayment.objects.filter(order_id=order_id).latest('created_at')
        self.assertEqual(payment.status, MarketplacePayment.Status.SUCCEEDED)

    def test_dispute_resolution_can_refund_buyer_and_republish_listing(self):
        self._submit_and_approve_verification()
        listing_id = self._create_listing()

        order_response = self.buyer_client.post(
            '/api/marketplace/orders/',
            {
                'listing_id': listing_id,
                'shipping_address': {'full_address': 'Oran'},
            },
            format='json',
        )
        order_id = order_response.data['id']

        self.buyer_client.post(
            f'/api/marketplace/orders/{order_id}/confirm_payment/',
            {},
            format='json',
        )

        dispute_response = self.buyer_client.post(
            f'/api/marketplace/orders/{order_id}/open_dispute/',
            {'reason': 'Vehicule non conforme a la description'},
            format='json',
        )
        self.assertEqual(dispute_response.status_code, 200)
        self.assertEqual(dispute_response.data['status'], MarketplaceOrder.Status.DISPUTED)

        resolve_response = self.admin_client.post(
            f'/api/marketplace/orders/{order_id}/resolve_dispute/',
            {'decision': 'refund_buyer', 'notes': 'Litige tranche en faveur de l acheteur'},
            format='json',
        )
        self.assertEqual(resolve_response.status_code, 200)
        self.assertEqual(resolve_response.data['status'], MarketplaceOrder.Status.REFUNDED)
        self.assertEqual(resolve_response.data['escrow']['status'], EscrowAccount.Status.REFUNDED)

        listing = MarketplaceListing.objects.get(id=listing_id)
        self.assertEqual(listing.status, MarketplaceListing.Status.PUBLISHED)
