from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404
from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..customPermissions import LinguistPermission, ReadOnly
from ..models import Word
from ..serializers import WordSerializer
from ..utils import getDimOptions


class WordList(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [ IsAdminUser|LinguistPermission|ReadOnly ]
    search_fields = ['^name']

class WordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [ IsAdminUser|LinguistPermission|ReadOnly ]
    lookup_field = 'name'

    def get_object(self):
        queryset = self.get_queryset()
        filter = {self.lookup_field: self.kwargs[self.lookup_field]}
        objs = get_list_or_404(queryset, **filter)
        return objs[0]

    def retrieve(self, request, name):
        word = self.get_object()
        serializer = self.get_serializer(word)
        options = getDimOptions(serializer.data['tagset'])
        serializer_data = serializer.data
        serializer_data['dimensions'] = options
        return Response(serializer_data,
                        headers={"Access-Control-Allow-Origin": "*"})
        
    def update(self, request, name):
        word = self.get_object()
        serializer = self.get_serializer(word, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, 
                        headers={"Access-Control-Allow-Origin": "*"})
