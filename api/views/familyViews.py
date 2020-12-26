from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser

from ..customPermissions import LinguistPermission, ReadOnly
from ..models import Family
from ..serializers import FamilySerializer

class FamilyList(generics.ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [ IsAdminUser|LinguistPermission|ReadOnly ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
