"""
Tests for the auth API
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from knox.models import AuthToken


REGISTER_URL = reverse('auth:knox_register')
LOGIN_URL = reverse('auth:knox_login')
LOGOUT_URL = reverse('auth:knox_logout')
LOGOUTALL_URL = reverse('auth:knox_logoutall')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the auth API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_succes(self):
        """Test creating a user succesful."""

        email = 'test@example.com123'
        password = 'testpass123123'

        payload = {
            'email': email,
            'password': password,
        }

        res = self.client.post(REGISTER_URL, payload)

        # Check in database
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

        # Check the response
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', res.data)
        self.assertIn('id', res.data['user'])
        self.assertIn('email', res.data['user'])
        self.assertEqual(res.data['user']['email'], email)
        self.assertIn('token', res.data)
        self.assertNotIn('password', res.data)

    def test_login_user_succesfully(self):
        """Test user login succesful."""

        email = 'test@example.com123'
        password = 'testpass123123'

        payload = {
            'email': email,
            'password': password,
        }

        create_user(email=email, password=password)

        res = self.client.post(LOGIN_URL, payload)

        # Check the response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('user', res.data)
        self.assertIn('id', res.data['user'])
        self.assertIn('email', res.data['user'])
        self.assertEqual(res.data['user']['email'], email)
        self.assertIn('token', res.data)
        self.assertNotIn('password', res.data)

        self.assertTrue(True)

    def test_logout_user_denied(self):
        """Test unauthenticated user logout """

        email = 'test@example.com123'
        password = 'testpass123123'

        payload = {
            'email': email,
            'password': password,
        }

        res = self.client.post(LOGOUT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logoutall_user_denied(self):
        """Test unauthenticated user logoutAll"""

        email = 'test@example.com123'
        password = 'testpass123123'

        payload = {
            'email': email,
            'password': password,
        }

        res = self.client.post(LOGOUTALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the public features of the auth API."""

    def setUp(self):
        self.client = APIClient()

    def test_logout_user(self):
        """Test user logout """

        # Create a user to authenticate

        email = 'test@example.com123'
        password = 'testpass123123'

        user = create_user(email=email, password=password)

        (_instance, token) = AuthToken.objects.create(user)

        res = self.client.post(
            LOGOUT_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(AuthToken.objects.filter(user=user).count(), 0)

    def test_logout_user_only_one_token_revoked(self):
        """Test user logout revokes only one token"""

        # Create a user to authenticate

        email = 'test@example.com123'
        password = 'testpass123123'

        user = create_user(email=email, password=password)

        (_instance, token) = AuthToken.objects.create(user)
        (_instance, token) = AuthToken.objects.create(user)
        (_instance, token) = AuthToken.objects.create(user)

        res = self.client.post(
            LOGOUT_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(AuthToken.objects.filter(user=user).count(), 2)

    def test_logout_all_user(self):
        """Test user logout all"""

        # Create a user to authenticate

        email = 'test@example.com123'
        password = 'testpass123123'

        user = create_user(email=email, password=password)

        (_instance, token) = AuthToken.objects.create(user)
        (_instance, token) = AuthToken.objects.create(user)
        (_instance, token) = AuthToken.objects.create(user)

        res = self.client.post(
            LOGOUTALL_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(AuthToken.objects.filter(user=user).count(), 0)
