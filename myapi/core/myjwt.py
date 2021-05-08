from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class Myuser:
    def __init__(self, validated_token):
        self.is_authenticated = True

        self.__setattr__(api_settings.USER_ID_CLAIM,validated_token.payload[api_settings.USER_ID_CLAIM])
        self.username = validated_token.payload["username"]
        self.first_name = validated_token.payload["first_name"]
        self.last_name = validated_token.payload["last_name"]
        self.is_staff = validated_token.payload["is_staff"]
        self.is_superuser = validated_token.payload["is_superuser"]


class MyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        return Myuser(validated_token)
