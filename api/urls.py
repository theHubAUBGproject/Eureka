from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIRootList.as_view(), name='root'),
    path('languages/', views.LanguageList.as_view(), name='languages'),
    path('languages/<int:pk>/', views.LanguageDetail.as_view(),
         name='languageDetail'),
    path('dimensions/', views.DimensionList.as_view(),
         name='dimensions'),
    path('dimensions/<int:pk>/', views.DimensionDetail.as_view(),
         name='dimensionDetail'),
    path('features/', views.FeatureList.as_view(), name='features'),
    path('features/<int:pk>/', views.FeatureDetail.as_view(),
         name='featureDetail'),
    path('words/', views.WordList.as_view(), name='words'),
    path('words/<int:pk>/', views.WordDetail.as_view(),
         name='wordDetail'),
    path('lemmas/', views.LemmaList.as_view(), name='lemmas'),
    path('lemmas/<int:pk>/', views.LemmaDetail.as_view(),
         name='lemmaDetail'),
    path('genuses/', views.GenusList.as_view(), name='genuses'),
    path('genuses/<int:pk>/', views.GenusDetail.as_view(),
         name='genusDetail'),
    path('tagsets/', views.TagSetList.as_view(), name='tagsets'),
    path('tagsets/<int:pk>/', views.TagSetDetail.as_view(),
         name='tagsetDetail'),
    path('families/', views.FamilyList.as_view(), name='families'),
    path('families/<int:pk>', views.FamilyDetail.as_view(),
         name='familyDetail')
]
