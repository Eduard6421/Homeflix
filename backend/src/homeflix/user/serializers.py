from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers, status
from django.contrib.auth.password_validation import validate_password as pwd_validator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email',)
        read_only_fields = ('id', 'email', )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = get_user_model() \
            .objects.create_user(email=email, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=9, max_length=128)

    def validate_password(self, value):
        pwd_validator(value)
        return value

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Email must be supplied', code=status.HTTP_400_BAD_REQUEST)

        if password is None:
            raise serializers.ValidationError(
                'Email must be supplied', code=status.HTTP_400_BAD_REQUEST)

        pwd_validator(password)

        user = authenticate(email=email, password=password)

        if user and user.is_active:
            return user

        raise serializers.ValidationError('Invalid login')
