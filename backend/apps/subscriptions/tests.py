from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class SubscriptionTest(TestCase):

    def setUp(self):
        from apps.subscriptions.models import Plan, Abonnement
        # Créer le plan AVANT de créer l'utilisateur pour que le signal de souscription fonctionne
        self.plan_free = Plan.objects.get_or_create(nom='free', defaults={
            'prix_mensuel': 0, 'estimations_par_mois': 5,
            'alertes_max': 2
        })[0]
        self.plan_pro = Plan.objects.get_or_create(nom='pro', defaults={
            'prix_mensuel': 15, 'estimations_par_mois': 100,
            'alertes_max': 20
        })[0]
        
        self.client = APIClient()
        self.user = User.objects.create_user('sub', 'sub@test.com', 'pass')
        self.client.force_authenticate(user=self.user)
        # L'abonnement est créé automatiquement par signal
        self.abonnement = self.user.subscription

    def test_liste_plans(self):
        resp = self.client.get('/api/subscriptions/plans/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_abonnement_actuel(self):
        resp = self.client.get('/api/subscriptions/mon-abonnement/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('plan', resp.data)
