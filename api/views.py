from django.http import Http404
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wordDictionary.models import (Feature, Language, Dimension, Word,
                                   Lemma, TagSet, Family, Genus)
from .serializers import (FeatureListSerializer, FeatureDetailSerializer,
                          LanguageSerializer, DimensionSerializer,
                          WordListSerializer, TagSetSerializer,
                          LemmaListSerializer, LemmaDetailSerializer,
                          FamilySerializer, GenusSerializer,
                          WordDetailSerializer, RelatedWordSerializer)
from .utils import getDimOptions


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


class FeatureList(APIView):
    def get(self, request, format=None):
        features = Feature.objects.all()
        serializer = FeatureListSerializer(features, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FeatureListSerializer(data=request.data)
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
        feature = self.get_feature(pk)
        serializer = FeatureDetailSerializer(feature)
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
        queryset = Dimension.objects.all()
        serializer = DimensionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(seld, request, format=None):
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
        serializer = WordListSerializer(words, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WordListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetail(APIView):
    def get_word(self, name):
        try:
            return Word.objects.filter(name=name)[:1]
        except Word.DoesNotExist:
            return Http404

    def get(self, request, slug):
        word = self.get_word(slug)
        serializer = WordDetailSerializer(word[0])
        options = getDimOptions(serializer.data['tagset'])
        serializer_data = serializer.data
        serializer_data['dimensions'] = options
        return Response(serializer_data,
                        headers={"Access-Control-Allow-Origin": "*"})

    def options(self, request, slug):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                     "access-control-allow-origin"})


class LemmaList(APIView):
    def get(self, request, format=None):
        lemmas = Lemma.objects.all()
        serializer = LemmaListSerializer(lemmas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LemmaListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LemmaDetail(APIView):
    def get_lemma(self, name):
        try:
            return Lemma.objects.get(name=name)
        except Lemma.DoesNotExist:
            return Http404

    def get_related_words(self, pk):
        try:
            related_words = Word.objects.filter(lemma=pk)
            return related_words
        except Word.DoesNotExist:
            return Http404

    def get(self, request, slug):
        lemma = self.get_lemma(name=slug)
        serializer = LemmaDetailSerializer(lemma)
        related_words = self.get_related_words(lemma.id)
        words = RelatedWordSerializer(related_words, many=True)
        lemma_data = serializer.data
        lemma_data['related_words'] = words.data
        return Response(lemma_data,
                        headers={"Access-Control-Allow-Origin": "*"})
  
    def options(self, request, slug):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


class GenusList(APIView):
    def get(self, request, format=None):
        genuses = Genus.objects.all()
        serializer = GenusSerializer(genuses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GenusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenusDetail(APIView):
    def get_genus(self, pk):
        try:
            return Genus.objects.get(pk=pk)
        except Genus.DoesNotExist:
            return Http404

    def get(self, request, pk):
        genus = self.get_genus(pk)
        serializer = GenusSerializer(genus)
        return Response(serializer.data)


class TagSetList(APIView):
    def get(self, request, format=None):
        tagsets = TagSet.objects.all()
        serializer = TagSetSerializer(tagsets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagSetDetail(APIView):
    def get_tagset(self, pk):
        try:
            return TagSet.objects.get(pk=pk)
        except TagSet.DoesNotExist:
            return Http404

    def get(self, request, pk):
        tagset = self.get_tagset(pk)
        serializer = TagSetSerializer(tagset)
        return Response(serializer.data)


class FamilyList(APIView):
    def get(self, request, format=None):
        families = Family.objects.all()
        serializer = FamilySerializer(families, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyDetail(APIView):
    def get_family(self, pk):
        try:
            return Family.objects.get(pk=pk)
        except Family.DoesNotExist:
            return Http404

    def get(self, request, pk):
        family = self.get_family(pk)
        serializer = FamilySerializer(family)
        return Response(serializer.data)
