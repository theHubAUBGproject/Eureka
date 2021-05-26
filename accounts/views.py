from api.models import User
from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.contrib.sites.shortcuts import get_current_site
from accounts.serializers import AuthTokenSerializer, UserSerializer, ForgotPasswordSerializer, ChangePasswordSerializer
from accounts.Util import Util

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

def generate_random_password():
    import string
    import random 
    random_password = ''
    for i in range(0,11):
        random_password += random.choice(string.ascii_letters)
    return random_password

class ForgotPasswordView(generics.UpdateAPIView):
    """
    An endpoint for recivering forgotten password.
    """
    serializer_class = ForgotPasswordSerializer
    model = User

    def get_object(self, queryset=None):
        email = self.request.data['email'] 
        user = get_object_or_404(User, email=email)
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = generate_random_password()
            self.object.set_password(new_password)
            self.object.save()
            # Prepare email
            current_site = get_current_site(request)
            data = { 'site':current_site, 'email':self.object.email, 'user':self.object.name, 'password':new_password }
            Util.send_forgot_passord_email(data)

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_403_FORBIDDEN)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
        
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)