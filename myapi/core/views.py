from django.utils import timezone
from rest_framework_simplejwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from myapi.core.models import User
from myapi.core.mytoken import MyTokenObtainPairSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!', 'user': request.user.__dict__}
        return Response(content)


class LogOutAll(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.__getattribute__(api_settings.USER_ID_CLAIM)
        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        # Set token_stale for user to prevent token refreshing with old refresh tokens
        user.token_stale = timezone.now() + api_settings.REFRESH_TOKEN_LIFETIME
        user.save()

        # Give new tokens to user
        new_token = MyTokenObtainPairSerializer.get_token(user)
        data = {'refresh': str(new_token), 'access': str(new_token.access_token)}

        return Response(data)

