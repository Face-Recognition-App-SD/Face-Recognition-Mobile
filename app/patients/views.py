"""
Views for the patients APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Patients
from patients import serializers


class PatientsViewSet(viewsets.ModelViewSet):
    """View for manage patients APIs."""
    serializer_class = serializers.PatientsDetailSerializer
    queryset = Patients.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipatientspes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PatientsSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new patients."""
        serializer.save(user=self.request.user)
