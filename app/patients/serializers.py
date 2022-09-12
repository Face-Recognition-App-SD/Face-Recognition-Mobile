"""
Serializers for patients APIs
"""
from rest_framework import serializers

from core.models import (
    Patients,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PatientsSerializer(serializers.ModelSerializer):
    """Serializer for patients."""

    tags = TagSerializer(many=True, required=False)

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
                  'tags',

                  ]

        read_only_fields = ['id']


class PatientsDetailSerializer(PatientsSerializer):
    """Serializer for Patients detail view."""

    class Meta(PatientsSerializer.Meta):
        fields = PatientsSerializer.Meta.fields + ['description']

    def _get_or_create_tags(self, tags, patients):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            patients.tags.add(tag_obj)

    # def create(self, validated_data):
    #     """Create a patients."""
    #     tags = validated_data.pop('tags', [])
    #     patients = Patients.objects.create(**validated_data)
    #     auth_user = self.context['request'].user
    #     for tag in tags:
    #         tag_obj, created = Tag.objects.get_or_create(
    #             user=auth_user,
    #             **tag,
    #         )
    #         patients.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a patients."""
        tags = validated_data.pop('tags', [])
        patients = Patients.objects.create(**validated_data)
        self._get_or_create_tags(tags, patients)

        return patients

    def update(self, instance, validated_data):
        """Update patients."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
