from djongo import models
from jsonfield import JSONField
# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class Dimension(models.Model):
    dimensionName = models.CharField(max_length=20)
    
    def __str__(self):
        return self.dimensionName


class Feature(models.Model):
    featureName = models.CharField(max_length=20)
    dimension = models.ArrayReferenceField(
        to = Dimension,
        default=None,
    )
    def __str__(self):
        return self.featureName

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