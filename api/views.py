from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ExpiringToken


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data.get('user', None)
        if not user:
            return Response(status=403, data={"fail_message": "incorrect credentials"})
        token, created = ExpiringToken.objects.get_or_create(user=user)
        if (timezone.now() - token.last_action).seconds > settings.TOKEN_EXPIRING_TIME:
            token.delete()
            token = ExpiringToken.objects.create(user=user)
        return Response({'token': token.key})