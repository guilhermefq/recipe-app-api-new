"""
Test form models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user_test@gmail.com', password='passwordtest'):
    """Create a user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_create_tag(self):
        """
        Test creating a new tag.
        """
        tag = models.Tag.objects.create(
            user=create_user(),
            name='Test tag',
        )

        self.assertEqual(tag.name, str(tag))
        self.assertEqual(tag.name, 'Test tag')

    def test_create_ingredient(self):
        """Test creating an ingredient is successful"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
