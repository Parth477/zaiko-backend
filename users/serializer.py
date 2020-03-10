from rest_framework import serializers

from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('password',)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user registration request data
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField(allow_blank=False, allow_null=False)
    # max_length defined from AbstractBaseUser class
    password = serializers.CharField(max_length=128, allow_blank=False, allow_null=False)


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    # password = PasswordSerializer()

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'contact_no', 'address', 'password', 'organization','user_role')

    def create(self, validated_data):
        # kwargs = {}
        # # user_password = validated_data('password')
        # user = User.objects.create(**validated_data)
        # # user_pwd = SetPassword.objects.create(user=user)
        # # user_pwd.set_password(user_password["password"])
        # token = Token.objects.create(user=user)
        # kwargs['user_data'] = user
        # kwargs['token'] = token.key
        # return user
        pass

    def update(self,instace, validated_data):
        pass


