from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.annonces.models import Annonce, Vehicule
from apps.subscriptions.models import Plan

from .models import UserProfileAnalysis
from .services.predictive_analytics import PredictiveAnalyticsService


class PredictiveAnalyticsTest(TestCase):
    def setUp(self):
        Plan.objects.get_or_create(
            nom='free',
            defaults={'prix_mensuel': 0, 'estimations_par_mois': 10, 'alertes_max': 2},
        )
        self.user = User.objects.create_user(
            username='predictive_user',
            email='predictive@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.clio = Vehicule.objects.create(
            marque='Renault',
            modele='Clio',
            categorie='citadine',
        )
        self.captur = Vehicule.objects.create(
            marque='Renault',
            modele='Captur',
            categorie='suv',
        )

        self._create_market_series(
            vehicule=self.clio,
            prices=[9800, 10100, 10500, 11050, 11400, 11850],
            carburant='essence',
            pays='FR',
        )
        self._create_market_series(
            vehicule=self.captur,
            prices=[15600, 15850, 16100, 16500],
            carburant='hybride',
            pays='FR',
        )

        UserProfileAnalysis.objects.create(
            user=self.user,
            budget_max=13000,
            budget_min=9000,
            types_vehicule=['citadine'],
            preferences_carburant=['essence'],
        )

    def _create_market_series(self, vehicule, prices, carburant, pays):
        now = timezone.now()
        for index, price in enumerate(prices):
            annonce = Annonce.objects.create(
                vehicule=vehicule,
                annee=2020 + min(index, 3),
                kilometrage=25000 + (index * 5000),
                carburant=carburant,
                boite='manuelle',
                prix=price,
                pays=pays,
                est_bonne_affaire=index % 2 == 0,
                url_originale=f'https://example.com/{vehicule.id}/{index}',
            )
            target_date = now - timedelta(days=(len(prices) - index) * 30)
            Annonce.objects.filter(pk=annonce.pk).update(
                date_publication=target_date,
                date_collecte=target_date,
                created_at=target_date,
                updated_at=target_date,
            )

    def test_predictive_service_generates_full_report(self):
        service = PredictiveAnalyticsService(self.user)
        report = service.build_predictive_report(
            filters={'marque': 'Renault', 'modele': 'Clio'},
            external_context={
                'economic': {
                    'inflation_rate': 5.8,
                    'interest_rate': 3.1,
                    'fuel_price_change_pct': 9,
                },
                'weather': {'severity_index': 40},
                'events': [
                    {
                        'label': 'Greve logistique',
                        'direction': 'increase',
                        'magnitude': 1.2,
                        'price_sensitivity': 1.4,
                    }
                ],
            },
            forecast_months=6,
            lookback_months=12,
        )

        self.assertIn('price_forecast', report)
        self.assertEqual(len(report['price_forecast']['forecast']), 6)
        self.assertGreater(report['current_market']['average_price'], 0)
        self.assertTrue(report['best_periods']['achat'])
        self.assertTrue(report['event_impact']['factors'])

    def test_market_insights_endpoint_returns_predictive_data(self):
        response = self.client.get('/api/ai/market-insights/?marque=Renault&modele=Clio')

        self.assertEqual(response.status_code, 200)
        self.assertIn('insights', response.data)
        self.assertGreaterEqual(response.data['total'], 1)
        self.assertIn('meilleures_periodes', response.data)

    def test_prediction_prix_endpoint_supports_year_horizons(self):
        response = self.client.post(
            '/api/ai/prediction-prix/',
            {
                'marque': 'Renault',
                'modele': 'Clio',
                'annees': [1],
                'external_context': {
                    'economic': {'inflation_rate': 4.5, 'interest_rate': 2.4}
                },
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('1_ans', response.data['predictions'])
        self.assertEqual(len(response.data['forecast']), 12)
        self.assertIn('impact_evenements', response.data)

    def test_analyse_predictive_endpoint_uses_profile_defaults(self):
        response = self.client.get('/api/ai/analyse-predictive/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['custom_trends']['personalization_used'])
        self.assertEqual(response.data['scope']['filters']['carburant'], 'essence')
        self.assertEqual(response.data['scope']['filters']['categorie'], 'citadine')
