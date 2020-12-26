from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Dimension
from ..serializers import DimensionSerializer
from ..utils import getAllFeatures


class DimensionList(generics.ListCreateAPIView):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']

    def options(self, request, lang):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


class DimensionDetail(generics.RetrieveUpdateAPIView):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    lookup_field = 'name'

    def retrieve(self, request, name, format=None):
        dimension = self.get_object()
        serializer = DimensionSerializer(dimension)
        dim_data = serializer.data
        dims = getAllFeatures(dimension=dimension)
        dim_data['options'] = dims
        return Response(dim_data, status=status.HTTP_200_OK)

    def options(self, request, name):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})
