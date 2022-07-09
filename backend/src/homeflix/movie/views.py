from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from homeflix.movie.models import Listing
from movie.serializers.listing_serializers import ListingSerializer
from movie.serializers.genre_serializers import GenreSerializer
from movie.serializers.movie_serializers import MovieSerializer
from movie.serializers.tag_serializers import TagSerializer

from user.permissions import IsAdmin, UserViewPermission
from movie.models import Movie, Genre, Tag

# Create your views here.


class MovieViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserViewPermission | IsAdmin]
    serializer_class = MovieSerializer

    queryset = Movie.objects.all()

    def get_queryset(self):

        queryset = self.queryset

        tag_ids = self.request.query_params.get('tags', False)
        genre_ids = self.request.query_params.get('genres', False)
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids)
        if genre_ids:
            queryset = queryset.filter(genres__id__in=genre_ids)

        return self.queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TagViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserViewPermission | IsAdmin]
    serializer_class = TagSerializer

    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GenreViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserViewPermission | IsAdmin]
    serializer_class = GenreSerializer

    queryset = Genre.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ListingViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserViewPermission | IsAdmin]
    serializer_class = ListingSerializer

    queryset = Listing.objects.all()

    def get_queryset(self):
        return self.query.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
