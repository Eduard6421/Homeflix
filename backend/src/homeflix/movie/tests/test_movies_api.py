"""
Tests for the Movies API
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from movie.models import Movie
from rest_framework.test import APIClient
from rest_framework import status


MOVIE_URL = reverse('movie:movies-list')


def movie_detail(movie_id):
    '''Create and return a profie URL'''
    return reverse('movie:movies-detail', args=[movie_id])


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicMovieApiTests(TestCase):
    """Test the public features of the porfile API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_movie_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            MOVIE_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_movie_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            movie_detail('random_movie'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_movie_denied(self):
        '''Unauthorized get profile'''

        payload = {
            'title': 'random movie'
        }

        res = self.client.post(
            MOVIE_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_movie_denied(self):

        payload = {
            'title': 'random movie'
        }

        res = self.client.patch(
            movie_detail('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(
            movie_detail('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_movie_denied(self):

        res = self.client.delete(
            movie_detail('random'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        Movie.objects.create(
            title='Jolly good show 2',
            created_by=superuser
        )

        res = self.client.get(MOVIE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_post_movie(self):

        payload = {
            'title': 'randommovietitle'
        }

        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        res = self.client.get(movie_detail(movie.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Jolly good show')

    def test_update_unauthorized_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        payload = {
            'title': 'newtitle'
        }

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_unauthorized_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(movie_detail(movie.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAdminMovieApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(email='user@example.com',
                                     password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        Movie.objects.create(
            title='Jolly good show 2',
            created_by=superuser
        )

        res = self.client.get(MOVIE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        res = self.client.get(movie_detail(movie.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Jolly good show')

    def test_post_movie(self):

        payload = {
            'title': 'randommovietitle'
        }

        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])

    def test_update_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        payload = {
            'title': 'newtitle'
        }

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])

        payload = {
            'title': 'updatedsecond'
        }

        res = self.client.put(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])

    def test_delete_unauthorized_movie(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        movie = Movie.objects.create(
            title='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(movie_detail(movie.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.filter(id=movie.id).count(), 0)
