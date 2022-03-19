from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    """This class serialize User model objects"""

    email = serializers.EmailField(required = True,validators = [UniqueValidator(User.objects.all())])
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2']


    def create(self,validated_data):
        """creates a new user"""

        #Checks whether both passwords are matching

        if(validated_data['password'] != validated_data['password2']):
            raise serializers.ValidationError({"password":"password field didn't match"})

        user = User.objects.create(username = validated_data['username'],
        email = validated_data['email'],
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        """updates a existing user"""

        #Restricting access to change username

        if(instance.username != validated_data.get('username',instance.username)):
            raise serializers.ValidationError({"username":"username cannot be changed"})

        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        return instance