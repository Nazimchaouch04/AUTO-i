from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.subscriptions.models import Plan


class AuthTest(TestCase):
    def setUp(self):
        Plan.objects.get_or_create(
            nom='free',
            defaults={'prix_mensuel': 0, 'estimations_par_mois': 10},
        )
        self.client = APIClient()

    def test_register(self):
        resp = self.client.post(
            '/api/auth/register/',
            {
                'username': 'newuser',
                'email': 'new@test.com',
                'password': 'StrongPass123',
                'password_confirm': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        self.assertIn('profil_data', resp.data)

    def test_register_email_duplique(self):
        User.objects.create_user('existing', 'taken@test.com', 'pass')
        resp = self.client.post(
            '/api/auth/register/',
            {
                'username': 'other',
                'email': 'taken@test.com',
                'password': 'StrongPass123',
                'password_confirm': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_username_case_insensitive_unique(self):
        User.objects.create_user('JohnDoe', 'john@test.com', 'pass1234')
        resp = self.client.post(
            '/api/auth/register/',
            {
                'username': 'johndoe',
                'email': 'john2@test.com',
                'password': 'StrongPass123',
                'password_confirm': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', resp.data)

    def test_login(self):
        User.objects.create_user('loginuser', 'login@test.com', 'pass1234')
        resp = self.client.post(
            '/api/auth/login/',
            {'username': 'loginuser', 'password': 'pass1234'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

    def test_login_with_email(self):
        User.objects.create_user('emailuser', 'emailuser@test.com', 'pass1234')
        resp = self.client.post(
            '/api/auth/login/',
            {'email': 'emailuser@test.com', 'password': 'pass1234'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('user_data', resp.data)

    def test_login_mauvais_mdp(self):
        User.objects.create_user('failuser', 'fail@test.com', 'correctpass')
        resp = self.client.post(
            '/api/auth/login/',
            {'username': 'failuser', 'password': 'wrongpass'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileTest(TestCase):
    def setUp(self):
        Plan.objects.get_or_create(
            nom='free',
            defaults={'prix_mensuel': 0, 'estimations_par_mois': 10},
        )
        self.client = APIClient()

    def test_profile_endpoint_recovers_missing_user_profile(self):
        user = User.objects.create_user('profileuser', 'profile@test.com', 'pass1234')

        # Simule un profil Django manquant pour verifier la resilience.
        if hasattr(user, 'profile'):
            user.profile.delete()

        self.client.force_authenticate(user=user)
        resp = self.client.get('/api/auth/profile/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('user', resp.data)
        self.assertIn('profil', resp.data)
