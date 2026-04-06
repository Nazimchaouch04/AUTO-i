from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ProfilJoueur, Defi, DefiJoueur
from apps.subscriptions.models import Plan

class GamificationTest(TestCase):

    def setUp(self):
        # Créer le plan gratuit pour éviter que le signal de souscription échoue
        Plan.objects.get_or_create(nom='free', defaults={'prix_mensuel': 0, 'estimations_par_mois': 10})
        self.user = User.objects.create_user('player', 'p@p.com', 'pass1234')
        # Le profil est créé par signal, on le récupère
        self.profil = self.user.profil
        self.profil.autocoin_balance = 100
        self.profil.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_add_coins(self):
        solde_initial = self.profil.autocoin_balance
        self.profil.add_coins(50)
        self.profil.refresh_from_db()
        self.assertEqual(self.profil.autocoin_balance, solde_initial + 50)

    def test_add_xp_sans_level_up(self):
        self.profil.add_xp(100)
        self.profil.refresh_from_db()
        self.assertEqual(self.profil.xp, 100)
        self.assertEqual(self.profil.niveau, 1)

    def test_level_up_niveau_2(self):
        self.profil.add_xp(600)
        self.profil.refresh_from_db()
        self.assertEqual(self.profil.niveau, 2)

    def test_level_up_multiple(self):
        self.profil.add_xp(5100)
        self.profil.refresh_from_db()
        self.assertGreaterEqual(self.profil.niveau, 4)

    def test_progression_pct(self):
        self.profil.xp = 250
        self.profil.niveau = 1
        self.profil.save()
        pct = self.profil.progression_pct()
        self.assertEqual(pct, 50)

    def test_get_profil_api(self):
        resp = self.client.get('/api/gamification/profil/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('xp', resp.data)
        self.assertIn('niveau', resp.data)
        self.assertIn('autocoin_balance', resp.data)

    def test_leaderboard_api(self):
        resp = self.client.get('/api/gamification/leaderboard/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
