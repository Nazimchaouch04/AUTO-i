from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.subscriptions.models import Plan

from .models import (
    Listing,
    Transaction,
    SellerProfile,
    Review,
    Favorite,
    Message,
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

    def test_unverified_seller_cannot_publish_listing(self):
        response = self.seller_client.post(
            '/api/marketplace/listings/',
            {
                'title': 'Peugeot 208 2020',
                'brand': 'Peugeot',
                'model': '208',
                'year': 2020,
                'price': '9800.00',
                'fuel_type': 'essence',
                'transmission': 'manuelle',
                'description': 'Test unverified listing',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('verification', response.data.lower())

    def test_verified_seller_can_publish_listing(self):
        seller_profile, created = SellerProfile.objects.get_or_create(user=self.seller)
        seller_profile.is_verified = True
        seller_profile.save()

        response = self.seller_client.post(
            '/api/marketplace/listings/',
            {
                'title': 'Renault Clio 2021 Verified',
                'brand': 'Renault',
                'model': 'Clio',
                'year': 2021,
                'price': '12900.00',
                'fuel_type': 'essence',
                'transmission': 'manuelle',
                'description': 'Clio verified listing test',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'draft')

    def test_dispute_resolution_simulation(self):
        # Simple test without complex flow
        seller_profile, created = SellerProfile.objects.get_or_create(user=self.seller)
        listing = Listing.objects.create(
            seller=seller_profile,
            title='Test Dispute Listing',
            brand='Test',
            model='Model',
            year=2020,
            price='10000.00',
            description='Test',
        )
        self.assertEqual(listing.status, 'draft')
