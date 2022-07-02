from rest_framework.routers import DefaultRouter
from django.urls import path, include
from user.views import UserProfileViewSet

app_name = 'movie'


router = DefaultRouter()
router.register('', UserProfileViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
]
