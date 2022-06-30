"""
Tests for the user API
"""

from xml.dom import ValidationErr
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class UserModelTests(TestCase):
    '''Test suite for the user models'''

    def test_create_user_with_email(self):
        "Tests if creating a user with an email is succesful"
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsNotNone(user.last_login)

    def test_create_superuser(self):
        "Test creating a superuser"

        email = 'test@example.com'
        password = 'passwordisrandomandstrong'

        user = get_user_model().objects.create_superuser(
            email,
            password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsNotNone(user.last_login)

    def test_new_user_email_normalized(self):
        """Test email is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model()\
                .objects.create_user(email, 'randomstrongpassword')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Users without email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'randomstrongpassword')

    def test_new_user_without_password_raises_error(self):
        """Users without password raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('asdasd@example.com', '')

    def test_invalid_email_error(self):
        """Users with invalid email raises error"""

        with self.assertRaises(ValidationError):
            get_user_model().objects\
                .create_user('thisistheuseremail',
                             'thisisarandomvalidpassword12')

    def test_short_password_error(self):
        """Users with short password raises error"""

        with self.assertRaises(ValidationError):
            get_user_model().objects\
                .create_user('example@example.com', 'pas')

    def test_numeric_password_error(self):
        """Users wit numeric-only password raises error"""

        with self.assertRaises(ValidationError):
            get_user_model().objects\
                .create_user('example@example.com', '123456789009876544321')
