from rest_framework import viewsets
from knox.auth import TokenAuthentication
from user.permissions import CreateOrDeleteAdminOnly
from user.serializers import UserProfileSerializer
from user.models import UserProfile


class UserProfileViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateOrDeleteAdminOnly]
    serializer_class = UserProfileSerializer

    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
