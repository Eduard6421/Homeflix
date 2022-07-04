from rest_framework.routers import DefaultRouter
from django.urls import path, include
from movie.views import MovieViewSet

app_name = 'movie'


router = DefaultRouter()
router.register('', MovieViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
]
