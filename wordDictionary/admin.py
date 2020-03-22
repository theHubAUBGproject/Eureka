from django.contrib import admin
from wordDictionary.models import Word, Feature, Dimension, Language


# Register your models here.
admin.site.register(Word)
admin.site.register(Feature)
admin.site.register(Dimension)
admin.site.register(Language)