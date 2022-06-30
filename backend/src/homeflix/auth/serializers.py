
from rest_framework import serializers
from knox.models import AuthToken

from user.serializers import UserSerializer


class ResponseSerializer(serializers.Serializer):

    user = UserSerializer()
    token = serializers.CharField()
