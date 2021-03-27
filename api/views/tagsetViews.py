from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import TagSet
from ..serializers import TagSetSerializer


class TagSetList(generics.ListCreateAPIView):
    queryset = TagSet.objects.all()
    serializer_class = TagSetSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'features']

class TagSetDetail(generics.RetrieveUpdateAPIView):
    queryset = TagSet.objects.all()
    serializer_class = TagSetSerializer
    lookup_field = 'name'
