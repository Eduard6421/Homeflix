import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

CONTENT_TYPE = (
    ('movie', "MOVIE"),
    ('show', "SHOW")
)


class Movie(models.Model):

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True)
    title = models.CharField(_('title'), max_length=30, blank=False,
                             null=False, validators=[MinLengthValidator(1)])
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_movies',
                                   related_query_name='created_by',
                                   blank=False, null=False)
    content_type = models.CharField(
        max_length=5, choices=CONTENT_TYPE,
        default='movie', blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class Tag(models.Model):

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True)
    name = models.CharField(_('tag name'), blank=False,
                            null=False, max_length=255)
    movies = models.ManyToManyField(
        Movie, related_name='tags', related_query_name='movie')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_tags',
                                   related_query_name='created_by',
                                   blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class Genre(models.Model):

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True)
    name = models.CharField(_('genre name'), blank=False,
                            null=False, max_length=255)
    movies = models.ManyToManyField(
        Movie, related_name='genres', related_query_name='movie')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_genres',
                                   related_query_name='created_by',
                                   blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class Listing(models.Model):

    class Meta:
        verbose_name = 'listing'
        verbose_name_plural = 'listings'

    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True)

    stream_url = models.URLField(_('stream url'), blank=False, null=False)
    season_number = models.PositiveSmallIntegerField(
        _('season number'), null=False, blank=False, default=0)
    episode_number = models.PositiveSmallIntegerField(
        _('episode number'), null=False, blank=False)
    content_description = models.TextField(
        _('content description'), null=False, blank=False, max_length=10000)

    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='listings',
        null=False, blank=False,)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_listings',
                                   related_query_name='created_by',
                                   blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
