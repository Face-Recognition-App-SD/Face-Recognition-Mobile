"""
Views for the patients APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'treatments',
                OpenApiTypes.STR,
                description='Comma separated list of treatment IDs to filter',
            ),
        ]
    )
)
class PatientsViewSet(viewsets.ModelViewSet):
    """View for manage patients APIs."""
    serializer_class = serializers.PatientsDetailSerializer
    queryset = Patients.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipatientspes for authenticated user."""
        tags = self.request.query_params.get('tags')
        treatment = self.request.query_params.get('treatment')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if treatment:
            treatmen_ids = self._params_to_ints(treatment)
            queryset = queryset.filter(treatment__id__in=treatmen_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

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
