from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# Create your models here.


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users mus have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_linguist(self, email, password=None, **extra_fields):
        """ Creates and saves a new linguist """
        user = self.create_user(email, password)
        user.is_linguist = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_linguist = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'



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
    approved = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Proposal(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True,related_name='author')
    date = models.DateTimeField(default=timezone.now)
    word = models.ForeignKey('Word', on_delete=models.PROTECT)
    proposedWord = models.CharField(max_length=255, default='')
    note = models.TextField()
    status = models.CharField(default='Pending', max_length=30)

    
class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['status', 'word']


class Notification(models.Model):
    proposal = models.ForeignKey(Proposal, null=True, on_delete=models.PROTECT)
    seen = models.BooleanField(default=False)
    toUser = models.ManyToManyField(User, related_name='toUser')
    fromUser = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='fromUser')
    date = models.DateTimeField(default=timezone.now)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['toUser','date']