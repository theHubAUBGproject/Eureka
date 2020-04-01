from django.shortcuts import render
from rest_framework import viewsets, permissions
from wordDictionary.models import Feature, Language, Dimension, Word
from .serializers import FeatureSerializer, LanguageSerializer, DimensionSerializer, WordSerializer

class FeatureView(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class DimensionView(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer

class WordView(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer