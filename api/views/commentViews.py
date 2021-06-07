from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from api.serializers import CommentSerializer
from api.models import Comment, User

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        id = self.kwargs['id']
        return Comment.objects.filter(proposal=id).order_by('-date')
