from urllib import parse

from django.urls import path

# flake8: noqa
import api.views as views

urlpatterns = [
    path('<slug:lang>/', views.APIRootList.as_view(), name='root'),
    # All-models views
    # path('<slug:lang>/users/', views.UserList.as_view(), name='users'),
    path('all/lemmas/', views.AllLemmasList.as_view(), name='all_lemmas'),
    path('<slug:lang>/families/', views.FamilyList.as_view(), name='families'),
    path('<slug:lang>/languages/', views.LanguageList.as_view(), name='languages'),
    path('<slug:lang>/dimensions/', views.DimensionList.as_view(),name='dimensions'),
    path('<slug:lang>/features/', views.FeatureList.as_view(), name='features'),
    path('<slug:lang>/genera/', views.GenusList.as_view(), name='genera'),
    path('<slug:lang>/notifications/', views.NotificationList.as_view(), name='notifications'),
    path('<slug:lang>/notifications/<str:id>', views.NotificationDetail.as_view(), name='notificationsDetail'),
    path('<slug:lang>/proposals/', views.ProposalList.as_view(), name='proposals'),
    path('<slug:lang>/proposals/<str:id>', views.ProposalDetail.as_view(), name='proposalDetail'),
    path('<slug:lang>/tagsets/', views.TagSetList.as_view(), name='tagsets'),
    path('<slug:lang>/lemmas/', views.LemmaList.as_view(), name='lemmas'),
    path('<slug:lang>/words/', views.WordList.as_view(), name='words'),
    # Detail-Views
    path('<str:lang>/dimensions/<str:name>/', views.DimensionDetail.as_view(), name='dimensionDetail'),
    path('<str:lang>/features/<str:name>/', views.FeatureDetail.as_view(),name='featureDetail'),
    path('<str:lang>/words/<str:name>/', views.WordDetail.as_view(),name='wordDetail'),
    path('<str:lang>/lemmas/<str:name>/', views.LemmaDetail.as_view(), name='lemmaDetail'),
    path('<str:lang>/tagsets/<str:name>/', views.TagSetDetail.as_view(),name='tagsetDetail'),
    # Download Views
    path('data/download/dimensions/', views.DimensionDownload.as_view(),name='dim-down'),
    path('data/download/features/', views.FeatureDownload.as_view(),name='feat-down'),
    path('data/download/languages/', views.LanguageDownload.as_view(),name='lang-down'),
    path('data/download/genera/', views.GenusDownload.as_view(),name='gen-down'),
    path('data/download/families/', views.FamilyDownload.as_view(),name='fam-down'),
    path('data/download/words/<str:languageName>/', views.WordDownload.as_view()),
    path('data/download/families/<str:familyName>/', views.FamilyQueryDownload.as_view()),
    path('data/download/genera/<str:genusName>/', views.GenusQueryDownload.as_view()),
    path('data/download/all/', views.AllLanguagesDownload.as_view()),
]
