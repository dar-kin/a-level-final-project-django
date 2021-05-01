from rest_framework import permissions
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from .models import ExpiringToken


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class ExpiringTokenAuthentication(TokenAuthentication):
    keyword = "Token"
    model = ExpiringToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if (timezone.now() - token.last_action).seconds > settings.TOKEN_EXPIRING_TIME:
            token.delete()
            raise AuthenticationFailed("Token has expired. Please, obtain a new one.")
        token.save()
        return user, token
