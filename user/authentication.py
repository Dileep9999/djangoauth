from .models import UserModel
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import exceptions
import jwt

class userAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token=request.META['HTTP_AUTHORIZATION']
            print(token,'=======================')
        except:
            print('token','=======================')
            return False
        if not token:
            return False
        try:
            user_data=jwt.decode(token,'secrect','utf-8')
            username=user_data['username']
        except:
            raise exceptions.AuthenticationFailed('Token corrupted')
        
            if not username:
                return False
            try:
                user=UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user in the Token')
        return True