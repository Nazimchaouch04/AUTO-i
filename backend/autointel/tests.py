from django.test import TestCase


class CoreApiTest(TestCase):
    def test_api_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'AutoIntel API')
        self.assertIn('/api/health/', response.json().get('endpoints', []))

    def test_api_health(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn(payload.get('status'), ['ok', 'degraded', 'healthy'])
        self.assertIn('db', payload)

