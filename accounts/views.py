from api.models import User
from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from accounts.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for the user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authentication user """
        return self.request.user

    def retrieve(self, request, **kwargs):
        user = self.get_object()
        user = get_object_or_404(User, email=user.email)
        serialized = UserSerializer(user)
        return Response(serialized.data,
                headers={"Access-Control-Allow-Origin": "*"},
                status=status.HTTP_200_OK)
