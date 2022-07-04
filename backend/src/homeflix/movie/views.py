from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from user.permissions import IsAdmin, UserViewPermission
from movie.models import Movie
from movie.serialisers import MovieSerializer

# Create your views here.


class MovieViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserViewPermission | IsAdmin]
    serializer_class = MovieSerializer

    queryset = Movie.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
