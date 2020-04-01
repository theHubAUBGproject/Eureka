from django.contrib import admin
<<<<<<< HEAD
from wordDictionary.models import  Word, Feature, Dimension, Language, Lemma, Family, TagSet, POS

=======
from django.contrib.admin.models import LogEntry
from wordDictionary.models import Word, Feature, Dimension, Language
>>>>>>> upstream/master


# Register your models here.
admin.site.register(Word)
admin.site.register(Feature)
admin.site.register(Dimension)
admin.site.register(Language)
<<<<<<< HEAD
admin.site.register(Lemma)
admin.site.register(Family)
admin.site.register(TagSet)
admin.site.register(POS)
=======
admin.site.register(LogEntry)
>>>>>>> upstream/master
