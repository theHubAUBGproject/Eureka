from django.contrib import admin
from wordDictionary.models import  Word, Feature, Dimension, Language, Lemma, Family



# Register your models here.
admin.site.register(Word)
admin.site.register(Feature)
admin.site.register(Dimension)
admin.site.register(Language)
admin.site.register(Lemma)
admin.site.register(Family)