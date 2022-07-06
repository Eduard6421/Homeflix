from django.test import TestCase
from django.contrib.auth import get_user_model

from movie.models import Movie, Tag


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


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
