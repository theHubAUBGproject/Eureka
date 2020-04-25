from django.http import Http404
from rest_framework.reverse import reverse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from wordDictionary.models import Feature, Language, Dimension, Word
from .serializers import FeatureSerializer, LanguageSerializer, DimensionSerializer, WordSerializer

class APIRootList(APIView):
    def get(self, request, format=None):
        data = {
            'languages': reverse('languages', request=request),
            'words': reverse('words', request=request),
            'features': reverse('features', request=request),
            'dimensions': reverse('dimensions', request=request)
        }
        return Response(data)

class FeatureList(APIView):
    def get(self, request, format=None):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = FeatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(request.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeatureDetail(APIView):
    def get_feature(self, pk):
        try:
            return Feature.objects.get(pk=pk)
        except Feature.DoesNotExist:
            return Http404
    
    def get(self, request, pk):
        feature = get_feature(pk)
        serializer = FeatureSerializer(feature)
        return Response(serializer.data)

class LanguageList(APIView):
    def get(self, request, format=None):
        queryset = Language.objects.all()
        serializer = LanguageSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        

class LanguageDetail(APIView):
    def get_language(self, pk):
        try:
            return Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        language = self.get_language(pk)
        serializer = LanguageSerializer(language)
        return Response(serializer.data)



class DimensionList(APIView):
    def get(self, request, format=None):
        queryset = Language.objects.all()
        serializer = DimensionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(seld, request,format=None):
        serializer = DimensionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class DimensionDetail(APIView):
    def get_dimension(self, pk):
        try:
            return Dimension.objects.get(pk=pk)
        except Dimension.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        dimension = self.get_dimension(pk)
        serializer = DimensionSerializer(dimension)
        return Response(serializer.data)

class WordList(APIView):
    def get(self, request, format=None):
        words = Word.objects.all()
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = WordSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WordDetail(APIView):
    def get_word(self, pk):
        try:
            return Word.objects.get(pk=pk)
        except Word.DoesNotExist:
            return Http404
    
    def get(self, request, pk):
        word = get_word(pk)
        serializer = WordSerializer(word)
        return Response(serializer.data)