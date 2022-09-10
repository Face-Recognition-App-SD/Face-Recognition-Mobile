"""
Views for the patient APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Patient
from patient import serializers


class PatientViewSet(viewsets.ModelViewSet):
    """View for manage patient APIs."""
    serializer_class = serializers.PatientDetailSerializer
    queryset = Patient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#  limiting the query of patint to only autheticated users

    def get_queryset(self):
        """Retrieve patients for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PatientSerializer

        return self.serializer_class
