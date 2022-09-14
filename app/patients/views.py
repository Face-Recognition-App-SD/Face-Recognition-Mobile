"""
Views for the patients APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Patients,
    Tag,
    Treatment,
)
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
        elif self.action == 'upload_image':
            return serializers.PatientsImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new patients."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to patients."""
        patients = self.get_object()
        serializer = self.get_serializer(patients, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Base view set for Patiens atributes"""


class BasePatientsAttrViewSet(mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BasePatientsAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class TreatmentViewSet(BasePatientsAttrViewSet):

    """Manage treatment in the database."""
    serializer_class = serializers.TreatmentSerializer
    queryset = Treatment.objects.all()
