from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Annonce, Vehicule
from apps.subscriptions.models import Plan

class AnnonceAPITest(TestCase):

    def setUp(self):
        # Créer le plan gratuit pour éviter que le signal de souscription échoue
        Plan.objects.get_or_create(nom='free', defaults={'prix_mensuel': 0, 'estimations_par_mois': 10})
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass1234')
        self.client.force_authenticate(user=self.user)
        self.vehicule = Vehicule.objects.get_or_create(marque='Renault', modele='Clio')[0]
        self.annonce = Annonce.objects.get_or_create(
            vehicule=self.vehicule, annee=2019, kilometrage=60000,
            carburant='essence', boite='manuelle', prix=9500, pays='DZ',
            url_originale='https://test.com/annonce/1'
        )[0]

    def test_liste_annonces(self):
        resp = self.client.get('/api/annonces/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)
        self.assertGreater(resp.data['count'], 0)

    def test_detail_annonce(self):
        resp = self.client.get(f'/api/annonces/{self.annonce.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['annee'], 2019)
        self.assertEqual(resp.data['prix'], '9500.00')

    def test_filtre_pays(self):
        resp = self.client.get('/api/annonces/?pays=DZ')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for a in resp.data['results']:
            self.assertEqual(a['pays'], 'DZ')

    def test_filtre_bonne_affaire(self):
        self.annonce.est_bonne_affaire = True
        self.annonce.save()
        resp = self.client.get('/api/annonces/?est_bonne_affaire=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for a in resp.data['results']:
            self.assertTrue(a['est_bonne_affaire'])

    def test_filtre_prix_max(self):
        resp = self.client.get('/api/annonces/?prix_max=10000')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_action_bonnes_affaires(self):
        resp = self.client.get('/api/annonces/bonnes_affaires/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_access_sans_auth(self):
        client_anon = APIClient()
        resp = client_anon.get('/api/annonces/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
