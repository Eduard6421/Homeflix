
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import (LogoutView as KnoxLogoutView,
                        LogoutAllView as KnoxLogoutAllView)
from auth.serializers import ResponseSerializer
from user.serializers import RegisterSerializer, LoginSerializer

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)


from auth.scheme import KnoxTokenScheme
assert KnoxTokenScheme

# Create your views here.


@extend_schema(
    responses={
        200: ResponseSerializer
    }
)
class RegisterView(GenericAPIView):
    '''Register a new user'''

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        (_instance, token) = AuthToken.objects.create(user)

        response_serializer = ResponseSerializer(
            {'user': user, 'token': token})

        return Response(status=status.HTTP_201_CREATED,
                        data=response_serializer.data)


@extend_schema(
    responses={
        200: ResponseSerializer
    }
)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        (_instance, token) = AuthToken.objects.create(user)

        response_serializer = ResponseSerializer(
            {'user': user, 'token': token})

        return Response(status=status.HTTP_200_OK,
                        data=response_serializer.data)


class LogoutView(KnoxLogoutView):
    '''Logout user out of the current session'''
    authentication_classes = [TokenAuthentication]


class LogoutAllView(KnoxLogoutAllView):
    '''Logout all user sessions'''
    authentication_classes = [TokenAuthentication]
