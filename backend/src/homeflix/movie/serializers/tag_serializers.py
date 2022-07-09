from rest_framework import serializers
from user.serializers import UserSerializer
from movie.models import Movie, Genre, Tag


class TagSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_by')
        read_only_fields = ('id', 'created_by')
