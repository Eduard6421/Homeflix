"""
Tests for the auth API
"""
''''''
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import UserProfile
PROFILE_URL = reverse('user:profile-list')


def profile_url(profile_id):
    '''Create and return a profie URL'''
    return reverse('user:profile-detail', args=[profile_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the porfile API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_profile_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            PROFILE_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            profile_url('random')
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_profile_denied(self):
        '''Unauthorized post profile'''

        payload = {'name': 'profile-name'}

        res = self.client.post(
            profile_url('asd'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_denied(self):
        '''Unauthorized put/patch profile'''

        payload = {'name': 'profile-name'}

        res = self.client.patch(
            profile_url('asd'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(
            profile_url('asd'),
            payload

        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_profile_denied(self):
        '''Unauthorized put/patch profile'''

        res = self.client.delete(
            profile_url('asd'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the public features of the auth API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='SRONGPAS$$word')
        self.client.force_authenticate(self.user)

    def test_list_profiles(self):
        '''Test user can list profiles'''

        UserProfile.objects.create(user=self.user, name='default')
        UserProfile.objects.create(user=self.user, name='default2')
        UserProfile.objects.create(user=self.user, name='default3')

        res = self.client.get(
            PROFILE_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_do_not_list_other_profiles(self):
        '''Test listed profiles do not include other user profiles'''

        second_user = create_user(email='randomemail@example.com',
                                  password='randompassword')

        UserProfile.objects.create(user=self.user, name='default')
        UserProfile.objects.create(user=self.user, name='default2')
        UserProfile.objects.create(user=second_user, name='default3')

        res = self.client.get(
            PROFILE_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_profile(self):
        '''Test to get an individual profile'''

        profile = UserProfile.objects.create(user=self.user, name='default')

        res = self.client.get(
            profile_url(profile.id)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], profile.name)

    def test_unauthorized_get_profile(self):
        '''Test to not get acces to an individual profile'''

        profile = UserProfile.objects.create(user=self.user, name='default')

        res = self.client.get(
            profile_url(profile.id)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], profile.name)

    def test_create_profile(self):
        '''Test user can succesfully create a profile'''
        payload = {
            'name': 'default'
        }

        res = self.client.post(PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_profile_name_too_short(self):
        '''Test user can succesfully create a profile'''
        payload = {
            'name': ''
        }

        res = self.client.post(PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile(self):
        '''Test user can succesfully update his profile'''

        payload = {
            'name': 'updated'
        }

        profile = UserProfile.objects.create(user=self.user, name='default')
        res = self.client.patch(profile_url(profile.id), payload)
        profile.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.name, payload['name'])

    def test_delete_profile(self):
        '''Test user can succesfuly delete his profile'''
        profile = UserProfile.objects.create(user=self.user, name='default')
        res = self.client.delete(profile_url(profile.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 0)
