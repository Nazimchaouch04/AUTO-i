from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.subscriptions.models import Plan

class EstimationAPITest(TestCase):

    def setUp(self):
        # Créer le plan gratuit pour éviter que le signal de souscription échoue
        Plan.objects.get_or_create(nom='free', defaults={'prix_mensuel': 0, 'estimations_par_mois': 10})
        self.client = APIClient()
        self.user = User.objects.create_user('estimateur', 'est@test.com', 'pass1234')
        self.client.force_authenticate(user=self.user)

    def test_estimation_complete(self):
        resp = self.client.post('/api/estimation/', {
            'marque': 'Renault', 'modele': 'Clio',
            'annee': 2019, 'kilometrage': 60000,
            'carburant': 'essence', 'boite': 'manuelle',
            'puissance': 90, 'pays': 'DZ'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('prix_estime', resp.data)
        self.assertIn('fourchette_basse', resp.data)
        self.assertIn('fourchette_haute', resp.data)
        self.assertIn('fiabilite', resp.data)
        self.assertGreater(float(resp.data['prix_estime']), 0)
        self.assertLess(
            float(resp.data['fourchette_basse']),
            float(resp.data['prix_estime']))
        self.assertGreater(
            float(resp.data['fourchette_haute']),
            float(resp.data['prix_estime']))

    def test_estimation_champs_manquants(self):
        resp = self.client.post('/api/estimation/', {'marque': 'Renault'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
