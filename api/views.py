from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .models import ExpiringToken


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data['user']
        token, created = ExpiringToken.objects.get_or_create(user=user)
        return Response({'token': token.key})