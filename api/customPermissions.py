from django.contrib.auth.models import Group
from rest_framework.permissions import  BasePermission, SAFE_METHODS


class LinguistPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            #User not logged in
            return False
        if (user.is_linguist):
            return True
        else:
            # User not linguist
            return False

class ReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        # SAFE_METHODS = [ 'GET', 'HEAD', 'OPTIONS']
        if(request.method in SAFE_METHODS):
            return True

