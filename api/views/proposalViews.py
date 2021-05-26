from api.models import Notification, Proposal, User, Word
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser, IsAuthenticated)
from rest_framework.response import Response

from ..customPermissions import LinguistPermission, ReadOnly
from ..serializers import (NotificationSerializer, ProposalSerializer,
                           SingleProposalSerializer)


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(toUser=user).order_by('-id')
    
class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    lookup_field = 'id'

class ProposalList(generics.ListCreateAPIView):
    # queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Proposal.objects.filter(author=user).order_by('-id')

    def create(self, request, lang, **kwargs):
        serializer = SingleProposalSerializer(data=request.data, many=True)
        if serializer.is_valid():
            user = self.request.user
            user = get_object_or_404(User, email=user.email)
            serializer.save(author=user)
            return Response(request.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_201_CREATED)

        return Response({'error':"Invalid format"},
                         status=status.HTTP_403_FORBIDDEN)

    def list(self, request, lang, **kwargs):
        user = self.request.user
        user = get_object_or_404(User, email=user.email)
        queryset = Proposal.objects.filter(author=user.id)
        serialized = ProposalSerializer(queryset, many=True)
        return Response(serialized.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_200_OK)

class ProposalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proposal.objects.all()
    serializer_class = SingleProposalSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    lookup_field = 'id'
