"""
Tests for the treatment API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Treatment

from patients.serializers import TreatmentSerializer


TREATMENTS_URL = reverse('patients:treatment-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTreatmentApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving treatment."""
        res = self.client.get(TREATMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTreatmentApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_treatment(self):
        """Test retrieving a list of treatment."""
        Treatment.objects.create(user=self.user, name='Kale')
        Treatment.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(TREATMENTS_URL)

        treatments = Treatment.objects.all().order_by('-name')
        serializer = TreatmentSerializer(treatments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_treatments_limited_to_user(self):
        """Test list of treatments is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Treatment.objects.create(user=user2, name='Breathing')
        treatment = Treatment.objects.create(user=self.user, name='Pepper')

        res = self.client.get(TREATMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], treatment.name)
        self.assertEqual(res.data[0]['id'], treatment.id)
