"""
Tests for patients APIs.
"""
# from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Patients

from patients.serializers import (
    PatientsSerializer,
    PatientsDetailSerializer,
)

PATIENTS_URL = reverse('patients:patients-list')


def detail_url(patients_id):
    """Create and return a patients detail URL."""
    return reverse('patients:patients-detail', args=[patients_id])


def create_patients(user, **params):
    """Create and return a sample patients."""
    defaults = {

        'first_name': 'Sample patients first_name',
        'last_name': 'Sample patients last_name',
        'med_list': 'sample med list',
        'age': 22,
        'phone_number': "+12345667",
        'date_of_birth': '2006-08-21',
        'street_address':  "sample address",
        'city_address': "sample city",
        'zipcode_address': "sample zip",
        'state_address': "sample state",
        'description': 'Sample description',
        'creation_date': '2006-08-21',
        'modified_date': '2006-08-21',
        'gender': 'Male',
        'emergency_contact_name': 'Sample contact name',
        'emergency_phone_number': '+12345678',
        'relationship': 'Father',
        'is_in_hospital': True,
        'link': 'http://example.com/patients.pdf',

    }
    defaults.update(params)

    patients = Patients.objects.create(user=user, **defaults)

    return patients

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicPatientsAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PATIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePatientsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_petients(self):
        """Test retrieving a list of petients."""
        create_patients(user=self.user)

        create_patients(user=self.user)

        res = self.client.get(PATIENTS_URL)

        petients = Patients.objects.all().order_by('-id')
        serializer = PatientsSerializer(petients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patients_list_limited_to_user(self):
        """Test list of petients is limited to authenticated user."""
        other_user = create_user(email='other@example.com',
                                 password='test123')
        create_patients(user=other_user)

        create_patients(user=self.user)

        res = self.client.get(PATIENTS_URL)

        petients = Patients.objects.filter(user=self.user)
        serializer = PatientsSerializer(petients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_patients_detail(self):
        """Test get patients detail."""
        patients = create_patients(user=self.user)

        url = detail_url(patients.id)
        res = self.client.get(url)

        serializer = PatientsDetailSerializer(patients)
        self.assertEqual(res.data, serializer.data)

    def test_create_patients(self):
        """Test creating a patients."""
        payload = {

            'first_name': 'Sample patients',
            'last_name': 'Sample patients last name',
            'age': 30,

        }
        res = self.client.post(PATIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patients = Patients.objects.get(id=res.data['id'])
        for k, v in payload.items():

            self.assertEqual(getattr(patients, k), v)
        self.assertEqual(patients.user, self.user)


    def test_partial_update(self):
        """Test partial update of a patient."""
        original_link = 'https://example.com/patient.pdf'
        patient = create_patients(
            user=self.user,
            first_name='Sample patient name',
            link=original_link,
        )

        payload = {'first_name': 'New patient first name'}
        url = detail_url(patient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.first_name, payload['first_name'])
        self.assertEqual(patient.link, original_link)
        self.assertEqual(patient.user, self.user)
