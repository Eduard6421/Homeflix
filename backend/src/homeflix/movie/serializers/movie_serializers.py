from rest_framework import serializers
from movie.serializers.genre_serializers import GenreSerializer
from movie.serializers.tag_serializers import TagSerializer
from user.serializers import UserSerializer
from movie.models import Movie, Genre, Tag


class MovieSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, required=False)
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'created_by', 'tags', 'genres')
        read_only_fields = ('id', 'created_by')

    def _get_or_create_tags(self, tags, movie):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(created_by=auth_user,
                                                         **tag)
            movie.tags.add(tag_obj)

    def _get_or_create_genres(self, genres, movie):
        auth_user = self.context['request'].user
        for genre in genres:
            genre, created = Genre.objects.get_or_create(created_by=auth_user,
                                                         **genre)
            movie.genres.add(genre)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        genres = validated_data.pop('genres', [])

        instance = Movie.objects.create(**validated_data)

        self._get_or_create_tags(tags, instance)
        self._get_or_create_genres(genres, instance)

        instance.save()

        return instance

    def update(self, instance, validated_data):

        tags = validated_data.pop('tags', [])
        genres = validated_data.pop('genres', [])

        self._get_or_create_tags(tags, instance)
        self._get_or_create_genres(genres, instance)

        instance.title = validated_data.get('title', instance.title)

        instance.save()

        return instance
