"""
Serializers for patients APIs
"""
from rest_framework import serializers

from core.models import Patients


class PatientsSerializer(serializers.ModelSerializer):
    """Serializer for patients."""

    class Meta:
        model = Patients
        # fields = ['id', 'first_name', 'last_name', 'age', 'link']
        fields = ['id',
                  'first_name',
                  'last_name',
                  'age',
                  'med_list',
                  'phone_number',
                  'date_of_birth',
                  'street_address',
                  'city_address',
                  'zipcode_address',
                  'state_address',
                  'link',
                  'creation_date',
                  'modified_date',
                  'emergency_contact_name',
                  'emergency_phone_number',
                  'relationship',
                  'gender',
                  'is_in_hospital',

                  ]

        read_only_fields = ['id']


class PatientsDetailSerializer(PatientsSerializer):
    """Serializer for Patients detail view."""

    class Meta(PatientsSerializer.Meta):
        fields = PatientsSerializer.Meta.fields + ['description']
