"""
Tests for the Tags API
"""

from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from movie.tests.test_movies_api import movie_detail
from movie.models import Movie, Tag
from rest_framework.test import APIClient
from rest_framework import status

MOVIE_URL = reverse('movie:movies-list')
TAG_URL = reverse('movie:tags-list')


def movie_detail(movie_id):
    '''Create and return a profie URL'''
    return reverse('movie:movies-detail', args=[movie_id])


def tag_url(tag_id):
    '''Create and return a tag url'''
    return reverse('movie:tags-detail', args=[tag_id])


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicTagApiTests(TestCase):
    """Test the public features of the porfile API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_tag_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            TAG_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tag_denied(self):
        '''Unauthorized get profile'''

        res = self.client.get(
            tag_url('random_tag'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_tag_denied(self):
        '''Unauthorized get profile'''

        payload = {
            'name': 'random tag'
        }

        res = self.client.post(
            TAG_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_tag_denied(self):

        payload = {
            'name': 'random tag'
        }

        res = self.client.patch(
            tag_url('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.put(
            tag_url('random'),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tag_denied(self):

        res = self.client.delete(
            tag_url('random'),
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_movies_with_tag_unauthenticated(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        movie.tags.add(tag)

        res = self.client.get(MOVIE_URL, {
            'QUERY_STRING': urlencode({'tags': tag.id})})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_tag_to_movie_unautenticated(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        payload = {
            'tags': [tag.id]
        }

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        Tag.objects.create(
            name='Thriller',
            created_by=superuser
        )

        Tag.objects.create(
            name='Comedy',
            created_by=superuser
        )

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Comedy',
            created_by=superuser
        )

        res = self.client.get(tag_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Comedy')

    def test_update_unauthorized_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        payload = {
            'name': 'newtitle'
        }

        res = self.client.patch(tag_url(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(tag_url(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_unauthorized_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(tag_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_movies_with_tag_unauthenticated(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        movie.tags.add(tag)

        res = self.client.get(MOVIE_URL, {
            'QUERY_STRING': urlencode({'tags': tag.id})})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], movie.title)
        self.assertEqual(len(res.data[0]['tags']), 1)
        self.assertEqual(res.data[0]['tags'][0]['name'], tag.name)

    def test_add_tag_to_movie_unautenticated(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        payload = {
            'tags': [tag.id]
        }

        res = self.client.patch(movie_detail(movie.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAdminTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(email='user@example.com',
                                     password='passwordrandopm12312')
        self.client.force_authenticate(self.user)

    def test_list_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        Tag.objects.create(
            name='Comedy',
            created_by=superuser
        )

        Tag.objects.create(
            name='Drama',
            created_by=superuser
        )

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.get(tag_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Jolly good show')

    def test_update_authorized_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Jolly good tag',
            created_by=superuser
        )

        payload = {
            'name': 'newtitle'
        }

        res = self.client.patch(tag_url(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

        payload = {
            'name': 'updatedsecond'
        }

        res = self.client.put(tag_url(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

    def test_delete_authorized_tag(self):

        superuser = create_superuser(
            email='admin@admin.com', password='adminpass2')

        tag = Tag.objects.create(
            name='Jolly good show',
            created_by=superuser
        )

        res = self.client.delete(tag_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.filter(id=tag.id).count(), 0)

    def test_get_movies_with_tag(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        movie.tags.add(tag)

        res = self.client.get(MOVIE_URL, {
            'QUERY_STRING': urlencode({'tags': tag.id})})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], movie.title)
        self.assertEqual(len(res.data[0]['tags']), 1)
        self.assertEqual(res.data[0]['tags'][0]['name'], tag.name)

    def test_add_tag_to_movie(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        payload = {
            'title': 'random_movie',
            'tags': [{'id': str(tag.id), 'name': 'Cute'}]
        }

        res = self.client.put(movie_detail(movie.id), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data['tags']), 1)
        self.assertEqual(res.data['tags'][0]['name'], tag.name)

    def test_add_tag_to_movie_partial(self):

        super_user = create_superuser(
            email='asd@example.com', password='1231h541hb')

        tag = Tag.objects.create(
            name='Cute',
            created_by=super_user
        )

        movie = Movie.objects.create(
            title='random_movie',
            created_by=super_user,
        )

        payload = {
            'tags': [{'id': str(tag.id), 'name': 'Cute'}]
        }

        res = self.client.patch(movie_detail(movie.id), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data['tags']), 1)
        self.assertEqual(res.data['tags'][0]['name'], tag.name)
