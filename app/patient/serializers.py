"""
Serializers for patient APIs
"""
from rest_framework import serializers

from core.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for patient."""

    class Meta:
        model = Patient
        fields = ['id',
                  'patient_email',
                  'patient_first_name',
                  'patient_description',
                  'patient_med_list',
                  'patient_phone_number',
                  'patient_date_of_birth',
                  'patient_street_address',
                  'patient_city_address',
                  'patient_zipcode_address',
                  'patient_creation_date',
                  'patient_modified_date',
                  'patient_link',
                  'patient_gender',
                  'emergency_contact_email',
                  'emergency_contact_name',
                  'emergency_phone_number',
                  'relationship',
                  ]
        read_only_fields = ['id']


class PatientDetailSerializer(PatientSerializer):
    """Serializer for patient detail view."""

    class Meta(PatientSerializer.Meta):
        fields = PatientSerializer.Meta.fields + ['patient_description']
