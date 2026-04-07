from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class AuthTest(TestCase):

    def setUp(self):
        from apps.subscriptions.models import Plan
        # Créer le plan gratuit pour éviter que le signal de souscription échoue lors du test de registration
        Plan.objects.get_or_create(nom='free', defaults={'prix_mensuel': 0, 'estimations_par_mois': 10})
        self.client = APIClient()

    def test_register(self):
        resp = self.client.post('/api/auth/register/', {
            'username': 'newuser', 'email': 'new@test.com',
            'password': 'StrongPass123', 'password_confirm': 'StrongPass123'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_register_email_duplique(self):
        User.objects.create_user('existing', 'taken@test.com', 'pass')
        resp = self.client.post('/api/auth/register/', {
            'username': 'other', 'email': 'taken@test.com',
            'password': 'StrongPass123', 'password_confirm': 'StrongPass123'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        User.objects.create_user('loginuser', 'login@test.com', 'pass1234')
        resp = self.client.post('/api/auth/login/', {
            'username': 'loginuser', 'password': 'pass1234'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

    def test_login_with_email(self):
        User.objects.create_user('emailuser', 'emailuser@test.com', 'pass1234')
        resp = self.client.post('/api/auth/login/', {
            'email': 'emailuser@test.com', 'password': 'pass1234'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

    def test_login_mauvais_mdp(self):
        User.objects.create_user('failuser', 'fail@test.com', 'correctpass')
        resp = self.client.post('/api/auth/login/', {
            'username': 'failuser', 'password': 'wrongpass'
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
