from django.test import TestCase
from django.contrib.auth import get_user_model

from movie.models import Movie, Genre


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


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
