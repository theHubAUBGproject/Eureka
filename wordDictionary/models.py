from djongo import models

from jsonfield import JSONField
# Create your models here.


class Feature(models.Model):
    featureName = models.CharField(max_length=20)
    currDimension = models.CharField(max_length=20, default=None)
    def __str__(self):
        return self.featureName

class Language(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class Dimension(models.Model):
    dimensionName = models.CharField(max_length=20)
    features = models.ArrayReferenceField(
        to = Feature,
        default=None,
    )
    def __str__(self):
        return self.dimensionName

class Word(models.Model):
    wordContent = models.CharField(max_length=50)
    rootWord = models.CharField(max_length=50)
    language = models.ArrayReferenceField(
        to = Language,
        default=None,
    )
    dimensions = JSONField()
    def __str__(self):
        return self.wordContent