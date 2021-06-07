from api.models import Notification, Proposal, User, Word
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, authentication
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
        if user.is_linguist:
            return Proposal.objects.filter().order_by('-id')
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
        all = self.get_queryset()
        serialized = ProposalSerializer(all, many=True)
        return Response(serialized.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_200_OK)


class ProposalsForApproval(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAdminUser|LinguistPermission]

    def get_queryset(self):
        return Proposal.objects.filter().order_by('-id')

    def list(self, request, lang, **kwargs):

        serialized = ProposalSerializer(self.get_queryset(), many=True)

        return Response(serialized.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_200_OK)


class ApproveProposal(generics.RetrieveUpdateAPIView):
    """ Approve a proposal  """
    queryset = Proposal.objects.all()
    serializer_class = SingleProposalSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        id = self.kwargs['id']
        proposal = get_object_or_404(Proposal, id=id)
        return proposal
    
    def partial_update(self, request, *args, **kwargs):
        curr_proposal = self.get_object()

        kwargs['partial'] = True
        

        # Update the word form
        word_object = get_object_or_404(Word, id = curr_proposal.word.id )  
        word_object.name = curr_proposal.proposedWord
        word_object.save()

        request.data['status'] = "Approved"

        # Notify the user here
        # ......

        return self.update(request, *args, **kwargs)


class DeclineProposal(generics.RetrieveUpdateAPIView):
    """ Decline a proposal  """
    queryset = Proposal.objects.all()
    serializer_class = SingleProposalSerializer
    permission_classes = [IsAdminUser|LinguistPermission]
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        id = self.kwargs['id']
        proposal = get_object_or_404(Proposal, id=id)

        return proposal
    
    def partial_update(self, request, *args, **kwargs):
        import json
        curr_proposal = self.get_object()
        kwargs['partial'] = True
        request.data['status'] = "Decline"
        # Notify the user here
        # ......

        return self.update(request, *args, **kwargs)


class ProposalDetail(generics.RetrieveAPIView):
    queryset = Proposal.objects.all()
    serializer_class = SingleProposalSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        id = self.kwargs['id']
        proposal = get_object_or_404(Proposal, id=id)
        return proposal
    
    


