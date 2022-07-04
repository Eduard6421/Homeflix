import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator


class Movie(models.Model):

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True)
    title = models.CharField(_('title'), max_length=30, blank=False,
                             null=False, validators=[MinLengthValidator(1)])
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_by',
                                   blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
