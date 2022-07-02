"""
Tests for the profile model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from user.models import UserProfile


def create_super_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(is_superuser=True, **params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class MovieModelTests(TestCase):
    '''Test suite for the user models'''

    def test_create_movie(self):

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_super_user(email, password)

        movie = Movie.objects.create(
            user=user,
            title='A Jolly good show',
            # type='movie',
            # genre='Animation',
            #director='director name',
            # cast='manyactors',


        )
