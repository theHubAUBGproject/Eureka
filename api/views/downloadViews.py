from django.http import Http404, HttpResponse
from rest_framework import status, generics
from rest_framework.response import Response
import csv
from rest_framework.views import APIView
from django.db import connection
from django.utils import timezone
from django.db.models import F
from django.db.models import Case, When, Value, CharField
from ..models import Genus, Dimension, Feature, Language, Family, Lemma, Word
from ..utils import qs_to_csv_response


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
        writer.writerow(['name', 'dimension'])
        for obj in items:
            writer.writerow([obj.name, obj.dimension])
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
            writer.writerow([obj.name, obj.family, obj.genus, obj.walsCode])
        return response


class WordDownload(APIView):
    """ Download a file with all the words of a language - api/download/word/language """
    def get(self, request, format=None,**kwargs):
        languageName = self.kwargs['languageName']
        languageName = "".join([languageName[0].upper(), languageName[1:].lower()])
        languageObject = Language.objects.get(name=languageName)
        querySet =  Word.objects.filter(language=languageObject.id).values(
            'name',
            lemma_name = F('lemma__name'),
            tagset_name = F('tagset__name'),
        )
        return qs_to_csv_response(querySet,languageObject)
