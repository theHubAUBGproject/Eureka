from djongo import models
from django import forms
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','email']

#++++++++++++++++++++++++++
class Genus(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class GenusForm(forms.ModelForm):
    class Meta:
        model=Genus
        fields=['name']

#****************************
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

    genus = models.EmbeddedField(
        model_container=Genus,
        model_form_class=GenusForm,
        default=None,
    )

    walsCode = models.CharField(max_length=15,blank=True)
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

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']

#++++++++++++++++++++++++

class POS(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['name']



#++++++++++++++++++++++++

class Lemma(models.Model):
    name = models.CharField(max_length=50)
    language = models.EmbeddedField(
        model_container = Language,
        model_form_class = LanguageForm,
        blank=True,
        default = None,
    )

    animacy = models.BooleanField(default=True)
    transivity = models.BooleanField(default=True)

    
    author = models.EmbeddedField(
        model_container = User,
        model_form_class = UserForm,
        blank = True,
        default = None,
    )
    pos = models.EmbeddedField(
        model_container = POS,
        model_form_class = POSForm,
        blank=True,
        default = None,
    )
    date_updated = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['name']

#++++++++++++++++++++++++


class TagSet(models.Model):
    name = models.CharField(max_length=50,blank=True, default="")
    features = models.ArrayReferenceField(
        to = Feature,
        default=None
    )
    def __str__(self):
        return self.name

class TagSetForm(forms.ModelForm):
    class Meta:
        model = TagSet
        fields = ['name','features']

#++++++++++++++++++++++++
class Word(models.Model):
    name = models.CharField(max_length=50)
    date_updated = models.DateTimeField(default=timezone.now)
    author = models.EmbeddedField(
        model_container = User,
        model_form_class = UserForm,
        blank = True,
        default = None,
    )
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
    tagset = models.EmbeddedField(
        model_container  = TagSet,
        model_form_class = TagSetForm,
        default=None,
    )
    def __str__(self):
        return self.name
