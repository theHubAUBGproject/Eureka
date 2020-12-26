from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (POS, Dimension,User, Family, Feature, Genus, Language, Lemma,
                     TagSet, Word, Proposal, Notification)


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

class LangLemmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lemma
        fields = ["name"]


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


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
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
        fields = ['id', 'name', 'tagset', 'approved']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        depth = 2 


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields='__all__'


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields='__all__'
        depth = 2


class SingleProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'