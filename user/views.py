from django.shortcuts import render
from .models import UserModel
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password,check_password
import json,jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .authentication import userAuth
import json

# Create your views here.
class Register(generics.RetrieveAPIView):
    permission_classes=(AllowAny,)
    def post(self,request,*args,**kwrgs):
        if request.data:
            if request.data['username'] and request.data['password']:
                user=UserModel()
                user.username=request.data['username']
                user.password=make_password(request.data['password'])
                if request.data['firstname'] and request.data['lastname']:
                    user.first_name=request.data['firstname']
                    user.lastname=request.data['lastname']
                try:
                    user.save()
                    token=str(jwt.encode({"username":user.username},"Secret").decode('utf-8'))
                    return Response(
                        {
                            "success":True,
                            "Message":"User Registerd Successfully",
                            "token":token,
                            "username":user.username
                        },
                        status=201,
                        content_type="application/json"
                    )
                except Exception as e:

                    return Response(
                        {
                            "Success":False,
                            "message":"User already Exist",
                        },
                        status=400
                    )
            return Response(
                {
                    "success":False,
                    "Message":"Misssing Username/password"
                }
            )



class Login(APIView):
    # authentication_classes = (userAuth,)
    permission_classes=(AllowAny,)
    def post(self,request,*args,**kwrgs):
         if request.data['username'] and request.data['password']:
             try:
                print(request.data['username'])
                user=UserModel.objects.get(username=request.data['username']) 
                pwd_valid = check_password(request.data['password'], user.password)
                if pwd_valid:
                    return Response(
                        {
                            "Success":True,
                            "token":str(jwt.encode({"username":user.username},"secrect").decode('utf-8')),
                            "username":user.username
                        }
                    )
                else:
                    return Response(
                        {
                            "Success":False,
                            "Message":"Password Mismatch"
                        
                        }
                    )
             except UserModel.DoesNotExist:
                 return Response(
                        {
                            "Success":False,
                            "Message":"User Mismatch"

                        }
                    )

class Profile(APIView):
    # authentication_classes = (userAuth,)
    permission_classes=(userAuth,)
    def get(self,request,*args,**krwgs):
        token=request.META['HTTP_AUTHORIZATION']
        user_data=jwt.decode(token,'secrect','utf-8')
        username=user_data['username']
        user=UserModel.objects.get(username=username)
        return Response(
            {
                "message":"token success",
                "username":user.username,
                "name":user.first_name + user.lastname
            }
        )