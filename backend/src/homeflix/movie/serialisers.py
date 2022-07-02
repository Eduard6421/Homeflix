from rest_framework import serializers
from user.serializers import UserSerializer
from movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    tags = UserSerializer(many=False, required=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'created_by',)
        read_only_fields = ('created_by', 'user')
