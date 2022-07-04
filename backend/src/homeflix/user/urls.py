from rest_framework.routers import DefaultRouter
from django.urls import path, include
from user.views import UserProfileViewSet

app_name = 'user'


router = DefaultRouter()
router.register('profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
