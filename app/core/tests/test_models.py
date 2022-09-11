"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_patients(self):
        """Test creating a patients is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        patients = models.Patients.objects.create(
            user=user,
            first_name='Sample patients name',
            last_name='Sample patients last name',
            age=5,
            med_list='samole med list',
            phone_number='+12345678',
            date_of_birth='2006-08-21',
            street_address="sample address",
            city_address="sample city",
            zipcode_address="sample zip",
            state_address="sample state",
            creation_date='2006-08-21',
            modified_date='2006-08-22',
            description='Sample receipe description.',
            gender='Male',
            emergency_contact_name='Sample contact name',
            emergency_phone_number='+12345678',
            relationship='Father',
            is_in_hospital=True,


        )

        self.assertEqual(str(patients), patients.first_name)
