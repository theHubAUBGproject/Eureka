from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import Language
from ..serializers import LanguageSerializer


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']
    
    def options(self, request):
        return Response(status=status.HTTP_200_OK,
                    headers={"Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Headers":
                                "access-control-allow-origin"})
