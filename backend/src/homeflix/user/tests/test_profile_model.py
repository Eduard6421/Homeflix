"""
Tests for the profile model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from user.models import UserProfile


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class UserProfileTests(TestCase):
    '''Test suite for the user models'''

    def test_create_profile_with_name(self):
        "Tests if creating a user with an email is succesful"

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_user(email=email, password=password)

        name = 'RandomProfileName'
        profile = UserProfile.objects.create(user=user, name=name)

        self.assertEqual(profile.name, name)
        self.assertEqual(profile.user, user)
