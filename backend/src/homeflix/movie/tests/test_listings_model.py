from django.test import TestCase
from django.contrib.auth import get_user_model

from movie.models import Movie, Listing


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


class ListingModelTests(TestCase):

    def test_create_genre(self):

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_superuser(email=email, password=password)

        movie = Movie.objects.create(
            title='A Jolly good show',
            created_by=user,
        )

        listing = Listing.objects.create(
            stream_url="https://example.com/",
            season_number=0,
            episode_number=1,
            content_description='The first episode of the movie',
            created_by=user,
            movie=movie
        )

        self.assertEqual(listing.stream_url, "https://example.com/")
        self.assertEqual(listing.season_number, 0)
        self.assertEqual(listing.episode_number, 1)
        self.assertEqual(listing.content_description,
                         'The first episode of the movie')
        self.assertEqual(listing.created_by, user)
        self.assertEqual(listing.movie, movie)
