import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from pyrsistent import optional


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        validate_password(password=password)
        user.set_password(password)
        user.full_clean()
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email,
                                 password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser',  True)
        return self._create_user(email=email,
                                 password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(_('username'), max_length=50, unique=True,
    #                            validators=[
    #    MinLengthValidator(3), MaxLengthValidator(50)])
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(_('password'), max_length=128)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_superuser = models.BooleanField(_('is admin'), default=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self,):
        return self.email

    def get_short_name(self, ):
        return self.email


# class UserProfile(models.Model):
#    user = models.OneToOneField(get_user_model())
