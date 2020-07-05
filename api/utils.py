from api.serializers import (FeatureSerializer,
                             DimensionSerializer)
from .models import Feature, Dimension, Word

from django.http import Http404, HttpResponse
from rest_framework.response import Response
import csv
from django.db import connection
from django.utils import timezone
from django.db.models import F
from io import StringIO, BytesIO
from zipfile import ZipFile
# Returns all the possible features for
# the word's dimension in following format:
# { 'dim1': [['feat1', True], ['feat2', False], ...], ... }

def getDimOptions(tagset):
    # result is returned as a dictionary
    result = {}
    dim = DimensionSerializer(Dimension.objects.all(), many=True)
    feat = FeatureSerializer(Feature.objects.all(), many=True)
    # stores all unique dimensions that are possible in a language
    tag_names = set([])
    # stores all feature names of a ward
    feat_names = []
    for i in tagset['features']:
        feat_names.append(i['name'])
        tag_names.add(i['dimension']['name'])
    for i in tag_names:
        result[i] = set([])
    for f in feat.data:
        for d in dim.data:
            if(f['dimension']['id'] == d['id'] and d['name'] in tag_names):
                result[d['name']].add(f['name'])
    return result


def getFeatures(tagset):
    result = []
    for i in tagset['features']:
        result.append({i['dimension']['name']: i['name']})
    return result

def getAllFeatures(dimension):
    result = set([])
    features = Feature.objects.filter(dimension=dimension.id)
    feats = FeatureSerializer(features, many=True)
    for feat in feats.data:
        result.add(feat['name'])
    return result


class Response():
    """ Class to help with custom responses """

    def csvResponse(self, querySet, filename):
        """ Get the queryset and creates the csv file """
        sql, params = querySet.query.sql_with_params()
        sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E',')"
        filename = f'{filename}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        with connection.cursor() as cur:
            sql = cur.mogrify(sql, params)
            cur.copy_expert(sql, response)
        return response

    def zipResponse(self, allLanguages, filename):
        """ Get the languages queryset and create the zip file """
        in_memory = BytesIO()
        zip = ZipFile(in_memory, "a")
        languageList = list(allLanguages)
        for language in languageList:
            # Determine the queryset
            querySet =  self.wordFormatFile(language)
            sql, params = querySet.query.sql_with_params()
            sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E',')"
            subfileName = f'{language}.csv'
            response = HttpResponse(content_type='text/csv')
            with connection.cursor() as cur:
                sql = cur.mogrify(sql, params)
                cur.copy_expert(sql, response)
                # Add to the zip file
                zip.writestr(subfileName, response.content)
        zip.close()
        # Creates the zip file response
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = f"attachment; filename={filename}.zip"
        in_memory.seek(0)
        response.write(in_memory.read())
        return response

    def wordFormatFile(self, languageObject):
        """ Fix the format in which words will be displayed in files """
        querySet =  Word.objects.filter(language=languageObject.id).values(
            'name',
            lemma_name = F('lemma__name'),
            tagset_name = F('tagset__name'),
        )
        return querySet
