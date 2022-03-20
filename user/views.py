from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.sites.models import Site
import requests
from django.urls import reverse
import os

class UserCreateApiView(GenericAPIView,CreateModelMixin):
    """View for registering new users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class UserApiView(APIView):
    """View for Retrieving,Updating and Deleting existing users."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        """Gives info about user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        """Updates user's details.

        *Does not update password
        """       

        serializer = UserSerializer(request.user,data = request.data,partial = True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self,request):
        """Delete a user."""
        User.objects.get(username = str(request.user)).delete()
        return Response({"detail":"Deleted successfully"},status=status.HTTP_200_OK)


class Social_Auth_Facebook(APIView):
    """Creates or verifies an user using Facebook Authenticaion"""

    def post(self,request):
        """Takes user_id and access_token and creates a new account"""

        user_id = request.data['user_id']
        access_token = request.data['access_token']
        url = f"https://graph.facebook.com/{user_id}"
        data = requests.get(url,params={'fields':'id,name,first_name,last_name,email','access_token':access_token})
        user_data = data.json()
        try:
            user = User.objects.get(email = user_data['email'])

        except User.DoesNotExist:
            user = User.objects.create(username = user_data['name'], email = user_data['email'], first_name = user_data['first_name'],
            last_name = user_data['last_name'])
            user.set_password(os.getenv("social_password"))
            user.save()

        finally:
            host = request.build_absolute_uri('/')
            token_url = reverse("token_obtain_pair")
            url = f"{host}{token_url[1:]}"
            print(url)
            payload = {"username":user.username,"password":os.getenv("social_password")}
            tokens = requests.post(url, data = payload)
            return Response(tokens.json())


