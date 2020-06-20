from django.urls import path
# flake8: noqa
from .views.dimensionViews import *
from .views.familyViews import *
from .views.featureViews import *
from .views.genusViews import *
from .views.languageViews import *
from .views.lemmaViews import *
from .views.rootView import *
from .views.tagsetViews import *
from .views.wordViews import *
from .views.userViews import *
from .views.downloadViews import *

urlpatterns = [
    path('', APIRootList.as_view(), name='root'),
    path('users/', UserList.as_view(), name='users'),
    path('languages/', LanguageList.as_view(), name='languages'),
    path('dimensions/', DimensionList.as_view(),
         name='dimensions'),
    path('dimensions/<slug:name>/', DimensionDetail.as_view(),
         name='dimensionDetail'),
    path('features/', FeatureList.as_view(), name='features'),
    path('features/<slug:name>/', FeatureDetail.as_view(),
         name='featureDetail'),
    path('words/', WordList.as_view(), name='words'),
    path('words/<slug:name>/', WordDetail.as_view(),
         name='wordDetail'),
    path('lemmas/', LemmaList.as_view(), name='lemmas'),
    path('lemmas/<slug:name>/', LemmaDetail.as_view(), name='lemmaDetail'),
    path('genuses/', GenusList.as_view(), name='genuses'),
    path('tagsets/', TagSetList.as_view(), name='tagsets'),
    path('tagsets/<slug:name>/', TagSetDetail.as_view(),
         name='tagsetDetail'),
    path('families/', FamilyList.as_view(), name='families'),

    path('download/dimensions', DimensionDownload.as_view(),name='dim-down'),
    path('download/features', FeatureDownload.as_view(),name='feat-down'),
    path('download/languages', LanguageDownload.as_view(),name='lang-down'),
    path('download/genus', GenusDownload.as_view(),name='gen-down'),
    path('download/words/<str:languageName>', WordDownload.as_view()),
]
