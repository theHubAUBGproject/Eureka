from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status

from ..models import Genus
from ..serializers import GenusSerializer


class GenusList(generics.ListCreateAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name']