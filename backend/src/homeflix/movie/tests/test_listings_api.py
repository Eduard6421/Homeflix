
from urllib.parse import urlencode
from venv import create
from django.test import TestCase
from django.urls import reverse
from movie.models import Movie, Genre
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

MOVIE_URL = reverse('movie:movies-list')
LISTING_URL = reverse('movie:listing-list')


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_listing(created_by, movie,
                   stream_url="https://example.com/",
                   season_number=0,
                   episode_number=1,
                   content_description='The first episode of the movie'):
    listing = Listing.objects.create(
        stream_url=stream_url,
        season_number=season_number,
        episode_number=episode_number,
        content_description=content_description,
        created_by=created_by,
        movie=movie
    )
    return listing


def listing_detail(listing_id):
    return reverse('movie:listing-detail', args=[listing_id])


class PublicGenreApiTests(TestCase):
    """Test the public features of the porfile API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_listing_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            LISTING_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_listing_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            listing_detail('random_listing'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_listing_denied(self):
        '''Unauthorized get profile'''

        payload = {
            'name': 'random listing'
        }

        res = self.client.post(
            LISTING_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_listing_denied(self):

        payload = {
            'name': 'random listing'
        }

        res = self.client.patch(
            listing_detail('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(
            listing_detail('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_listing_denied(self):

        res = self.client.delete(
            listing_detail('random'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='A new movie',
            superuser=superuser
        )

        create_listing(created_by=superuser, movie=movie)

        res = self.client.get(LISTING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_get_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='A new movie',
            superuser=superuser
        )

        create_listing(created_by=superuser, movie=movie)

        res = self.client.get(LISTING_URL)

        res = self.client.get(listing_detail(movie.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Comedy')

    def test_update_unauthorized_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='A new movie',
            superuser=superuser
        )

        listing = create_listing(created_by=superuser, movie=movie)

        payload = {
            'episode_number': 2
        }

        res = self.client.put(listing_detail(listing.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(listing_detail(genre.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_unauthorized_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(genre_url(genre.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_movies_with_genre(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        genre = Genre.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        movie.genres.add(genre)

        res = self.client.get(MOVIE_URL, {
            'QUERY_STRING': urlencode({'genres': genre.id})})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], movie.title)
        self.assertEqual(len(res.data[0]['genres']), 1)
        self.assertEqual(res.data[0]['genres'][0]['name'], genre.name)

    def test_add_genre_to_movie_unauthorized(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        genre = Genre.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        payload = {
            'genres': [genre.id]
        }

        res = self.client.patch(listing_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
