from rest_framework_simplejwt.authentication import JWTAuthentication


class Myuser:
    def __init__(self, validated_token):
        self.is_authenticated = True

        self.username = validated_token.payload["username"]
        self.first_name = validated_token.payload["first_name"]
        self.last_name = validated_token.payload["last_name"]
        self.is_staff = validated_token.payload["is_staff"]
        self.is_superuser = validated_token.payload["is_superuser"]


class MyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        return Myuser(validated_token)
