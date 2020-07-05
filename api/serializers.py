from .models import (Feature, Language, Dimension, Word, TagSet,
                     Genus, Family, Lemma, POS)
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    dimension = DimensionSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = '__all__'


class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    genus = GenusSerializer(read_only=True)
    family = FamilySerializer(read_only=True)
    
    class Meta:
        model = Language
        fields = '__all__'


class LemmaSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    pos = PosSerializer(read_only=True)

    class Meta:
        model = Lemma
        lookup_field = 'name'
        fields = '__all__'


class TagSetSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = TagSet
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    lemma = LemmaSerializer(read_only=True)
    tagset = TagSetSerializer(read_only=True)
    
    class Meta:
        model = Word
        fields = '__all__'


class RelatedWordSerializer(serializers.ModelSerializer):
    tagset = TagSetSerializer(read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'name', 'tagset']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'groups']
