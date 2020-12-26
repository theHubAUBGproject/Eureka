from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,BasePermission, IsAuthenticated, SAFE_METHODS
from ..models import Notification, Proposal
from ..serializers import NotificationSerializer, ProposalSerializer, SingleProposalSerializer

from ..customPermissions import LinguistPermission, ReadOnly


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

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
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]
    
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


