"""
Test form models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """
    Test models.
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        email = 'user_test@example.com'
        password = 'passwordtest'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new users is normalized.
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'passwordtest')

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test creating a new user without an email raises ValueError.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'passwordtest')

    def test_create_new_superuser(self):
        """
        Test creating a new superuser.
        """
        user = get_user_model().objects.create_superuser(
            'superuser_test@example.com',
            'passwordtest'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """
        Test creating a new recipe.
        """
        user = get_user_model().objects.create_user(
            'user_test@gmail.com',
            'passwordtest',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Test recipe',
            time_minutes=10,
            price=Decimal('5.55'),
            description='This is a test recipe.',
        )

        self.assertEqual(recipe.title, str(recipe))
        self.assertEqual(recipe.title, 'Test recipe')
        self.assertEqual(recipe.time_minutes, 10)
        self.assertEqual(recipe.price, Decimal('5.55'))
