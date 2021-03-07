from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,BasePermission, IsAuthenticated, SAFE_METHODS
from api.models import Notification, Proposal, User
from ..serializers import NotificationSerializer, ProposalSerializer, SingleProposalSerializer
from django.shortcuts import get_object_or_404
from ..customPermissions import LinguistPermission, ReadOnly


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(toUser=user).order_by('-id')
        
    def options(self, request, lang):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "Access-Control-Allow-Origin"})
    

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    lookup_field = 'id'
        
    def options(self, request, lang, name):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


class ProposalList(generics.ListCreateAPIView):
    # queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Proposal.objects.filter(author=user).order_by('-id')

    def create(self, request, **kwargs):
        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            user = get_object_or_404(User, email=user.email)
            serializer.save(author=user)
            return Response(request.data, status=status.HTTP_201_CREATED)

        return Response({'error':"Invalid format"},
                         status=status.HTTP_403_FORBIDDEN)
    
    def options(self, request, lang):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})

class ProposalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proposal.objects.all()
    serializer_class = SingleProposalSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    lookup_field = 'id'


    def options(self, request, lang, name):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


