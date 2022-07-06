"""
Tests for the profile model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from movie.models import Movie, Tag, Genre, Listing


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_movie(**params):
    return Movie.objects.create(**params)


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


class TagModelTests(TestCase):

    def test_create_tag(self):

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_superuser(email=email, password=password)

        tag = Tag.objects.create(
            name='#Winner',
            created_by=user,
        )

        self.assertEqual(tag.name, '#Winner')
        self.assertEqual(tag.created_by, user)

        movie = Movie.objects.create(
            title='A Jolly good show',
            created_by=user,
        )

        movie.tags.add(tag)
        movie.save()
        movie.refresh_from_db()

        self.assertEqual(movie.tags.count(), 1)
        self.assertEqual(movie.tags.all()[0].name, '#Winner')


class GenreModelTests(TestCase):

    def test_create_genre(self):

        email = 'user@example.com'
        password = 'my5trongrand0mp4ss'

        user = create_superuser(email=email, password=password)

        genre = Genre.objects.create(
            name='#Winner',
            created_by=user,
        )

        self.assertEqual(genre.name, '#Winner')
        self.assertEqual(genre.created_by, user)

        movie = Movie.objects.create(
            title='A Jolly good show',
            created_by=user,
        )

        movie.genres.add(genre)
        movie.save()
        movie.refresh_from_db()

        self.assertEqual(movie.genres.count(), 1)
        self.assertEqual(movie.genres.all()[0].name, '#Winner')


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
