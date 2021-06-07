from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (POS, Dimension, Family, Feature, Genus, Language, Lemma,
                     Notification, Proposal, TagSet, User, Word, Comment)


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

class ProposalWordSerializer(serializers.ModelSerializer):
    lemma = LangLemmaSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    class Meta:
        model = Word
        fields = ['id', 'name', 'lemma', 'language']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_staff', 'is_linguist']
        depth = 1


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields='__all__'


class ProposalSerializer(serializers.ModelSerializer):
    word = ProposalWordSerializer(read_only=True)
    class Meta:
        model = Proposal
        fields='__all__'


class WordForProposalSerializer(serializers.ModelSerializer):
    lemma = LemmaSerializer()
    class Meta:
        model = Word
        fields = ['name', 'lemma']


class SingleProposalSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    word = WordForProposalSerializer()
    class Meta:
        model = Proposal
        fields = '__all__'

class CreateProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'