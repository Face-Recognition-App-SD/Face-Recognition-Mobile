"""
Tests for patient APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Patient
from patient.serializers import (

    PatientSerializer,
    PatientDetailSerializer,
)

PATIENT_URL = reverse('patient:patient-list')


def detail_url(patient_id):
    """Create and return a patient detail URL."""
    return reverse('patient:patient-detail', args=[patient_id])


def create_patient(user, **params):
    """Create and return a sample patient."""
    defaults = {
        'patient_first_name': 'Sample patient name',
        'patient_description': 'Sample description',
        'patient_link': 'http://example.com/patient.pdf',
    }
    defaults.update(params)

    patient = Patient.objects.create(user=user, **defaults)
    return patient


class PublicPatientAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PATIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePatientApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user1@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_patients(self):

        """Test retrieving a list of patients."""
        create_patient(user=self.user)

        create_patient(user=self.user)
        res = self.client.get(PATIENT_URL)

        patients = Patient.objects.all().order_by('-id')
        serializer = PatientSerializer(patients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patient_list_limited_to_user(self):
        """Test list of patient is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_patient(user=other_user)
        create_patient(user=self.user)

        res = self.client.get(PATIENT_URL)

        patients = Patient.objects.filter(user=self.user)
        serializer = PatientSerializer(patients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_patient_detail(self):
        """Test get patient detail."""
        patient = create_patient(user=self.user)

        url = detail_url(patient.id)
        res = self.client.get(url)

        serializer = PatientDetailSerializer(patient)
        self.assertEqual(res.data, serializer.data)
