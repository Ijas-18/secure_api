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
