from wordDictionary.models import (Feature, Language, Dimension, Word, TagSet,
                                   Genus, Family, Lemma, POS)
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


class FeatureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class FeatureDetailSerializer(serializers.ModelSerializer):
    dimension = DimensionSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = '__all__'


class LemmaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lemma
        fields = '__all__'


class LemmaDetailSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    pos = PosSerializer(read_only=True)

    class Meta:
        model = Lemma
        lookup_field = 'name'
        fields = '__all__'


class TagSetSerializer(serializers.ModelSerializer):
    features = FeatureDetailSerializer(many=True, read_only=True)

    class Meta:
        model = TagSet
        fields = '__all__'


class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class WordDetailSerializer(serializers.ModelSerializer):
    lemma = LemmaDetailSerializer(read_only=True)
    tagset = TagSetSerializer(read_only=True)

    class Meta:
        model = Word
        fields = '__all__'


class RelatedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'name']
