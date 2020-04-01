from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('language', views.LanguageView)
router.register('dimension', views.DimensionView)
router.register('feature', views.FeatureView)
router.register('word', views.WordView)

urlpatterns = [
    path('', include(router.urls))
]