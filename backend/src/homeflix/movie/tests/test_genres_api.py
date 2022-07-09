"""
Tests for the Genres API
"""

from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from movie.tests.test_movies_api import movie_detail
from movie.models import Movie, Genre
from rest_framework.test import APIClient
from rest_framework import status

GENRE_URL = reverse('movie:genres-list')
MOVIE_URL = reverse('movie:movies-list')


def genre_url(genre_id):
    '''Create and return a genre url'''
    return reverse('movie:genres-detail', args=[genre_id])


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicGenreApiTests(TestCase):
    """Test the public features of the porfile API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_genre_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            GENRE_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_genre_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            genre_url('random_genre'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_genre_denied(self):
        '''Unauthorized get profile'''

        payload = {
            'name': 'random genre'
        }

        res = self.client.post(
            GENRE_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_genre_denied(self):

        payload = {
            'name': 'random genre'
        }

        res = self.client.patch(
            genre_url('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(
            genre_url('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_genre_denied(self):

        res = self.client.delete(
            genre_url('random'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_movies_with_genre_unauthorized(self):

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

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

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

        res = self.client.patch(genre_url(movie.id), payload)

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

        Genre.objects.create(
            name='Thriller',
            created_by=superuser
        )

        Genre.objects.create(
            name='Comedy',
            created_by=superuser
        )

        res = self.client.get(GENRE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Comedy',
            created_by=superuser
        )

        res = self.client.get(genre_url(genre.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Comedy')

    def test_update_unauthorized_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        payload = {
            'name': 'newtitle'
        }

        res = self.client.patch(genre_url(genre.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(genre_url(genre.id), payload)

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

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAdminGenreApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(email='user@example.com',
                                     password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        Genre.objects.create(
            name='Comedy',
            created_by=superuser
        )

        Genre.objects.create(
            name='Drama',
            created_by=superuser
        )

        res = self.client.get(GENRE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.get(genre_url(genre.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Jolly good show')

    def test_update_authorized_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        payload = {
            'name': 'newtitle'
        }

        res = self.client.patch(genre_url(genre.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

        payload = {
            'name': 'updatedsecond'
        }

        res = self.client.put(genre_url(genre.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

    def test_delete_authorized_genre(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        genre = Genre.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(genre_url(genre.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.filter(id=genre.id).count(), 0)

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

    def test_add_genre_to_movie(self):

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
            'title': 'random_movie',
            'genres': [{'id': str(genre.id), 'name': 'Cute'}]
        }

        res = self.client.put(movie_detail(movie.id), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['genres']), 1)
        self.assertEqual(res.data['genres'][0]['name'], genre.name)

    def test_add_genre_to_movie_partial(self):

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
            'genres': [{'id': str(genre.id), 'name': 'Cute'}]
        }

        res = self.client.patch(movie_detail(movie.id), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['genres']), 1)
        self.assertEqual(res.data['genres'][0]['name'], genre.name)
