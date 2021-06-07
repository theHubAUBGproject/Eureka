from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, authentication
from rest_framework.response import Response
from api.serializers import CommentCreateSerializer, CommentListSerializer
from api.models import Comment, User
from django.shortcuts import get_object_or_404


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        id = self.kwargs['id']
        comments = Comment.objects.filter(proposal_id=id).order_by('-date')
        return comments


class CommentCreate(generics.CreateAPIView):

    serializer_class = CommentCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    def create(self, request, lang, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            user = get_object_or_404(User, email=user.email)
            serializer.save(author=user)
            return Response(request.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_201_CREATED)

        return Response({'error':"Invalid format"},
                         status=status.HTTP_403_FORBIDDEN)