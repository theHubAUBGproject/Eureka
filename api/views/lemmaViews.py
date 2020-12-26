from django.http import Http404
from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models import Language, Lemma, Word
from ..serializers import (LangLemmaSerializer, LemmaSerializer,
                           RelatedWordSerializer)

from rest_framework.permissions import IsAdminUser

from ..customPermissions import LinguistPermission, ReadOnly

paginator = PageNumberPagination()

'''
Endpoint for lemmas in particular language
'''
class LemmaList(generics.ListCreateAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LangLemmaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['language', 'animacy', 'transivity', 'author', 'pos', 'date_updated']
    
    permission_classes = [ IsAdminUser|LinguistPermission|ReadOnly ]

    search_fields = ['^name']
    paginator.page_size = 72

    def list(self, request, lang, **kwargs):
        language = Language.objects.get(walsCode=lang)
        queryset = Lemma.objects.filter(language=language.id).filter(name__contains=self.request.GET.get("search", ""))
        serializer_class = self.get_serializer_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        
    def options(self, request, lang):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})

'''
Endpoint for all lemmas regardless of language
'''
class AllLemmasList(generics.ListAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LangLemmaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['^name']

    def options(self, request):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


'''
Endpoint for a single lemma
'''
class LemmaDetail(generics.RetrieveUpdateAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LemmaSerializer
    lookup_field = 'name'

    def get_related_words(self, pk):
        try:
            related_words = Word.objects.filter(lemma=pk)
            return related_words
        except Word.DoesNotExist:
            return Http404

    def get_object(self, name):
        queryset = self.get_queryset()
        filter = {'name': name}
        objs = get_list_or_404(queryset, **filter)
        return objs[0]

    def retrieve(self, request, lang, name, format=None):
        lemma = self.get_object(name)
        serializer = LemmaSerializer(lemma)
        related_words = self.get_related_words(lemma.id)
        words = RelatedWordSerializer(related_words, many=True)
        lemma_data = serializer.data
        words_data = words.data
        lemma_data['related_words'] = words_data
        return Response(lemma_data,
                        headers={"Access-Control-Allow-Origin": "*"},
                        status=status.HTTP_200_OK)

    def options(self, request, lang, name):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})
