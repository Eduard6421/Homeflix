from rest_framework import serializers
from homeflix.movie.serializers.movie_serializers import MovieSerializer
from movie.models import Listing
from user.serializers import UserSerializer


class ListingSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(many=False, read_only=True)
    movie = MovieSerializer(many=False)

    class Meta:
        model = Listing
        fields = ('id', 'name', 'created_by', 'stream_url', 'season_number',
                  'episode_number', 'content_description', 'movie')
        read_only_fields = ('id', 'created_by')
