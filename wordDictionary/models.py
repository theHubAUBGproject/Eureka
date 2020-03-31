from djongo import models
from django import forms
from jsonfield import JSONField
# Create your models here.

#++++++++++++++++++++++++++

class Family(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']
#++++++++++++++++++++++++++

class Language(models.Model):
    name = models.CharField(max_length=15)
    family = models.EmbeddedField(
        model_container = Family,
        model_form_class = FamilyForm,
        default = None,
    )
    def __str__(self):
        return self.name

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']

#++++++++++++++++++++++++++++

class Dimension(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class DimensionForm(forms.ModelForm):
    class Meta:
        model = Dimension
        fields = ['name']

#++++++++++++++++++++++++

class Feature(models.Model):
    name = models.CharField(max_length=20)
    dimension = models.EmbeddedField(
        model_container = Dimension,
        model_form_class = DimensionForm,
        default=None,
    )
    def __str__(self):
        return self.name

#++++++++++++++++++++++++

class Lemma(models.Model):
    name = models.CharField(max_length=50)
    language = models.EmbeddedField(
        model_container = Language,
        model_form_class = LanguageForm,
        default=None,
    )
    def __str__(self):
        return self.name

class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['name']

#------------------------

class Word(models.Model):
    name = models.CharField(max_length=50)

    lemma = models.EmbeddedField(
        model_container = Lemma,
        model_form_class = LemmaForm,
        default=None,
    )

    language = models.EmbeddedField(
        model_container = Language,
        model_form_class = LanguageForm,
        default=None,
    )
    dimensions = JSONField()
    def __str__(self):
        return self.name