from django.http import Http404, FileResponse, HttpResponse
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Feature, Language, Dimension, Word, Lemma, TagSet, Family, Genus, POS
from .serializers import (FeatureSerializer, LanguageSerializer, DimensionSerializer,
                          WordSerializer, TagSetSerializer, LemmaSerializer,
                          FamilySerializer, GenusSerializer, RelatedWordSerializer)
import csv

class APIRootList(APIView):
    def get(self, request, format=None):
        data = {
            'languages': reverse('languages', request=request),
            'words': reverse('words', request=request),
            'features': reverse('features', request=request),
            'dimensions': reverse('dimensions', request=request),
            'lemmas': reverse('lemmas', request=request),
            'tagsets': reverse('tagsets', request=request),
            'families': reverse('families', request=request),
            'genuses': reverse('genuses', request=request)
        }
        return Response(data)


class FeatureList(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'dimension']    


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'family', 'genus', 'walsCode']


class DimensionList(generics.ListCreateAPIView):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class WordList(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class LemmaList(generics.ListCreateAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LemmaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['language', 'animacy', 'transivity', 'author', 'pos', 'date_updated']
    search_fields = ['name']


class GenusList(generics.ListCreateAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class TagSetList(generics.ListCreateAPIView):
    queryset = TagSet.objects.all()
    serializer_class = TagSetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'features']


class FamilyList(generics.ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class GenusDownload(APIView):
    """ Download a .csv file with all the Genuses """
    def get(self, request, format=None):
        items = Genus.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['content-disposition'] = 'attachment; filename="genus.csv"'
        writer = csv.writer(response, delimiter=';' )
        writer.writerow(['name'])
        for obj in items:
            writer.writerow([obj.name])
        return response


class DimensionDownload(APIView):
    """ Download a .csv file with all the Dimensions """
    def get(self, request, format=None):
        items = Dimension.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['content-disposition'] = 'attachment; filename="dimensions.csv"'
        writer = csv.writer(response, delimiter=';' )
        writer.writerow(['name'])
        for obj in items:
            writer.writerow([obj.name])
        return response


class FeatureDownload(APIView):
    """ Download a .csv file with all the Features """
    def get(self, request, format=None):
        items = Feature.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['content-disposition'] = 'attachment; filename="features.csv"'
        writer = csv.writer(response, delimiter=';' )
        writer.writerow(['name','dimension'])
        for obj in items:
            writer.writerow([obj.name,obj.dimension])
        return response


class LanguageDownload(APIView):
    """ Download a .csv file with all the Languages available """
    def get(self, request, format=None):
        items = Language.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['content-disposition'] = 'attachment; filename="languages.csv"'
        writer = csv.writer(response, delimiter=';' )
        writer.writerow(['name','family','genus','walsCode'])
        for obj in items:
            writer.writerow([obj.name,obj.family,obj.genus,obj.walsCode])
        return response


class WordDownload(generics.ListAPIView):
    """ Download a .csv file with all the words of a language - api/download/word/LANGUAGE """
    def get(self, request, format=None,**kwargs):
        lang = self.kwargs['str']
        lang.lower()
        filePath  = "".join(['data/langs/Complete/', lang, '.csv'])
        response  = FileResponse(open(filePath,'rb'))
        return response