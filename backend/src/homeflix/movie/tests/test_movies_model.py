"""
Tests for the profile model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from movie.models import Movie


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class MovieModelTests(TestCase):
    '''Test suite for the user models'''

    def test_create_movie(self):

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_superuser(email=email, password=password)

        movie = Movie.objects.create(
            title='A Jolly good show',
            created_by=user,
            # type='movie',
            # genre='Animation',
            #director='director name',
            # cast='manyactors',
        )

        self.assertEqual(movie.title, 'A Jolly good show')
        self.assertEqual(movie.created_by, user)
