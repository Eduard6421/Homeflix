from rest_framework import viewsets
from knox.auth import TokenAuthentication
from user.permissions import UserViewPermission, IsAdmin
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserProfileSerializer
from user.models import UserProfile


class UserProfileViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
