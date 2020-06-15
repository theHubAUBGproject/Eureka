from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIRootList.as_view(), name='root'),
    path('languages/', views.LanguageList.as_view(), name='languages'),
    path('dimensions/', views.DimensionList.as_view(), name='dimensions'),
    path('features/', views.FeatureList.as_view(), name='features'),
    path('words/', views.WordList.as_view(), name='words'),
    path('lemmas', views.LemmaList.as_view(), name='lemmas'),
    path('genuses/', views.GenusList.as_view(), name='genuses'),
    path('tagsets/', views.TagSetList.as_view(), name='tagsets'),
    path('families/', views.FamilyList.as_view(), name='families'),

    path('download/dimensions',views.DimensionDownload.as_view(),name='dim-down'),
    path('download/features',views.FeatureDownload.as_view(),name='feat-down'),
    path('download/languages',views.LanguageDownload.as_view(),name='lang-down'),
    path('download/genus',views.GenusDownload.as_view(),name='gen-down'),
    path('download/words/<str:str>/',views.WordDownload.as_view()),
]
