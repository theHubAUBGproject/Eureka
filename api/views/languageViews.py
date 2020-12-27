from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Language, Lemma
from ..serializers import LanguageSerializer


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['^name']

    def list(self, request, lang):
        queryset = self.get_queryset()
        if("populated" in request.query_params):
            pop_languages = Lemma.objects.all().values_list('language').distinct()
            queryset = Language.objects.filter(id__in=pop_languages)
        serialized = LanguageSerializer(queryset, many=True)
        return Response(serialized.data,
                        headers={"Access-Control-Allow-Origin": "*"},
                        status=status.HTTP_200_OK)

    def options(self, request, lang):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})
