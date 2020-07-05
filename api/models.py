from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']


class Genus(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class GenusForm(forms.ModelForm):
    class Meta:
        model = Genus
        fields = ['name']


class Family(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']


class Language(models.Model):
    name = models.CharField(max_length=30)
    family = models.ForeignKey('Family', on_delete=models.PROTECT, null=True)
    genus = models.ForeignKey('Genus', on_delete=models.PROTECT, null=True)
    walsCode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']


class Dimension(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DimensionForm(forms.ModelForm):
    class Meta:
        model = Dimension
        fields = ['name']


class Feature(models.Model):
    name = models.CharField(max_length=50)
    dimension = models.ForeignKey(
        'Dimension',
        on_delete=models.PROTECT,
        null=True
    )
    label = models.CharField(max_length=15, null=True)
    def __str__(self):
        return self.name


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']


class POS(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['name']


class Lemma(models.Model):
    name = models.CharField(max_length=70)
    language = models.ForeignKey(
        'Language',
        on_delete=models.PROTECT,
        null=True
    )
    animacy = models.BooleanField(default=True)
    transivity = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    pos = models.ForeignKey('POS', on_delete=models.PROTECT, null=True)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['name']


class TagSet(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name


class TagSetForm(forms.ModelForm):
    class Meta:
        model = TagSet
        fields = ['name', 'features']


class Word(models.Model):
    name = models.CharField(max_length=110)
    date_updated = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    lemma = models.ForeignKey('Lemma', on_delete=models.PROTECT, null=True)
    language = models.ForeignKey(
        'Language',
        on_delete=models.PROTECT,
        null=True
    )
    tagset = models.ForeignKey('TagSet', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
