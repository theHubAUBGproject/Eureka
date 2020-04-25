from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.APIRootList.as_view(), name='root'),
    path('languages/', views.LanguageList.as_view(), name='languages'),
    path('languages/<int:pk>/', views.LanguageDetail.as_view(), name='languageDetail'),
    path('dimensions/', views.DimensionList.as_view(), name='dimensions'),
    path('dimensions/<int:pk>/', views.DimensionDetail.as_view(), name='dimensionDetail'),
    path('features/', views.FeatureList.as_view(), name='features'),
    path('features/<int:pk>/', views.FeatureDetail.as_view(), name='featureDetail'),
    path('words/', views.WordList.as_view(), name='words'),
    path('words/<int:pk>/', views.WordDetail.as_view(), name='wordDetail')
]