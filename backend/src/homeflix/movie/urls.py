from rest_framework.routers import DefaultRouter
from django.urls import path, include
from movie.views import GenreViewSet, TagViewSet, MovieViewSet

app_name = 'movie'


router = DefaultRouter()
router.register('', MovieViewSet, basename='movies')
router.register('tags/', TagViewSet, basename='tags')
router.register('genres/', GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls)),
]
