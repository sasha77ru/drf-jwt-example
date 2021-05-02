from importlib._common import _

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Works exactly as MyTokenObtainPairSerializer but get auth from an old refresh token
class MyTokenRefreshSerializer(MyTokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        # Skip ancestor __init__
        serializers.Serializer.__init__(self,*args, **kwargs)

    def validate(self, attrs):
        foo = self.my_get_validated_token(self.initial_data["refresh"])
        # Get user from an old refresh token
        self.user = JWTAuthentication().get_user(foo)
        refresh = self.get_token(self.user)

        data = {}

        if api_settings.ROTATE_REFRESH_TOKENS: data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    def my_get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        try:
            return RefreshToken(raw_token)
        except TokenError as e:
            raise InvalidToken({
            'detail': _('Given token not valid for Refresh token type')
            })


class MyTokenRefreshView(TokenObtainPairView):
    serializer_class = MyTokenRefreshSerializer

