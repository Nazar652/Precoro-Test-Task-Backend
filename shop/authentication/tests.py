# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_success(self):
        url = reverse('login_view')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Login successful')

    def test_login_failure(self):
        url = reverse('login_view')
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Invalid credentials')

    def test_logout(self):
        # First login the user
        self.client.login(username='testuser', password='testpass')

        url = reverse('logout_view')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Logout successful')

    def test_check_authentication_authenticated(self):
        # First login the user
        self.client.login(username='testuser', password='testpass')

        url = reverse('check')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['isAuthenticated'])
        self.assertEqual(response.json()['username'], 'testuser')
        self.assertEqual(response.json()['id'], self.user.id)

    def test_check_authentication_unauthenticated(self):
        url = reverse('check')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['isAuthenticated'])
