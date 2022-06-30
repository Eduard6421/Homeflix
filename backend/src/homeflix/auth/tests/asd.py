"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

    path('register/', RegisterView.as_view(), name='knox_register'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),
]


REGISTER_URL = reverse('user:knox_register')
LOGIN_URL = reverse('user:knox_login')
LOGOUT_URL = reverse('user:knox_logout')
LOGOUTALL_URL = reverse('user:knox_logoutall')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicAuthApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    ''''''

    def test_create_user_succes(self):
        """Test creating a user succesful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_fail(self):
        """Test creating a user that already uses the email"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123123',
            'name': 'Test Name'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creatign a user with a password too short"""

        payload = {
            'email': 'newtestclient@example.com',
            'password': '123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""

        user_details = {
            'name': 'User name',
            'email': 'test@example.com',
            'password': 'test-user-password123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user_with_bad_password(self):
        '''Test which checks that no token is returned if password is bad'''

        create_user(email='asd@example.com', password='password123456789')

        payload = {'email': 'asd@example.com', 'password': 'badpassword'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        '''Test where we check if a token is returned if passw'''

        payload = {'email': 'asd@example.com', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_revoke_token_unauthorized(self):

        payload = {
            'token': 'randomstring',
        }

        res = self.client.delete(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(email='newtest@example.com',
                                password='testpass123', name='Test Client')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''Test retrieve profile for logged in user.'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test POST """
        res = self.client.post(ME_URL, {})

        self.assertEqual(
            res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):

        payload = {'name': 'updated_name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

    '''
    def test_revoked_token_deleted(self):
        # Test which checks if the auth token is deleted when doing logout
        res = self.client.delete(TOKEN_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unexistent_token(self):
        """Test when logging out with unexistent user"""
        payload = {
            'token': 'randomstring',
        }

        res = self.client.delete(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    '''
